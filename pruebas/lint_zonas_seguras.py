r"""
lint_zonas_seguras.py
---------------------
Linter automático de Safe Zones para videos verticales 9:16 (TikTok / Reels / Shorts).

Verifica por frame que las zonas prohibidas de AGENTS.md estén vacías de contenido
brillante (UI/mockups). Umbrales calibrados sobre el video 14:
  - 60 frames de un video conforme  -> 0 px en TODAS las zonas
  - frames pre-fix que violaban     -> >=135 px en alguna zona
Por eso el umbral es 100 px por zona: separación total, sin falsos positivos.

Zonas verificadas:
  1. superior    y=0..249    (batería, hora, LIVE, pestañas TikTok) — siempre vacía.
  2. inferior    y=1651..1919 (username, caption, audio de TikTok) — siempre vacía.
  3. margen_izq  y=250..899,  x=0..69    (mockups deben vivir en x>=90)
  4. margen_der  y=250..899,  x=1011..1079 (mockups deben vivir en x<=990)

NO verifica la franja y=900..1650: ahí vive Byte (zona exclusiva) y su
sprite/confeti rozar bordes es legítimo. Limitación conocida de v1: un banner
ubicado SOLO en y=1200..1650 sin tocar los bordes ni la zona superior no se
detecta (detectar eso exige distinguir a Byte del banner).

Uso:
    python pruebas/lint_zonas_seguras.py <ruta> [<ruta>...] [--fps 2] [--sin-evidencia]

  - Acepta MP4 (se muestrean frames cada 1/`--fps` s), PNG/JPG sueltos o directorios
    (se recorren *.mp4, *.png, *.jpg dentro, sin recursión).
  - Con violación guarda el frame de evidencia en test_artifacts/lint_evidencia/
    y termina con exit code 1 (listo para CI o para el fin del pipeline).
  - --sin-evidencia no escribe PNGs de evidencia (solo reporte).

El script NO modifica nada; es 100% lectura.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List

import numpy as np
from PIL import Image

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.rutas import DIR_RAIZ as _DIR_RAIZ  # noqa: F401  (fija el cwd lógico del proyecto)

# Umbrales calibrados (ver docstring). lum = promedio RGB.
UMBRAL_PX_ZONA = 100
LUM_BRILLO = 110.0


@dataclass(frozen=True)
class Zona:
    nombre: str
    descripcion: str
    y0: int
    y1: int  # exclusivo
    x0: int
    x1: int  # exclusivo

    @property
    def area(self) -> int:
        return (self.y1 - self.y0) * (self.x1 - self.x0)


ZONAS: List[Zona] = [
    Zona("superior", "zona muerta TikTok (y<250)", 0, 250, 0, 1080),
    Zona("inferior", "username/caption/audio TikTok (y>1650)", 1651, 1920, 0, 1080),
    Zona("margen_izq", "mockups deben vivir en x>=90", 250, 900, 0, 70),
    Zona("margen_der", "mockups deben vivir en x<=990", 250, 900, 1011, 1080),
]


@dataclass
class Violacion:
    zona: Zona
    px: int

    @property
    def pct_zona(self) -> float:
        return 100.0 * self.px / max(1, self.zona.area)


def _mascara_brillo(im: np.ndarray) -> np.ndarray:
    """True donde el pixel es 'contenido UI' (brillante)."""
    return im.astype(np.float32).mean(axis=2) > LUM_BRILLO


def _bbox(mask_zona: np.ndarray) -> tuple[int, int, int, int] | None:
    """Bounding box (y0, x0, y1, x1) de los píxeles encendidos, o None."""
    ys, xs = np.nonzero(mask_zona)
    if len(ys) == 0:
        return None
    return int(ys.min()), int(xs.min()), int(ys.max()) + 1, int(xs.max()) + 1


def analizar_frame(im: np.ndarray) -> List[Violacion]:
    """Devuelve las violaciones de un frame ya cargado (HxWx3 RGB uint8)."""
    if im.ndim != 3 or im.shape[2] != 3:
        raise ValueError(f"Se esperaba RGB HxWx3, se obtuvo forma {im.shape}")
    mascara = _mascara_brillo(im)
    violaciones: List[Violacion] = []
    for zona in ZONAS:
        px = int(mascara[zona.y0:zona.y1, zona.x0:zona.x1].sum())
        if px > UMBRAL_PX_ZONA:
            violaciones.append(Violacion(zona=zona, px=px))
    return violaciones


def _iter_frames_imagenes(rutas: Iterable[Path]) -> Iterator[tuple[Path, np.ndarray]]:
    for ruta in rutas:
        with Image.open(ruta) as im:
            yield ruta, np.asarray(im.convert("RGB"))


def _iter_frames_video(ruta: Path, fps: float) -> Iterator[tuple[Path, np.ndarray]]:
    """Muestrea un MP4 a `fps` cuadros/s usando ffmpeg (sin dependencias extra)."""
    with tempfile.TemporaryDirectory(prefix="lintzs_") as tmp:
        patron = Path(tmp) / "f_%05d.png"
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", str(ruta),
                "-vf", f"fps={fps}",
                str(patron),
            ],
            check=True,
            capture_output=True,
        )
        for png in sorted(Path(tmp).glob("f_*.png")):
            with Image.open(png) as im:
                yield png, np.asarray(im.convert("RGB"))


def _rutas_de_entrada(entradas: List[Path]) -> tuple[List[Path], List[Path]]:
    """Separa (imagenes, videos) aceptando archivos y directorios."""
    imagenes: List[Path] = []
    videos: List[Path] = []
    for e in entradas:
        if e.is_dir():
            for hijo in sorted(e.iterdir()):
                suf = hijo.suffix.lower()
                if suf in (".png", ".jpg", ".jpeg"):
                    imagenes.append(hijo)
                elif suf == ".mp4":
                    videos.append(hijo)
        elif e.suffix.lower() == ".mp4":
            videos.append(e)
        elif e.suffix.lower() in (".png", ".jpg", ".jpeg"):
            imagenes.append(e)
        else:
            raise FileNotFoundError(f"Entrada no soportada: {e}")
    return imagenes, videos


def _guardar_evidencia(frame: np.ndarray, etiqueta: str, violaciones: List[Violacion]) -> Path:
    dir_ev = DIR_RAIZ / "test_artifacts" / "lint_evidencia"
    dir_ev.mkdir(parents=True, exist_ok=True)
    base = np.asarray(frame).copy()
    for v in violaciones:
        z = v.zona
        # marca la zona violada con un marco rojo de 6 px y tenue adentro
        base[z.y0:z.y1, z.x0:z.x0 + 6] = (255, 0, 0)
        base[z.y0:z.y1, z.x1 - 6:z.x1] = (255, 0, 0)
        base[z.y0:z.y0 + 6, z.x0:z.x1] = (255, 0, 0)
        base[z.y1 - 6:z.y1, z.x0:z.x1] = (255, 0, 0)
    salida = dir_ev / f"{etiqueta}.png"
    Image.fromarray(base).save(salida)
    return salida


def lintear(
    imagenes: List[Path],
    videos: List[Path],
    fps: float,
    guardar_evidencia: bool,
) -> int:
    """Analiza todo. Devuelve la cantidad total de frames con violación."""
    frames_totales = 0
    frames_malos = 0

    def _procesar(origen: Path, etiqueta: str, im: np.ndarray) -> None:
        nonlocal frames_totales, frames_malos
        frames_totales += 1
        violaciones = analizar_frame(im)
        if not violaciones:
            return
        frames_malos += 1
        print(f"  [FAIL] {etiqueta}")
        for v in violaciones:
            ys, xs = np.nonzero(_mascara_brillo(im)[v.zona.y0:v.zona.y1, v.zona.x0:v.zona.x1])
            bbox = (
                f"y={ys.min() + v.zona.y0}..{ys.max() + v.zona.y0}, "
                f"x={xs.min() + v.zona.x0}..{xs.max() + v.zona.x0}"
                if len(ys)
                else "-"
            )
            print(
                f"         zona '{v.zona.nombre}' ({v.zona.descripcion}): "
                f"{v.px} px ({v.pct_zona:.2f}% de la zona) en [{bbox}]"
            )
        if guardar_evidencia:
            ruta_ev = _guardar_evidencia(im, etiqueta, violaciones)
            print(f"         evidencia: {ruta_ev}")

    for ruta in imagenes:
        for png, im in _iter_frames_imagenes([ruta]):
            _procesar(ruta, ruta.stem, im)

    for ruta in videos:
        for i, (_, im) in enumerate(_iter_frames_video(ruta, fps)):
            _procesar(ruta, f"{ruta.stem}_frame_{i:04d}", im)

    print(
        f"\n[RESUMEN] frames analizados: {frames_totales} | "
        f"con violación: {frames_malos} | umbral: {UMBRAL_PX_ZONA} px/zona"
    )
    if frames_malos:
        print("[RESULTADO] FAIL — hay contenido en zonas prohibidas.")
    else:
        print("[RESULTADO] PASS — zonas prohibidas vacías.")
    return frames_malos


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Linter de Safe Zones (TikTok/Reels) para videos 9:16 del proyecto."
    )
    parser.add_argument(
        "entradas", nargs="+", type=Path,
        help="MP4, PNG/JPG o directorios (se recorren *.mp4/*.png/*.jpg)",
    )
    parser.add_argument("--fps", type=float, default=2.0,
                        help="muestreo de MP4 en cuadros/s (default: 2)")
    parser.add_argument("--sin-evidencia", action="store_true",
                        help="no guardar PNGs de evidencia en test_artifacts/lint_evidencia/")
    args = parser.parse_args(argv)

    imagenes, videos = _rutas_de_entrada(args.entradas)
    if not imagenes and not videos:
        print("No hay archivos MP4/PNG/JPG que analizar en las entradas dadas.")
        return 0

    print(f"[LINTER SAFE ZONES] imágenes={len(imagenes)} videos={len(videos)} fps={args.fps}")
    frames_malos = lintear(
        imagenes=imagenes,
        videos=videos,
        fps=args.fps,
        guardar_evidencia=not args.sin_evidencia,
    )
    return 1 if frames_malos else 0


if __name__ == "__main__":
    sys.exit(main())

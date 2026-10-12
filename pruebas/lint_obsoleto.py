r"""
lint_obsoleto.py
----------------
Detector de artefactos obsoletos (cachés silenciosas) del proyecto.

El pipeline tiene cachés que se saltan la regeneración si el artefacto
"parece" válido (existe y supera un tamaño mínimo). Si cambia la FUENTE
(código de planos, sprite original, guion), el artefacto queda viejo en
silencio: así se publicó el video 14 con el layout anterior (bug que
terminó resolviéndose con --forzar-fondos). Este linter compara mtimes
y falla (exit 1) antes de que un artefacto viejo se publique.

Cheques (por cada carpeta de videos/):
  fondos  : intermedios/fondos/*.mp4 vs src/mockups/**/*.py +
            src/registro_videos.py (+ validez > 50000 bytes, umbral de
            generar_fondos_del_video en registro_videos.py:482).
  sprites : assets/byte/transparentes/{clave}_{base}_transparente.png vs
            el sprite original (ruta_in de sprites_para) +
            src/shorts_assembler.py (dueño de quitar_fondo) (+ validez
            > 5000 bytes, umbral del PASO 4 en prueba_end_to_end.py:845).
  final   : final/*.mp4 vs el guion JSON, los fondos, los sprites, el
            video base y el código de ensamblaje (shorts_assembler,
            generar_animacion_byte, generar_paisaje_sonoro): el MP4
            publicado debe ser más nuevo que todo lo que lo compone.

NO cubre (limitaciones documentadas):
  - SFX de assets/audio (caché if-not-exists dentro de
    generar_paisaje_sonoro; extensión futura posible).
  - Falsos positivos tras `git pull` (el checkout renueva los mtimes de
    los .py sin cambiar contenido): el reporte indica la fuente exacta;
    si el contenido no cambió, re-corre el pipeline o descarta el aviso.
  - touching un .py ajeno a la caché (p. ej. generar_ass dentro de
    shorts_assembler.py) marca los sprites aunque quitar_fondo no haya
    cambiado: se regeneran barato, sin créditos.

Uso:
    python pruebas/lint_obsoleto.py [carpeta_video ...] [--solo fondos|sprites|final]

  - --solo es repetible (--solo fondos --solo sprites ejecuta solo esos).
  - Sin argumentos: todas las carpetas de videos/.
  - Acepta rutas ("videos/video_14_agua_ia") o nombres ("video_14_agua_ia").
  - Exit 1 si hay algún FAIL; 0 en caso contrario. Solo lectura.
  - Tests: python pruebas/test_lint_obsoleto.py
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.rutas import (  # noqa: E402
    DIR_BYTE_TRANSPARENTES,
    DIR_GUIONES,
    DIR_MOCKUPS,
    DIR_SRC,
    DIR_VIDEOS,
)
from src.registro_videos import resolver_carpeta, sprites_para  # noqa: E402

MIN_FONDO_BYTES = 50_000   # umbral de generar_fondos_del_video (src/registro_videos.py:482)
MIN_SPRITE_BYTES = 5_000   # umbral del PASO 4 (pruebas/prueba_end_to_end.py:845)

CHEQUES: Tuple[str, ...] = ("fondos", "sprites", "final")

ARCHIVOS_ENSAMBLAJE = (
    "shorts_assembler.py",
    "generar_animacion_byte.py",
    "generar_paisaje_sonoro.py",
)


@dataclass
class Hallazgo:
    carpeta: str
    cheque: str
    ok: bool
    detalle: str
    remedio: str = ""


# ---------------------------------------------------------------------------
# Utilidades de tiempo
# ---------------------------------------------------------------------------

def _mtime(ruta: Path) -> float:
    return ruta.stat().st_mtime


def _fmt(t: float) -> str:
    return datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M")


def _rel(ruta: Path) -> str:
    try:
        return str(ruta.relative_to(DIR_RAIZ))
    except ValueError:
        return str(ruta)


def _mas_nuevo(rutas: Sequence[Path]) -> Optional[Tuple[Path, float]]:
    mejor: Optional[Tuple[Path, float]] = None
    for p in rutas:
        try:
            t = _mtime(p)
        except OSError:
            continue
        if mejor is None or t > mejor[1]:
            mejor = (p, t)
    return mejor


def _lista_cortada(items: Sequence[str], maximo: int = 3) -> str:
    if len(items) <= maximo:
        return "; ".join(items)
    extra = len(items) - maximo
    return "; ".join(items[:maximo]) + f" (+{extra} más)"


# ---------------------------------------------------------------------------
# Fuentes de verdad por cheque
# ---------------------------------------------------------------------------

def fuentes_de_fondos() -> List[Path]:
    rutas = [p for p in DIR_MOCKUPS.rglob("*.py") if p.exists()]
    registro = DIR_SRC / "registro_videos.py"
    if registro.exists():
        rutas.append(registro)
    return sorted(rutas)


def fuente_quitar_fondo() -> Path:
    return DIR_SRC / "shorts_assembler.py"


def fuentes_de_ensamblaje() -> List[Path]:
    return [DIR_SRC / n for n in ARCHIVOS_ENSAMBLAJE if (DIR_SRC / n).exists()]


def mapa_de_guiones(dir_guiones: Path = DIR_GUIONES) -> Dict[str, Tuple[str, Path]]:
    """Mapa carpeta_de_video -> (nombre_base, ruta_guion), igual que el pipeline."""
    mapa: Dict[str, Tuple[str, Path]] = {}
    if not dir_guiones.is_dir():
        return mapa
    for p in sorted(dir_guiones.glob("guion_*.json")):
        nombre_base, carpeta = resolver_carpeta(p.stem)
        mapa[carpeta] = (nombre_base, p)
    return mapa


# ---------------------------------------------------------------------------
# Cheques
# ---------------------------------------------------------------------------

def chequear_fondos(
    carpeta: Path,
    fuentes: Optional[Sequence[Path]] = None,
) -> Optional[Hallazgo]:
    """None si la carpeta no tiene fondos (nada que verificar)."""
    dir_fondos = carpeta / "intermedios" / "fondos"
    mp4s = sorted(dir_fondos.glob("*.mp4")) if dir_fondos.is_dir() else []
    if not mp4s:
        return None

    fuentes = list(fuentes) if fuentes is not None else fuentes_de_fondos()
    problemas: List[str] = []

    invalidos = [p for p in mp4s if p.stat().st_size <= MIN_FONDO_BYTES]
    problemas.extend(
        f"{p.name} pesa {p.stat().st_size} bytes (< {MIN_FONDO_BYTES})"
        for p in invalidos
    )

    nuevo = _mas_nuevo(fuentes)
    if nuevo:
        fuente_ruta, fuente_t = nuevo
        viejos = [p for p in mp4s if p not in invalidos and _mtime(p) < fuente_t]
        problemas.extend(
            f"{p.name} más viejo que {_rel(fuente_ruta)} ({_fmt(fuente_t)})"
            for p in viejos
        )
        if not problemas:
            return Hallazgo(
                carpeta=carpeta.name,
                cheque="fondos",
                ok=True,
                detalle=f"{len(mp4s)} MP4 al día (fuente más nueva: "
                        f"{_rel(fuente_ruta)} {_fmt(fuente_t)})",
            )

    return Hallazgo(
        carpeta=carpeta.name,
        cheque="fondos",
        ok=False,
        detalle=_lista_cortada(problemas),
        remedio="re-corrida completa con --forzar-fondos",
    )


def chequear_sprites(
    nombre_base: str,
    mockup: Optional[str],
    dir_salida: Path = DIR_BYTE_TRANSPARENTES,
    fuente_codigo: Optional[Path] = None,
    pares: Optional[Sequence[Tuple[str, Path]]] = None,
) -> Optional[Hallazgo]:
    pares = list(pares) if pares is not None else list(sprites_para(nombre_base, mockup))
    if not pares:
        return None

    fuente_codigo = fuente_codigo if fuente_codigo is not None else fuente_quitar_fondo()
    t_codigo = _mtime(fuente_codigo) if fuente_codigo.exists() else None

    problemas: List[str] = []
    for clave, ruta_in in pares:
        salida = dir_salida / f"{clave}_{nombre_base}_transparente.png"
        if not ruta_in.exists():
            problemas.append(f"{salida.name}: fuente original inexistente ({_rel(ruta_in)})")
            continue
        if not salida.exists():
            problemas.append(f"{salida.name}: falta (nunca se generó)")
            continue
        if salida.stat().st_size <= MIN_SPRITE_BYTES:
            problemas.append(
                f"{salida.name} pesa {salida.stat().st_size} bytes (< {MIN_SPRITE_BYTES})"
            )
            continue
        if _mtime(salida) < _mtime(ruta_in):
            problemas.append(
                f"{salida.name} más viejo que su original "
                f"{ruta_in.name} ({_fmt(_mtime(ruta_in))})"
            )
            continue
        if t_codigo is not None and _mtime(salida) < t_codigo:
            problemas.append(
                f"{salida.name} más viejo que {_rel(fuente_codigo)} ({_fmt(t_codigo)})"
            )

    if not problemas:
        detalle = f"{len(pares)} sprites al día"
        if t_codigo is not None:
            detalle += f" (código: {_rel(fuente_codigo)} {_fmt(t_codigo)})"
        return Hallazgo(
            carpeta="", cheque="sprites", ok=True, detalle=detalle
        )

    return Hallazgo(
        carpeta="",
        cheque="sprites",
        ok=False,
        detalle=_lista_cortada(problemas),
        remedio="borrar los sprites indicados y re-corrida del pipeline (el PASO 4 los regenera)",
    )


def chequear_final(
    carpeta: Path,
    fuentes: Sequence[Tuple[str, Path]],
) -> Optional[Hallazgo]:
    """None si no hay MP4 publicado (nada que verificar)."""
    dir_final = carpeta / "final"
    mp4s = sorted(dir_final.glob("*.mp4")) if dir_final.is_dir() else []
    if not mp4s:
        return None
    final = max(mp4s, key=_mtime)
    t_final = _mtime(final)

    disponibles: List[Tuple[str, Path]] = []
    for etiqueta, ruta in fuentes:
        try:
            if ruta.exists():
                disponibles.append((etiqueta, ruta))
        except OSError:
            continue
    if not disponibles:
        return None

    mas_viejo = [
        (etiqueta, ruta) for etiqueta, ruta in disponibles
        if _mtime(ruta) > t_final
    ]
    if not mas_viejo:
        return Hallazgo(
            carpeta=carpeta.name,
            cheque="final",
            ok=True,
            detalle=f"{final.name} ({_fmt(t_final)}) más nuevo que "
                    f"{len(disponibles)} fuentes",
        )

    detalle = _lista_cortada(
        [
            f"más viejo que {etiqueta}: {_rel(ruta)} ({_fmt(_mtime(ruta))})"
            for etiqueta, ruta in mas_viejo
        ]
    )
    return Hallazgo(
        carpeta=carpeta.name,
        cheque="final",
        ok=False,
        detalle=detalle,
        remedio="re-renderizar antes de publicar (pipeline completo)",
    )


# ---------------------------------------------------------------------------
# Composición por carpeta de video
# ---------------------------------------------------------------------------

def fuentes_de_video(
    carpeta: Path,
    nombre_base: Optional[str],
    mockup: Optional[str],
    ruta_guion: Optional[Path],
) -> List[Tuple[str, Path]]:
    """Fuentes que debe reflejar el MP4 publicado (cheque 'final')."""
    fuentes: List[Tuple[str, Path]] = []
    if ruta_guion is not None:
        fuentes.append(("guion", ruta_guion))

    dir_fondos = carpeta / "intermedios" / "fondos"
    if dir_fondos.is_dir():
        fuentes.extend(("fondos", p) for p in sorted(dir_fondos.glob("*.mp4")))

    if nombre_base:
        dir_salida = DIR_BYTE_TRANSPARENTES
        for clave, _ in sprites_para(nombre_base, mockup):
            salida = dir_salida / f"{clave}_{nombre_base}_transparente.png"
            if salida.exists():
                fuentes.append(("sprites", salida))

    base = carpeta / "intermedios"
    bases = sorted(base.glob("video_*_base.mp4")) if base.is_dir() else []
    fuentes.extend(("base", p) for p in bases)

    fuentes.extend(("código", p) for p in fuentes_de_ensamblaje())
    return fuentes


def hallazgos_de_video(
    carpeta: Path,
    nombre_base: Optional[str],
    mockup: Optional[str],
    ruta_guion: Optional[Path],
    solo: Optional[str] = None,
    fuentes_fondos: Optional[Sequence[Path]] = None,
    fuente_codigo_sprites: Optional[Path] = None,
    pares_sprites: Optional[Sequence[Tuple[str, Path]]] = None,
) -> List[Optional[Hallazgo]]:
    """Devuelve un hallazgo por cheque activo (None = n/a), en orden CHEQUES."""
    activos = (solo,) if solo else CHEQUES
    resultados: List[Optional[Hallazgo]] = []

    for cheque in activos:
        if cheque == "fondos":
            resultados.append(
                chequear_fondos(carpeta, fuentes=fuentes_fondos)
            )
        elif cheque == "sprites":
            if nombre_base is None:
                resultados.append(None)
            else:
                h = chequear_sprites(
                    nombre_base,
                    mockup,
                    fuente_codigo=fuente_codigo_sprites,
                    pares=pares_sprites,
                )
                if h is not None:
                    h.carpeta = carpeta.name
                resultados.append(h)
        elif cheque == "final":
            if nombre_base is None and ruta_guion is None:
                resultados.append(None)
            else:
                resultados.append(
                    chequear_final(
                        carpeta, fuentes_de_video(carpeta, nombre_base, mockup, ruta_guion)
                    )
                )
    return resultados


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _resolver_carpetas(solicitadas: Sequence[str]) -> List[Path]:
    if not solicitadas:
        return [
            d for d in sorted(DIR_VIDEOS.iterdir())
            if d.is_dir() and any((d / n).is_dir() for n in ("entrada", "intermedios", "final"))
        ]
    carpetas: List[Path] = []
    for texto in solicitadas:
        p = Path(texto)
        if p.is_dir():
            carpetas.append(p.resolve())
        elif (DIR_VIDEOS / texto).is_dir():
            carpetas.append((DIR_VIDEOS / texto).resolve())
        else:
            raise FileNotFoundError(f"No existe la carpeta de video: {texto}")
    return carpetas


def _guion_de_carpeta(
    carpeta: Path, mapa: Dict[str, Tuple[str, Path]]
) -> Tuple[Optional[str], Optional[str], Optional[Path]]:
    """(nombre_base, mockup_sugerido, ruta_guion) para una carpeta; None si no hay."""
    entrada = mapa.get(carpeta.name)
    ruta: Optional[Path] = None
    if entrada is None:
        candidatos = sorted((carpeta / "entrada").glob("guion*.json")) if (carpeta / "entrada").is_dir() else []
        if not candidatos:
            return None, None, None
        nombre_base, _carpeta = resolver_carpeta(candidatos[0].stem)
        return nombre_base, None, candidatos[0]
    nombre_base, ruta = entrada
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            guion = json.load(f)
        mockup = guion.get("mockup_sugerido", "bandeja_correo")
    except (OSError, json.JSONDecodeError):
        mockup = None
    return nombre_base, mockup, ruta


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Detector de artefactos obsoletos (cachés silenciosas) del pipeline."
    )
    parser.add_argument(
        "carpetas", nargs="*", default=[],
        help="carpetas de video (ruta o nombre); default: todas las de videos/",
    )
    parser.add_argument(
        "--solo", action="append", choices=CHEQUES, default=None,
        help="ejecutar solo ese cheque (repetible: --solo fondos --solo sprites)",
    )
    parser.add_argument(
        "--dir-guiones", type=Path, default=DIR_GUIONES,
        help="directorio de guiones JSON (para tests)",
    )
    args = parser.parse_args(argv)

    carpetas = _resolver_carpetas(args.carpetas)
    if not carpetas:
        print("No hay carpetas de video que analizar.")
        return 0

    activos = tuple(dict.fromkeys(args.solo)) if args.solo else CHEQUES
    mapa = mapa_de_guiones(args.dir_guiones)

    print(f"[ARTEFACTOS OBSOLETOS] carpetas={len(carpetas)} cheques={','.join(activos)}\n")

    total_ok = 0
    total_fail = 0

    for carpeta in carpetas:
        nombre_base, mockup, ruta_guion = _guion_de_carpeta(carpeta, mapa)
        etiqueta = carpeta.name
        if nombre_base:
            etiqueta += f" (guion: {nombre_base}" + (f", mockup: {mockup})" if mockup else ")")
        else:
            etiqueta += " [sin guion asociado; sprites/final n/a]"
        print(f"{etiqueta}:")

        for cheque in activos:
            resultados = hallazgos_de_video(
                carpeta, nombre_base, mockup, ruta_guion, solo=cheque
            )
            hallazgo = resultados[0] if resultados else None
            if hallazgo is None:
                print(f"  [ -- ] {cheque:<7} n/a")
                continue
            if hallazgo.ok:
                total_ok += 1
                print(f"  [OK]  {cheque:<7} {hallazgo.detalle}")
            else:
                total_fail += 1
                print(f"  [FAIL] {cheque:<7} {hallazgo.detalle}")
                if hallazgo.remedio:
                    print(f"         remedio: {hallazgo.remedio}")
        print()

    print(f"[RESUMEN] veredictos OK={total_ok} FAIL={total_fail}")
    if total_fail:
        print("[RESULTADO] FAIL — hay artefactos con caché vencida (no publicar/re-renderizar sin regenerar).")
        return 1
    print("[RESULTADO] PASS — todos los artefactos reflejan sus fuentes actuales.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
Test unitario de la integración de validaciones al pipeline
(src/chequeos_pipeline.py: pre_vuelo y post_vuelo).

pre_vuelo: validar_guion + lint_obsoleto (fondos/sprites) de la carpeta.
post_vuelo: lint_zonas_seguras sobre un MP4 mínimo generado con ffmpeg
(lavfi: negro conforme; negro + barra blanca arriba = violación).

No gasta créditos ElevenLabs ni ejecuta el pipeline completo.

Ejecutar: python pruebas/test_chequeos_pipeline.py
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.chequeos_pipeline import post_vuelo, pre_vuelo

MIN_FONDO_BYTES = 50_001
T_VIEJO = 1_000_000_000  # 2001: más viejo que cualquier fuente real


def _guion(ruta: Path, contenido: dict) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(contenido, ensure_ascii=False), encoding="utf-8")
    return ruta


def _video(ruta: Path, vf: str = None) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=1",
        "-t", "1",
    ]
    if vf:
        cmd.extend(["-vf", vf])
    cmd.append(str(ruta))
    subprocess.run(cmd, check=True, capture_output=True)
    return ruta


class TestPreVueloGuion(unittest.TestCase):
    def test_guion_con_puntos_bloquea(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = _guion(Path(tmp) / "g.json", {
                "hook": "Esto tiene un punto final.",
                "problema": "otro bloque",
                "resultado": "fin",
                "cierre": "pregunta",
            })
            rc = pre_vuelo(ruta, carpeta_video=None)
        self.assertEqual(rc, 1)

    def test_guion_limpio_pasa(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = _guion(Path(tmp) / "g.json", {
                "hook": "Esto no tiene puntos, solo comas",
                "problema": "y sigue fluyendo",
                "resultado": "todo bien",
                "cierre": "pregunta abierta",
            })
            rc = pre_vuelo(ruta, carpeta_video=None)
        self.assertEqual(rc, 0)

    def test_sin_guion_pasa_omitido(self):
        rc = pre_vuelo(None, carpeta_video=None)
        self.assertEqual(rc, 0)

    def test_guion_inexistente_pasa_omitido(self):
        rc = pre_vuelo(Path("no_existe_xyz.json"), carpeta_video=None)
        self.assertEqual(rc, 0)


class TestPreVueloArtefactos(unittest.TestCase):
    def _carpeta(self, base: Path, t_fondo: float) -> Path:
        carpeta = base / "video_99_pre_vuelo"
        fondo = carpeta / "intermedios/fondos/fondo_escena_0.mp4"
        fondo.parent.mkdir(parents=True, exist_ok=True)
        fondo.write_bytes(b"\0" * MIN_FONDO_BYTES)
        os.utime(fondo, (t_fondo, t_fondo))
        return carpeta

    def test_fondo_viejo_bloquea(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = self._carpeta(Path(tmp), T_VIEJO)
            rc = pre_vuelo(None, carpeta_video=carpeta)
        self.assertEqual(rc, 1)

    def test_fondo_al_dia_pasa(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = self._carpeta(Path(tmp), time.time())
            rc = pre_vuelo(None, carpeta_video=carpeta)
        self.assertEqual(rc, 0)

    def test_carpeta_inexistente_pasa_omitido(self):
        rc = pre_vuelo(None, carpeta_video=Path("no_existe_xyz"))
        self.assertEqual(rc, 0)


class TestPostVuelo(unittest.TestCase):
    def test_video_negro_pasa(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp4 = _video(Path(tmp) / "negro.mp4")
            rc = post_vuelo(mp4, guardar_evidencia=False)
        self.assertEqual(rc, 0)

    def test_barra_blanca_en_zona_superior_falla(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp4 = _video(
                Path(tmp) / "violacion.mp4",
                vf="drawbox=x=200:y=100:w=600:h=80:color=white:t=fill",
            )
            rc = post_vuelo(mp4, guardar_evidencia=False)
        self.assertEqual(rc, 1)

    def test_sin_mp4_pasa_omitido(self):
        rc = post_vuelo(Path("no_existe_xyz.mp4"), guardar_evidencia=False)
        self.assertEqual(rc, 0)

    def test_ruta_none_pasa_omitido(self):
        rc = post_vuelo(None, guardar_evidencia=False)
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

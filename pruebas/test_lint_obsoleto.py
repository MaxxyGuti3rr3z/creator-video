"""
Test unitario del detector de artefactos obsoletos (pruebas/lint_obsoleto.py).

Usa tempdirs con mtimes forzados (os.utime) para simular cachés vencidas,
sin tocar los videos reales del proyecto.

Ejecutar: python pruebas/test_lint_obsoleto.py
"""
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from pruebas.lint_obsoleto import (
    MIN_FONDO_BYTES,
    MIN_SPRITE_BYTES,
    chequear_fondos,
    chequear_final,
    chequear_sprites,
    hallazgos_de_video,
    main,
    mapa_de_guiones,
)

T_VIEJO = 1_000_000_000   # 2001-09-09
T_NUEVO = 2_000_000_000   # 2033-05-18


def _archivo(ruta: Path, tamano: int = 10, t: float = T_NUEVO) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(b"\0" * tamano)
    os.utime(ruta, (t, t))
    return ruta


def _fuente(ruta: Path, t: float) -> Path:
    return _archivo(ruta, tamano=5, t=t)


class TestFondos(unittest.TestCase):
    def test_fondos_al_dia(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = Path(tmp)
            _archivo(carpeta / "intermedios/fondos/fondo_escena_0.mp4", MIN_FONDO_BYTES + 1, T_NUEVO)
            fuente = _fuente(carpeta / "planos.py", T_VIEJO)
            h = chequear_fondos(carpeta, fuentes=[fuente])
        self.assertIsNotNone(h)
        self.assertTrue(h.ok, h.detalle)

    def test_fondos_mas_viejos_que_fuente(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = Path(tmp)
            _archivo(carpeta / "intermedios/fondos/fondo_escena_0.mp4", MIN_FONDO_BYTES + 1, T_VIEJO)
            _archivo(carpeta / "intermedios/fondos/fondo_escena_1.mp4", MIN_FONDO_BYTES + 1, T_VIEJO)
            fuente = _fuente(carpeta / "planos.py", T_NUEVO)
            h = chequear_fondos(carpeta, fuentes=[fuente])
        self.assertFalse(h.ok)
        self.assertIn("más viejo que", h.detalle)
        self.assertIn("--forzar-fondos", h.remedio)

    def test_fondos_demasiado_pequenos(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = Path(tmp)
            _archivo(carpeta / "intermedios/fondos/fondo_escena_0.mp4", 100, T_NUEVO)
            fuente = _fuente(carpeta / "planos.py", T_VIEJO)
            h = chequear_fondos(carpeta, fuentes=[fuente])
        self.assertFalse(h.ok)
        self.assertIn("bytes", h.detalle)

    def test_sin_fondos_es_n_a(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(chequear_fondos(Path(tmp), fuentes=[]))


class TestSprites(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.salida = self.base / "transparentes"
        self.original = _archivo(self.base / "original.png", 100, T_NUEVO)
        self.codigo = _fuente(self.base / "shorts_assembler.py", T_VIEJO)
        self.pares = [("byte_feliz", self.original)]

    def tearDown(self):
        self.tmp.cleanup()

    def _sprites(self):
        return chequear_sprites(
            "guion_99_prueba",
            "mockup_x",
            dir_salida=self.salida,
            fuente_codigo=self.codigo,
            pares=self.pares,
        )

    def test_sprites_al_dia(self):
        _archivo(self.salida / "byte_feliz_guion_99_prueba_transparente.png",
                  MIN_SPRITE_BYTES + 1, T_NUEVO)
        h = self._sprites()
        self.assertTrue(h.ok, h.detalle)

    def test_sprite_mas_viejo_que_original(self):
        _archivo(self.salida / "byte_feliz_guion_99_prueba_transparente.png",
                  MIN_SPRITE_BYTES + 1, T_VIEJO)
        h = self._sprites()
        self.assertFalse(h.ok)
        self.assertIn("más viejo que su original", h.detalle)

    def test_sprite_mas_viejo_que_codigo(self):
        _archivo(self.salida / "byte_feliz_guion_99_prueba_transparente.png",
                  MIN_SPRITE_BYTES + 1, T_VIEJO - 75)
        os.utime(self.original, (T_VIEJO - 100, T_VIEJO - 100))
        os.utime(self.codigo, (T_VIEJO - 50, T_VIEJO - 50))
        h = self._sprites()
        self.assertFalse(h.ok)
        self.assertIn("shorts_assembler.py", h.detalle)
        self.assertIn("borrar", h.remedio)

    def test_sprite_falta(self):
        h = self._sprites()
        self.assertFalse(h.ok)
        self.assertIn("falta", h.detalle)

    def test_sprite_pequeno(self):
        _archivo(self.salida / "byte_feliz_guion_99_prueba_transparente.png",
                  100, T_NUEVO)
        h = self._sprites()
        self.assertFalse(h.ok)
        self.assertIn("bytes", h.detalle)

    def test_fuente_original_inexistente(self):
        self.pares = [("byte_feliz", self.base / "no_existe.png")]
        _archivo(self.salida / "byte_feliz_guion_99_prueba_transparente.png",
                  MIN_SPRITE_BYTES + 1, T_NUEVO)
        h = self._sprites()
        self.assertFalse(h.ok)
        self.assertIn("inexistente", h.detalle)


class TestFinal(unittest.TestCase):
    def test_final_al_dia(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = Path(tmp)
            _archivo(carpeta / "final/video_x.mp4", 1000, T_NUEVO)
            fuentes = [("guion", _fuente(carpeta / "guion.json", T_VIEJO))]
            h = chequear_final(carpeta, fuentes)
        self.assertTrue(h.ok, h.detalle)

    def test_final_mas_viejo_que_guion(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = Path(tmp)
            _archivo(carpeta / "final/video_x.mp4", 1000, T_VIEJO)
            fuentes = [("guion", _fuente(carpeta / "guion.json", T_NUEVO))]
            h = chequear_final(carpeta, fuentes)
        self.assertFalse(h.ok)
        self.assertIn("guion", h.detalle)
        self.assertIn("re-renderizar", h.remedio)

    def test_final_mas_viejo_que_varias_fuentes(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = Path(tmp)
            _archivo(carpeta / "final/video_x.mp4", 1000, T_VIEJO)
            fuentes = [
                ("fondos", _fuente(carpeta / "fondos/f.mp4", T_NUEVO)),
                ("código", _fuente(carpeta / "src.py", T_NUEVO)),
            ]
            h = chequear_final(carpeta, fuentes)
        self.assertFalse(h.ok)
        self.assertIn("más", h.detalle)

    def test_final_ausente_es_n_a(self):
        with tempfile.TemporaryDirectory() as tmp:
            fuentes = [("guion", _fuente(Path(tmp) / "guion.json", T_NUEVO))]
            self.assertIsNone(chequear_final(Path(tmp), fuentes))


class TestComposicion(unittest.TestCase):
    def test_solo_un_cheque(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = Path(tmp)
            resultados = hallazgos_de_video(
                carpeta, nombre_base=None, mockup=None, ruta_guion=None, solo="fondos"
            )
        self.assertEqual(len(resultados), 1)

    def test_sprites_n_a_sin_nombre_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            carpeta = Path(tmp)
            resultados = hallazgos_de_video(
                carpeta, nombre_base=None, mockup=None, ruta_guion=None, solo="sprites"
            )
        self.assertEqual(resultados, [None])

    def test_mapa_de_guiones_resuelve_video_14(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "guion_14_agua_ia.json"
            ruta.write_text(json.dumps({"mockup_sugerido": "agua_ia"}), encoding="utf-8")
            mapa = mapa_de_guiones(Path(tmp))
        self.assertIn("video_14_agua_ia", mapa)
        nombre_base, guion = mapa["video_14_agua_ia"]
        self.assertEqual(nombre_base, "guion_14_agua_ia")
        self.assertEqual(guion, ruta)


class TestCLI(unittest.TestCase):
    def _carpeta_falsa(self, base: Path, t_fondo: float) -> Path:
        carpeta = base / "video_99_prueba_cli"
        _archivo(carpeta / "intermedios/fondos/fondo_escena_0.mp4",
                 MIN_FONDO_BYTES + 1, t_fondo)
        return carpeta

    def test_exit_fail_con_fondo_viejo(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "videos"
            carpeta = self._carpeta_falsa(base, T_VIEJO)
            dir_guiones = Path(tmp) / "guiones"
            dir_guiones.mkdir()
            rc = main([
                str(carpeta), "--solo", "fondos",
                "--dir-guiones", str(dir_guiones),
            ])
        self.assertEqual(rc, 1)

    def test_exit_pass_con_fondo_al_dia(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "videos"
            carpeta = self._carpeta_falsa(base, time.time())
            dir_guiones = Path(tmp) / "guiones"
            dir_guiones.mkdir()
            rc = main([
                str(carpeta), "--solo", "fondos",
                "--dir-guiones", str(dir_guiones),
            ])
        self.assertEqual(rc, 0)

    def test_carpeta_inexistente_error(self):
        with self.assertRaises(FileNotFoundError):
            main(["no_existe_xyz", "--solo", "fondos"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

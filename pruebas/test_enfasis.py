"""
Tests de src/enfasis.py + src/eventos_voz.py (t_enfasis):
punch-in de énfasis sobre la capa bg, con curva sincronizada a la voz.

Ejecutar: python pruebas/test_enfasis.py
"""
import math
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.enfasis import (
    ANCLA_X_PX,
    ANCLA_Y_PX,
    DURACION_ENFASIS_SEG,
    EXP_POTENCIA,
    INTENSIDAD_PUNCH_IN,
    INTENSIDAD_PUNCH_SUAVE,
    MAX_POR_ESCENA,
    PuntoEnfasis,
    SEPARACION_MIN_SEG,
    construir_expresion_zoom,
    construir_filtro_enfasis,
    factor_zoom,
    seleccionar_puntos_enfasis,
)
from src.eventos_voz import construir_eventos_escena, encontrar_todos


class TestSeleccionarPuntos(unittest.TestCase):
    def test_vacio_da_tupla_vacia(self):
        self.assertEqual(seleccionar_puntos_enfasis([], 5.0), ())

    def test_duracion_no_positiva(self):
        self.assertEqual(seleccionar_puntos_enfasis([1.0], 0.0), ())
        self.assertEqual(seleccionar_puntos_enfasis([1.0], -1.0), ())

    def test_max_cero(self):
        self.assertEqual(seleccionar_puntos_enfasis([1.0], 5.0, max_por_escena=0), ())

    def test_filtra_fuera_de_rango_y_no_finitos(self):
        puntos = seleccionar_puntos_enfasis(
            [-0.5, 1.0, 99.0, float("nan"), float("inf")], 5.0
        )
        self.assertEqual([p.t_inicio for p in puntos], [1.0])

    def test_limita_a_max_por_escena(self):
        puntos = seleccionar_puntos_enfasis([0.5, 2.0, 3.5], 10.0, max_por_escena=2)
        self.assertEqual(len(puntos), 2)
        self.assertEqual([p.t_inicio for p in puntos], [0.5, 2.0])

    def test_separacion_minima(self):
        # 0.5 y 1.0 están a 0.5s (< 1.5s) -> el segundo se descarta
        puntos = seleccionar_puntos_enfasis([0.5, 1.0, 3.0], 10.0)
        self.assertEqual([p.t_inicio for p in puntos], [0.5, 3.0])

    def test_alterna_tipos_e_intensidades_no_negativas(self):
        puntos = seleccionar_puntos_enfasis([0.5, 2.0, 3.5], 10.0, max_por_escena=3)
        self.assertEqual([p.tipo for p in puntos],
                         ["punch_in", "punch_suave", "punch_in"])
        for p in puntos:
            self.assertGreaterEqual(p.intensidad, 0.0)
        self.assertAlmostEqual(puntos[0].intensidad, INTENSIDAD_PUNCH_IN)
        self.assertAlmostEqual(puntos[1].intensidad, INTENSIDAD_PUNCH_SUAVE)

    def test_ordenados_y_determinista(self):
        a = seleccionar_puntos_enfasis([3.0, 0.5, 2.0], 10.0)
        b = seleccionar_puntos_enfasis([0.5, 2.0, 3.0], 10.0)
        self.assertEqual(a, b)


class TestFactorZoom(unittest.TestCase):
    PUNTOS = (
        PuntoEnfasis(1.0, INTENSIDAD_PUNCH_IN, "punch_in"),
        PuntoEnfasis(3.0, INTENSIDAD_PUNCH_SUAVE, "punch_suave"),
    )

    def test_exactamente_1_fuera_de_ventanas(self):
        for t in (0.0, 0.99, 1.21, 2.99, 3.21, 5.0, 10.0):
            self.assertAlmostEqual(factor_zoom(t, self.PUNTOS), 1.0, places=9,
                                   msg=f"t={t}")

    def test_exactamente_1_en_bordes_de_ventana(self):
        for t0 in (1.0, 3.0):
            self.assertAlmostEqual(factor_zoom(t0, self.PUNTOS), 1.0, places=9)
            self.assertAlmostEqual(
                factor_zoom(t0 + DURACION_ENFASIS_SEG, self.PUNTOS), 1.0, places=9
            )

    def test_pico_en_ventana_con_intensidad(self):
        # Pico de sin(pi*u^EXP) = 1 en u^EXP=0.5 -> u=0.5^(1/EXP) < 1 (subida rápida)
        u_pico = 0.5 ** (1.0 / EXP_POTENCIA)
        t_pico = 1.0 + u_pico * DURACION_ENFASIS_SEG
        z = factor_zoom(t_pico, self.PUNTOS)
        self.assertAlmostEqual(z, 1.0 + INTENSIDAD_PUNCH_IN, places=6)

    def test_rango_acotado_y_sin_nan(self):
        for i in range(0, 600):
            t = i / 100.0
            z = factor_zoom(t, self.PUNTOS)
            self.assertFalse(math.isnan(z))
            self.assertGreaterEqual(z, 1.0)
            self.assertLessEqual(z, 1.0 + INTENSIDAD_PUNCH_IN + 1e-9)

    def test_sin_puntos_da_1(self):
        self.assertEqual(factor_zoom(1.0, ()), 1.0)


class TestExpresionFFmpeg(unittest.TestCase):
    PUNTOS = (PuntoEnfasis(0.5, INTENSIDAD_PUNCH_IN, "punch_in"),)

    def test_sin_puntos_da_uno(self):
        self.assertEqual(construir_expresion_zoom(()), "1")

    def test_base_on_usa_variable_on(self):
        expr = construir_expresion_zoom(self.PUNTOS, fps=30, base="on")
        self.assertIn("on", expr)
        self.assertNotIn("(t-", expr)
        # t0=0.5s -> frame 15 (0.5*30)
        self.assertIn("15.0000", expr)

    def test_base_t_usa_variable_t(self):
        expr = construir_expresion_zoom(self.PUNTOS, fps=30, base="t")
        self.assertIn("(t-0.5000)", expr)
        self.assertNotIn("on", expr)

    def test_base_invalida_lanza(self):
        with self.assertRaises(ValueError):
            construir_expresion_zoom(self.PUNTOS, base="x")

    def test_expresion_contiene_intensidad_y_between(self):
        expr = construir_expresion_zoom(self.PUNTOS, base="on")
        self.assertIn(f"{INTENSIDAD_PUNCH_IN:.4f}", expr)
        self.assertIn("between(", expr)
        self.assertIn("clip(", expr)
        self.assertTrue(expr.startswith("1+"))


class TestFiltroEnfasis(unittest.TestCase):
    PUNTOS = (
        PuntoEnfasis(0.5, INTENSIDAD_PUNCH_IN, "punch_in"),
        PuntoEnfasis(2.0, INTENSIDAD_PUNCH_SUAVE, "punch_suave"),
    )

    def test_sin_puntos_da_vacio(self):
        self.assertEqual(construir_filtro_enfasis(()), "")

    def test_filtro_contiene_estructura_esperada(self):
        f = construir_filtro_enfasis(self.PUNTOS)
        self.assertTrue(f.startswith("zoompan=z='1+"))
        self.assertIn(f"x='{ANCLA_X_PX}-{ANCLA_X_PX}/zoom'", f)
        self.assertIn(f"y='{ANCLA_Y_PX}-{ANCLA_Y_PX}/zoom'", f)
        self.assertIn("d=1:s=1080x1920:fps=30", f)

    def test_ancla_es_la_documentada(self):
        self.assertEqual((ANCLA_X_PX, ANCLA_Y_PX), (540, 250))


class TestEventosVozCompat(unittest.TestCase):
    def _seg_y_al(self):
        seg = {"texto": "activa modo avion ahora", "inicio": 10.0, "fin": 14.0}
        al = {
            "characters": list("activa modo avion ahora"),
            "character_start_times_seconds": [10.0 + i * 0.2 for i in range(23)],
            "character_end_times_seconds": [10.0 + (i + 1) * 0.2 for i in range(23)],
        }
        return seg, al

    def test_t_enfasis_es_tupla_ordenada_sin_duplicados(self):
        seg, al = self._seg_y_al()
        ev = construir_eventos_escena(seg, al, ui_clave=["modo", "modo"])
        self.assertIsInstance(ev["t_enfasis"], tuple)
        self.assertEqual(ev["t_enfasis"], tuple(sorted(set(ev["t_enfasis"]))))
        self.assertTrue(all(t >= 0.0 for t in ev["t_enfasis"]))

    def test_t_enfasis_vacia_sin_ui_clave(self):
        seg, al = self._seg_y_al()
        ev = construir_eventos_escena(seg, al)
        self.assertEqual(ev["t_enfasis"], ())

    def test_t_ui_y_t_pildora_siguen_funcionando(self):
        seg, al = self._seg_y_al()
        ev = construir_eventos_escena(seg, al, pildora="avion", ui_clave=["activa"])
        self.assertIsNotNone(ev["t_ui"])
        self.assertIsNotNone(ev["t_pildora"])

    def test_encontrar_todos_todas_las_ocurrencias(self):
        palabras = [
            ("hola", 0.0, 0.2), ("mundo", 0.2, 0.4),
            ("hola", 0.4, 0.6), ("adios", 0.6, 0.8),
        ]
        self.assertEqual(encontrar_todos(palabras, "hola"), [0.0, 0.4])
        self.assertEqual(encontrar_todos(palabras, "nada"), [])


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg no disponible")
class TestIntegracionFFmpeg(unittest.TestCase):
    """Render corto con punch-in al 100% + lint_zonas_seguras en PASS."""

    def test_punch_in_no_viola_safe_zones(self):
        try:
            from PIL import Image, ImageDraw
            from pruebas.lint_zonas_seguras import analizar_frame
        except ImportError:
            from lint_zonas_seguras import analizar_frame

        with tempfile.TemporaryDirectory(prefix="test_enfasis_") as tmp:
            tmp_path = Path(tmp)
            bg = tmp_path / "bg.png"
            # Fondo sintético: mockup brillante en y=252..900, x=100..980
            im = Image.new("RGB", (1080, 1920), (18, 18, 32))
            ImageDraw.Draw(im).rectangle([100, 252, 980, 900], fill=(235, 235, 240))
            im.save(bg)

            # 2 punch-ins: fuerte al inicio + suave a mitad (peor caso de rango)
            puntos = seleccionar_puntos_enfasis([0.1, 1.0, 2.5], 3.0)
            self.assertEqual(len(puntos), 2)
            filtro = construir_filtro_enfasis(puntos)

            salida = tmp_path / "punch.mp4"
            cmd = [
                "ffmpeg", "-y", "-loglevel", "error",
                "-loop", "1", "-framerate", "30", "-i", str(bg),
                "-vf", f"{filtro},fps=30",
                "-t", "3", str(salida),
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"FFmpeg falló: {res.stderr[-500:]}")

            # Muestrear frames y verificar que NINGÚN frame viola safe zones
            frames_dir = tmp_path / "frames"
            frames_dir.mkdir()
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", str(salida),
                 "-vf", "fps=10", str(frames_dir / "f_%03d.png")],
                check=True, capture_output=True,
            )
            frames = sorted(frames_dir.glob("f_*.png"))
            self.assertGreater(len(frames), 10)
            for fp in frames:
                with Image.open(fp) as img:
                    violaciones = analizar_frame(
                        __import__("numpy").asarray(img.convert("RGB"))
                    )
                self.assertEqual(
                    violaciones, [],
                    f"Safe zones violadas en {fp.name}: {violaciones}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)

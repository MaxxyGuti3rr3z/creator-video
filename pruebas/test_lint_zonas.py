"""
Test unitario del linter de Safe Zones (pruebas/lint_zonas_seguras.py).

Usa imágenes sintéticas (numpy) para no depender de videos reales:
  - frame negro                -> PASS (0 violaciones)
  - bloque brillante en cada zona prohibida -> FAIL de esa zona
  - contenido legítimo (Byte centrado abajo, UI en el centro) -> PASS
  - bloque < umbral 100 px     -> PASS (margen de calibración)

Ejecutar: python pruebas/test_lint_zonas.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from pruebas.lint_zonas_seguras import (
    UMBRAL_PX_ZONA,
    ZONAS,
    analizar_frame,
    main,
)


def _frame(color: int = 0) -> np.ndarray:
    return np.full((1920, 1080, 3), color, dtype=np.uint8)


def _pegar(im: np.ndarray, y0: int, x0: int, alto: int, ancho: int, color: int = 255) -> np.ndarray:
    im[y0:y0 + alto, x0:x0 + ancho] = color
    return im


class TestZonas(unittest.TestCase):
    def test_zonas_cubren_toda_la_pantalla_sin_solape_en_margenes(self):
        # la superior e inferior cubren el ancho completo; los márgenes solo franja UI
        sup, inf, mi, md = ZONAS
        self.assertEqual((sup.y0, sup.y1), (0, 250))
        self.assertEqual((inf.y0, inf.y1), (1651, 1920))
        self.assertEqual((mi.x0, mi.x1), (0, 70))
        self.assertEqual((md.x0, md.x1), (1011, 1080))
        self.assertEqual((mi.y0, mi.y1), (250, 900))


class TestAnalizarFrame(unittest.TestCase):
    def test_frame_negro_pasa(self):
        self.assertEqual(analizar_frame(_frame()), [])

    def test_frame_gris_oscuro_pasa(self):
        # sin contenido brillante (lum <= 110): no es UI
        self.assertEqual(analizar_frame(_frame(100)), [])

    def test_zona_superior_falla(self):
        # badge tipo el del hero antiguo: y=110, alto 80
        im = _pegar(_frame(), 110, 300, 80, 400)
        viol = analizar_frame(im)
        self.assertEqual([v.zona.nombre for v in viol], ["superior"])
        self.assertGreaterEqual(viol[0].px, UMBRAL_PX_ZONA)

    def test_zona_inferior_falla(self):
        # píldora/tabbar de audio de TikTok: y=1700
        im = _pegar(_frame(), 1700, 200, 100, 600)
        viol = analizar_frame(im)
        self.assertEqual([v.zona.nombre for v in viol], ["inferior"])

    def test_margen_izquierdo_falla(self):
        # mockup que invade x<70 en la franja UI
        im = _pegar(_frame(), 300, 0, 300, 69)
        viol = analizar_frame(im)
        self.assertEqual([v.zona.nombre for v in viol], ["margen_izq"])

    def test_margen_derecho_falla(self):
        im = _pegar(_frame(), 300, 1011, 300, 69)
        viol = analizar_frame(im)
        self.assertEqual([v.zona.nombre for v in viol], ["margen_der"])

    def test_multiples_zonas_a_la_vez(self):
        im = _pegar(_frame(), 110, 300, 80, 400)
        im = _pegar(im, 1700, 200, 100, 600)
        viol = analizar_frame(im)
        self.assertEqual(sorted(v.zona.nombre for v in viol), ["inferior", "superior"])

    def test_byte_en_zona_inferior_central_pasa(self):
        # Byte centrado (x=285..795) en y=1120..1650: contenido brillante legítimo
        im = _pegar(_frame(), 1120, 285, 530, 510)
        self.assertEqual(analizar_frame(im), [])

    def test_ui_en_centro_de_franja_pasa(self):
        # mockup dentro de x=90..990, y=250..780: posición correcta
        im = _pegar(_frame(), 300, 150, 400, 700)
        self.assertEqual(analizar_frame(im), [])

    def test_bloque_bajo_umbral_pasa(self):
        # 10x10 = 100 px exactos: no supera el umbral estricto (>100)
        im = _pegar(_frame(), 10, 10, 10, 10)
        self.assertEqual(analizar_frame(im), [])

    def test_bloque_sobre_umbral_falla(self):
        # 11x11 = 121 px: supera el umbral
        im = _pegar(_frame(), 10, 10, 11, 11)
        viol = analizar_frame(im)
        self.assertEqual([v.zona.nombre for v in viol], ["superior"])
        self.assertEqual(viol[0].px, 121)


class TestCLI(unittest.TestCase):
    def test_exit_code_pass_y_fail(self):
        from PIL import Image

        with tempfile.TemporaryDirectory(prefix="lintzs_test_") as tmp:
            tmp = Path(tmp)
            Image.fromarray(_frame()).save(tmp / "limpio.png")
            Image.fromarray(_pegar(_frame(), 110, 300, 80, 400)).save(tmp / "sucio.png")

            rc_ok = main([str(tmp / "limpio.png"), "--sin-evidencia"])
            rc_fail = main([str(tmp / "sucio.png"), "--sin-evidencia"])

        self.assertEqual(rc_ok, 0)
        self.assertEqual(rc_fail, 1)

    def test_directorio_vacio_pasa(self):
        with tempfile.TemporaryDirectory(prefix="lintzs_vacio_") as tmp:
            rc = main([tmp, "--sin-evidencia"])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

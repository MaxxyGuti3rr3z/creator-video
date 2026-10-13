"""
Tests de los helpers de animación (src/mockups/motion.py) y la planificación
de SFX por segmentos (src/generar_paisaje_sonoro.py::_planificar_sfx).

Ejecutar: python pruebas/test_motion_y_sfx.py
"""
import sys
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.generar_paisaje_sonoro import _planificar_sfx
from src.mockups.motion import clamp, ease_out_back, pop_scale, type_chars, type_words
from src.mockups.motor import squash_stretch
from src.mockups.planos.video_15_celular import _badge, _pildora


class TestEasing(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(clamp(-1.0), 0.0)
        self.assertEqual(clamp(2.0), 1.0)
        self.assertEqual(clamp(0.42), 0.42)

    def test_ease_out_back_extremos(self):
        self.assertAlmostEqual(ease_out_back(0.0), 0.0, places=6)
        self.assertAlmostEqual(ease_out_back(1.0), 1.0, places=6)

    def test_ease_out_back_overshoot_intermedio(self):
        valores = [ease_out_back(u / 100.0) for u in range(1, 100)]
        self.assertGreater(max(valores), 1.0)
        self.assertLess(max(valores), 1.2)


class TestPopScale(unittest.TestCase):
    def test_invisible_antes_de_t0(self):
        self.assertEqual(pop_scale(0.0, t0=0.1), 0.0)
        self.assertEqual(pop_scale(0.05, t0=0.1), 0.0)

    def test_estable_en_1_tras_dur(self):
        self.assertEqual(pop_scale(1.0, t0=0.0, dur=0.35), 1.0)
        self.assertEqual(pop_scale(0.5, t0=0.1, dur=0.35), 1.0)

    def test_overshoot_limitado(self):
        for i in range(1, 35):
            s = pop_scale(i * 0.01, t0=0.0, dur=0.35, overshoot_max=1.04)
            self.assertLessEqual(s, 1.04, f"pop_scale superó el tope en t={i * 0.01:.2f}")


class TestTyping(unittest.TestCase):
    def test_vacio_antes_de_t0(self):
        self.assertEqual(type_chars("hola", 0.1, t0=0.15), "")
        self.assertEqual(type_words(["a", "b"], 0.1, t0=0.15), "")

    def test_texto_completo_al_final(self):
        self.assertEqual(type_chars("hola", 5.0, t0=0.15, cps=28.0), "hola")
        self.assertEqual(type_words(["uno", "dos"], 5.0, t0=0.15, wps=4.0), "uno dos")

    def test_parcial_a_28cps(self):
        # t=0.5, t0=0.15 → 0.35s * 28 cps = 9 chars
        self.assertEqual(type_chars("abcdefghij", 0.5, t0=0.15, cps=28.0), "abcdefghi")


class TestPlanificarSfx(unittest.TestCase):
    SEGMENTOS_15 = [
        {"tipo": "cold_open", "texto": "a", "inicio": 0.0, "fin": 3.0},
        {"tipo": "hook", "texto": "b", "inicio": 3.0, "fin": 7.0},
        {"tipo": "problema", "texto": "c", "inicio": 7.0, "fin": 12.0},
        {"tipo": "punto_1", "texto": "d", "inicio": 12.0, "fin": 18.0},
        {"tipo": "punto_2", "texto": "e", "inicio": 18.0, "fin": 23.0},
        {"tipo": "resultado", "texto": "f", "inicio": 23.0, "fin": 27.0},
        {"tipo": "cierre", "texto": "g", "inicio": 27.0, "fin": 30.5},
    ]

    def test_vacio_devuelve_whoosh_unico(self):
        plan = _planificar_sfx([])
        self.assertEqual(plan, [("whoosh", 0.0, 0.35)])

    def test_siete_segmentos_conteo_y_claves(self):
        plan = _planificar_sfx(self.SEGMENTOS_15)
        # escena0: whoosh+bounce (2) + 6 transiciones*2 (12) + chime (1)
        # + click/slide*2 (4) + riser+impact (2) = 21
        self.assertEqual(len(plan), 21)
        self.assertIn(("whoosh", 0.0, 0.35), plan)
        self.assertIn(("bounce", 0.08, 0.30), plan)
        self.assertIn(("whoosh", 2.85, 0.38), plan)   # hook 3.0 - 0.15
        self.assertIn(("bounce", 3.08, 0.30), plan)
        self.assertIn(("chime", 23.22, 0.65), plan)   # resultado + 0.22
        self.assertIn(("click", 13.2, 0.70), plan)    # punto_1 + 1.2
        self.assertIn(("slide", 13.7, 0.45), plan)    # punto_1 + 1.7
        self.assertIn(("click", 19.2, 0.70), plan)    # punto_2 + 1.2
        self.assertIn(("slide", 19.7, 0.45), plan)    # punto_2 + 1.7
        self.assertIn(("riser", 22.15, 0.50), plan)   # resultado 23.0 - 0.85
        self.assertIn(("impact", 23.22, 0.55), plan)  # capa con el chime

    def test_payoff_cierre_cuando_no_hay_resultado(self):
        segs = [
            {"tipo": "cold_open", "inicio": 0.0, "fin": 3.0},
            {"tipo": "cierre", "inicio": 3.0, "fin": 6.0},
        ]
        plan = _planificar_sfx(segs)
        self.assertIn(("riser", 2.15, 0.50), plan)   # cierre 3.0 - 0.85
        self.assertIn(("impact", 3.22, 0.55), plan)
        self.assertNotIn(("chime", 3.22, 0.65), plan)  # el chime es solo de resultado

    def test_tiempos_no_negativos(self):
        segs = [
            {"tipo": "cold_open", "inicio": 0.0},
            {"tipo": "hook", "inicio": 0.1},   # whoosh en 0.1-0.15 → clamp 0.0
        ]
        plan = _planificar_sfx(segs)
        for nombre, t, _volumen in plan:
            self.assertGreaterEqual(t, 0.0, f"SFX {nombre} con tiempo negativo")


class TestSquashStretch(unittest.TestCase):
    def test_contacto_aplasta_levemente(self):
        # t=0: sin(0)=0 → rebote en suelo, cos(0)=1 → contacto
        sx, sy = squash_stretch(0.0)
        self.assertLess(sy, 1.0)
        self.assertGreater(sx, 1.0)

    def test_apice_estira_levemente(self):
        # t*pi/6 con frec=3 → t*3 = pi/2 → ápice (cos=0)
        sx, sy = squash_stretch(3.14159265 / 6.0)
        self.assertGreater(sy, 1.0)
        self.assertLess(sx, 1.0)

    def test_amplitud_sutil(self):
        # Calibrado sutil: ni el squash ni el stretch superan ~7%
        for i in range(0, 40):
            t = i * 0.05
            sx, sy = squash_stretch(t)
            self.assertGreaterEqual(sy, 0.92, f"sy demasiado aplastado en t={t:.2f}")
            self.assertLessEqual(sy, 1.03, f"sy demasiado estirado en t={t:.2f}")
            self.assertGreaterEqual(sx, 0.96, f"sx demasiado angosto en t={t:.2f}")
            self.assertLessEqual(sx, 1.08, f"sx demasiado ancho en t={t:.2f}")


class TestBadgeYPildora(unittest.TestCase):
    def _frame(self):
        from PIL import Image
        return Image.new("RGBA", (1080, 1920), (0, 0, 0, 255))

    def test_badge_invisible_en_t0(self):
        frame = self._frame()
        antes = frame.copy()
        _badge(frame, 1080, "TEXTO LARGO DE PRUEBA", t_sec=0.0)
        self.assertEqual(frame.tobytes(), antes.tobytes())

    def test_badge_visible_y_anclado_arriba(self):
        frame = self._frame()
        _badge(frame, 1080, "TEXTO LARGO DE PRUEBA", t_sec=0.5)
        pix = frame.load()
        # Banda superior del badge (y=256, sobre el texto) debe ser relleno rojo
        r, g, b, _a = pix[540, 256]
        self.assertGreater(r, 150)
        self.assertLess(g, 100)

    def test_pildora_typing_y_anclaje(self):
        frame = self._frame()
        _pildora(frame, 1080, "PREGUNTA LARGA DE PRUEBA", t_sec=1.0)
        pix = frame.load()
        r, g, b, _a = pix[540, 825]
        # Píldora con texto completo: píxel del texto/blanco o borde celeste
        self.assertTrue(r > 120 or b > 150, f"píxel inesperado {(r, g, b)}")

    def test_pildora_vacia_antes_de_t0(self):
        frame = self._frame()
        antes = frame.copy()
        _pildora(frame, 1080, "PRUEBA", t_sec=0.05)
        self.assertEqual(frame.tobytes(), antes.tobytes())


if __name__ == "__main__":
    unittest.main(verbosity=2)

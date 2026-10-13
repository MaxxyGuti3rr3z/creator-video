"""
Tests de src/director_gancho.py (variantes A/B/C) y pruebas/lint_gancho.py.

Ejecutar: python pruebas/test_director_gancho.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.director_gancho import (
    ARQUETIPOS_GANCHO,
    TRATAMIENTOS,
    VarianteGancho,
    seleccionar_para_produccion,
    variantes_gancho,
)
from pruebas import lint_gancho
from src.shorts_assembler import _expresion_zoom_gancho


class TestVariantesGancho(unittest.TestCase):
    def test_devuelve_tres_variantes_con_ids(self):
        vs = variantes_gancho(15)
        self.assertEqual(len(vs), 3)
        self.assertEqual([v.id for v in vs], ["A", "B", "C"])

    def test_arquetipos_validos_y_unicos(self):
        vs = variantes_gancho(1)
        arquetipos = [v.arquetipo for v in vs]
        self.assertEqual(len(set(arquetipos)), 3)
        for a in arquetipos:
            self.assertIn(a, ARQUETIPOS_GANCHO)

    def test_determinista_misma_semilla(self):
        self.assertEqual(variantes_gancho(7), variantes_gancho(7))

    def test_semillas_distintas_rotan(self):
        # Con 3 arquetipos y 3 semillas, el orden de A debe cubrir los 3
        ordenes_a = {variantes_gancho(s)[0].arquetipo for s in (0, 1, 2)}
        self.assertEqual(ordenes_a, set(ARQUETIPOS_GANCHO))

    def test_preferido_va_en_a(self):
        vs = variantes_gancho(3, arquetipo_preferido="mockup_inmediato")
        self.assertEqual(vs[0].arquetipo, "mockup_inmediato")
        self.assertEqual(vs[0].id, "A")

    def test_preferido_invalido_se_ignora(self):
        vs = variantes_gancho(3, arquetipo_preferido="no_existe")
        self.assertEqual(len(vs), 3)
        self.assertNotIn("no_existe", [v.arquetipo for v in vs])

    def test_excluir_reduce_variantes(self):
        vs = variantes_gancho(5, excluir=("texto_pantalla",))
        self.assertEqual(len(vs), 2)
        self.assertNotIn("texto_pantalla", [v.arquetipo for v in vs])

    def test_excluir_todo_da_vacio(self):
        self.assertEqual(variantes_gancho(5, excluir=ARQUETIPOS_GANCHO), ())

    def test_descripciones_no_vacias(self):
        for v in variantes_gancho(0):
            self.assertTrue(v.descripcion)


class TestSeleccionarProduccion(unittest.TestCase):
    def test_default_es_a(self):
        vs = variantes_gancho(2)
        self.assertEqual(seleccionar_para_produccion(vs).id, "A")

    def test_preferencia_por_id(self):
        vs = variantes_gancho(2)
        self.assertEqual(seleccionar_para_produccion(vs, "B").id, "B")

    def test_preferencia_inexistente_cae_a_a(self):
        vs = variantes_gancho(2)
        self.assertEqual(seleccionar_para_produccion(vs, "Z").id, "A")

    def test_vacio_da_none(self):
        self.assertIsNone(seleccionar_para_produccion([]))


class TestTratamientos(unittest.TestCase):
    def test_cada_arquetipo_tiene_tratamiento(self):
        for a in ARQUETIPOS_GANCHO:
            self.assertIn(a, TRATAMIENTOS)

    def test_escalas_siempre_mayores_iguales_a_1(self):
        for a, t in TRATAMIENTOS.items():
            self.assertGreaterEqual(t["z_min"], 1.0, a)
            self.assertGreaterEqual(t["z_max"], 1.0, a)
            self.assertGreaterEqual(t["escala_choque_byte"], 1.0, a)

    def test_control_sin_zoom(self):
        t = TRATAMIENTOS["texto_pantalla"]
        self.assertEqual(t["z_max"], 1.0)
        self.assertEqual(_expresion_zoom_gancho(t, 100), "")


class TestExpresionZoomGancho(unittest.TestCase):
    def test_punch_b_entre_1_y_zmax(self):
        expr = _expresion_zoom_gancho(TRATAMIENTOS["byte_reacciona"], 100)
        self.assertTrue(expr.startswith("zoompan=z='1+"))
        self.assertIn("0.0400", expr)  # amplitud = z_max - 1 = 0.04
        self.assertIn("on", expr)
        self.assertIn("540-540/zoom", expr)

    def test_lento_c_lineal(self):
        expr = _expresion_zoom_gancho(TRATAMIENTOS["mockup_inmediato"], 100)
        self.assertIn("clip(on/", expr)
        self.assertIn("0.0300", expr)  # amplitud = z_max - 1 = 0.03

    def test_control_vacio(self):
        self.assertEqual(_expresion_zoom_gancho(TRATAMIENTOS["texto_pantalla"], 100), "")


class TestLintGancho(unittest.TestCase):
    def _guion(self, **kw):
        base = {
            "video": 99,
            "cold_open": "Dicen que tu asistente de voz te escucha todo el dia,",
            "hook": "Y por eso el miedo vuelve,",
        }
        base.update(kw)
        return base

    def _problemas(self, guion):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / f"guion_{guion.get('video', 99):02d}_test.json"
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(guion, f, ensure_ascii=False)
            numero = lint_gancho._numero_desde_ruta(ruta)
            return lint_gancho._revisar_guion(ruta, guion, numero)

    def test_guion_conforme_sin_problemas(self):
        self.assertEqual(self._problemas(self._guion()), [])

    def test_puntos_en_cold_open(self):
        ps = self._problemas(self._guion(cold_open="Esto tiene punto. Y sigue,"))
        self.assertIn("sin_puntos", [p.check for p in ps])

    def test_puntos_en_hook(self):
        ps = self._problemas(self._guion(hook="Esto también."))
        self.assertIn("sin_puntos", [p.check for p in ps])

    def test_cold_open_demasiado_largo(self):
        ps = self._problemas(self._guion(cold_open=" ".join(["palabra"] * 19)))
        self.assertIn("longitud", [p.check for p in ps])

    def test_hook_demasiado_largo(self):
        ps = self._problemas(self._guion(hook=" ".join(["palabra"] * 21)))
        self.assertIn("longitud", [p.check for p in ps])

    def test_porcentaje_inventado(self):
        ps = self._problemas(self._guion(hook="Ahorra un 90% de tiempo,"))
        self.assertIn("sin_promesas", [p.check for p in ps])

    def test_garantia_imposible(self):
        ps = self._problemas(self._guion(hook="Garantizado sin fallas,"))
        self.assertIn("sin_promesas", [p.check for p in ps])

    def test_rotacion_mismo_preferido_consecutivo(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_g = Path(tmp)
            for num in (1, 2):
                g = self._guion(video=num)
                with open(dir_g / f"guion_{num:02d}_x.json", "w", encoding="utf-8") as f:
                    json.dump(g, f)
            # Fijar el mismo preferido en ambos configs del registro no es
            # posible aquí (CONFIGS es real); se prueba la función directamente.
            problemas, n = lint_gancho.auditar(dir_g)
            self.assertEqual(n, 2)
            # Sin gancho_preferido fijo en el registro, no hay rotación FAIL
            self.assertEqual([p for p in problemas if p.check == "rotacion"], [])

    def test_rotacion_detecta_mismo_preferido(self):
        por_numero = {10: "byte_reacciona", 11: "byte_reacciona"}
        ps = lint_gancho._revisar_rotacion(11, "byte_reacciona", por_numero)
        self.assertEqual([p.check for p in ps], ["rotacion"])

    def test_auditar_catalogo_real_no_crashea(self):
        problemas, n = lint_gancho.auditar(DIR_RAIZ / "guiones")
        self.assertGreater(n, 0)
        # El catálogo histórico puede tener FAIL legítimos; solo verificamos
        # que la auditoría corre y devuelve la estructura correcta.
        for p in problemas:
            self.assertTrue(p.check and p.mensaje)


if __name__ == "__main__":
    unittest.main(verbosity=2)

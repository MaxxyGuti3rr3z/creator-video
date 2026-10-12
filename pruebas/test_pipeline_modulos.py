r"""
Test unitario de la partición del monolito:
  - src/bloques_narrativos.py
  - src/audio_elevenlabs.py (hash + índice de caché; NUNCA llama a la API)
  - src/segmentacion.py (segmentación con alignments sintéticos)
  - import del orquestador pruebas/prueba_end_to_end.py (no ejecuta main)

Nunca gasta créditos de ElevenLabs ni ejecuta el pipeline completo.

Ejecutar: python pruebas/test_pipeline_modulos.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.bloques_narrativos import (
    concatenar_texto_completo,
    construir_bloques_narrativos,
)
from src.audio_elevenlabs import (
    VOICE_SETTINGS_DEFAULT,
    calcular_hash_audio,
    cargar_indice_cache,
    guardar_indice_cache,
)
from src.segmentacion import calcular_segmentos_reales


def guion_estructurado(cold_open=True):
    g = {
        "hook": "¿Bandeja de entrada llena?",
        "problema": "Los mensajes repetitivos te roban la energía",
        "demostracion": [
            {"accion": "Shortwave redacta borradores automáticos"},
            {"accion": "SaneBox filtra los correos importantes"},
        ],
        "resultado": "Recuperas tu foco en minutos",
        "cierre": "Comentá cuántos correos sin leer tenés",
    }
    if cold_open:
        g["cold_open"] = "Son las nueve de la mañana y ya son cincuenta correos nuevos"
    return g


def guion_legado():
    return {
        "hook": "¿Bandeja de entrada llena de mensajes repetitivos que te roban la energía?",
        "puntos": [
            {
                "herramienta_o_tip": "Shortwave",
                "explicacion": "Redacta borradores automáticos con inteligencia artificial.",
                "opinion_byte": "Me encanta cómo clava un tono natural.",
            },
            {
                "herramienta_o_tip": "SaneBox",
                "explicacion": "Filtra tus correos importantes a carpetas secundarias.",
                "opinion_byte": "Después de revisarlo te limpia todo el caos.",
            },
        ],
        "cierre": "Comentá abajo cuántos correos sin leer acumulás hoy.",
    }


def alineacion_sintetica(bloques, paso=0.1):
    """Alignment carácter-por-carácter sintético (monótono, sin solapes)."""
    completo = " ".join(b["texto"] for b in bloques)
    chars = list(completo)
    n = len(chars)
    return {
        "characters": chars,
        "character_start_times_seconds": [round(i * paso, 3) for i in range(n)],
        "character_end_times_seconds": [round((i + 1) * paso, 3) for i in range(n)],
    }, round(n * paso, 3)


class TestBloquesNarrativos(unittest.TestCase):
    def test_estructura_completa_con_cold_open(self):
        bloques = construir_bloques_narrativos(guion_estructurado(cold_open=True))
        tipos = [b["tipo"] for b in bloques]
        self.assertEqual(
            tipos,
            ["cold_open", "hook", "problema", "punto_1", "punto_2", "resultado", "cierre"],
        )

    def test_estructura_completa_sin_cold_open(self):
        bloques = construir_bloques_narrativos(guion_estructurado(cold_open=False))
        tipos = [b["tipo"] for b in bloques]
        self.assertEqual(
            tipos,
            ["hook", "problema", "punto_1", "punto_2", "resultado", "cierre"],
        )

    def test_fallback_legado_cuatro_bloques(self):
        bloques = construir_bloques_narrativos(guion_legado())
        tipos = [b["tipo"] for b in bloques]
        self.assertEqual(tipos, ["hook", "punto_1", "punto_2", "cierre"])
        self.assertIn("Shortwave", bloques[1]["texto"])
        self.assertIn("tono natural", bloques[1]["texto"])

    def test_bloque_vacio_filtrado(self):
        g = guion_estructurado(cold_open=True)
        g["resultado"] = "   "
        tipos = [b["tipo"] for b in construir_bloques_narrativos(g)]
        self.assertNotIn("resultado", tipos)
        self.assertEqual(len(tipos), 6)

    def test_concatenar_cold_open_continuo(self):
        bloques = construir_bloques_narrativos(guion_estructurado(cold_open=True))
        texto = concatenar_texto_completo(bloques)
        self.assertNotIn("\n\n", texto)
        self.assertTrue(texto.startswith("Son las nueve"))
        self.assertIn("? ", texto)

    def test_concatenar_hook_problema_con_interrogante(self):
        bloques = construir_bloques_narrativos(guion_estructurado(cold_open=False))
        texto = concatenar_texto_completo(bloques)
        escena, resto = texto.split("\n\n", 1)
        self.assertEqual(
            escena,
            "¿Bandeja de entrada llena? Los mensajes repetitivos te roban la energía",
        )
        self.assertFalse(escena.endswith(","))
        self.assertIn("\n\n", resto)

    def test_concatenar_hook_problema_sin_signo_usa_coma(self):
        bloques = [
            {"tipo": "hook", "texto": "Esto te interesa"},
            {"tipo": "problema", "texto": "Tu bandeja está colapsada"},
            {"tipo": "cierre", "texto": "Dejá tu comentario"},
        ]
        texto = concatenar_texto_completo(bloques)
        escena = texto.split("\n\n", 1)[0]
        self.assertEqual(escena, "Esto te interesa, Tu bandeja está colapsada")

    def test_concatenar_legado_separa_con_dobles_saltos(self):
        bloques = construir_bloques_narrativos(guion_legado())
        texto = concatenar_texto_completo(bloques)
        self.assertEqual(texto.count("\n\n"), 3)


class TestAudioCache(unittest.TestCase):
    def test_hash_determinista(self):
        h1 = calcular_hash_audio("Hola mundo", "voz_1")
        h2 = calcular_hash_audio("Hola mundo", "voz_1")
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)

    def test_hash_sensible_a_los_factores(self):
        base = calcular_hash_audio("Hola mundo", "voz_1")
        self.assertNotEqual(base, calcular_hash_audio("Hola mundo!", "voz_1"))
        self.assertNotEqual(base, calcular_hash_audio("Hola mundo", "voz_2"))
        self.assertNotEqual(
            base,
            calcular_hash_audio(
                "Hola mundo", "voz_1",
                voice_settings={**VOICE_SETTINGS_DEFAULT, "speed": 1.0},
            ),
        )

    def test_indice_cache_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "sub" / "cache_audio_index.json"
            indice = {"abc": {"voice_id": "v1", "texto_preview": "Previsualización"}}
            guardar_indice_cache(indice, ruta)
            self.assertTrue(ruta.exists())
            self.assertEqual(cargar_indice_cache(ruta), indice)

    def test_indice_cache_inexistente_devuelve_vacio(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cargar_indice_cache(Path(tmp) / "no_existe.json"), {})

    def test_indice_cache_corrupto_devuelve_vacio(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "cache_audio_index.json"
            ruta.write_text("{esto no es json", encoding="utf-8")
            self.assertEqual(cargar_indice_cache(ruta), {})


class TestSegmentacion(unittest.TestCase):
    def test_seis_bloques_producen_cinco_escenas(self):
        bloques = construir_bloques_narrativos(guion_estructurado(cold_open=False))
        alignment, duracion = alineacion_sintetica(bloques)
        segs = calcular_segmentos_reales(alignment, bloques, duracion)

        self.assertEqual(len(segs), 5)
        self.assertEqual(
            [s["tipo"] for s in segs],
            ["escena_problema", "punto_1", "punto_2", "resultado", "cierre"],
        )
        self.assertEqual(segs[0]["inicio"], 0.0)
        self.assertEqual(segs[-1]["fin"], round(duracion, 3))
        for a, b in zip(segs, segs[1:]):
            self.assertEqual(a["fin"], b["inicio"], f"descontinuidad entre {a['tipo']} y {b['tipo']}")
        for s in segs:
            self.assertLessEqual(s["inicio"], s["fin"])

        texto_problema = f"{bloques[0]['texto']} {bloques[1]['texto']}"
        self.assertEqual(segs[0]["texto"], texto_problema)
        self.assertEqual(len(segs[0]["bloques_internos"]), 2)

    def test_siete_bloques_cold_open_mantienen_siete_escenas(self):
        bloques = construir_bloques_narrativos(guion_estructurado(cold_open=True))
        alignment, duracion = alineacion_sintetica(bloques)
        segs = calcular_segmentos_reales(alignment, bloques, duracion)

        self.assertEqual(len(segs), 7)
        self.assertEqual(segs[0]["tipo"], "cold_open")
        self.assertEqual(segs[0]["inicio"], 0.0)
        self.assertEqual(segs[-1]["fin"], round(duracion, 3))
        for a, b in zip(segs, segs[1:]):
            self.assertEqual(a["fin"], b["inicio"])

    def test_cuatro_bloques_legado_usa_fallback(self):
        bloques = construir_bloques_narrativos(guion_legado())
        alignment, duracion = alineacion_sintetica(bloques)
        segs = calcular_segmentos_reales(alignment, bloques, duracion)

        self.assertEqual(len(segs), 4)
        self.assertEqual(
            [s["tipo"] for s in segs], ["hook", "punto_1", "punto_2", "cierre"]
        )
        self.assertEqual(segs[0]["inicio"], 0.0)
        self.assertEqual(segs[-1]["fin"], round(duracion, 3))
        for a, b in zip(segs, segs[1:]):
            self.assertEqual(a["fin"], b["inicio"])


class TestOrquestador(unittest.TestCase):
    def test_import_orquestador_con_api_intacta(self):
        from pruebas import prueba_end_to_end as e2e

        self.assertTrue(callable(e2e.main))
        self.assertTrue(callable(e2e.cargar_guion))
        self.assertIsInstance(e2e.GUION_REAL, dict)
        self.assertIn("hook", e2e.GUION_REAL)
        primera_linea = next(l for l in e2e.__doc__.splitlines() if l.strip())
        self.assertEqual(primera_linea.strip(), "prueba_end_to_end.py")

    def test_cargar_guion_explicito_guion_14(self):
        from pruebas.prueba_end_to_end import cargar_guion

        guion, v_paths, nombre_base, ruta = cargar_guion("guion_14_agua_ia.json")

        self.assertIsInstance(guion, dict)
        self.assertIn("hook", guion)
        self.assertIn("problema", guion)
        self.assertIsInstance(nombre_base, str)
        self.assertTrue(nombre_base)
        self.assertEqual(
            set(v_paths.keys()), {"base", "entrada", "intermedios", "final"}
        )
        self.assertIsNotNone(ruta)
        self.assertEqual(ruta.suffix, ".json")
        self.assertTrue(ruta.exists())
        self.assertTrue(all(isinstance(p, Path) for p in v_paths.values()))

    def test_cargar_guion_inexistente_cae_al_guion_de_prueba(self):
        from unittest import mock

        from pruebas import prueba_end_to_end as e2e

        # ruta_video tiene efectos secundarios (mkdir): se sustituye por tmp
        with tempfile.TemporaryDirectory() as tmp:
            fake = {k: Path(tmp) / k for k in ("base", "entrada", "intermedios", "final")}
            with mock.patch.object(e2e, "ruta_video", return_value=fake):
                guion, v_paths, nombre_base, ruta = e2e.cargar_guion("no_existe_xyz.json")

        self.assertEqual(guion, e2e.GUION_REAL)
        self.assertIsNone(ruta)
        self.assertEqual(nombre_base, "prueba_real")
        self.assertEqual(v_paths, fake)


if __name__ == "__main__":
    unittest.main(verbosity=2)

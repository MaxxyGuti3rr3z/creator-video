"""
Tests de src/eventos_voz.py: sincronía UI-voz a partir del alignment
carácter por carácter de ElevenLabs.

Ejecutar: python pruebas/test_eventos_voz.py
"""
import sys
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.eventos_voz import (
    construir_eventos_escena,
    encontrar_inicio,
    normalizar,
    palabras_de_segmento,
)


def alignment_sintetico(texto: str, cps: float = 12.0, offset: float = 0.0) -> dict:
    """Alignment carácter por carácter con tiempos uniformes a cps chars/s."""
    chars = list(texto)
    starts = [offset + i / cps for i in range(len(chars))]
    ends = [offset + (i + 1) / cps for i in range(len(chars))]
    return {
        "characters": chars,
        "character_start_times_seconds": starts,
        "character_end_times_seconds": ends,
    }


class TestNormalizar(unittest.TestCase):
    def test_minusculas_y_acentos(self):
        self.assertEqual(normalizar("Buscá"), "busca")
        self.assertEqual(normalizar("MÁS"), "mas")
        self.assertEqual(normalizar("pedís"), "pedis")

    def test_puntuacion_pegada(self):
        self.assertEqual(normalizar("mensajes,"), "mensajes")
        self.assertEqual(normalizar("¿Cuál?"), "cual")


class TestPalabrasDeSegmento(unittest.TestCase):
    def test_extraccion_basica(self):
        seg = {"texto": "hola  mundo cruel", "inicio": 2.0, "fin": 4.0}
        al = alignment_sintetico("hola  mundo cruel", offset=2.0)
        pals = palabras_de_segmento(seg, al)
        self.assertEqual([p[0] for p in pals], ["hola", "mundo", "cruel"])
        self.assertAlmostEqual(pals[0][1], 2.0, places=2)
        self.assertAlmostEqual(pals[1][1], 2.0 + 6 / 12.0, places=2)

    def test_ventana_de_segmento(self):
        seg = {"texto": "mundo", "inicio": 0.4, "fin": 0.9}
        al = alignment_sintetico("hola  mundo cruel")
        pals = palabras_de_segmento(seg, al)
        self.assertEqual([p[0] for p in pals], ["mundo"])

    def test_alignment_incompleto_fallback_uniforme(self):
        seg = {"texto": "dos palabras", "inicio": 1.0, "fin": 3.0}
        pals = palabras_de_segmento(seg, {"characters": [], "character_start_times_seconds": []})
        self.assertEqual(len(pals), 2)
        self.assertAlmostEqual(pals[0][1], 1.0)
        self.assertAlmostEqual(pals[1][1], 2.0)


class TestEncontrarInicio(unittest.TestCase):
    PALABRAS = [
        ("pero", 10.0, 10.2),
        ("la", 10.2, 10.3),
        ("asistente", 10.3, 10.8),
        ("recien", 11.0, 11.3),
        ("despues", 11.3, 11.7),
    ]

    def test_match_acentos_insensible(self):
        self.assertAlmostEqual(encontrar_inicio(self.PALABRAS, "después"), 11.3, places=2)
        self.assertAlmostEqual(encontrar_inicio(self.PALABRAS, "RECién"), 11.0, places=2)

    def test_match_frase_consecutiva(self):
        self.assertAlmostEqual(
            encontrar_inicio(self.PALABRAS, "recién después"), 11.0, places=2
        )

    def test_prefijo_mas_largo_gana(self):
        # "recien despues" (2 palabras) debe matchear en recien (11.0), no en despues
        self.assertAlmostEqual(
            encontrar_inicio(self.PALABRAS, "recién después x"), 11.0, places=2
        )

    def test_sin_match_devuelve_none(self):
        self.assertIsNone(encontrar_inicio(self.PALABRAS, "zzz inexistente"))
        self.assertIsNone(encontrar_inicio([], "hola"))


class TestConstruirEventosEscena(unittest.TestCase):
    def test_typing_sincronizado_y_ui(self):
        texto = "Dicen que tu celular te escucha todo el día"
        seg = {"texto": texto, "inicio": 0.0, "fin": 3.5}
        ev = construir_eventos_escena(
            seg, alignment_sintetico(texto),
            pildora="tu celular te escucha", ui_clave=["escucha"],
        )
        # "tu celular te escucha" arranca en la 't' de "tu" (idx 10 chars)
        self.assertAlmostEqual(ev["t_pildora"], 10 / 12.0, places=2)
        self.assertAlmostEqual(ev["t_ui"], 24 / 12.0, places=2)

    def test_tiempos_relativos_a_la_escena(self):
        texto = "procesa recién después"
        seg = {"texto": texto, "inicio": 7.0, "fin": 9.0}
        al = alignment_sintetico(texto)
        # desplazamos el alignment global al inicio del segmento
        al = {
            "characters": al["characters"],
            "character_start_times_seconds": [t + 7.0 for t in al["character_start_times_seconds"]],
            "character_end_times_seconds": [t + 7.0 for t in al["character_end_times_seconds"]],
        }
        ev = construir_eventos_escena(seg, al, pildora="recién después")
        self.assertAlmostEqual(ev["t_pildora"], 8 / 12.0, places=2)
        self.assertLess(ev["t_pildora"], 2.0)  # local a la escena

    def test_fallback_proporcional_sin_match(self):
        seg = {"texto": "nada que ver", "inicio": 0.0, "fin": 10.0}
        ev = construir_eventos_escena(seg, alignment_sintetico("nada que ver"), pildora="texto imposible")
        self.assertAlmostEqual(ev["t_pildora"], 3.0, places=2)  # 30% de 10s
        self.assertIsNone(ev["t_ui"])

    def test_sin_pildora_ni_clave(self):
        seg = {"texto": "hola", "inicio": 0.0, "fin": 1.0}
        ev = construir_eventos_escena(seg, alignment_sintetico("hola"))
        self.assertIsNone(ev["t_pildora"])
        self.assertIsNone(ev["t_ui"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

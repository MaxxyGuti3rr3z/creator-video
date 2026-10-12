"""
Test unitario del linter de subtítulos ASS (pruebas/lint_subtitulos.py).

Construye .ass sintéticos mínimos (header + estilo + metadata + diálogos)
y verifica cada regla, sin depender de los videos reales del repo.

Ejecutar: python pruebas/test_lint_subtitulos.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from pruebas.lint_subtitulos import (
    ESTILO_ESPERADO,
    lintear_ass,
    main,
)

ESTILO_LINEA = (
    "Style: KaraokeByte,Arial,46,&H0000F5FF,&H00FFFFFF,&H00000000,&H90000000,"
    "-1,0,0,0,100,100,1,0,1,4.5,2.5,2,80,80,860,1"
)

METADATA = [
    {"tipo": "cold_open", "texto": "a", "inicio": 0.0, "fin": 3.0},
    {"tipo": "punto_1", "texto": "b", "inicio": 3.0, "fin": 6.0},
]

# 5 palabras, \\N presente, sublíneas de 3 y 2, \\k suma 136 cs = duración 1.36s
DLG_BUENO = (
    "Dialogue: 0,0:00:00.00,0:00:01.36,KaraokeByte,,0,0,0,,"
    "{\\k38}DICEN {\\k14}QUE {\\k27}CADA\\N{\\k50}PREGUNTA {\\k7}A"
)
# Demo (punto_1) de 3 palabras con \\N, \\k suma 60 = 0.60s
DLG_DEMO = (
    "Dialogue: 0,0:00:03.00,0:00:03.60,KaraokeByte,,0,0,0,,"
    "{\\k20}UNA {\\k20}COSA {\\k20}MÁS\\N"
    ""
)


def ass_texto(dialogos, estilo=ESTILO_LINEA, metadata=METADATA):
    meta = "; SEGMENTS_METADATA: " + json.dumps(metadata)
    lineas = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        meta,
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        estilo,
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ] + list(dialogos)
    return "\n".join(lineas) + "\n"


def escribir(tmp: Path, contenido: str, nombre="test.ass") -> Path:
    p = tmp / nombre
    p.write_text(contenido, encoding="utf-8")
    return p


class TestEstilo(unittest.TestCase):
    def _problemas(self, estilo):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir(Path(tmp), ass_texto([DLG_BUENO], estilo=estilo))
            problemas, _ = lintear_ass(ruta)
        return problemas

    def test_archivo_bueno_sin_problemas(self):
        self.assertEqual(self._problemas(ESTILO_LINEA), [])

    def test_fontsize_58_falla(self):
        estilo = ESTILO_LINEA.replace("Arial,46,", "Arial,58,")
        self.assertTrue(any("Fontsize" in p for p in self._problemas(estilo)))

    def test_margin_l_cero_falla(self):
        estilo = ESTILO_LINEA.replace(",2,80,80,860,1", ",2,0,80,860,1")
        self.assertTrue(any("MarginL" in p for p in self._problemas(estilo)))

    def test_color_primario_blanco_falla(self):
        estilo = ESTILO_LINEA.replace("&H0000F5FF,", "&H00FFFFFF,", 1)
        self.assertTrue(any("PrimaryColour" in p for p in self._problemas(estilo)))

    def test_margin_v_900_falla(self):
        estilo = ESTILO_LINEA.replace(",80,80,860,1", ",80,80,900,1")
        self.assertTrue(any("MarginV" in p for p in self._problemas(estilo)))

    def test_playres_malo_falla(self):
        with tempfile.TemporaryDirectory() as tmp:
            contenido = ass_texto([DLG_BUENO]).replace("PlayResX: 1080", "PlayResX: 720")
            ruta = escribir(Path(tmp), contenido)
            problemas, _ = lintear_ass(ruta)
        self.assertTrue(any("PlayResX" in p for p in problemas))

    def test_estilo_ausente_falla(self):
        contenido = "\n".join(
            l for l in ass_texto([DLG_BUENO]).splitlines() if not l.startswith("Style:")
        ) + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir(Path(tmp), contenido)
            problemas, _ = lintear_ass(ruta)
        self.assertTrue(any("KaraokeByte" in p or "Style" in p for p in problemas))


class TestDialogos(unittest.TestCase):
    def _problemas(self, dialogos, metadata=METADATA):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir(Path(tmp), ass_texto(dialogos, metadata=metadata))
            problemas, _ = lintear_ass(ruta)
        return problemas

    def test_tres_palabras_sin_n_falla(self):
        dlg = (
            "Dialogue: 0,0:00:00.00,0:00:00.50,KaraokeByte,,0,0,0,,"
            "{\\k17}UNA {\\k17}DOS {\\k16}TRES"
        )
        self.assertTrue(any("\\N" in p for p in self._problemas([dlg])))

    def test_tres_sublineas_fallan(self):
        dlg = (
            "Dialogue: 0,0:00:00.00,0:00:00.60,KaraokeByte,,0,0,0,,"
            "{\\k20}UNA\\N{\\k20}DOS\\N{\\k20}TRES"
        )
        self.assertTrue(any("sublíneas" in p for p in self._problemas([dlg])))

    def test_cuatro_palabras_en_sublinea_fallan(self):
        dlg = (
            "Dialogue: 0,0:00:00.00,0:00:00.80,KaraokeByte,,0,0,0,,"
            "{\\k20}UNA {\\k20}DOS {\\k20}TRES {\\k20}CUATRO\\N"
        )
        self.assertTrue(any("sublínea con 4 palabras" in p for p in self._problemas([dlg])))

    def test_sublinea_larga_en_caracteres_falla(self):
        dlg = (
            "Dialogue: 0,0:00:00.00,0:00:00.60,KaraokeByte,,0,0,0,,"
            "{\\k20}CONVERSACIONES {\\k20}EXTRAORDINARIAS {\\k20}INTERNACIONALES\\N"
        )
        self.assertTrue(any("caracteres" in p for p in self._problemas([dlg])))

    def test_k_desbalanceado_falla(self):
        dlg = (
            "Dialogue: 0,0:00:00.00,0:00:01.00,KaraokeByte,,0,0,0,,"
            "{\\k20}UNA {\\k20}DOS\\N"
        )
        self.assertTrue(any("suma de \\k" in p for p in self._problemas([dlg])))

    def test_solape_falla(self):
        dlg1 = (
            "Dialogue: 0,0:00:00.00,0:00:01.36,KaraokeByte,,0,0,0,,"
            "{\\k38}DICEN {\\k14}QUE {\\k27}CADA\\N{\\k50}PREGUNTA {\\k7}A"
        )
        dlg2 = (
            "Dialogue: 0,0:00:01.00,0:00:01.60,KaraokeByte,,0,0,0,,"
            "{\\k30}LA {\\k30}IA\\N"
        )
        self.assertTrue(any("solapa" in p for p in self._problemas([dlg1, dlg2])))

    def test_texto_vacio_falla(self):
        dlg = "Dialogue: 0,0:00:00.00,0:00:00.50,KaraokeByte,,0,0,0,,{}"
        self.assertTrue(any("vacío" in p for p in self._problemas([dlg])))

    def test_sin_k_falla(self):
        dlg = "Dialogue: 0,0:00:00.00,0:00:00.50,KaraokeByte,,0,0,0,,HOLA MUNDO\\N"
        self.assertTrue(any("\\k" in p for p in self._problemas([dlg])))

    def test_chunk_clave_de_siete_falla(self):
        dlg = (
            "Dialogue: 0,0:00:00.00,0:00:01.40,KaraokeByte,,0,0,0,,"
            "{\\k20}UNA {\\k20}DOS {\\k20}TRES\\N{\\k20}CUATRO {\\k20}CINCO {\\k20}SEIS {\\k20}SIETE"
        )
        self.assertTrue(any("máximo 6" in p for p in self._problemas([dlg])))

    def test_chunk_demo_de_cinco_falla(self):
        dlg = (
            "Dialogue: 0,0:00:03.00,0:00:03.80,KaraokeByte,,0,0,0,,"
            "{\\k16}UNA {\\k16}DOS {\\k16}TRES\\N{\\k16}CUATRO {\\k16}CINCO"
        )
        self.assertTrue(any("máximo 4" in p for p in self._problemas([dlg])))

    def test_chunk_demo_de_tres_pasa(self):
        self.assertEqual(self._problemas([DLG_DEMO]), [])

    def test_sin_metadata_universal_seis(self):
        dlg7 = (
            "Dialogue: 0,0:00:00.00,0:00:01.40,KaraokeByte,,0,0,0,,"
            "{\\k20}UNA {\\k20}DOS {\\k20}TRES\\N{\\k20}CUATRO {\\k20}CINCO {\\k20}SEIS {\\k20}SIETE"
        )
        self.assertTrue(any("máximo 6" in p for p in self._problemas([dlg7], metadata=[])))

    def test_dialogos_en_tiempos_de_demo_validos(self):
        self.assertEqual(self._problemas([DLG_BUENO, DLG_DEMO]), [])


class TestCLI(unittest.TestCase):
    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            bueno = escribir(tmp, ass_texto([DLG_BUENO]), "bueno.ass")
            malo = escribir(
                tmp,
                ass_texto([DLG_BUENO], estilo=ESTILO_LINEA.replace("Arial,46,", "Arial,58,")),
                "malo.ass",
            )
            rc_ok = main([str(bueno)])
            rc_fail = main([str(malo)])
            rc_dir = main([str(tmp)])
        self.assertEqual(rc_ok, 0)
        self.assertEqual(rc_fail, 1)
        self.assertEqual(rc_dir, 1)

    def test_directorio_vacio_pasa(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc = main([tmp])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

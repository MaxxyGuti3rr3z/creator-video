"""
Tests de src/registro_experimentos.py: formato puro + E/S de CSV en tmp.

Ejecutar: python pruebas/test_registro_experimentos.py
"""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.registro_experimentos import (
    COLUMNAS,
    Experimento,
    formatear_fila,
    leer_experimentos,
    registrar_experimento,
)


def _exp(**kw) -> Experimento:
    base = dict(
        video=15,
        variante_id="B",
        arquetipo_gancho="byte_reacciona",
        punch_enfasis=True,
        ruta_mp4="videos/video_15/final/video_15.mp4",
        notas="prueba",
        fecha_utc="2026-10-13T00:00:00Z",
    )
    base.update(kw)
    return Experimento(**base)


class TestFormatearFila(unittest.TestCase):
    def test_orden_de_columnas(self):
        fila = formatear_fila(_exp())
        self.assertEqual(len(fila), len(COLUMNAS))
        self.assertEqual(fila[0], "2026-10-13T00:00:00Z")
        self.assertEqual(fila[1], "15")
        self.assertEqual(fila[2], "B")
        self.assertEqual(fila[3], "byte_reacciona")
        self.assertEqual(fila[4], "si")
        self.assertEqual(fila[5], "videos/video_15/final/video_15.mp4")
        self.assertEqual(fila[6], "prueba")

    def test_punch_enfasis_si_no(self):
        self.assertEqual(formatear_fila(_exp(punch_enfasis=True))[4], "si")
        self.assertEqual(formatear_fila(_exp(punch_enfasis=False))[4], "no")

    def test_fecha_none_genera_utc(self):
        fila = formatear_fila(_exp(fecha_utc=None))
        self.assertTrue(fila[0].endswith("Z"))
        self.assertRegex(fila[0], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class TestRegistroCSV(unittest.TestCase):
    def test_crea_con_cabecera_y_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "datos" / "experimentos.csv"
            registrar_experimento(ruta, _exp(variante_id="A"))
            registrar_experimento(ruta, _exp(variante_id="B"))
            filas = leer_experimentos(ruta)
            self.assertEqual(len(filas), 2)
            self.assertEqual(list(filas[0].keys()), list(COLUMNAS))
            self.assertEqual([f["variante_id"] for f in filas], ["A", "B"])

    def test_no_duplica_cabecera(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "exp.csv"
            for _ in range(3):
                registrar_experimento(ruta, _exp())
            contenido = ruta.read_text(encoding="utf-8").splitlines()
            self.assertEqual(contenido[0], ",".join(COLUMNAS))
            self.assertEqual(len(contenido), 4)  # 1 cabecera + 3 filas

    def test_leer_inexistente_da_vacio(self):
        self.assertEqual(leer_experimentos(Path("no/existe.csv")), [])

    def test_campos_con_comas_escapan(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "exp.csv"
            registrar_experimento(ruta, _exp(notas="a,b;c"))
            fila = leer_experimentos(ruta)[0]
            self.assertEqual(fila["notas"], "a,b;c")


if __name__ == "__main__":
    unittest.main(verbosity=2)

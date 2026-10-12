r"""
Test unitario del CI local (pruebas/ci_local.py).

Verifica el registro de suites, el parseo de salida de unittest y el CLI
--lista; no ejecuta las suites (evita recursión: ci_local corre test_ci_local).

Ejecutar: python pruebas/test_ci_local.py
"""
import subprocess
import sys
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from pruebas import ci_local

RUTA_CI = DIR_RAIZ / "pruebas" / "ci_local.py"

SUITES_CON_FFMPEG = {"test_chequeos_pipeline", "test_shorts_assembler"}


def ejecutar_cli(*args):
    return subprocess.run(
        [sys.executable, str(RUTA_CI), *args],
        cwd=str(DIR_RAIZ),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


class TestRegistroSuites(unittest.TestCase):
    def test_las_rutas_del_registro_existentes(self):
        for suite in ci_local.SUITES:
            self.assertTrue(
                (DIR_RAIZ / suite.ruta).is_file(), f"no existe: {suite.ruta}"
            )

    def test_rutas_unicas(self):
        rutas = [s.ruta for s in ci_local.SUITES]
        self.assertEqual(len(rutas), len(set(rutas)))

    def test_ffmpeg_marcado_solo_en_las_dos_que_lo_necesitan(self):
        con_ffmpeg = {s.nombre for s in ci_local.SUITES if s.requiere_ffmpeg}
        self.assertEqual(con_ffmpeg, SUITES_CON_FFMPEG)

    def test_seleccionar_sin_ffmpeg_excluye_solo_esas(self):
        puros = ci_local.seleccionar(sin_ffmpeg=True)
        todas = ci_local.seleccionar(sin_ffmpeg=False)
        self.assertEqual(len(todas), len(ci_local.SUITES))
        self.assertTrue(all(not s.requiere_ffmpeg for s in puros))
        self.assertEqual(
            {s.nombre for s in todas} - {s.nombre for s in puros},
            SUITES_CON_FFMPEG,
        )


class TestParsearSalida(unittest.TestCase):
    def test_suite_ok(self):
        salida = ".......\n----------------------------------------------------------------------\nRan 19 tests in 0.165s\n\nOK\n"
        self.assertEqual(ci_local.parsear_salida(salida, 0), (19, True))

    def test_suite_con_fallos(self):
        salida = "F\n----------------------------------------------------------------------\nRan 3 tests in 0.01s\n\nFAILED (failures=1)\n"
        self.assertEqual(ci_local.parsear_salida(salida, 1), (3, False))

    def test_suite_crasheada_sin_resumen(self):
        salida = "Traceback (most recent call last):\n  ...\nModuleNotFoundError: 'x'\n"
        self.assertEqual(ci_local.parsear_salida(salida, 1), (0, False))

    def test_exit_cero_sin_resumen_no_es_ok(self):
        self.assertEqual(ci_local.parsear_salida("algo raro\n", 0), (0, False))


class TestCLI(unittest.TestCase):
    def test_lista_exit_0_sin_ejecutar_suites(self):
        proc = ejecutar_cli("--lista")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("test_lint_zonas", proc.stdout)
        self.assertIn("test_ci_local", proc.stdout)
        self.assertNotIn("Ran", proc.stdout)

    def test_lista_sin_ffmpeg_excluye_las_dos(self):
        proc = ejecutar_cli("--sin-ffmpeg", "--lista")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        lineas = proc.stdout.splitlines()
        linea_shorts = next(l for l in lineas if "test_shorts_assembler" in l)
        self.assertIn("[excluida: ffmpeg]", linea_shorts)
        linea_pura = next(l for l in lineas if "test_lint_zonas" in l)
        self.assertNotIn("excluida", linea_pura)


class TestHook(unittest.TestCase):
    def test_hook_existe_y_es_lf(self):
        hook = DIR_RAIZ / ".githooks" / "pre-push"
        self.assertTrue(hook.is_file(), ".githooks/pre-push no existe")
        contenido = hook.read_bytes()
        self.assertTrue(contenido.startswith(b"#!/bin/sh\n"))
        self.assertNotIn(b"\r", contenido, "el hook debe quedar en LF")
        self.assertIn(b"ci_local.py", contenido)

    def test_gitattributes_protege_los_hooks(self):
        attrs = DIR_RAIZ / ".gitattributes"
        self.assertTrue(attrs.is_file())
        self.assertIn(".githooks", attrs.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

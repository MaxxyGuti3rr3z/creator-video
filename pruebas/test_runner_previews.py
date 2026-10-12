r"""
Test unitario del runner de previews (pruebas/previews.py).

Verifica el registro contra los scripts reales (glob test_previews_*.py),
la importabilidad de los módulos y el CLI — sin renderizar PNG.

Los scripts 10-14 se importan (main() invocable) porque no tienen side
effects a nivel módulo; director/06/09/09_v2 ejecutan mkdir al importar,
así que solo se comprueba su existencia con find_spec.

Ejecutar: python pruebas/test_runner_previews.py
"""
import importlib
import subprocess
import sys
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from pruebas import previews

RUTA_RUNNER = DIR_RAIZ / "pruebas" / "previews.py"

# Módulos sin side effects a nivel módulo (sin mkdir al importar)
MODULOS_SEGUROS = (
    "test_previews_video_10",
    "test_previews_video_11",
    "test_previews_video_12",
    "test_previews_video_13",
    "test_previews_video_14",
)


def ejecutar_cli(*args):
    return subprocess.run(
        [sys.executable, str(RUTA_RUNNER), *args],
        cwd=str(DIR_RAIZ),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


class TestRegistro(unittest.TestCase):
    def test_registro_cubre_todos_los_scripts(self):
        encontrados = {p.stem for p in (DIR_RAIZ / "pruebas").glob("test_previews_*.py")}
        registrados = {modulo for modulo, _ in previews.REGISTRO.values()}
        self.assertEqual(
            registrados,
            encontrados,
            "registro y glob test_previews_*.py divergen: "
            f"solo en registro={registrados - encontrados}, "
            f"solo en disco={encontrados - registrados}",
        )

    def test_claves_normalizadas_y_alias(self):
        for clave in previews.REGISTRO:
            self.assertEqual(previews.normalizar_clave(clave), clave, clave)
        self.assertEqual(previews.normalizar_clave(" 09V2 "), "09_v2")
        self.assertEqual(previews.normalizar_clave("09_v2"), "09_v2")
        self.assertNotIn("09v2", previews.REGISTRO)

    def test_modulos_del_registro_existentes(self):
        for clave, (modulo, _desc) in previews.REGISTRO.items():
            self.assertTrue(previews.existe_modulo(modulo), f"{clave} -> pruebas/{modulo}.py")

    def test_modulo_de_resuelve_alias(self):
        self.assertEqual(
            previews.modulo_de("09v2"), "test_previews_video_09_v2"
        )
        with self.assertRaises(KeyError):
            previews.modulo_de("no_existe")


class TestScriptsImportables(unittest.TestCase):
    def test_scripts_seguros_importan_con_main(self):
        for nombre in MODULOS_SEGUROS:
            mod = importlib.import_module(f"pruebas.{nombre}")
            self.assertTrue(callable(getattr(mod, "main", None)), nombre)


class TestCLI(unittest.TestCase):
    def test_sin_argumentos_lista_exit_0(self):
        proc = ejecutar_cli()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("Previews disponibles", proc.stdout)
        self.assertIn("14", proc.stdout)
        self.assertIn("director", proc.stdout)
        self.assertNotIn("Ran", proc.stdout)

    def test_lista_explicito_exit_0(self):
        proc = ejecutar_cli("--lista")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("test_previews_video_14", proc.stdout)

    def test_clave_desconocida_exit_2(self):
        proc = ejecutar_cli("no_existe")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("desconocida", proc.stdout)
        self.assertIn("Claves validas", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)

r"""
ci_local.py
-----------
CI local: corre las suites de tests del proyecto con resumen por suite y
exit code (0 = todo verde, 1 = alguna suite falló o crasheó).

Uso:
    python pruebas/ci_local.py                 # todas las suites (requiere ffmpeg, ~3 min)
    python pruebas/ci_local.py --sin-ffmpeg    # solo suites puras (~40 s, sin ffmpeg)
    python pruebas/ci_local.py --lista         # muestra las suites sin ejecutarlas
    python pruebas/ci_local.py --instalar-hook # git config core.hooksPath .githooks

El hook pre-push (.githooks/pre-push) llama a este script: un push con una
suite roja se corta. Desinstalar: git config --unset core.hooksPath.
Saltear una corrida puntual: git push --no-verify.

Solo lectura salvo --instalar-hook (modifica .git/config local).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))


@dataclass(frozen=True)
class Suite:
    ruta: str              # relativa a DIR_RAIZ
    requiere_ffmpeg: bool

    @property
    def nombre(self) -> str:
        return Path(self.ruta).stem


# Orden de corrida: suites rápidas primero, ffmpeg al final.
SUITES: Tuple[Suite, ...] = (
    Suite("pruebas/test_lint_zonas.py", False),
    Suite("pruebas/test_lint_obsoleto.py", False),
    Suite("pruebas/test_lint_subtitulos.py", False),
    Suite("pruebas/test_lint_anti_template.py", False),
    Suite("pruebas/test_chequeos_pipeline.py", True),
    Suite("pruebas/test_registro_videos.py", False),
    Suite("pruebas/test_motion_y_sfx.py", False),
    Suite("pruebas/test_eventos_voz.py", False),
    Suite("pruebas/test_enfasis.py", False),
    Suite("pruebas/test_director_gancho.py", False),
    Suite("pruebas/test_registro_experimentos.py", False),
    Suite("pruebas/test_pipeline_modulos.py", False),
    Suite("pruebas/test_runner_previews.py", False),
    Suite("pruebas/archivo_pruebas/test_shorts_assembler.py", True),
    Suite("pruebas/test_ci_local.py", False),
)

SEP = "=" * 65


def seleccionar(sin_ffmpeg: bool = False) -> List[Suite]:
    """Suites a ejecutar; con sin_ffmpeg se excluyen las que necesitan ffmpeg."""
    if sin_ffmpeg:
        return [s for s in SUITES if not s.requiere_ffmpeg]
    return list(SUITES)


def parsear_salida(salida: str, returncode: int) -> Tuple[int, bool]:
    """
    Extrae (número de tests, ok) de la salida de unittest.
    ok requiere el resumen 'Ran N tests' Y exit code 0; sin 'Ran' = crasheo.
    """
    m = re.search(r"Ran (\d+) tests? in", salida)
    tests = int(m.group(1)) if m else 0
    return tests, (m is not None and returncode == 0)


def ejecutar_suite(suite: Suite) -> dict:
    """Corre una suite como subprocess y devuelve tests/estado/duración/salida."""
    ruta = DIR_RAIZ / suite.ruta
    entorno = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    inicio = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, str(ruta)],
        cwd=str(DIR_RAIZ),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=entorno,
    )
    duracion = time.perf_counter() - inicio
    salida = (proc.stdout or "") + (proc.stderr or "")
    tests, ok = parsear_salida(salida, proc.returncode)
    if ok:
        estado = "OK"
    elif not re.search(r"Ran \d+ tests? in", salida):
        estado = "CRASH"
    else:
        estado = "FAIL"
    return {
        "suite": suite,
        "tests": tests,
        "estado": estado,
        "duracion": duracion,
        "salida": salida,
        "returncode": proc.returncode,
    }


def correr(suites: Sequence[Suite]) -> int:
    """Ejecuta las suites, imprime tabla + resumen y devuelve exit code."""
    con_ffmpeg = any(s.requiere_ffmpeg for s in suites)
    print(SEP)
    print(f" CI LOCAL — {len(suites)} suites (ffmpeg: {'sí' if con_ffmpeg else 'no'})")
    print(SEP)

    resultados = []
    for suite in suites:
        r = ejecutar_suite(suite)
        resultados.append(r)
        marca = "ffmpeg " if suite.requiere_ffmpeg else ""
        detalle = (
            f"{r['tests']} tests"
            if r["estado"] == "OK"
            else f"exit {r['returncode']}"
        )
        print(f" [{r['estado']:<5}] {suite.nombre:<30} {marca:<7} {detalle:<10} {r['duracion']:.1f}s")

    fallidos = [r for r in resultados if r["estado"] != "OK"]
    if fallidos:
        print()
        for r in fallidos:
            print(f"--- salida de {r['suite'].nombre} ({r['estado']}) ---")
            lineas = r["salida"].strip().splitlines()
            for linea in lineas[-40:]:
                print(f"  {linea}")
            print()

    total_tests = sum(r["tests"] for r in resultados)
    total_seg = sum(r["duracion"] for r in resultados)
    print(SEP)
    print(
        f" TOTAL: {total_tests} tests | {len(resultados)} suites | "
        f"{total_seg:.1f}s | {len(fallidos)} fallo(s)"
    )
    print(SEP)
    return 1 if fallidos else 0


def lista(sin_ffmpeg: bool = False) -> int:
    suites = seleccionar(sin_ffmpeg)
    print(f"Suites del CI ({len(suites)}"
          f"{', sin ffmpeg' if sin_ffmpeg else ', todas'}):")
    for suite in SUITES:
        marcador = "" if suite in suites else "  [excluida: ffmpeg]"
        marca = " [ffmpeg]" if suite.requiere_ffmpeg else ""
        print(f"  {suite.nombre:<32}{marca}{marcador}")
    print()
    print("  Ejecutar: python pruebas/ci_local.py [--sin-ffmpeg]")
    return 0


def instalar_hook() -> int:
    hook = DIR_RAIZ / ".githooks" / "pre-push"
    if not hook.is_file():
        print(f"[CI] Falta el hook: {hook}")
        return 1
    actual = subprocess.run(
        ["git", "config", "core.hooksPath"],
        cwd=str(DIR_RAIZ), capture_output=True, text=True,
    )
    valor = (actual.stdout or "").strip()
    if actual.returncode == 0 and valor == ".githooks":
        print("[CI] Hook ya instalado (core.hooksPath=.githooks).")
        return 0
    if actual.returncode == 0 and valor:
        print(f"[CI] core.hooksPath ya apunta a '{valor}'; no se sobrescribe.")
        print("[CI] Para instalar este: git config --unset core.hooksPath && "
              "python pruebas/ci_local.py --instalar-hook")
        return 1
    subprocess.run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=str(DIR_RAIZ), check=True,
    )
    print("[CI] Hook pre-push instalado: core.hooksPath=.githooks")
    print("[CI] Cada push correrá python pruebas/ci_local.py (saltear: git push --no-verify)")
    print("[CI] Desinstalar: git config --unset core.hooksPath")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ci_local.py",
        description="CI local: corre las suites con resumen y exit code.",
    )
    parser.add_argument("--sin-ffmpeg", action="store_true",
                        help="excluye las suites que necesitan ffmpeg")
    parser.add_argument("--lista", action="store_true",
                        help="muestra las suites sin ejecutarlas")
    parser.add_argument("--instalar-hook", action="store_true",
                        help="instala el hook pre-push (.githooks)")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.instalar_hook:
        return instalar_hook()
    if args.lista:
        return lista(sin_ffmpeg=args.sin_ffmpeg)
    return correr(seleccionar(sin_ffmpeg=args.sin_ffmpeg))


if __name__ == "__main__":
    sys.exit(main())

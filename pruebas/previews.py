r"""
previews.py
-----------
Runner único para los scripts de previews visuales (test_previews_*.py).

Uso:
    python pruebas/previews.py                # lista las previews disponibles
    python pruebas/previews.py 14             # previews del video 14
    python pruebas/previews.py 09_v2          # variante v2 del video 09
    python pruebas/previews.py director       # 5 arquetipos (guion 05)
    python pruebas/previews.py --todos        # todas las previews
    python pruebas/previews.py --lista        # mismo que sin argumentos

No gasta créditos ni ejecuta el pipeline: cada script solo renderiza PNG de
diagnóstico en videos/video_XX/intermedios/previews_director/.

Exit: 0 = OK, 1 = alguna preview falló, 2 = clave desconocida.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

# clave CLI -> (módulo en pruebas/, descripción corta)
REGISTRO: Dict[str, Tuple[str, str]] = {
    "director": ("test_previews_director", "Guion 05: 5 arquetipos cinematograficos"),
    "06": ("test_previews_video_06", "Guion 06: Atencion al cliente con IA (5 arquetipos)"),
    "09": ("test_previews_video_09", "Guion 09: Diseno de Flyers (arquetipos)"),
    "09_v2": ("test_previews_video_09_v2", "Video 09 v2: 7 escenas hiperdinamicas"),
    "10": ("test_previews_video_10", "Video 10: Cotizacion automatica (7 micro-escenas)"),
    "11": ("test_previews_video_11", "Video 11: 50 Archivos (7 micro-escenas)"),
    "12": ("test_previews_video_12", "Video 12: Ciberseguridad y Google Ads (7 micro-escenas)"),
    "13": ("test_previews_video_13", "Video 13: Portal de Noticias de IA (7 micro-escenas)"),
    "14": ("test_previews_video_14", "Video 14: Agua e IA (7 micro-escenas)"),
    "15": ("test_previews_video_15", "Video 15: IA en tu celular (7 micro-escenas)"),
}

ALIAS: Dict[str, str] = {
    "09v2": "09_v2",
}


def normalizar_clave(clave: str) -> str:
    """Normaliza la clave CLI (minúsculas + alias conocidos)."""
    c = clave.strip().lower()
    return ALIAS.get(c, c)


def modulo_de(clave: str) -> str:
    """Devuelve el nombre del módulo de una clave; KeyError si no existe."""
    return REGISTRO[normalizar_clave(clave)][0]


def existe_modulo(nombre_modulo: str) -> bool:
    """True si el módulo pruebas.<nombre> existe (sin importarlo)."""
    return importlib.util.find_spec(f"pruebas.{nombre_modulo}") is not None


def mostrar_lista(salida=sys.stdout) -> None:
    print("Previews disponibles (PNG de diagnostico, sin creditos):", file=salida)
    print("", file=salida)
    for clave, (modulo, desc) in REGISTRO.items():
        print(f"  {clave:<10} {desc}", file=salida)
        print(f"  {'':<10} -> pruebas/{modulo}.py", file=salida)
    print("", file=salida)
    print("  Ejemplos: python pruebas/previews.py 14", file=salida)
    print("            python pruebas/previews.py 09_v2", file=salida)
    print("            python pruebas/previews.py --todos", file=salida)


def ejecutar(claves: Sequence[str]) -> int:
    """Ejecuta los main() de las claves dadas; continúa si una falla."""
    fallos: List[Tuple[str, str]] = []
    for clave in claves:
        modulo, desc = REGISTRO[clave]
        print("=" * 65)
        print(f"[PREVIEWS] {clave} — {desc}")
        print(f"[PREVIEWS] modulo pruebas/{modulo}.py")
        print("=" * 65)
        try:
            mod = importlib.import_module(f"pruebas.{modulo}")
            mod.main()
            print(f"[PREVIEWS] {clave}: OK")
        except Exception as exc:  # noqa: BLE001 — reporta y sigue con el resto
            fallos.append((clave, repr(exc)))
            print(f"[PREVIEWS] {clave}: FALLO — {exc!r}")

    print()
    print("=" * 65)
    if fallos:
        print(f"[PREVIEWS] {len(fallos)} fallo(s) de {len(claves)}:")
        for clave, err in fallos:
            print(f"  - {clave}: {err}")
        print("=" * 65)
        return 1
    print(f"[PREVIEWS] Todas OK ({len(claves)} preview(s)).")
    print("=" * 65)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="previews.py",
        description="Runner unico de previews visuales (PNG de diagnostico).",
    )
    parser.add_argument("claves", nargs="*", help="claves de preview (ej: 14, 09_v2, director)")
    parser.add_argument("--todos", action="store_true", help="ejecuta todas las previews")
    parser.add_argument("--lista", action="store_true", help="lista las previews disponibles")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.lista or (not args.claves and not args.todos):
        mostrar_lista()
        return 0

    if args.todos:
        claves = list(REGISTRO)
    else:
        claves = [normalizar_clave(c) for c in args.claves]

    desconocidas = [c for c in claves if c not in REGISTRO]
    if desconocidas:
        print(f"[PREVIEWS] Clave(s) desconocida(s): {', '.join(desconocidas)}")
        print("[PREVIEWS] Claves validas:", ", ".join(REGISTRO))
        return 2

    return ejecutar(claves)


if __name__ == "__main__":
    sys.exit(main())

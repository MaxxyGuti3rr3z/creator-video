r"""
lint_anti_template.py
---------------------
Linter de rotación anti-template entre videos consecutivos.

Fuerza las prohibiciones de `.agents/rules/arquitectura_visual_variada.md`
(§2 clonación de estructura, §3 rotación de sprites) y la rotación de
formato de cierre de AGENTS.md. Cuatro chequeos:

  1. estructura   — dos videos consecutivos con el mismo generador de
                    fondos / mockup = misma estructura visual prohibida.
  2. byte_agotado — el sprite `byte_agotado` no puede aparecer en dos
                    videos consecutivos.
  3. sprite_escenas — el mismo sprite no puede usarse en dos escenas
                    consecutivas del MISMO video.
  4. cierre       — dos videos consecutivos con el mismo formato de cierre
                    (encuesta A/B/C, Battle VS, pregunta de debate,
                    medidor de dolor). Formato "otro" no se compara.

Fuentes (todas rastreadas por git; NO depende de videos/):
  - guiones/guion_NN_*.json  (mockup/cierre reales)
  - src/registro_videos.py   (generador de fondos y sprites por video)

Calibración contra el catálogo real (videos 02-14): chequeos 1 y 2 en cero
violaciones; los únicos FAIL son violaciones legítimas históricas (los
videos 02-13 son anteriores a la regla): pares 02->03, 08->09 y 12->13
repiteven formato de cierre, y el video 13 repite sprite en punto_1 ->
punto_2. Un video nuevo NO debe heredar esas violaciones.

Uso:
    python pruebas/lint_anti_template.py                  # auditoría del catálogo
    python pruebas/lint_anti_template.py guiones/guion_15_x.json
    python pruebas/lint_anti_template.py --dir DIR        # catálogo alternativo

  - Con rutas posicionales solo se REPORTAN los problemas que involucran
    esos guiones (pre-vuelo del video nuevo contra sus vecinos).
  - Exit 1 si hay algún FAIL. Solo lectura.
  - Tests: python pruebas/test_lint_anti_template.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.registro_videos import CONFIGS  # noqa: E402

# Formatos de cierre que participan en la rotación obligatoria.
FORMATOS_ROTACION = ("encuesta_abc", "battle_vs", "pregunta_debate", "medidor_dolor")

_POR_ID = {cfg.id: cfg for cfg in CONFIGS}


# ---------------------------------------------------------------------------
# Modelo
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class VideoCatalogo:
    """Datos anti-template de un guion del catálogo."""

    numero: int
    nombre: str
    # Estructura visual: generador de fondos (si hay config) o mockup del guion
    estructura: str
    cierre: str
    # (bloque, archivo) en orden narrativo, solo el nombre del archivo
    sprites: Tuple[Tuple[str, str], ...]


@dataclass(frozen=True)
class Problema:
    check: str          # estructura | byte_agotado | sprite_escenas | cierre
    numeros: Tuple[int, ...]   # videos implicados
    mensaje: str


# ---------------------------------------------------------------------------
# Clasificación de cierre
# ---------------------------------------------------------------------------

def clasificar_cierre(texto: str) -> str:
    """
    Clasifica el texto de cierre en un formato de rotación o 'otro'.

    Prioridad: encuesta A/B/C > Battle VS > medidor de dolor >
    compartir > pregunta de debate > otro.
    """
    t = (texto or "").lower()
    if "team" in t and " o " in t:
        return "encuesta_abc"
    if re.search(r"\bvs\b", t):
        return "battle_vs"
    if re.search(r"cu[a\u00e1]ntos?\b|cu[a\u00e1]ntas\b", t):
        return "medidor_dolor"
    if "compart" in t:
        return "compartir"
    if any(k in t for k in ("contame", "cont\u00e1me", "dejame", "dej\u00e1me", "comenta")):
        return "pregunta_debate"
    return "otro"


# ---------------------------------------------------------------------------
# Carga del catálogo
# ---------------------------------------------------------------------------

def _sprites_de_video(numero: int) -> Tuple[Tuple[str, str], ...]:
    """Sprites (bloque, archivo) del registro para un video; () si no hay config."""
    cfg = _POR_ID.get(f"{numero:02d}")
    if cfg is None:
        return ()
    return tuple((bloque, ruta.name) for bloque, ruta in cfg.sprites)


def _estructura_de_video(numero: int, data: dict) -> str:
    """Estructura visual: generador de fondos > clave de mockup > campo del guion."""
    cfg = _POR_ID.get(f"{numero:02d}")
    if cfg is not None and cfg.generador_fondos:
        return cfg.generador_fondos
    if cfg is not None and cfg.claves_mockup:
        return cfg.claves_mockup[0]
    return data.get("mockup_sugerido") or data.get("tipo_mockup") or "desconocido"


def cargar_catalogo(rutas: Sequence[Path]) -> List[VideoCatalogo]:
    """
    Carga guiones JSON en VideoCatalogo ordenados por número.
    Si hay dos rutas con el mismo número, gana la última.
    """
    por_numero: Dict[int, VideoCatalogo] = {}
    for ruta in rutas:
        m = re.search(r"guion_(\d+)", ruta.stem)
        if not m:
            print(f"  [AVISO] nombre sin 'guion_NN', se omite: {ruta.name}")
            continue
        numero = int(m.group(1))
        data = json.loads(Path(ruta).read_text(encoding="utf-8"))
        por_numero[numero] = VideoCatalogo(
            numero=numero,
            nombre=ruta.stem,
            estructura=_estructura_de_video(numero, data),
            cierre=data.get("cierre", "") or "",
            sprites=_sprites_de_video(numero),
        )
    return [por_numero[n] for n in sorted(por_numero)]


# ---------------------------------------------------------------------------
# Chequeos
# ---------------------------------------------------------------------------

def _usa_agotado(v: VideoCatalogo) -> bool:
    return any("byte_agotado" in archivo for _, archivo in v.sprites)


def checar_videos(videos: Sequence[VideoCatalogo]) -> List[Problema]:
    """
    Aplica los 4 chequeos anti-template. Lista vacía = sin violaciones.
    Los pares consecutivos exigen números adyacentes (N, N+1).
    """
    problemas: List[Problema] = []
    por_numero = {v.numero: v for v in videos}
    nums = sorted(por_numero)

    # --- Entre videos consecutivos -------------------------------------
    for a, b in zip(nums, nums[1:]):
        if b != a + 1:
            continue
        va, vb = por_numero[a], por_numero[b]

        if va.estructura == vb.estructura and va.estructura != "desconocido":
            problemas.append(Problema(
                check="estructura",
                numeros=(a, b),
                mensaje=(
                    f"par {a:02d}->{b:02d}: misma estructura visual "
                    f"'{va.estructura}' en videos consecutivos"
                ),
            ))

        if _usa_agotado(va) and _usa_agotado(vb):
            problemas.append(Problema(
                check="byte_agotado",
                numeros=(a, b),
                mensaje=(
                    f"par {a:02d}->{b:02d}: sprite 'byte_agotado' en dos "
                    f"videos consecutivos"
                ),
            ))

        fa, fb = clasificar_cierre(va.cierre), clasificar_cierre(vb.cierre)
        if fa == fb and fa in FORMATOS_ROTACION:
            problemas.append(Problema(
                check="cierre",
                numeros=(a, b),
                mensaje=(
                    f"par {a:02d}->{b:02d}: mismo formato de cierre "
                    f"'{fa}' en videos consecutivos"
                ),
            ))

    # --- Dentro de cada video ------------------------------------------
    for v in videos:
        archivos = [archivo for _, archivo in v.sprites]
        for i in range(len(archivos) - 1):
            if archivos[i] == archivos[i + 1]:
                bloque_a = v.sprites[i][0]
                bloque_b = v.sprites[i + 1][0]
                problemas.append(Problema(
                    check="sprite_escenas",
                    numeros=(v.numero,),
                    mensaje=(
                        f"video {v.numero:02d}: mismo sprite en escenas "
                        f"consecutivas {bloque_a} -> {bloque_b} ({archivos[i]})"
                    ),
                ))

    return problemas


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Linter de rotación anti-template entre videos consecutivos."
    )
    parser.add_argument(
        "rutas", nargs="*", type=Path,
        help="guiones JSON en foco (default: auditoría de todo el catálogo)",
    )
    parser.add_argument(
        "--dir", type=Path, default=None,
        help="directorio del catálogo de guiones (default: guiones/)",
    )
    args = parser.parse_args(argv)

    dir_catalogo = args.dir if args.dir is not None else DIR_RAIZ / "guiones"
    rutas_catalogo = (
        sorted(dir_catalogo.glob("guion_*.json")) if dir_catalogo.is_dir() else []
    )
    # Los guiones en foco se agregan al catálogo (ganan si repiten número)
    rutas = rutas_catalogo + list(args.rutas)

    videos = cargar_catalogo(rutas)
    if not videos:
        print("No hay guiones que analizar.")
        return 0

    focos = set()
    for ruta in args.rutas:
        m = re.search(r"guion_(\d+)", Path(ruta).stem)
        if m:
            focos.add(int(m.group(1)))

    todos = checar_videos(videos)
    problemas = (
        [p for p in todos if any(n in focos for n in p.numeros)] if focos else todos
    )

    pares = sum(
        1 for a, b in zip([v.numero for v in videos], [v.numero for v in videos][1:])
        if b == a + 1
    )
    alcance = f"foco={sorted(focos)}" if focos else "catálogo completo"
    print(f"[LINTER ANTI-TEMPLATE] guiones={len(videos)} pares={pares} ({alcance})\n")

    if problemas:
        for p in problemas:
            print(f"[FAIL] {p.mensaje}")
    else:
        print("[OK]   sin violaciones de rotación anti-template")

    print(f"\n[RESUMEN] problemas={len(problemas)} videos={len(videos)}")
    if problemas:
        print("[RESULTADO] FAIL — corregir la rotación "
              "(ver .agents/rules/arquitectura_visual_variada.md).")
        return 1
    print("[RESULTADO] PASS — rotación anti-template conforme.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

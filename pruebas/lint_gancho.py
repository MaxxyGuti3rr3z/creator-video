r"""
lint_gancho.py
--------------
Linter del gancho inicial (cold_open + hook) de un guion.

Valida las reglas mecánicas del proyecto sobre el primer segmento, que es
lo que el viewer ve en los primeros segundos (donde se decide el swipe):

  1. sin_puntos      — cold_open/hook sin puntos (`.`): la regla crítica de
                       AGENTS.md (los puntos causan pausas de 1-2 s en
                       ElevenLabs; emplear comas o redacción continua).
  2. longitud        — cold_open ≤ 18 palabras y hook ≤ 20 palabras
                       (calibrado sobre el catálogo real 01-15: máximos
                       históricos 15 y 17, con margen de 3).
  3. sin_promesas    — sin métricas inventadas ni promesas imposibles
                       (porcentajes, "cero", "garantiz", "100%", "siempre
                       funciona", "el más rápido"): regla de AGENTS.md.
  4. rotacion        — dos videos consecutivos no pueden fijar el MISMO
                       arquetipo de gancho (ConfigVideo.gancho_preferido);
                       anti-template. Sin preferido fijo, la rotación por
                       semilla (número de video) ya es distinta por video.

Fuentes (rastreadas por git; NO depende de videos/):
  - guiones/guion_NN_*.json  (cold_open/hook reales)
  - src/registro_videos.py   (gancho_preferido por video)

Uso:
    python pruebas/lint_gancho.py                      # auditoría del catálogo
    python pruebas/lint_gancho.py guiones/guion_16_x.json
    python pruebas/lint_gancho.py --dir DIR            # catálogo alternativo

  - Con rutas posicionales solo se REPORTAN los problemas de esos guiones.
  - Exit 1 si hay algún FAIL. Solo lectura.
  - Tests: python pruebas/test_director_gancho.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.registro_videos import CONFIGS  # noqa: E402

# Umbrales calibrados sobre el catálogo real (ver docstring)
MAX_PALABRAS_COLD_OPEN = 18
MAX_PALABRAS_HOOK = 20

# Patrones de métricas inventadas / promesas imposibles (AGENTS.md)
_PATRONES_PROMESA = (
    (r"\d+\s*%", "porcentaje"),
    (r"\bcero\b", "cero absoluto"),
    (r"\bgarantiz", "garantía imposible"),
    (r"100\s*%", "cien por ciento"),
    (r"siempre funciona", "promesa absoluta"),
    (r"el m[a\u00e1]s r[a\u00e1]pido", "superlativo no verificable"),
)

_POR_ID = {cfg.id: cfg for cfg in CONFIGS}


@dataclass(frozen=True)
class Problema:
    check: str          # sin_puntos | longitud | sin_promesas | rotacion
    video: int
    mensaje: str


def _leer_guion(ruta: Path) -> Dict:
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def _numero_desde_ruta(ruta: Path) -> Optional[int]:
    m = re.search(r"guion_(\d+)", ruta.stem)
    return int(m.group(1)) if m else None


def _numero_desde_guion(guion: Dict) -> Optional[int]:
    v = guion.get("video")
    try:
        return int(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def _gancho_preferido(numero: Optional[int]) -> Optional[str]:
    if numero is None:
        return None
    cfg = _POR_ID.get(f"{numero:02d}")
    return getattr(cfg, "gancho_preferido", None) if cfg else None


def _revisar_guion(ruta: Path, guion: Dict, numero: Optional[int]) -> List[Problema]:
    problemas: List[Problema] = []
    cold_open = str(guion.get("cold_open", "") or "")
    hook = str(guion.get("hook", "") or "")
    vid = numero if numero is not None else -1

    # 1. sin_puntos (regla crítica ElevenLabs)
    for nombre, texto in (("cold_open", cold_open), ("hook", hook)):
        if "." in texto:
            problemas.append(Problema(
                "sin_puntos", vid,
                f"{nombre} contiene punto(s) '.': causa pausas de 1-2 s en "
                f"ElevenLabs (usar comas o redacción continua): {texto[:60]!r}",
            ))

    # 2. longitud (calibrada)
    n_co, n_hk = len(cold_open.split()), len(hook.split())
    if n_co > MAX_PALABRAS_COLD_OPEN:
        problemas.append(Problema(
            "longitud", vid,
            f"cold_open tiene {n_co} palabras (> {MAX_PALABRAS_COLD_OPEN})",
        ))
    if n_hk > MAX_PALABRAS_HOOK:
        problemas.append(Problema(
            "longitud", vid,
            f"hook tiene {n_hk} palabras (> {MAX_PALABRAS_HOOK})",
        ))

    # 3. sin_promesas (métricas inventadas / promesas imposibles)
    for nombre, texto in (("cold_open", cold_open), ("hook", hook)):
        for patron, etiqueta in _PATRONES_PROMESA:
            if re.search(patron, texto, flags=re.IGNORECASE):
                problemas.append(Problema(
                    "sin_promesas", vid,
                    f"{nombre} contiene '{etiqueta}' (métrica inventada o "
                    f"promesa imposible): {texto[:60]!r}",
                ))

    return problemas


def _revisar_rotacion(
    numero: Optional[int], preferido: Optional[str], por_numero: Dict[int, Optional[str]]
) -> List[Problema]:
    """Dos videos consecutivos no pueden fijar el mismo arquetipo de gancho."""
    if numero is None or not preferido:
        return []
    problemas: List[Problema] = []
    for vecino in (numero - 1, numero + 1):
        pref_vecino = por_numero.get(vecino)
        if pref_vecino and pref_vecino == preferido:
            problemas.append(Problema(
                "rotacion", numero,
                f"video {numero} fija gancho '{preferido}' igual que el video "
                f"{vecino} (anti-template; rotar arquetipos)",
            ))
    return problemas


def auditar(dir_guiones: Path) -> Tuple[List[Problema], int]:
    """Audita todo el catálogo. Devuelve (problemas, guiones_auditados)."""
    guiones = sorted(dir_guiones.glob("guion_*.json"))
    cargados: List[Tuple[Optional[int], Dict]] = []
    for ruta in guiones:
        try:
            cargados.append((_numero_desde_ruta(ruta), _leer_guion(ruta)))
        except (json.JSONDecodeError, OSError):
            continue

    por_numero: Dict[int, Optional[str]] = {}
    for numero, guion in cargados:
        if numero is None:
            numero = _numero_desde_guion(guion)
        if numero is not None:
            por_numero[numero] = _gancho_preferido(numero)

    problemas: List[Problema] = []
    for numero, guion in cargados:
        if numero is None:
            numero = _numero_desde_guion(guion)
        problemas.extend(_revisar_guion(Path("(catálogo)"), guion, numero))
        problemas.extend(_revisar_rotacion(numero, _gancho_preferido(numero), por_numero))
    return problemas, len(cargados)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Linter del gancho (cold_open/hook) para guiones del proyecto."
    )
    parser.add_argument(
        "entradas", nargs="*", type=Path,
        help="rutas de guiones .json (sin args: audita todo guiones/)",
    )
    parser.add_argument("--dir", type=Path, default=DIR_RAIZ / "guiones",
                        help="directorio del catálogo (default: guiones/)")
    args = parser.parse_args(argv)

    if args.entradas:
        problemas: List[Problema] = []
        auditados = 0
        for ruta in args.entradas:
            numero = _numero_desde_ruta(ruta)
            guion = _leer_guion(ruta)
            if numero is None:
                numero = _numero_desde_guion(guion)
            auditados += 1
            problemas.extend(_revisar_guion(ruta, guion, numero))
            por_numero = {numero: _gancho_preferido(numero)} if numero is not None else {}
            problemas.extend(
                _revisar_rotacion(numero, _gancho_preferido(numero), por_numero)
            )
    else:
        problemas, auditados = auditar(args.dir)

    print(f"[LINT GANCHO] guiones auditados: {auditados}")
    if not problemas:
        print("[RESULTADO] PASS — gancho conforme.")
        return 0
    for p in problemas:
        print(f"  [FAIL] video {p.video} ({p.check}): {p.mensaje}")
    print(f"[RESULTADO] FAIL — {len(problemas)} problema(s) en el gancho.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

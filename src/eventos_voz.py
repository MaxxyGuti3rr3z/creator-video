"""
src.eventos_voz
 ---------------------------------------------------------------------------
 Sincronía de la UI con la locución: convierte los timestamps por carácter del
 alignment de ElevenLabs en tiempos de evento por escena (pop de notificación,
 inicio del typing de la píldora, etc.), para que la animación respire al
 ritmo exacto de la voz.

 El matching es difuso sobre palabras normalizadas (minúsculas, sin acentos ni
 puntuación), de modo que "Buscá" coincide con "busca" en la narración.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List, Optional, Sequence, Tuple

# (palabra_normalizada, t_inicio_global, t_fin_global)
Palabra = Tuple[str, float, float]


def normalizar(texto: str) -> str:
    """Minúsculas + sin acentos + sin puntuación pegada a la palabra."""
    bajo = unicodedata.normalize("NFD", texto.lower())
    sin_acentos = "".join(c for c in bajo if unicodedata.category(c) != "Mn")
    return re.sub(r"[^\w]+", "", sin_acentos, flags=re.UNICODE)


def palabras_de_segmento(seg: Dict[str, Any], alignment: Dict[str, Any]) -> List[Palabra]:
    """
    Reconstruye las palabras de un segmento con sus tiempos globales a partir
    del alignment carácter por carácter ({characters, character_start_times_seconds,
    character_end_times_seconds}). Devuelve [] si el alignment es incompleto.
    """
    chars = alignment.get("characters") or []
    starts = alignment.get("character_start_times_seconds") or []
    ends = alignment.get("character_end_times_seconds") or []
    if not chars or len(starts) != len(chars) or len(ends) != len(chars):
        # Alignment ausente/incompleto: se avanza vacío y aplica el fallback
        # uniforme de más abajo (si hay texto en el segmento).
        chars, starts, ends = [], [], []

    texto = str(seg.get("texto", ""))
    t_ini_seg = float(seg.get("inicio", 0.0))
    t_fin_seg = float(seg.get("fin", t_ini_seg))

    palabras: List[Palabra] = []
    actual: List[str] = []
    t_ini_actual: Optional[float] = None
    t_fin_actual: float = t_ini_seg

    def cerrar() -> None:
        nonlocal actual, t_ini_actual
        if actual:
            cruda = "".join(actual)
            norm = normalizar(cruda)
            if norm and t_ini_actual is not None:
                palabras.append((norm, t_ini_actual, t_fin_actual))
        actual = []
        t_ini_actual = None

    # Recorre solo los chars dentro de la ventana temporal del segmento
    for ch, t0, t1 in zip(chars, starts, ends):
        if t0 < t_ini_seg - 0.05 or t0 > t_fin_seg + 0.05:
            cerrar()
            continue
        if ch.isspace():
            cerrar()
            continue
        if t_ini_actual is None:
            t_ini_actual = float(t0)
        t_fin_actual = float(t1)
        actual.append(ch)
    cerrar()

    if not palabras and texto:
        # Fallback sin alignment: reparte el segmento uniforme (solo orden)
        frags = [f for f in re.split(r"\s+", texto) if f]
        if frags:
            paso = (t_fin_seg - t_ini_seg) / max(1, len(frags))
            palabras = [
                (normalizar(f) or f.lower(), t_ini_seg + i * paso, t_ini_seg + (i + 1) * paso)
                for i, f in enumerate(frags)
            ]
    return palabras


def encontrar_inicio(
    palabras: Sequence[Palabra],
    objetivo: str,
) -> Optional[float]:
    """
    Devuelve el tiempo global de inicio de la primera ocurrencia de `objetivo`
    (texto libre o palabra clave; se compara la mayor cantidad consecutiva de
    palabras normalizadas). None si no hay match.
    """
    frags = [normalizar(f) for f in re.split(r"\s+", objetivo.strip()) if normalizar(f)]
    if not frags or not palabras:
        return None
    norm_seg = [p[0] for p in palabras]
    for largo in range(len(frags), 0, -1):
        clave = frags[:largo]
        n = len(clave)
        for i in range(len(norm_seg) - n + 1):
            if norm_seg[i : i + n] == clave:
                return palabras[i][1]
    return None


def encontrar_todos(
    palabras: Sequence[Palabra],
    objetivo: str,
) -> List[float]:
    """
    Devuelve los tiempos globales de TODAS las ocurrencias de `objetivo`
    (misma heurística de mayor subcadena que encontrar_inicio). Vacío si no
    hay match. Útil para tiempos de énfasis (punch-in) por palabra clave.
    """
    frags = [normalizar(f) for f in re.split(r"\s+", objetivo.strip()) if normalizar(f)]
    if not frags or not palabras:
        return []
    norm_seg = [p[0] for p in palabras]
    for largo in range(len(frags), 0, -1):
        clave = frags[:largo]
        n = len(clave)
        coincidencias = [
            palabras[i][1]
            for i in range(len(norm_seg) - n + 1)
            if norm_seg[i : i + n] == clave
        ]
        if coincidencias:
            return coincidencias
    return []


def construir_eventos_escena(
    seg: Dict[str, Any],
    alignment: Dict[str, Any],
    pildora: Optional[str] = None,
    ui_clave: Optional[Sequence[str]] = None,
    fraccion_fallback: float = 0.30,
) -> Dict[str, Any]:
    """
    Eventos de una escena en tiempo LOCAL (segundos desde el inicio del segmento):
      - t_ui:       pop del elemento UI hero (primer keyword de ui_clave hallado).
      - t_pildora:  inicio del typing de la píldora (match difuso de su texto).
      - t_enfasis:  tupla con los tiempos locales de TODAS las ocurrencias de
                    cada keyword de ui_clave (puntos candidatos a punch-in).
                    Vacía si no hay keywords ni matches (compat: consumidores
                    existentes solo leen t_ui/t_pildora).
    Los valores None significan "sin sync de voz" (el plano usa su fallback fijo).
    """
    inicio = float(seg.get("inicio", 0.0))
    dur = max(0.0, float(seg.get("fin", inicio)) - inicio)
    palabras = palabras_de_segmento(seg, alignment)

    t_ui: Optional[float] = None
    candidatos_enfasis: List[float] = []
    if ui_clave:
        for clave in ui_clave:
            ocurrencias = encontrar_todos(palabras, clave)
            candidatos_enfasis.extend(max(0.0, g - inicio) for g in ocurrencias)
            if t_ui is None and ocurrencias:
                t_ui = max(0.0, ocurrencias[0] - inicio)

    t_pildora: Optional[float] = None
    if pildora:
        g = encontrar_inicio(palabras, pildora)
        if g is not None:
            t_pildora = max(0.0, g - inicio)

    if t_pildora is None and pildora:
        t_pildora = dur * fraccion_fallback

    return {
        "t_ui": t_ui,
        "t_pildora": t_pildora,
        "t_enfasis": tuple(sorted(set(candidatos_enfasis))),
    }

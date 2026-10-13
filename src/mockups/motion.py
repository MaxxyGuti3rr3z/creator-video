"""
src.mockups.motion
 ---------------------------------------------------------------------------
 Helpers de animación por-frame (funciones de t_sec) para los planos PIL.
 Todo es determinístico y depende solo del tiempo de escena, sin estado.
"""

from typing import List


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else (hi if x > hi else x)


def ease_out_back(t: float, c1: float = 1.70158) -> float:
    """Ease-out-back estándar: 0->0, 1->1, con overshoot intermedio ~1.1."""
    u = clamp(t)
    c3 = c1 + 1.0
    return 1.0 + c3 * (u - 1.0) ** 3 + c1 * (u - 1.0) ** 2


def pop_scale(
    t: float,
    t0: float = 0.0,
    dur: float = 0.35,
    overshoot_max: float = 1.04,
) -> float:
    """
    Escala de entrada con muelle para badges/píldoras/cajas.
    0 antes de t0, sube con overshoot (limitado a overshoot_max por safe zones)
    y queda en 1.0 al terminar.
    """
    if t <= t0:
        return 0.0
    u = (t - t0) / dur if dur > 0 else 1.0
    if u >= 1.0:
        return 1.0
    return min(ease_out_back(u), overshoot_max)


def type_chars(texto: str, t: float, t0: float = 0.15, cps: float = 28.0) -> str:
    """Revela 'texto' carácter a carácter (typing) a partir de t0 a cps chars/s."""
    if t <= t0:
        return ""
    n = int((t - t0) * cps)
    if n >= len(texto):
        return texto
    return texto[:n]


def type_words(palabras: List[str], t: float, t0: float = 0.15, wps: float = 4.0) -> str:
    """Revela una lista de palabras completa por palabra (para kinetic typography)."""
    if t <= t0:
        return ""
    n = int((t - t0) * wps)
    if n >= len(palabras):
        return " ".join(palabras)
    return " ".join(palabras[:n])

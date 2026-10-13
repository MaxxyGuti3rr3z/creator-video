"""
src.enfasis
 ---------------------------------------------------------------------------
 Punch-in de énfasis: zoom breve (≈0.20 s) sobre la capa de fondo+mockup en
 el instante de una palabra clave, sincronizado con el cambio a blanco del
 subtítulo. Diseño anti-safe-zones (medido sobre el video 15, 55 frames):

   Contenido brillante del mockup vive en y=252..900, x=100..980; Byte (overlay
   separado, NO escalado) en y≤1642. Un zoom uniforme >1.007x de la capa
   compuesta completa es imposible sin violar las zonas (span brillante
   1390px × 1.04 = 1445.6 > 1400 permitidos, para cualquier ancla: exigiría
   ancla ≤302 y ≥1442 simultáneamente). Por eso el punch escala SOLO el
   fondo+mockup con ancla (540, 250): a 1.04x → mockup top 252→252.08 ✓,
   x=100→82.4 ✓, x=980→997.6 ✓. Byte se overlay después, intacto.

   Videos cinemáticos (Byte horneado en el bg) quedan excluidos en el
   orquestador: con Byte dentro del bg ningún ancla admite 3-4%.

   Restricciones FFmpeg verificadas empíricamente:
   - `crop` exige entrada ≥ tamaño de salida → Z<1 rompe el filtro.
   - `zoompan` no admite `t` en expresiones → se usa `on` (frame de salida).
   - `zoompan` con z≥1 recorta (sin bordes negros); con z<1 los revela.
   Por eso el rango es Z∈[1.0, 1.035] y se alterna punch fuerte/suave.

Funciones puras (sin E/S): selección de puntos y construcción del filtro.
La integración vive en shorts_assembler.ensamblar_video.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple

# --- Constantes de diseño (unidades documentadas) ---------------------------

# Escala máxima del punch-in fuerte (fracción: 3.5% de zoom)
INTENSIDAD_PUNCH_IN: float = 0.035
# Punch-in suave alternado (fracción: 2% de zoom). Se descartó el "alejamiento"
# con Z<1: crop exige entrada ≥1080x1920 (rompe con Z<1) y zoompan con z<1
# revela bordes negros. La variedad de ritmo se logra alternando intensidad.
INTENSIDAD_PUNCH_SUAVE: float = 0.02
# Duración total del efecto (segundos)
DURACION_ENFASIS_SEG: float = 0.20
# Máximo de punch-ins por escena
MAX_POR_ESCENA: int = 2
# Separación mínima entre punch-ins consecutivos (segundos)
SEPARACION_MIN_SEG: float = 1.5
# Ancla del zoom (píxeles en el canvas 1080x1920): centrada en X, al borde
# superior del mockup en Y, de modo que el mockup no sube fuera de y≥250.
ANCLA_X_PX: int = 540
ANCLA_Y_PX: int = 250
# Exponente de la curva de subida (u^EXP_POTENCIA): <1 = pico temprano
# (subida rápida con ease-out y retorno suave; 1.0 en t0 y en t0+DUR).
EXP_POTENCIA: float = 0.6


@dataclass(frozen=True, slots=True)
class PuntoEnfasis:
    """Un punch-in en tiempo LOCAL de escena (segundos).

    intensidad: fracción de escala SIEMPRE ≥ 0 (Z = 1 + intensidad ∈ [1, 1.035];
    se descartó Z<1 por las restricciones de crop/zoompan documentadas arriba).
    tipo: "punch_in" (fuerte) o "punch_suave" (contraste anti-repetitivo).
    """

    t_inicio: float
    intensidad: float
    tipo: str


def _bump_en_t(t: float, punto: PuntoEnfasis, dur: float) -> float:
    """Contribución de un punto a la escala en el instante t (curva pura)."""
    if t < punto.t_inicio or t > punto.t_inicio + dur:
        return 0.0
    u = (t - punto.t_inicio) / dur
    u = min(max(u, 0.0), 1.0)
    return punto.intensidad * math.sin(math.pi * (u ** EXP_POTENCIA))


def factor_zoom(t: float, puntos: Sequence[PuntoEnfasis],
                dur: float = DURACION_ENFASIS_SEG) -> float:
    """Escala total (1.0 = sin cambio) en el instante t (segundos locales).

    Garantiza exactamente 1.0 fuera de las ventanas de efecto y ≈1.0 en los
    bordes de cada ventana (sin NaN ni escalas fuera de rango).
    """
    return 1.0 + sum(_bump_en_t(t, p, dur) for p in puntos)


def seleccionar_puntos_enfasis(
    t_candidatos: Sequence[float],
    duracion_escena: float,
    max_por_escena: int = MAX_POR_ESCENA,
    separacion_min: float = SEPARACION_MIN_SEG,
) -> Tuple[PuntoEnfasis, ...]:
    """Filtra, separa, limita y alterna punch fuerte/suave (Z≥1 siempre).

    - Descarta candidatos fuera de [0, duracion_escena] y no finitos.
    - Conserva los primeros `max_por_escena` con separación ≥ separacion_min.
    - Alterna tipos: índice par → punch_in (3.5%), impar → punch_suave (2%).
    - Entrada vacía (o sin candidatos válidos) → tupla vacía.
    """
    if duracion_escena <= 0 or max_por_escena <= 0:
        return ()

    validos: List[float] = sorted({
        float(t) for t in t_candidatos
        if math.isfinite(float(t)) and 0.0 <= float(t) <= duracion_escena
    })

    elegidos: List[float] = []
    for t in validos:
        if elegidos and (t - elegidos[-1]) < separacion_min:
            continue
        elegidos.append(t)
        if len(elegidos) >= max_por_escena:
            break

    puntos: List[PuntoEnfasis] = []
    for i, t in enumerate(elegidos):
        if i % 2 == 0:
            puntos.append(PuntoEnfasis(t, INTENSIDAD_PUNCH_IN, "punch_in"))
        else:
            puntos.append(PuntoEnfasis(t, INTENSIDAD_PUNCH_SUAVE, "punch_suave"))
    return tuple(puntos)


def _expresion_bump_ffmpeg(
    punto: PuntoEnfasis, dur: float, base: str, fps: int
) -> str:
    """Término FFmpeg de un punto: I*sin(PI*clip(u,0,1)^p)*between(...).

    `base` es la variable temporal: "t" (segundos) o "on" (frame de salida).
    zoompan NO admite `t`, por eso la variante "on" con fps=30 (t = on/fps).
    """
    t0 = punto.t_inicio * (fps if base == "on" else 1.0)
    dur_b = dur * (fps if base == "on" else 1.0)
    u = f"clip(({base}-{t0:.4f})/{dur_b:.4f},0,1)"
    return (
        f"{punto.intensidad:.4f}*sin(PI*pow({u},{EXP_POTENCIA}))"
        f"*between({base},{t0:.4f},{t0 + dur_b:.4f})"
    )


def construir_expresion_zoom(
    puntos: Sequence[PuntoEnfasis],
    fps: int = 30,
    dur: float = DURACION_ENFASIS_SEG,
    base: str = "on",
) -> str:
    """Expresión FFmpeg de la escala Z(variable) — SIEMPRE Z≥1 (sin NaN).

    - base="on" (default): para `zoompan` (frame de salida; t = on/fps).
    - base="t": para `scale ... eval=frame` (segundos).
    Devuelve "1" sin puntos; con puntos, "1+bump1+bump2...". La curva vale
    exactamente 1.0 en el inicio y el fin de cada ventana de efecto.
    """
    if base not in ("on", "t"):
        raise ValueError(f"base debe ser 'on' o 't', no {base!r}")
    if not puntos:
        return "1"
    terminos = "+".join(
        _expresion_bump_ffmpeg(p, dur, base, fps) for p in puntos
    )
    return f"1+{terminos}"


def construir_filtro_enfasis(
    puntos: Sequence[PuntoEnfasis],
    fps: int = 30,
    dur: float = DURACION_ENFASIS_SEG,
) -> str:
    """Filtro FFmpeg (zoompan) del punch-in sobre la capa bg, o "" sin puntos.

    zoompan con z≥1 recorta (nunca revela bordes). El ancla (ANCLA_X_PX,
    ANCLA_Y_PX) se fija con x/y: un punto de entrada (px,py) cae en
    ((px-ax)*z+ax, (py-ay)*z+ay); el contenido se aleja del ancla, de modo
    que el mockup (y≥252) jamás sube fuera de y≥250 ni roza x<70/x>1011
    con z≤1.035 (verificado: x=100→84.6, x=980→995.4, y=252→252.07).
    """
    if not puntos:
        return ""
    z_expr = construir_expresion_zoom(puntos, fps=fps, dur=dur, base="on")
    return (
        f"zoompan=z='{z_expr}':"
        f"x='{ANCLA_X_PX}-{ANCLA_X_PX}/zoom':"
        f"y='{ANCLA_Y_PX}-{ANCLA_Y_PX}/zoom':"
        f"d=1:s=1080x1920:fps={fps}"
    )

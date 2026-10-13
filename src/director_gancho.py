"""
src.director_gancho
 ---------------------------------------------------------------------------
 Director del gancho inicial: define las variantes VISUALES A/B/C del
 primer segmento (cold_open / hook) de un video, con el MISMO audio y los
 MISMOS subtítulos (0 créditos ElevenLabs — restricción de la tarea).

 Cada variante cambia solo el tratamiento visual del clip 0 dentro de
 shorts_assembler.ensamblar_video:
   - texto_pantalla  (A, control): comportamiento por defecto, sin cambios.
   - byte_reacciona  (B): punch de impacto en el fondo (z 1.00→1.04→1.00 en
     ~1.2 s) y Byte entra con escala de choque, acompañando la reacción.
   - mockup_inmediato(C): zoom-in lento y constante del fondo (1.00→1.03)
     que empuja la mirada al mockup desde el primer frame; Byte lateral.

 Seguridad anti-safe-zones: todo zoom usa ancla (540, 250) y z∈[1.0, 1.04]
 (mismo rango verificado del punch-in de src/enfasis.py; z<1 está prohibido
 porque crop/zoompan revelan bordes). El linter lint_zonas_seguras es el
 árbitro final.

 Determinismo: la rotación se deriva solo de la semilla (número de video) y
 del orden fijo de ARQUETIPOS_GANCHO; no usa random de Python (estable entre
 versiones). Funciones puras, sin E/S.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

# Orden fijo de arquetipos (rotación anti-template; coherente con
# .agents/rules/arquitectura_visual_variada.md)
ARQUETIPOS_GANCHO: Tuple[str, ...] = (
    "texto_pantalla",
    "byte_reacciona",
    "mockup_inmediato",
)

_DESCRIPCIONES = {
    "texto_pantalla": "Control: fondo con paneo suave y Byte desde abajo (comportamiento histórico).",
    "byte_reacciona": "Punch de impacto en el fondo + Byte con escala de choque al entrar.",
    "mockup_inmediato": "Zoom-in lento del fondo que empuja al mockup; Byte entra lateral.",
}

# Curvas de tratamiento visual por arquetipo (solo clip 0; valores de escala)
# z_min/z_max: rango del zoom del fondo (siempre ≥1.0)
# dur_zoom_up/dur_zoom_down: segundos de subida y retorno del punch (B)
# dur_zoom_lento: segundos del zoom-in constante (C)
# escala_choque_byte: escala inicial de Byte en B (1.0 = sin choque)
# entrada_byte: "abajo" (A), "choque" (B), "lateral" (C)
TRATAMIENTOS = {
    "texto_pantalla": {
        "z_min": 1.0, "z_max": 1.0,
        "dur_zoom_up": 0.0, "dur_zoom_down": 0.0,
        "dur_zoom_lento": 0.0,
        "escala_choque_byte": 1.0,
        "entrada_byte": "abajo",
    },
    "byte_reacciona": {
        "z_min": 1.0, "z_max": 1.04,
        "dur_zoom_up": 0.30, "dur_zoom_down": 1.20,
        "dur_zoom_lento": 0.0,
        "escala_choque_byte": 1.25,
        "entrada_byte": "choque",
    },
    "mockup_inmediato": {
        "z_min": 1.0, "z_max": 1.03,
        "dur_zoom_up": 0.0, "dur_zoom_down": 0.0,
        "dur_zoom_lento": 2.50,
        "escala_choque_byte": 1.0,
        "entrada_byte": "lateral",
    },
}


@dataclass(frozen=True, slots=True)
class VarianteGancho:
    """Una variante visual del gancho: id (A/B/C), arquetipo y descripción."""

    id: str
    arquetipo: str
    descripcion: str


def _rotar(arquetipos: Sequence[str], semilla: int) -> Tuple[str, ...]:
    """Rotación determinista: desplaza la lista según la semilla (sin random)."""
    if not arquetipos:
        return ()
    k = int(semilla) % len(arquetipos)
    return tuple(arquetipos[k:]) + tuple(arquetipos[:k])


def variantes_gancho(
    semilla: int,
    arquetipo_preferido: Optional[str] = None,
    excluir: Sequence[str] = (),
) -> Tuple[VarianteGancho, ...]:
    """Devuelve las variantes A/B/C (o menos si se excluyen arquetipos).

    - El arquetipo preferido (de ConfigVideo.gancho_preferido) va en A si es
      válido y no está excluido.
    - Los arquetipos en `excluir` (p. ej. el del video anterior, anti-template)
      se descartan. Pueden quedar 1-2 variantes; el orquestador ajusta N.
    - Determinista: mismo semilla + mismas entradas => mismas variantes.
    """
    válidos = tuple(a for a in ARQUETIPOS_GANCHO if a not in set(excluir))
    if not válidos:
        return ()

    orden: list[str] = []
    if arquetipo_preferido in válidos:
        orden.append(arquetipo_preferido)
    resto = [a for a in _rotar(válidos, semilla) if a != arquetipo_preferido]
    orden.extend(resto)

    ids = ("A", "B", "C")
    return tuple(
        VarianteGancho(ids[i], arquetipo, _DESCRIPCIONES[arquetipo])
        for i, arquetipo in enumerate(orden[: len(ids)])
    )


def seleccionar_para_produccion(
    variantes: Sequence[VarianteGancho],
    preferencia: Optional[str] = None,
) -> Optional[VarianteGancho]:
    """Variante que va a final/: la de id `preferencia` si existe, si no la A."""
    if not variantes:
        return None
    if preferencia:
        for v in variantes:
            if v.id == preferencia:
                return v
    return variantes[0]

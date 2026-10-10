"""
byte_emociones.py
-----------------
Librería de secuencias emocionales y micro-expresiones para Byte el Zorrito.
Permite que Byte NO se quede congelado en una sola pose estática durante toda una escena:
- Define transiciones de emoción basadas en puntos clave temporales (ej: de agobiado a tecleando con furia).
- Añade micro-reacciones VFX sincronizadas (gotas de sudor animadas, chispas de IA, aura de pulso zen).
- Mantiene la identidad de Byte consistente con sus sprites aprobados.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math

try:
    from src.rutas import DIR_BYTE_TRANSPARENTES, DIR_BYTE_ILUSTRACIONES
except ImportError:
    from rutas import DIR_BYTE_TRANSPARENTES, DIR_BYTE_ILUSTRACIONES


@dataclass
class EstadoEmocion:
    tiempo_inicio: float  # Segundo dentro de la escena donde inicia
    sprite_clave: str     # Clave del sprite en el catálogo
    tipo_vfx: Optional[str] = None  # "gotas_estres", "chispas_ia", "aura_zen", "confeti"
    factor_rebote: float = 1.0     # Intensidad de micro-salto


# Catálogo de sprites transparentes limpios disponibles
CATALOGO_SPRITES: Dict[str, Path] = {
    "estresado": DIR_BYTE_TRANSPARENTES / "escena_problema_guion_04_transparente.png",
    "enojado_laptop": DIR_BYTE_TRANSPARENTES / "punto_2_guion_04_transparente.png",
    "ojos_estrella": DIR_BYTE_TRANSPARENTES / "punto_1_guion_04_transparente.png",
    "pacifico_zen": DIR_BYTE_TRANSPARENTES / "resultado_guion_04_transparente.png",
    "saltando_feliz": DIR_BYTE_TRANSPARENTES / "cierre_guion_04_transparente.png",
    "serio_analitico": DIR_BYTE_TRANSPARENTES / "cierre_transparente.png",
}

# Secuencias emocionales estándar recomendadas por tipo de escena
SECUENCIAS_PREDETERMINADAS: Dict[str, List[EstadoEmocion]] = {
    # Escena Problema: empieza agobiado con las manos en la cabeza y luego salta a pelear con la máquina
    "escena_problema": [
        EstadoEmocion(tiempo_inicio=0.0, sprite_clave="estresado", tipo_vfx="gotas_estres", factor_rebote=0.8),
        EstadoEmocion(tiempo_inicio=3.5, sprite_clave="enojado_laptop", tipo_vfx=None, factor_rebote=1.2),
    ],
    # Escena Solución 1 (Descubrimiento): curiosidad analítica -> gran asombro con estrellas
    "punto_1": [
        EstadoEmocion(tiempo_inicio=0.0, sprite_clave="serio_analitico", tipo_vfx=None, factor_rebote=0.9),
        EstadoEmocion(tiempo_inicio=2.8, sprite_clave="ojos_estrella", tipo_vfx="chispas_ia", factor_rebote=1.3),
    ],
    # Escena Solución 2 (Ejecución): tecleando con ritmo -> satisfacción
    "punto_2": [
        EstadoEmocion(tiempo_inicio=0.0, sprite_clave="enojado_laptop", tipo_vfx=None, factor_rebote=1.0),
        EstadoEmocion(tiempo_inicio=3.2, sprite_clave="ojos_estrella", tipo_vfx="chispas_ia", factor_rebote=1.1),
    ],
    # Escena Resultado: meditación zen en paz mental
    "resultado": [
        EstadoEmocion(tiempo_inicio=0.0, sprite_clave="pacifico_zen", tipo_vfx="aura_zen", factor_rebote=0.5),
    ],
    # Escena Cierre: euforia y celebración
    "cierre": [
        EstadoEmocion(tiempo_inicio=0.0, sprite_clave="saltando_feliz", tipo_vfx="confeti", factor_rebote=1.4),
    ]
}


def resolver_sprite_momento(
    tipo_escena: str,
    tiempo_segundos: float,
    secuencia_personalizada: Optional[List[EstadoEmocion]] = None
) -> Tuple[Image.Image, Optional[str], float]:
    """
    Determina qué sprite y VFX de Byte corresponden al segundo exacto de la escena:
    Retorna (imagen_sprite_rgba, tipo_vfx, factor_rebote).
    """
    secuencia = secuencia_personalizada or SECUENCIAS_PREDETERMINADAS.get(tipo_escena)
    if not secuencia:
        p = CATALOGO_SPRITES.get("ojos_estrella")
        return Image.open(p).convert("RGBA"), None, 1.0

    estado_actual = secuencia[0]
    for est in secuencia:
        if tiempo_segundos >= est.tiempo_inicio:
            estado_actual = est
        else:
            break

    p_sprite = CATALOGO_SPRITES.get(estado_actual.sprite_clave, CATALOGO_SPRITES["ojos_estrella"])
    if not p_sprite.exists():
        # Fallback seguro
        p_sprite = DIR_BYTE_TRANSPARENTES / "punto_1_guion_04_transparente.png"

    img_sprite = Image.open(p_sprite).convert("RGBA")
    return img_sprite, estado_actual.tipo_vfx, estado_actual.factor_rebote


def dibujar_micro_vfx(
    canvas_byte: Image.Image,
    tipo_vfx: str,
    progreso_t: float
) -> Image.Image:
    """Añade micro-reacciones visuales sutiles sobre el sprite de Byte."""
    if not tipo_vfx:
        return canvas_byte

    w, h = canvas_byte.size
    capa_vfx = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(capa_vfx)

    if tipo_vfx == "gotas_estres":
        # Gotas de sudor flotando a los lados de la cabeza
        for i, lado in enumerate([-1, 1]):
            caida = ((progreso_t * 3.0 + i * 0.5) % 1.0)
            gx = w // 2 + lado * (w // 3)
            gy = int(h * 0.28 + caida * 40)
            tam = int(12 * (1.0 - caida * 0.3))
            alpha = int(240 * (1.0 - caida))
            draw.ellipse([gx - tam // 2, gy, gx + tam // 2, gy + tam * 2], fill=(56, 189, 248, alpha))

    elif tipo_vfx == "chispas_ia":
        # Destellos y chispas de IA alrededor de las orejas/cabeza
        for i in range(4):
            fase = (progreso_t * 2.5 + i * 0.25) % 1.0
            ang = i * (math.pi / 2) + progreso_t * 2
            dist = 180 + math.sin(fase * math.pi) * 30
            cx = int(w // 2 + math.cos(ang) * dist)
            cy = int(h * 0.38 + math.sin(ang) * dist * 0.6)
            tam = int(10 * math.sin(fase * math.pi))
            if tam > 2:
                col = (6, 182, 212, int(220 * math.sin(fase * math.pi)))
                draw.line([(cx - tam, cy), (cx + tam, cy)], fill=col, width=2)
                draw.line([(cx, cy - tam), (cx, cy + tam)], fill=col, width=2)

    elif tipo_vfx == "aura_zen":
        # Anillo de respiración que pulsa suavemente detrás/alrededor
        pulso = 0.5 + 0.5 * math.sin(progreso_t * math.pi * 3)
        r = int(220 + pulso * 35)
        alpha = int(120 * (1.0 - pulso * 0.4))
        draw.ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r], outline=(52, 211, 153, alpha), width=3)

    capa_vfx = capa_vfx.filter(ImageFilter.GaussianBlur(radius=2))
    return Image.alpha_composite(canvas_byte, capa_vfx)

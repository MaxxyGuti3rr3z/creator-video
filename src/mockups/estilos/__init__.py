"""
Librería de Estilos y Variaciones Visuales para Byte el Zorrito.
"""

from .temas import (
    TemaMockup,
    TEMA_LIGHT_SLATE,
    TEMA_DARK_OBSIDIAN,
    TEMA_GLASS,
    TEMA_CYBER_NEON,
    obtener_tema
)

from .fondos import (
    renderizar_fondo_aurora,
    renderizar_fondo_cyber_spotlight,
    renderizar_fondo_studio_minimal,
    renderizar_fondo_estilizado
)

from .byte_emociones import (
    EstadoEmocion,
    CATALOGO_SPRITES,
    SECUENCIAS_PREDETERMINADAS,
    resolver_sprite_momento,
    dibujar_micro_vfx
)

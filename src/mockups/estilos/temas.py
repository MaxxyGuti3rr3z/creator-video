"""
temas.py
--------
Librería de temas visuales para las ventanas de mockup de Byte el Zorrito.
Mantiene estrictamente la identidad de marca:
- 3 puntos simples en gris neutro (#94A3B8, sin colores macOS semáforo).
- Sello visible "Simulación ilustrativa" dentro de la zona segura.
- Zona segura y legibilidad máxima vertical 9:16.
Permite alternar entre estilos: Light Slate, Dark Obsidian, Glassmorphism y Cyber Neon.
"""

from dataclasses import dataclass
from typing import Tuple, Dict, Any


@dataclass
class TemaMockup:
    nombre: str
    # Ventana exterior
    bg_ventana: Tuple[int, int, int, int]
    border_ventana: Tuple[int, int, int, int]
    sombra_alpha: int
    radius: int
    # Encabezado (Header)
    header_bg: Tuple[int, int, int, int]
    header_line: Tuple[int, int, int, int]
    dot_color: Tuple[int, int, int]
    txt_titulo: Tuple[int, int, int]
    txt_subtitulo: Tuple[int, int, int]
    # Sello de simulación ilustrativa
    sello_bg: Tuple[int, int, int, int]
    sello_border: Tuple[int, int, int, int]
    sello_txt: Tuple[int, int, int]
    # Contenido interior / Tarjetas
    card_bg: Tuple[int, int, int, int]
    card_border: Tuple[int, int, int, int]
    card_txt_primario: Tuple[int, int, int]
    card_txt_secundario: Tuple[int, int, int]
    # Acentos y badges por defecto
    accent_color: Tuple[int, int, int]
    accent_bg: Tuple[int, int, int, int]
    accent_txt: Tuple[int, int, int]


# ---------------------------------------------------------------------------
# Catálogo de Temas Disponibles
# ---------------------------------------------------------------------------

# 1. Light Slate (Estilo clásico editorial claro)
TEMA_LIGHT_SLATE = TemaMockup(
    nombre="light_slate",
    bg_ventana=(255, 255, 255, 252),
    border_ventana=(226, 232, 240, 255),
    sombra_alpha=70,
    radius=24,
    header_bg=(248, 250, 252, 255),
    header_line=(226, 232, 240, 255),
    dot_color=(148, 163, 184),
    txt_titulo=(30, 41, 59),
    txt_subtitulo=(100, 116, 139),
    sello_bg=(241, 245, 249, 230),
    sello_border=(203, 213, 225, 255),
    sello_txt=(100, 116, 139),
    card_bg=(248, 250, 252, 255),
    card_border=(226, 232, 240, 255),
    card_txt_primario=(30, 41, 59),
    card_txt_secundario=(100, 116, 139),
    accent_color=(6, 182, 212),
    accent_bg=(224, 242, 254, 255),
    accent_txt=(3, 105, 161)
)

# 2. Dark Obsidian (Modo oscuro sofisticado, alta gama dev/tech)
TEMA_DARK_OBSIDIAN = TemaMockup(
    nombre="dark_obsidian",
    bg_ventana=(22, 27, 34, 248),
    border_ventana=(48, 54, 61, 255),
    sombra_alpha=110,
    radius=24,
    header_bg=(13, 17, 23, 255),
    header_line=(48, 54, 61, 255),
    dot_color=(139, 148, 158),
    txt_titulo=(240, 246, 252),
    txt_subtitulo=(139, 148, 158),
    sello_bg=(33, 38, 45, 230),
    sello_border=(48, 54, 61, 255),
    sello_txt=(139, 148, 158),
    card_bg=(29, 35, 44, 255),
    card_border=(56, 64, 76, 255),
    card_txt_primario=(240, 246, 252),
    card_txt_secundario=(139, 148, 158),
    accent_color=(56, 189, 248),
    accent_bg=(12, 74, 110, 180),
    accent_txt=(186, 230, 253)
)

# 3. Glassmorphism (Translúcido esmerilado con brillo perimetral suave)
TEMA_GLASS = TemaMockup(
    nombre="glassmorphism",
    bg_ventana=(255, 255, 255, 190),
    border_ventana=(255, 255, 255, 210),
    sombra_alpha=85,
    radius=26,
    header_bg=(255, 255, 255, 160),
    header_line=(226, 232, 240, 180),
    dot_color=(148, 163, 184),
    txt_titulo=(15, 23, 42),
    txt_subtitulo=(71, 85, 105),
    sello_bg=(255, 255, 255, 200),
    sello_border=(203, 213, 225, 200),
    sello_txt=(71, 85, 105),
    card_bg=(255, 255, 255, 170),
    card_border=(255, 255, 255, 230),
    card_txt_primario=(15, 23, 42),
    card_txt_secundario=(71, 85, 105),
    accent_color=(99, 102, 241),
    accent_bg=(238, 242, 255, 200),
    accent_txt=(67, 56, 202)
)

# 4. Cyber Neon (Fondo oscuro profundo con borde y acento luminoso)
TEMA_CYBER_NEON = TemaMockup(
    nombre="cyber_neon",
    bg_ventana=(15, 17, 26, 250),
    border_ventana=(99, 102, 241, 160),
    sombra_alpha=120,
    radius=22,
    header_bg=(10, 12, 20, 255),
    header_line=(99, 102, 241, 120),
    dot_color=(100, 116, 139),
    txt_titulo=(248, 250, 252),
    txt_subtitulo=(148, 163, 184),
    sello_bg=(24, 27, 40, 240),
    sello_border=(99, 102, 241, 140),
    sello_txt=(165, 180, 252),
    card_bg=(22, 25, 38, 255),
    card_border=(45, 52, 78, 255),
    card_txt_primario=(248, 250, 252),
    card_txt_secundario=(148, 163, 184),
    accent_color=(129, 140, 248),
    accent_bg=(30, 27, 75, 200),
    accent_txt=(199, 210, 254)
)

CATALOGO_TEMAS: Dict[str, TemaMockup] = {
    "light_slate": TEMA_LIGHT_SLATE,
    "dark_obsidian": TEMA_DARK_OBSIDIAN,
    "glassmorphism": TEMA_GLASS,
    "cyber_neon": TEMA_CYBER_NEON
}


def obtener_tema(nombre_o_alias: str) -> TemaMockup:
    """Retorna la configuración de tema correspondiente con fallback a light_slate."""
    key = str(nombre_o_alias).lower().strip()
    if "dark" in key or "oscuro" in key or "obsidian" in key:
        return TEMA_DARK_OBSIDIAN
    if "glass" in key or "cristal" in key or "translucido" in key:
        return TEMA_GLASS
    if "neon" in key or "cyber" in key:
        return TEMA_CYBER_NEON
    return CATALOGO_TEMAS.get(key, TEMA_LIGHT_SLATE)

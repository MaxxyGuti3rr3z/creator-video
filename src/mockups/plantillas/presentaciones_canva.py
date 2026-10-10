"""
plantillas/presentaciones_canva.py
----------------------------------
Plantilla para Video 5 (Punto 2: Canva):
- Pulido visual y estilización de presentaciones con IA.
- Mobile-First: Letras grandes (21px a 27px) y alto contraste visual.
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    dibujar_chispa_ia,
    dibujar_icono_check,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Canva",
    "Estudio de Diseño con IA",
    "Magic Design Activo",
    "Pulido visual en un clic",
    "Colores, fuentes y composición armónica",
    "Diseño profesional terminado",
    "Paleta ejecutiva aplicada",
    "Listo para compartir con el equipo"
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el pulido visual de presentaciones en Canva."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Canva",
        subtitulo="Diseño con IA",
        tipo_mockup=tipo_mockup
    )

    f_tit_27 = obtener_fuente(27, bold=True)
    f_bold_22 = obtener_fuente(22, bold=True)
    f_sub_21 = obtener_fuente(21, bold=False)
    f_badge_19 = obtener_fuente(19, bold=True)
    f_btn_21 = obtener_fuente(21, bold=True)

    # 1. Badge superior de estado
    badge_w = 240
    badge_h = 36
    bx = ancho - badge_w - 205
    by = (66 - badge_h) // 2
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=8, fill=(245, 243, 255), outline=(147, 51, 234))
    dibujar_chispa_ia(draw, bx + 16, by + 18, 7, (147, 51, 234))
    draw.text((bx + 34, by + 7), "Pulido visual con IA", fill=(107, 33, 168), font=f_badge_19)

    cur_y = iy + 4

    # 2. Barra de Herramienta / Magic Design
    h_tool = 64
    draw.rounded_rectangle(
        [ix, cur_y, ix + iw, cur_y + h_tool],
        radius=12,
        fill=(250, 245, 255),
        outline=(168, 85, 247),
        width=2
    )

    dibujar_chispa_ia(draw, ix + 24, cur_y + 32, 9, (147, 51, 234))
    draw.text((ix + 46, cur_y + 10), "Magic Design • Canva:", fill=(107, 33, 168), font=f_badge_19)
    draw.text((ix + 46, cur_y + 32), "Aplica armonía de colores, jerarquía de fuentes e íconos en 1 clic", fill=(15, 23, 42), font=f_bold_22)

    cur_y += h_tool + 14

    # 3. Vista de Diapositiva con acabado visual pulido
    h_slide = 250
    draw.rounded_rectangle(
        [ix, cur_y, ix + iw, cur_y + h_slide],
        radius=14,
        fill=(255, 255, 255),
        outline=(147, 51, 234),
        width=2
    )

    # Header de la diapositiva pulida
    draw.text((ix + 24, cur_y + 18), "Informe Trimestral • Acabado Profesional", fill=(15, 23, 42), font=f_tit_27)
    draw.text((ix + 24, cur_y + 56), "Diseño visual armónico, espaciado cuidado y presentación lista para el cliente", fill=(100, 116, 139), font=f_sub_21)

    # 3 Elementos destacados de diseño
    y_blocks = cur_y + 100
    h_b = 120
    w_b = (iw - 48 - 24) // 3

    blocks = [
        ("Tipografía", "Jerarquía visual limpia", (124, 58, 237), (245, 243, 255)),
        ("Paleta", "Colores de marca cuidados", (14, 165, 233), (240, 249, 255)),
        ("Composición", "Gráficos y balance visual", (16, 185, 129), (236, 253, 245))
    ]

    for idx_b, (tit_b, sub_b, col_b, bg_b) in enumerate(blocks):
        bx0 = ix + 24 + idx_b * (w_b + 12)
        bx1 = bx0 + w_b
        draw.rounded_rectangle([bx0, y_blocks, bx1, y_blocks + h_b], radius=10, fill=bg_b, outline=(*col_b[:3], 90), width=1)
        draw.rounded_rectangle([bx0, y_blocks, bx0 + 6, y_blocks + h_b], radius=3, fill=col_b)
        draw.text((bx0 + 16, y_blocks + 18), tit_b, fill=col_b, font=f_bold_22)
        draw.text((bx0 + 16, y_blocks + 56), sub_b, fill=(51, 65, 85), font=f_sub_21)

    cur_y += h_slide + 14

    # 4. Barra de confirmación inferior
    h_bot = ih - (cur_y - iy)
    draw.rounded_rectangle([ix, cur_y, ix + iw, cur_y + h_bot], radius=10, fill=(245, 243, 255), outline=(216, 180, 254), width=1)
    dibujar_icono_check(draw, ix + 28, cur_y + 14, (124, 58, 237), tam=16, grosor=3)
    draw.text((ix + 56, cur_y + 10), "Canva pule el resultado para que el informe se vea impecable", fill=(107, 33, 168), font=f_bold_22)

    return img

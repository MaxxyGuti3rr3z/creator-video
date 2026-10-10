"""
plantillas/presentaciones_gamma.py
----------------------------------
Plantilla para Video 5 (Punto 1: Gamma):
- Generación de presentaciones completas a partir de una idea o prompt.
- Mobile-First: Textos grandes (21px a 27px), cero espacio muerto.
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
    "Gamma",
    "Generador de Presentaciones",
    "Generando desde una idea",
    "Crear presentación de informe trimestral",
    "Deck generado en segundos",
    "Estructura y diseño listos",
    "Resultados Q3 • Crecimiento Sostenible",
    "Tarjetas ordenadas con datos clave",
    "Listo para exponer"
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza la generación de presentaciones en Gamma."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Gamma",
        subtitulo="Presentación con IA",
        tipo_mockup=tipo_mockup
    )

    f_tit_27 = obtener_fuente(27, bold=True)
    f_bold_22 = obtener_fuente(22, bold=True)
    f_sub_21 = obtener_fuente(21, bold=False)
    f_badge_19 = obtener_fuente(19, bold=True)
    f_btn_21 = obtener_fuente(21, bold=True)

    # 1. Badge superior de estado
    badge_w = 250
    badge_h = 36
    bx = ancho - badge_w - 205
    by = (66 - badge_h) // 2
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=8, fill=(240, 249, 255), outline=(14, 165, 233))
    dibujar_chispa_ia(draw, bx + 16, by + 18, 7, (14, 165, 233))
    draw.text((bx + 34, by + 7), "Deck generado con IA", fill=(3, 105, 161), font=f_badge_19)

    cur_y = iy + 4

    # 2. Barra de Prompt / Idea inicial
    h_prompt = 64
    draw.rounded_rectangle(
        [ix, cur_y, ix + iw, cur_y + h_prompt],
        radius=12,
        fill=(248, 250, 252),
        outline=(14, 165, 233) if etapa >= 1 else (226, 232, 240),
        width=2
    )

    dibujar_chispa_ia(draw, ix + 24, cur_y + 32, 8, (14, 165, 233))
    draw.text((ix + 44, cur_y + 10), "Idea inicial:", fill=(3, 105, 161), font=f_badge_19)
    draw.text((ix + 44, cur_y + 32), "Armar presentación ejecutiva de informe con datos y gráficos", fill=(15, 23, 42), font=f_bold_22)

    cur_y += h_prompt + 14

    # 3. Diapositiva Generada (Ocupa el centro con diseño moderno)
    h_slide = 250
    draw.rounded_rectangle(
        [ix, cur_y, ix + iw, cur_y + h_slide],
        radius=14,
        fill=(255, 255, 255),
        outline=(14, 165, 233),
        width=2
    )

    # Header de la diapositiva en Gamma
    draw.text((ix + 24, cur_y + 18), "Informe Trimestral • Estrategia y Avances", fill=(15, 23, 42), font=f_tit_27)
    draw.text((ix + 24, cur_y + 56), "Diapositivas formateadas automáticamente sin lidiar con plantillas", fill=(100, 116, 139), font=f_sub_21)

    # 3 Bloques / Tarjetas de contenido generado
    y_cards = cur_y + 100
    h_mini = 120
    w_mini = (iw - 48 - 24) // 3

    cards_info = [
        ("Objetivos", "Estructura clara", (37, 99, 235), (239, 246, 255)),
        ("Métricas", "Datos organizados", (5, 150, 105), (236, 253, 245)),
        ("Conclusiones", "Cierre impactante", (124, 58, 237), (245, 243, 255))
    ]

    for idx_c, (tit_c, sub_c, col_c, bg_c) in enumerate(cards_info):
        cx0 = ix + 24 + idx_c * (w_mini + 12)
        cx1 = cx0 + w_mini
        draw.rounded_rectangle([cx0, y_cards, cx1, y_cards + h_mini], radius=10, fill=bg_c, outline=(*col_c[:3], 80), width=1)
        draw.rounded_rectangle([cx0, y_cards, cx0 + 6, y_cards + h_mini], radius=3, fill=col_c)
        draw.text((cx0 + 16, y_cards + 18), tit_c, fill=col_c, font=f_bold_22)
        draw.text((cx0 + 16, y_cards + 56), sub_c, fill=(51, 65, 85), font=f_sub_21)

    cur_y += h_slide + 14

    # 4. Botón de acción / Listo para presentar
    h_bot = ih - (cur_y - iy)
    draw.rounded_rectangle([ix, cur_y, ix + iw, cur_y + h_bot], radius=10, fill=(240, 249, 255), outline=(186, 230, 253), width=1)
    dibujar_icono_check(draw, ix + 28, cur_y + 14, (3, 105, 161), tam=16, grosor=3)
    draw.text((ix + 56, cur_y + 10), "Gamma generó la base completa en segundos para empezar rápido", fill=(3, 105, 161), font=f_bold_22)

    return img

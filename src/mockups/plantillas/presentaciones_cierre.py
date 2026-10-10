"""
plantillas/presentaciones_cierre.py
-----------------------------------
Plantilla para Video 5 (Cierre / Interacción):
- "¿Cuál parte de tus informes automatizarías primero?"
- Mobile-First: Pregunta destacada y tarjetas interactivas grandes.
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    dibujar_chispa_ia,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Comunidad",
    "Tu Opinión",
    "Pregunta del día",
    "¿Cuál parte de tus informes automatizarías primero?",
    "Búsqueda de datos",
    "Diseño de diapositivas",
    "Redacción de conclusiones",
    "Dejámelo en comentarios"
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza la pregunta interactiva de cierre."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Comunidad",
        subtitulo="Tu Opinión",
        tipo_mockup=tipo_mockup
    )

    f_tit_28 = obtener_fuente(28, bold=True)
    f_bold_23 = obtener_fuente(23, bold=True)
    f_sub_21 = obtener_fuente(21, bold=False)
    f_badge_19 = obtener_fuente(19, bold=True)

    # 1. Badge superior derecho
    badge_w = 200
    badge_h = 36
    bx = ancho - badge_w - 205
    by = (66 - badge_h) // 2
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=8, fill=(254, 243, 199), outline=(245, 158, 11))
    draw.text((bx + 26, by + 7), "Pregunta del día", fill=(180, 83, 9), font=f_badge_19)

    cur_y = iy + 10

    # 2. Tarjeta con la Pregunta Destacada (Centrada y grande)
    h_q = 130
    draw.rounded_rectangle([ix, cur_y, ix + iw, cur_y + h_q], radius=14, fill=(240, 249, 255), outline=(14, 165, 233), width=2)
    dibujar_chispa_ia(draw, ix + 32, cur_y + 36, 10, (14, 165, 233))
    draw.text((ix + 54, cur_y + 22), "Pregunta para vos:", fill=(3, 105, 161), font=f_badge_19)
    draw.text((ix + 32, cur_y + 60), "¿Cuál parte de tus informes automatizarías primero?", fill=(15, 23, 42), font=f_tit_28)

    cur_y += h_q + 16

    # 3. Tres Opciones de Votación / Comentarios
    opciones = [
        ("A", "Búsqueda y extracción de datos", (37, 99, 235), (239, 246, 255)),
        ("B", "Diseño y formateo de diapositivas", (124, 58, 237), (245, 243, 255)),
        ("C", "Redacción de resúmenes y conclusiones", (16, 185, 129), (236, 253, 245))
    ]

    h_op = 76
    for idx_o, (letra, texto_op, col_op, bg_op) in enumerate(opciones):
        oy = cur_y + idx_o * (h_op + 12)
        resaltar = (idx_o == (etapa % 3))
        bd_c = col_op if resaltar else (226, 232, 240)
        fill_c = bg_op if resaltar else (255, 255, 255)

        draw.rounded_rectangle([ix, oy, ix + iw, oy + h_op], radius=12, fill=fill_c, outline=bd_c, width=2 if resaltar else 1)
        
        # Círculo con Letra A / B / C
        draw.ellipse([ix + 20, oy + 16, ix + 64, oy + 60], fill=col_op)
        draw.text((ix + 34, oy + 24), letra, fill=(255, 255, 255), font=f_bold_23)

        draw.text((ix + 80, oy + 24), texto_op, fill=(15, 23, 42), font=f_bold_23)

    return img

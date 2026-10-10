"""
plantillas/presentaciones_resultado.py
--------------------------------------
Plantilla para Video 5 (Resultado / Alivio):
- "Terminás con un material presentable, ordenado y visual, sin convertir cada informe en un proyecto interminable".
- Sin métricas numéricas inventadas: Conceptos cualitativos ("Presentable", "Ordenado", "Visual").
- Mobile-First: Letras grandes (22px a 28px) y máximo aprovechamiento de la pantalla.
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    dibujar_icono_check,
    dibujar_chispa_ia,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Presentaciones",
    "Resultado Final",
    "Material Listo",
    "¡Presentación Completa y Lista!",
    "Informe ordenado, claro y con diseño profesional",
    "Estructura desde una idea generada con Gamma",
    "Estilo visual y paleta pulida con Canva",
    "Cero horas perdidas en formateo manual",
    "Presentable",
    "Ordenado",
    "Visual"
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el resultado final de la presentación terminada."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Presentaciones",
        subtitulo="Resultado Final",
        tipo_mockup=tipo_mockup
    )

    f_badge = obtener_fuente(19, bold=True)
    f_big = obtener_fuente(28, bold=True)
    f_sub = obtener_fuente(22, bold=False)
    f_item = obtener_fuente(22, bold=True)

    # 1. Badge superior derecho
    badge_w = 180
    badge_h = 36
    bx = ancho - badge_w - 205
    by = (66 - badge_h) // 2
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=8, fill=(16, 185, 129))
    dibujar_icono_check(draw, bx + 16, by + 11, (255, 255, 255), tam=14, grosor=3)
    draw.text((bx + 38, by + 7), "Material Listo", fill=(255, 255, 255), font=f_badge)

    cx = ix + iw // 2

    # 2. Gran Badge Circular Esmeralda
    cy_badge = iy + 55
    r_circ = 38
    draw.ellipse([cx - r_circ - 10, cy_badge - r_circ - 10, cx + r_circ + 10, cy_badge + r_circ + 10], fill=(236, 253, 245))
    draw.ellipse([cx - r_circ, cy_badge - r_circ, cx + r_circ, cy_badge + r_circ], fill=(16, 185, 129))
    dibujar_icono_check(draw, cx - 16, cy_badge - 17, (255, 255, 255), tam=32, grosor=4)

    dibujar_chispa_ia(draw, cx - 80, cy_badge - 16, 10, (245, 158, 11))
    dibujar_chispa_ia(draw, cx + 82, cy_badge - 12, 10, (6, 182, 212))

    # 3. Títulos (Grandes y centrados)
    tit_txt = "¡Presentación Completa y Lista!"
    bbox_t = draw.textbbox((0, 0), tit_txt, font=f_big)
    tw = bbox_t[2] - bbox_t[0]
    draw.text((cx - tw // 2, cy_badge + r_circ + 16), tit_txt, fill=(15, 23, 42), font=f_big)

    sub_txt = "Informe ordenado, claro y con diseño profesional"
    bbox_s = draw.textbbox((0, 0), sub_txt, font=f_sub)
    sw = bbox_s[2] - bbox_s[0]
    draw.text((cx - sw // 2, cy_badge + r_circ + 54), sub_txt, fill=(100, 116, 139), font=f_sub)

    # 4. Tarjeta Checklist Ancha
    y_card = cy_badge + r_circ + 96
    h_card = 160
    draw.rounded_rectangle([ix, y_card, ix + iw, y_card + h_card], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=2)

    items_chk = [
        "Estructura desde una idea generada con Gamma",
        "Estilo visual y paleta pulida con Canva",
        "Cero horas perdidas en formateo manual"
    ]

    iy_item = y_card + 18
    for it in items_chk:
        draw.ellipse([ix + 24, iy_item + 3, ix + 52, iy_item + 31], fill=(209, 250, 229))
        dibujar_icono_check(draw, ix + 32, iy_item + 9, (5, 150, 105), tam=14, grosor=3)
        draw.text((ix + 64, iy_item + 4), it, fill=(30, 41, 59), font=f_item)
        iy_item += 46

    # 5. Badges Cualitativos de Alivio (Regla: Sin métricas numéricas inventadas)
    y_pills = y_card + h_card + 14
    pills = [("Presentable", (16, 185, 129)), ("Ordenado", (14, 165, 233)), ("Visual", (124, 58, 237))]
    pw = 220
    ph = 44
    gap_p = (iw - (pw * len(pills))) // (len(pills) - 1)

    for idx_p, (txt_p, col_p) in enumerate(pills):
        px = ix + idx_p * (pw + gap_p)
        draw.rounded_rectangle([px, y_pills, px + pw, y_pills + ph], radius=10, fill=(255, 255, 255), outline=col_p, width=2)
        dibujar_chispa_ia(draw, px + 22, y_pills + 22, 7, col_p)
        draw.text((px + 38, y_pills + 10), txt_p, fill=col_p, font=f_badge)

    return img

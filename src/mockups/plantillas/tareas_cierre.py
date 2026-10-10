"""
plantillas/tareas_cierre.py
---------------------------
Plantilla para la escena final/cierre en la gestión de tareas.
Muestra la tarjeta de celebración con métricas estrictamente CUALITATIVAS:
- 'Al Día' (Tareas Resueltas)
- 'Más Liviano' (Flujo Continuo)
- 'Menos Caos' (Paz Mental)
Prohibido números inventados de tiempo o porcentajes.
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
import math
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    dibujar_icono_check,
    dibujar_chispa_ia,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Lista Andes",
    "Organización Exitosa",
    "¡Día completado con éxito!",
    "Todas tus tareas fueron priorizadas, agendadas y finalizadas",
    "Al Día",
    "Tareas Resueltas",
    "Más Liviano",
    "Flujo Continuo",
    "Menos Caos",
    "Paz Mental",
    "Dejá tu comentario abajo"
]

METRICAS_CUALITATIVAS = [
    {"val": "Al Día", "lbl": "Tareas Resueltas", "col": (6, 182, 212), "bg": (236, 254, 255)},
    {"val": "Más Liviano", "lbl": "Flujo Continuo", "col": (16, 185, 129), "bg": (236, 253, 245)},
    {"val": "Menos Caos", "lbl": "Paz Mental", "col": (99, 102, 241), "bg": (238, 242, 255)},
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza la tarjeta de cierre celebratorio con métricas cualitativas y micro-etapas."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Lista Andes",
        subtitulo="Organización Exitosa",
        tipo_mockup=tipo_mockup
    )

    f_tit_gran = obtener_fuente(22, bold=True)
    f_sub = obtener_fuente(13, bold=False)
    f_metric_val = obtener_fuente(18, bold=True)
    f_metric_lbl = obtener_fuente(11, bold=False)
    f_cta = obtener_fuente(13, bold=True)

    cx = ix + iw // 2

    # 1. Gran Badge Circular con Checkmark Esmeralda/Cyan
    cy_badge = iy + 62
    r_base = 34
    # Micro-pulso según etapa
    pulso = int(3 * math.sin(p_etapa * math.pi * 2)) if etapa >= 1 else 0
    r_circulo = r_base + pulso

    # Halo translúcido
    draw.ellipse([cx - r_circulo - 8, cy_badge - r_circulo - 8, cx + r_circulo + 8, cy_badge + r_circulo + 8], fill=(207, 250, 254, 150))
    # Círculo principal
    draw.ellipse([cx - r_circulo, cy_badge - r_circulo, cx + r_circulo, cy_badge + r_circulo], fill=(6, 182, 212))

    # Checkmark blanco
    chk_tam = 28
    dibujar_icono_check(draw, cx - chk_tam // 2, cy_badge - int(chk_tam * 0.55), (255, 255, 255), tam=chk_tam, grosor=3)

    # Chispas festivas
    dibujar_chispa_ia(draw, cx - 60, cy_badge - 18, 7, (245, 158, 11))
    dibujar_chispa_ia(draw, cx + 64, cy_badge - 14, 8, (16, 185, 129))
    dibujar_chispa_ia(draw, cx + 48, cy_badge + 26, 6, (244, 63, 94))

    # 2. Títulos
    tit_txt = "¡Día completado con éxito!"
    bbox_t = draw.textbbox((0, 0), tit_txt, font=f_tit_gran)
    tw = bbox_t[2] - bbox_t[0]
    draw.text((cx - tw // 2, cy_badge + r_base + 18), tit_txt, fill=(15, 23, 42), font=f_tit_gran)

    sub_txt = "Todas tus tareas fueron priorizadas, agendadas y finalizadas"
    bbox_s = draw.textbbox((0, 0), sub_txt, font=f_sub)
    sw = bbox_s[2] - bbox_s[0]
    draw.text((cx - sw // 2, cy_badge + r_base + 48), sub_txt, fill=(100, 116, 139), font=f_sub)

    # 3. 3 Tarjetas de Métricas Cualitativas
    y_cards = cy_badge + r_base + 82
    w_card = 230
    h_card = 72
    gap_card = 18
    total_w = 3 * w_card + 2 * gap_card
    start_x = cx - total_w // 2

    for m_i, m in enumerate(METRICAS_CUALITATIVAS):
        mx = start_x + m_i * (w_card + gap_card)
        
        # Revelado progresivo en micro-etapas
        resaltada = (etapa == m_i or etapa >= 2)
        border_c = m["col"] if resaltada else (226, 232, 240)
        bg_c = m["bg"] if resaltada else (255, 255, 255)

        draw.rounded_rectangle([mx, y_cards, mx + w_card, y_cards + h_card], radius=10, fill=bg_c, outline=border_c, width=2 if resaltada else 1)
        
        bbox_v = draw.textbbox((0, 0), m["val"], font=f_metric_val)
        vw = bbox_v[2] - bbox_v[0]
        draw.text((mx + (w_card - vw) // 2, y_cards + 12), m["val"], fill=m["col"], font=f_metric_val)
        
        bbox_l = draw.textbbox((0, 0), m["lbl"], font=f_metric_lbl)
        lw = bbox_l[2] - bbox_l[0]
        draw.text((mx + (w_card - lw) // 2, y_cards + 42), m["lbl"], fill=(71, 85, 105), font=f_metric_lbl)

    # 4. Barra CTA inferior
    y_cta = y_cards + h_card + 22
    cta_w = 360
    cta_h = 42
    cta_x = cx - cta_w // 2
    draw.rounded_rectangle([cta_x, y_cta, cta_x + cta_w, y_cta + cta_h], radius=21, fill=(15, 23, 42))
    cta_txt = "Dejá tu comentario abajo"
    bbox_c = draw.textbbox((0, 0), cta_txt, font=f_cta)
    cw = bbox_c[2] - bbox_c[0]
    draw.text((cta_x + (cta_w - cw) // 2, y_cta + 12), cta_txt, fill=(255, 255, 255), font=f_cta)

    return img

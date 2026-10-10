"""
plantillas/tareas_problema.py
-----------------------------
Plantilla para la escena de caos / problema del gestor de tareas.
Mobile-First / Alta Legibilidad:
- Fuentes grandes (20px a 25px) para lectura nítida en smartphones.
- Máximo aprovechamiento del espacio sin márgenes muertos.
- 3 tareas clave de impacto con estados de atraso destacados.
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    dibujar_icono_reloj,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Lista Andes",
    "Bandeja de Pendientes",
    "Pendientes sin orden",
    "Buscar tareas acumuladas sin clasificar...",
    "Enviar propuesta comercial",
    "Llamar a proveedor de insumos",
    "Revisar informe de métricas",
    "Responder dudas del cliente",
    "Venció ayer",
    "Atrasado",
    "Para hoy",
    "Ventas",
    "Operaciones",
    "Estrategia",
    "Soporte",
    "Pendiente sin organizar",
    "Acumulado sin fecha"
]

ITEMS_PROBLEMA = [
    {"tit": "Enviar propuesta comercial", "sub": "Ventas • Pendiente sin organizar", "tag": "Venció ayer", "cor": (225, 29, 72), "bg_tag": (254, 226, 226)},
    {"tit": "Llamar a proveedor de insumos", "sub": "Operaciones • Pendiente sin organizar", "tag": "Atrasado", "cor": (225, 29, 72), "bg_tag": (254, 226, 226)},
    {"tit": "Revisar informe de métricas", "sub": "Estrategia • Pendiente sin organizar", "tag": "Para hoy", "cor": (100, 116, 139), "bg_tag": (241, 245, 249)},
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el caos de tareas con tipografía grande y alta legibilidad."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0)
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Lista Andes",
        subtitulo="Bandeja de Pendientes",
        tipo_mockup=tipo_mockup
    )

    # Tipografías Mobile-First escaladas (19px - 25px)
    f_tit_25 = obtener_fuente(25, bold=True)
    f_sub_20 = obtener_fuente(20, bold=False)
    f_badge_19 = obtener_fuente(19, bold=True)

    # 1. Badge superior de advertencia (con margen seguro respecto al sello)
    chip_w = 240
    chip_h = 36
    chip_x = ancho - chip_w - 205
    chip_y = (66 - chip_h) // 2
    draw.rounded_rectangle([chip_x, chip_y, chip_x + chip_w, chip_y + chip_h], radius=8, fill=(254, 226, 226), outline=(244, 63, 94))
    draw.ellipse([chip_x + 14, chip_y + 13, chip_x + 24, chip_y + 23], fill=(225, 29, 72))
    draw.text((chip_x + 32, chip_y + 7), "Pendientes sin orden", fill=(153, 27, 27), font=f_badge_19)

    # 2. Barra de búsqueda o alerta
    bar_y = iy + 4
    h_bar = 48
    draw.rounded_rectangle([ix, bar_y, ix + iw, bar_y + h_bar], radius=10, fill=(241, 245, 249), outline=(226, 232, 240))
    draw.ellipse([ix + 20, bar_y + 14, ix + 34, bar_y + 28], outline=(148, 163, 184), width=2)
    draw.line([(ix + 31, bar_y + 25), (ix + 39, bar_y + 33)], fill=(148, 163, 184), width=2)
    draw.text((ix + 52, bar_y + 12), "Buscar tareas acumuladas sin clasificar...", fill=(100, 116, 139), font=f_sub_20)

    # 3. Filas de tareas de impacto (3 filas grandes que ocupan el espacio)
    start_y = bar_y + h_bar + 14
    row_h = 112
    espacio_filas = 14

    for i, it in enumerate(ITEMS_PROBLEMA):
        ry = start_y + i * (row_h + espacio_filas)
        if ry + row_h > alto - 10:
            break

        # Resaltado dinámico según etapa
        resaltar = (etapa >= 1 and i < 2)
        bg_card = (255, 241, 242) if resaltar else (255, 255, 255)
        border_card = (251, 113, 133) if resaltar else (226, 232, 240)

        draw.rounded_rectangle([ix, ry, ix + iw, ry + row_h], radius=12, fill=bg_card, outline=border_card, width=2)

        # Borde lateral rojo indicador de urgencia
        draw.rounded_rectangle([ix, ry, ix + 8, ry + row_h], radius=4, fill=it["cor"])

        # Círculo checkbox grande
        c_col = it["cor"] if i < 2 else (203, 213, 225)
        cx0, cy0 = ix + 30, ry + (row_h - 32) // 2
        draw.ellipse([cx0, cy0, cx0 + 32, cy0 + 32], outline=c_col, width=3)

        # Textos de la tarea (Grandes y claros)
        draw.text((ix + 78, ry + 22), it["tit"], fill=(15, 23, 42), font=f_tit_25)
        draw.text((ix + 78, ry + 60), it["sub"], fill=(100, 116, 139), font=f_sub_20)

        # Tag lateral derecho grande
        tag_w = 150
        tag_h = 40
        tag_x = ix + iw - tag_w - 20
        tag_y = ry + (row_h - tag_h) // 2
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=8, fill=it["bg_tag"], outline=(*it["cor"][:3], 120))
        draw.text((tag_x + 18, tag_y + 9), it["tag"], fill=it["cor"], font=f_badge_19)

    return img

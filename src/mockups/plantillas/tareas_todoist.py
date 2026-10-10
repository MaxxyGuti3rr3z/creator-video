"""
plantillas/tareas_todoist.py
----------------------------
Plantilla para el punto 1 del gestor de tareas:
Mobile-First / Alta Legibilidad:
- Fuentes grandes (20px a 25px) para lectura clara en smartphones.
- Máximo aprovechamiento del espacio sin márgenes muertos.
- Prioridades P1 y P2 destacadas en grande.
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    dibujar_banderin,
    dibujar_cursor_moderno,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Lista Andes",
    "Organización Inteligente",
    "Todas",
    "Por Prioridad",
    "Para Hoy",
    "PRIORIDAD ALTA (P1)",
    "PRIORIDAD MEDIA (P2)",
    "Enviar propuesta comercial",
    "Llamar a proveedor de insumos",
    "Revisar informe de métricas",
    "Proyecto: Ventas",
    "Proyecto: Operaciones",
    "Proyecto: Estrategia",
    "Alta P1",
    "Med P2",
    "Organizado por Prioridad"
]

ITEMS_TODOIST = [
    {"tit": "Enviar propuesta comercial", "sub": "Proyecto: Ventas", "prio": "Alta P1", "cor": (225, 29, 72), "bg": (254, 226, 226), "sec": "PRIORIDAD ALTA (P1)"},
    {"tit": "Llamar a proveedor de insumos", "sub": "Proyecto: Operaciones", "prio": "Alta P1", "cor": (225, 29, 72), "bg": (254, 226, 226), "sec": None},
    {"tit": "Revisar informe de métricas", "sub": "Proyecto: Estrategia", "prio": "Med P2", "cor": (217, 119, 6), "bg": (254, 243, 199), "sec": "PRIORIDAD MEDIA (P2)"},
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza la organización de tareas con textos grandes y lectura instantánea."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0)
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Lista Andes",
        subtitulo="Organización Inteligente",
        tipo_mockup=tipo_mockup
    )

    # Tipografías Mobile-First escaladas (19px - 25px)
    f_tit_25 = obtener_fuente(25, bold=True)
    f_sub_20 = obtener_fuente(20, bold=False)
    f_tab_21 = obtener_fuente(21, bold=True)
    f_tab_inact = obtener_fuente(21, bold=False)
    f_badge_19 = obtener_fuente(19, bold=True)
    f_sec_18 = obtener_fuente(18, bold=True)

    # 1. Chip superior: 'Organizado por Prioridad' (con margen seguro respecto al sello)
    chip_w = 280
    chip_h = 36
    chip_x = ancho - chip_w - 205
    chip_y = (66 - chip_h) // 2
    draw.rounded_rectangle([chip_x, chip_y, chip_x + chip_w, chip_y + chip_h], radius=8, fill=(224, 242, 254), outline=(14, 165, 233))
    dibujar_banderin(draw, chip_x + 14, chip_y + 11, 14, (2, 132, 199))
    draw.text((chip_x + 34, chip_y + 8), "Organizado por Prioridad", fill=(3, 105, 161), font=f_badge_19)

    # 2. Pestañas de filtro grandes
    tab_y = iy + 4
    pestanias = ["Todas", "Por Prioridad", "Para Hoy"]
    cx = ix + 10
    for idx_tab, nom in enumerate(pestanias):
        activa = (idx_tab == 1)
        w_tab = 150
        if activa:
            draw.text((cx, tab_y), nom, fill=(15, 23, 42), font=f_tab_21)
            draw.line([(cx - 4, tab_y + 32), (cx + w_tab - 10, tab_y + 32)], fill=(14, 165, 233), width=4)
        else:
            draw.text((cx, tab_y), nom, fill=(148, 163, 184), font=f_tab_inact)
        cx += w_tab + 26

    # 3. Listado de tareas con secciones de prioridad
    cur_y = tab_y + 46
    row_h = 92
    espacio_filas = 10

    for i, it in enumerate(ITEMS_TODOIST):
        if it["sec"]:
            dibujar_banderin(draw, ix + 10, cur_y + 3, 12, it["cor"])
            draw.text((ix + 30, cur_y), it["sec"], fill=it["cor"], font=f_sec_18)
            cur_y += 26

        resaltado = (etapa >= 1 and i == 0)
        bg_card = (254, 242, 242) if resaltado else (255, 255, 255)
        border_card = (252, 165, 165) if resaltado else (226, 232, 240)

        draw.rounded_rectangle([ix, cur_y, ix + iw, cur_y + row_h], radius=12, fill=bg_card, outline=border_card, width=2)
        draw.rounded_rectangle([ix, cur_y, ix + 8, cur_y + row_h], radius=4, fill=it["cor"])

        # Checkbox grande
        draw.ellipse([ix + 26, cur_y + (row_h - 28) // 2, ix + 54, cur_y + (row_h - 28) // 2 + 28], outline=(203, 213, 225), width=3)

        # Textos grandes
        draw.text((ix + 70, cur_y + 16), it["tit"], fill=(15, 23, 42), font=f_tit_25)
        draw.text((ix + 70, cur_y + 50), it["sub"], fill=(100, 116, 139), font=f_sub_20)

        # Badge de prioridad lateral
        badge_w = 120
        badge_h = 36
        badge_x = ix + iw - badge_w - 20
        badge_y = cur_y + (row_h - badge_h) // 2
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=8, fill=it["bg"], outline=(*it["cor"][:3], 120))
        draw.text((badge_x + 22, badge_y + 7), it["prio"], fill=it["cor"], font=f_badge_19)

        cur_y += row_h + espacio_filas

    return img

"""
plantillas/tareas_resultado.py
------------------------------
Plantilla para la escena de resultado/alivio en la gestión de tareas.
Mobile-First / Alta Legibilidad:
- Fuentes grandes (20px a 25px) para lectura clara y descanso visual.
- Aprovechamiento completo de la ventana sin márgenes muertos ni textos diminutos.
- Tareas completadas con checks grandes y sensación inmediata de alivio.
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
    "Lista Andes",
    "Objetivos del Día",
    "Todas Completadas",
    "Bandeja Despejada",
    "Enviar propuesta comercial",
    "Llamar a proveedor de insumos",
    "Revisar informe de métricas",
    "Reunión de coordinación",
    "Actualizar base de datos",
    "Respuesta a clientes",
    "Ventas",
    "Operaciones",
    "Estrategia",
    "Completada",
    "Al Día"
]

TAREAS_COMPLETADAS = [
    {"tit": "Enviar propuesta comercial", "sub": "Ventas • Enviado a tiempo", "etapa_tildado": 0},
    {"tit": "Llamar a proveedor de insumos", "sub": "Operaciones • Confirmado", "etapa_tildado": 0},
    {"tit": "Revisar informe de métricas", "sub": "Estrategia • Aprobado", "etapa_tildado": 1},
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el resultado de tareas completadas con tipografía grande y alta legibilidad."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Lista Andes",
        subtitulo="Objetivos del Día",
        tipo_mockup=tipo_mockup
    )

    # Tipografías Mobile-First escaladas (19px - 25px)
    f_tit_25 = obtener_fuente(25, bold=True)
    f_sub_20 = obtener_fuente(20, bold=False)
    f_badge_19 = obtener_fuente(19, bold=True)
    f_banner_22 = obtener_fuente(22, bold=True)

    # 1. Badge superior derecho: 'Todas Completadas' o 'Al Día' (con margen seguro)
    badge_txt = "Todas Completadas" if etapa >= 2 else "Al Día"
    badge_w = 210
    badge_h = 36
    bx = ancho - badge_w - 230
    by = (66 - badge_h) // 2
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=8, fill=(236, 253, 245), outline=(16, 185, 129))
    dibujar_icono_check(draw, bx + 14, by + 11, (16, 185, 129), tam=14, grosor=3)
    draw.text((bx + 38, by + 7), badge_txt, fill=(16, 185, 129), font=f_badge_19)

    # 2. Banner de Alivio y Logro (Grande y visible)
    banner_y = iy + 4
    h_banner = 50
    draw.rounded_rectangle([ix, banner_y, ix + iw, banner_y + h_banner], radius=10, fill=(240, 253, 250), outline=(153, 246, 228), width=2)
    dibujar_chispa_ia(draw, ix + 24, banner_y + 25, 8, (13, 148, 136))
    draw.text((ix + 44, banner_y + 12), "Bandeja Despejada • Todo al día y organizado", fill=(13, 148, 136), font=f_banner_22)

    # 3. Filas de tareas completadas de impacto (3 filas grandes)
    cur_y = banner_y + h_banner + 14
    row_h = 105
    espacio_filas = 12

    for idx, t_info in enumerate(TAREAS_COMPLETADAS):
        tildada = (etapa >= t_info["etapa_tildado"])
        
        bg_card = (248, 250, 252) if tildada else (255, 255, 255)
        bd_card = (209, 250, 229) if tildada else (226, 232, 240)
        col_txt = (100, 116, 139) if tildada else (15, 23, 42)
        col_sub = (148, 163, 184) if tildada else (100, 116, 139)

        draw.rounded_rectangle([ix, cur_y, ix + iw, cur_y + row_h], radius=12, fill=bg_card, outline=bd_card, width=2)
        draw.rounded_rectangle([ix, cur_y, ix + 8, cur_y + row_h], radius=4, fill=(16, 185, 129) if tildada else (203, 213, 225))

        # Checkbox grande
        cx0, cy0 = ix + 28, cur_y + (row_h - 36) // 2
        if tildada:
            draw.ellipse([cx0, cy0, cx0 + 36, cy0 + 36], fill=(16, 185, 129))
            dibujar_icono_check(draw, cx0 + 9, cy0 + 10, (255, 255, 255), tam=18, grosor=3)
        else:
            draw.ellipse([cx0, cy0, cx0 + 36, cy0 + 36], outline=(203, 213, 225), width=3)

        # Textos grandes
        draw.text((ix + 80, cur_y + 20), t_info["tit"], fill=col_txt, font=f_tit_25)
        draw.text((ix + 80, cur_y + 56), t_info["sub"], fill=col_sub, font=f_sub_20)

        # Si está tildada, tachado suave del título
        if tildada:
            bbox_t = draw.textbbox((ix + 80, cur_y + 20), t_info["tit"], font=f_tit_25)
            line_y = (bbox_t[1] + bbox_t[3]) // 2
            draw.line([(bbox_t[0], line_y), (bbox_t[2], line_y)], fill=(148, 163, 184), width=2)

        # Tag lateral derecho
        tag_w = 140
        tag_h = 38
        tag_x = ix + iw - tag_w - 20
        tag_y = cur_y + (row_h - tag_h) // 2
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=8, fill=(236, 253, 245), outline=(167, 243, 208))
        draw.text((tag_x + 16, tag_y + 8), "Completada", fill=(5, 150, 105), font=f_badge_19)

        cur_y += row_h + espacio_filas

    return img

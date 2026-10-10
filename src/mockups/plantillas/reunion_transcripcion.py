"""
plantillas/reunion_transcripcion.py
-----------------------------------
Plantilla para Punto 1 de reuniones (estilo Otter.ai).
Muestra:
- Cabecera con indicador REC coral.
- Mini grilla de participantes a la izquierda.
- Panel derecho con transcripción en vivo y puntos clave destacados.
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
import math
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    dibujar_chispa_ia,
    dibujar_icono_check,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Sala Andes",
    "Transcripción Inteligente",
    "REC",
    "Carla Méndez",
    "Diego Ruiz",
    "Lucía Paz",
    "Martín Vega",
    "Transcripción en vivo",
    "Otter.ai Activo",
    "¿Para cuándo estimamos el cierre del presupuesto y las metas de Q3?",
    "Cerramos el presupuesto el viernes y enviamos el reporte a todo el equipo.",
    "Perfecto, ya tengo lista la documentación y los accesos del servidor.",
    "PUNTOS CLAVE (IA)",
    "Presupuesto cerrado este viernes.",
    "Documentación y accesos listos."
]

PARTICIPANTES = [
    {"nom": "Carla Méndez", "corto": "Carla M.", "ini": "CM", "col": (37, 99, 235)},
    {"nom": "Diego Ruiz", "corto": "Diego R.", "ini": "DR", "col": (5, 150, 105)},
    {"nom": "Lucía Paz", "corto": "Lucía P.", "ini": "LP", "col": (124, 58, 237)},
    {"nom": "Martín Vega", "corto": "Martín V.", "ini": "MV", "col": (217, 119, 6)},
]

DIALOGOS = [
    {"idx": 0, "hora": "00:41:12", "txt": "¿Para cuándo estimamos el cierre del presupuesto y las metas de Q3?"},
    {"idx": 1, "hora": "00:41:18", "txt": "Cerramos el presupuesto el viernes y enviamos el reporte a todo el equipo."},
    {"idx": 2, "hora": "00:41:25", "txt": "Perfecto, ya tengo lista la documentación y los accesos del servidor."},
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza la transcripción en vivo con micro-etapas cada <= 3s."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Sala Andes",
        subtitulo="Transcripción Inteligente",
        tipo_mockup=tipo_mockup
    )

    f_rec = obtener_fuente(12, bold=True)
    f_tit_sec = obtener_fuente(12, bold=True)
    f_pan_tit = obtener_fuente(14, bold=True)
    f_chip = obtener_fuente(11, bold=True)
    f_hablante = obtener_fuente(12, bold=True)
    f_hora = obtener_fuente(10, bold=False)
    f_texto = obtener_fuente(12, bold=False)
    f_ini = obtener_fuente(12, bold=True)

    # 1. Badge REC superior
    tiempo_rec_str = f"00:41:{12 + int(tiempo_segundos):02d}"
    badge_w = 120
    badge_h = 26
    bx = ix + iw - badge_w
    by = iy
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=13, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
    draw.ellipse([bx + 10, by + 8, bx + 18, by + 16], fill=(244, 63, 94))
    draw.text((bx + 24, by + 5), f"REC {tiempo_rec_str}", fill=(225, 29, 72), font=f_rec)

    # 2. Columna Izquierda: Grilla 2x2 de llamada
    w_izq = 210
    h_col = ih - 10
    y_col = iy + 8

    draw.rounded_rectangle([ix, y_col, ix + w_izq, y_col + h_col], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((ix + 12, y_col + 10), "Participantes (4)", fill=(71, 85, 105), font=f_tit_sec)

    grid_y = y_col + 32
    gap_g = 8
    w_cell = (w_izq - 24 - gap_g) // 2
    h_cell = 70

    for idx, p in enumerate(PARTICIPANTES):
        fila = idx // 2
        col = idx % 2
        cx0 = ix + 12 + col * (w_cell + gap_g)
        cy0 = grid_y + fila * (h_cell + gap_g)
        cx1 = cx0 + w_cell
        cy1 = cy0 + h_cell

        es_hablante = (idx == etapa)
        bd = (14, 165, 233) if es_hablante else (226, 232, 240)
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=8, fill=(255, 255, 255), outline=bd, width=2 if es_hablante else 1)

        av_r = 14
        av_cx = (cx0 + cx1) // 2
        av_cy = cy0 + 22
        draw.ellipse([av_cx - av_r, av_cy - av_r, av_cx + av_r, av_cy + av_r], fill=p["col"])
        bbox_i = draw.textbbox((0, 0), p["ini"], font=f_ini)
        draw.text((av_cx - (bbox_i[2] - bbox_i[0]) // 2, av_cy - (bbox_i[3] - bbox_i[1]) // 2 - 1), p["ini"], fill=(255, 255, 255), font=f_ini)

        bbox_n = draw.textbbox((0, 0), p["corto"], font=obtener_fuente(10, bold=True))
        draw.text(((cx0 + cx1) // 2 - (bbox_n[2] - bbox_n[0]) // 2, cy1 - 18), p["corto"], fill=(30, 41, 59), font=obtener_fuente(10, bold=True))

    # 3. Columna Derecha: Panel de Transcripción
    x_der = ix + w_izq + 14
    w_der = iw - w_izq - 14

    draw.rounded_rectangle([x_der, y_col, x_der + w_der, y_col + h_col], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

    # Cabecera transcripción
    h_pan_top = 36
    draw.rounded_rectangle([x_der, y_col, x_der + w_der, y_col + h_pan_top], radius=10, fill=(248, 250, 252))
    draw.line([(x_der, y_col + h_pan_top), (x_der + w_der, y_col + h_pan_top)], fill=(226, 232, 240), width=1)
    
    dibujar_chispa_ia(draw, x_der + 16, y_col + 18, 5, (14, 165, 233))
    draw.text((x_der + 28, y_col + 9), "Transcripción en vivo", fill=(15, 23, 42), font=f_pan_tit)

    # Chip Otter
    cw = 110
    cx_chip = x_der + w_der - cw - 12
    cy_chip = y_col + 6
    draw.rounded_rectangle([cx_chip, cy_chip, cx_chip + cw, cy_chip + 24], radius=6, fill=(240, 249, 255), outline=(186, 230, 253))
    dibujar_icono_check(draw, cx_chip + 8, cy_chip + 7, (2, 132, 199), tam=9, grosor=2)
    draw.text((cx_chip + 22, cy_chip + 4), "Otter.ai Activo", fill=(2, 132, 199), font=f_chip)

    # Mensajes de diálogo
    cur_dy = y_col + h_pan_top + 10
    for d_i in range(min(etapa + 1, len(DIALOGOS))):
        dia = DIALOGOS[d_i]
        part = PARTICIPANTES[dia["idx"]]

        # Barra lateral de color
        draw.rounded_rectangle([x_der + 12, cur_dy, x_der + 15, cur_dy + 42], radius=1, fill=part["col"])
        
        # Nombre + Hora
        draw.text((x_der + 24, cur_dy), part["nom"], fill=part["col"], font=f_hablante)
        draw.text((x_der + 150, cur_dy + 2), dia["hora"], fill=(148, 163, 184), font=f_hora)
        
        # Diálogo
        draw.text((x_der + 24, cur_dy + 18), dia["txt"], fill=(51, 65, 85), font=f_texto)
        cur_dy += 54

    # Tarjeta de Puntos Clave en etapa 2
    if etapa >= 2:
        py_ptos = y_col + h_col - 82
        draw.rounded_rectangle([x_der + 12, py_ptos, x_der + w_der - 12, py_ptos + 72], radius=8, fill=(236, 254, 255), outline=(6, 182, 212), width=1)
        dibujar_chispa_ia(draw, x_der + 24, py_ptos + 16, 6, (8, 145, 178))
        draw.text((x_der + 36, py_ptos + 8), "PUNTOS CLAVE (IA)", fill=(8, 145, 178), font=f_chip)
        draw.text((x_der + 24, py_ptos + 28), "• Presupuesto cerrado este viernes.", fill=(15, 23, 42), font=f_texto)
        draw.text((x_der + 24, py_ptos + 46), "• Documentación y accesos listos.", fill=(15, 23, 42), font=f_texto)

    return img

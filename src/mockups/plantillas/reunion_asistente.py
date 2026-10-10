"""
plantillas/reunion_asistente.py
-------------------------------
Plantilla para Punto 2 de reuniones (estilo Fireflies.ai).
Muestra:
- Asistente IA sumado como participante activo a la llamada.
- Panel derecho con notas generadas automáticamente y checklist de tareas asignadas.
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
    "Asistente IA Conectado",
    "5 en llamada (+IA)",
    "Fireflies Notetaker",
    "Asistente IA activo",
    "Anotando diálogo...",
    "Notas de reunión",
    "Compartido con 4 personas",
    "Enviar presupuesto Q3 ajustado",
    "Diego R. • Viernes",
    "Migrar servidores de producción",
    "Lucía P. • Martes",
    "Compartir minuta a stakeholders",
    "Carla M. • Hoy"
]

PARTICIPANTES_HUMANOS = [
    {"nom": "Carla M.", "ini": "CM", "col": (37, 99, 235)},
    {"nom": "Diego R.", "ini": "DR", "col": (5, 150, 105)},
    {"nom": "Lucía P.", "ini": "LP", "col": (124, 58, 237)},
    {"nom": "Martín V.", "ini": "MV", "col": (217, 119, 6)},
]

TAREAS_ASIGNADAS = [
    {"tit": "Enviar presupuesto Q3 ajustado", "sub": "Diego R. • Viernes", "etapa_chk": 0},
    {"tit": "Migrar servidores de producción", "sub": "Lucía P. • Martes", "etapa_chk": 1},
    {"tit": "Compartir minuta a stakeholders", "sub": "Carla M. • Hoy", "etapa_chk": 2},
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el asistente IA tomando notas y asignando tareas."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Sala Andes",
        subtitulo="Asistente IA Conectado",
        tipo_mockup=tipo_mockup
    )

    f_badge = obtener_fuente(11, bold=True)
    f_pan_tit = obtener_fuente(14, bold=True)
    f_bold_13 = obtener_fuente(13, bold=True)
    f_reg_11 = obtener_fuente(11, bold=False)

    # 1. Badge superior derecho
    badge_w = 140
    badge_h = 26
    bx = ix + iw - badge_w
    by = iy
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=13, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw.ellipse([bx + 10, by + 8, bx + 18, by + 16], fill=(16, 185, 129))
    draw.text((bx + 24, by + 5), "5 en llamada (+IA)", fill=(22, 101, 52), font=f_badge)

    # 2. Columna Izquierda: 4 Humanos + Asistente IA
    w_izq = 210
    h_col = ih - 10
    y_col = iy + 8

    draw.rounded_rectangle([ix, y_col, ix + w_izq, y_col + h_col], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((ix + 12, y_col + 10), "Participantes (4 + 1 IA)", fill=(71, 85, 105), font=obtener_fuente(11, bold=True))

    grid_y = y_col + 30
    w_cell = (w_izq - 24 - 8) // 2
    h_cell = 64

    for idx, p in enumerate(PARTICIPANTES_HUMANOS):
        fila = idx // 2
        col = idx % 2
        cx0 = ix + 12 + col * (w_cell + 8)
        cy0 = grid_y + fila * (h_cell + 6)
        cx1 = cx0 + w_cell
        cy1 = cy0 + h_cell

        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        av_r = 13
        av_cx = (cx0 + cx1) // 2
        av_cy = cy0 + 20
        draw.ellipse([av_cx - av_r, av_cy - av_r, av_cx + av_r, av_cy + av_r], fill=p["col"])
        bbox_i = draw.textbbox((0, 0), p["ini"], font=obtener_fuente(11, bold=True))
        draw.text((av_cx - (bbox_i[2] - bbox_i[0]) // 2, av_cy - (bbox_i[3] - bbox_i[1]) // 2 - 1), p["ini"], fill=(255, 255, 255), font=obtener_fuente(11, bold=True))
        bbox_n = draw.textbbox((0, 0), p["nom"], font=obtener_fuente(10, bold=True))
        draw.text(((cx0 + cx1) // 2 - (bbox_n[2] - bbox_n[0]) // 2, cy1 - 18), p["nom"], fill=(30, 41, 59), font=obtener_fuente(10, bold=True))

    # Bot Asistente IA (Card abajo)
    y_bot = grid_y + 2 * (h_cell + 6) + 4
    h_bot = 80
    draw.rounded_rectangle([ix + 12, y_bot, ix + w_izq - 12, y_bot + h_bot], radius=8, fill=(240, 253, 250), outline=(14, 165, 233), width=2)
    bot_cx = ix + 32
    bot_cy = y_bot + h_bot // 2
    draw.ellipse([bot_cx - 14, bot_cy - 14, bot_cx + 14, bot_cy + 14], fill=(224, 242, 254))
    dibujar_chispa_ia(draw, bot_cx, bot_cy, 8, (14, 165, 233))
    draw.text((ix + 54, y_bot + 14), "Fireflies Notetaker", fill=(15, 23, 42), font=obtener_fuente(11, bold=True))
    draw.text((ix + 54, y_bot + 32), "Asistente IA activo", fill=(13, 148, 136), font=obtener_fuente(10, bold=True))
    draw.text((ix + 54, y_bot + 48), "Anotando diálogo...", fill=(100, 116, 139), font=obtener_fuente(9, bold=False))

    # 3. Columna Derecha: Notas y Checklist de Tareas
    x_der = ix + w_izq + 14
    w_der = iw - w_izq - 14

    draw.rounded_rectangle([x_der, y_col, x_der + w_der, y_col + h_col], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

    # Cabecera
    h_pan_top = 36
    draw.rounded_rectangle([x_der, y_col, x_der + w_der, y_col + h_pan_top], radius=10, fill=(248, 250, 252))
    draw.line([(x_der, y_col + h_pan_top), (x_der + w_der, y_col + h_pan_top)], fill=(226, 232, 240), width=1)
    
    dibujar_chispa_ia(draw, x_der + 16, y_col + 18, 5, (14, 165, 233))
    draw.text((x_der + 28, y_col + 9), "Notas de reunión", fill=(15, 23, 42), font=f_pan_tit)

    # Badge Compartido con 4 personas
    sw = 160
    sx0 = x_der + w_der - sw - 12
    sy0 = y_col + 6
    draw.rounded_rectangle([sx0, sy0, sx0 + sw, sy0 + 24], radius=6, fill=(240, 253, 250), outline=(204, 251, 241))
    dibujar_icono_check(draw, sx0 + 8, sy0 + 7, (13, 148, 136), tam=9, grosor=2)
    draw.text((sx0 + 22, sy0 + 4), "Compartido con 4 personas", fill=(13, 148, 136), font=f_badge)

    # Filas de Tareas Asignadas que se van tildando
    ty = y_col + h_pan_top + 16
    r_h = 58

    for t_i, t_data in enumerate(TAREAS_ASIGNADAS):
        tildada = (etapa >= t_data["etapa_chk"])
        
        bg_card = (240, 253, 250) if tildada else (255, 255, 255)
        bd_card = (14, 165, 233) if tildada else (226, 232, 240)
        draw.rounded_rectangle([x_der + 14, ty, x_der + w_der - 14, ty + r_h], radius=8, fill=bg_card, outline=bd_card, width=1)

        # Checkbox
        cx_c = x_der + 28
        cy_c = ty + 18
        if tildada:
            draw.ellipse([cx_c, cy_c, cx_c + 20, cy_c + 20], fill=(14, 165, 233))
            dibujar_icono_check(draw, cx_c + 4, cy_c + 5, (255, 255, 255), tam=11, grosor=2)
        else:
            draw.ellipse([cx_c, cy_c, cx_c + 20, cy_c + 20], outline=(203, 213, 225), width=2)

        draw.text((cx_c + 32, ty + 10), t_data["tit"], fill=(15, 23, 42), font=f_bold_13)
        draw.text((cx_c + 32, ty + 30), t_data["sub"], fill=(100, 116, 139), font=f_reg_11)

        ty += r_h + 12

    return img

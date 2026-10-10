"""
plantillas/reunion_hook.py
--------------------------
Plantilla para el hook / problema de reuniones.
Muestra:
- Arriba: Tira de videollamada con 4 participantes activos hablando rápido.
- Abajo: Bloc de notas manual donde se intenta anotar a mano, atrasándose con cursor titilando.
- Estética limpia, 3 puntos neutros, sello ilustrativo.
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
import math
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Sala Andes",
    "Videollamada en Vivo",
    "EN VIVO",
    "Carla M.",
    "Diego R.",
    "Lucía P.",
    "Martín V.",
    "Bloc de notas de la llamada (a mano)",
    "Atrasado 15 seg",
    "Presupuesto Q3: Diego dijo que se cierra el viernes...",
    "Servidores: Lucía mencionó una migración urgente...",
    "Acción pendiente: Enviar resumen a... (¡incompleto!)"
]

PARTICIPANTES = [
    {"corto": "Carla M.", "ini": "CM", "col": (37, 99, 235)},
    {"corto": "Diego R.", "ini": "DR", "col": (5, 150, 105)},
    {"corto": "Lucía P.", "ini": "LP", "col": (124, 58, 237)},
    {"corto": "Martín V.", "ini": "MV", "col": (217, 119, 6)},
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el hook de videollamada y toma de notas manual."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Sala Andes",
        subtitulo="Videollamada en Vivo",
        tipo_mockup=tipo_mockup
    )

    f_rec = obtener_fuente(12, bold=True)
    f_part_nom = obtener_fuente(12, bold=True)
    f_part_ini = obtener_fuente(14, bold=True)
    f_nota_tit = obtener_fuente(13, bold=True)
    f_nota_txt = obtener_fuente(13, bold=False)
    f_alerta = obtener_fuente(11, bold=True)

    # 1. Badge superior derecho: 'EN VIVO' con contador
    seg_rapidos = int((tiempo_segundos * 1.5) % 60)
    tiempo_rec_str = f"00:41:{12 + seg_rapidos:02d}"
    badge_w = 140
    badge_h = 26
    bx = ix + iw - badge_w
    by = iy
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=13, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
    draw.ellipse([bx + 10, by + 8, bx + 18, by + 16], fill=(244, 63, 94))
    draw.text((bx + 24, by + 5), f"EN VIVO {tiempo_rec_str}", fill=(225, 29, 72), font=f_rec)

    # 2. Tira de 4 participantes en miniatura
    y_strip = iy + 36
    h_strip = 120
    draw.rounded_rectangle([ix, y_strip, ix + iw, y_strip + h_strip], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)

    gap = 12
    w_tile = (iw - 16 * 2 - 3 * gap) // 4
    hablante_activo = (etapa % 4)

    for idx, p in enumerate(PARTICIPANTES):
        tx0 = ix + 16 + idx * (w_tile + gap)
        tx1 = tx0 + w_tile
        ty0 = y_strip + 12
        ty1 = y_strip + h_strip - 12

        es_hablante = (idx == hablante_activo)
        b_col = (14, 165, 233) if es_hablante else (226, 232, 240)
        draw.rounded_rectangle([tx0, ty0, tx1, ty1], radius=8, fill=(255, 255, 255), outline=b_col, width=2 if es_hablante else 1)

        # Avatar
        av_r = 16
        av_cx = (tx0 + tx1) // 2
        av_cy = ty0 + 26
        draw.ellipse([av_cx - av_r, av_cy - av_r, av_cx + av_r, av_cy + av_r], fill=p["col"])
        bbox_i = draw.textbbox((0, 0), p["ini"], font=f_part_ini)
        draw.text((av_cx - (bbox_i[2] - bbox_i[0]) // 2, av_cy - (bbox_i[3] - bbox_i[1]) // 2 - 1), p["ini"], fill=(255, 255, 255), font=f_part_ini)

        # Nombre
        bbox_n = draw.textbbox((0, 0), p["corto"], font=f_part_nom)
        draw.text(((tx0 + tx1) // 2 - (bbox_n[2] - bbox_n[0]) // 2, ty1 - 20), p["corto"], fill=(30, 41, 59), font=f_part_nom)

        if es_hablante:
            draw.ellipse([av_cx + av_r - 5, av_cy + av_r - 5, av_cx + av_r + 3, av_cy + av_r + 3], fill=(16, 185, 129))

    # 3. Zona Inferior: Bloc de Notas Manual
    y_notes = y_strip + h_strip + 14
    h_notes = ih - (y_notes - iy)
    draw.rounded_rectangle([ix, y_notes, ix + iw, y_notes + h_notes], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

    # Cabecera del bloc
    h_nb_top = 34
    draw.rounded_rectangle([ix, y_notes, ix + iw, y_notes + h_nb_top], radius=10, fill=(248, 250, 252))
    draw.line([(ix, y_notes + h_nb_top), (ix + iw, y_notes + h_nb_top)], fill=(226, 232, 240), width=1)
    draw.text((ix + 16, y_notes + 8), "Bloc de notas de la llamada (a mano)", fill=(71, 85, 105), font=f_nota_tit)

    # Alerta atrasado
    pill_w = 120
    pill_h = 22
    px0 = ix + iw - pill_w - 12
    py0 = y_notes + 6
    draw.rounded_rectangle([px0, py0, px0 + pill_w, py0 + pill_h], radius=6, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
    draw.text((px0 + 14, py0 + 4), "Atrasado 15 seg", fill=(225, 29, 72), font=f_alerta)

    # Renglones tipeados con cursor parpadeante
    lineas = [
        "Presupuesto Q3: Diego dijo que se cierra el viernes...",
        "Servidores: Lucía mencionó una migración urgente...",
        "Acción pendiente: Enviar resumen a... (¡incompleto!)"
    ]

    ny = y_notes + h_nb_top + 16
    for l_idx in range(min(etapa + 1, len(lineas))):
        txt_linea = lineas[l_idx]
        draw.text((ix + 20, ny), f"• {txt_linea}", fill=(51, 65, 85), font=f_nota_txt)
        ny += 28

    # Cursor titilando en la última línea activa
    if int(tiempo_segundos * 3) % 2 == 0:
        bbox_last = draw.textbbox((ix + 20, ny - 28), f"• {lineas[min(etapa, len(lineas) - 1)]}", font=f_nota_txt)
        draw.line([(bbox_last[2] + 4, ny - 26), (bbox_last[2] + 4, ny - 10)], fill=(30, 41, 59), width=2)

    return img

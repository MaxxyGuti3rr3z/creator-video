"""
plantillas/tareas_calendario.py
-------------------------------
Plantilla para la escena de calendario inteligente / auto-agendado estilo Motion.
Muestra un calendario semanal genérico donde las tareas encajan automáticamente
en los huecos vacíos entre eventos con animación de ajuste secuencial (snap).
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
import math
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    dibujar_chispa_ia,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Lista Andes",
    "Calendario Semanal IA",
    "Auto-Agendado en Huecos",
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Daily Equipo",
    "Informe",
    "Propuesta",
    "Soporte",
    "Demo Interna",
    "Base datos",
    "Proveedor",
    "Coordinación",
    "Responder",
    "Presentación",
    "Cierre Semanal",
    "Ajuste Inteligente (Snap)"
]

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

HORAS = ["09:00", "11:00", "13:00", "15:00", "17:00"]

EVENTOS_FIJOS = [
    {"dia": 0, "h_idx": 0.2, "dur": 0.7, "tit": "Daily Equipo", "sub": "Fija • 30m", "bg": (241, 245, 249), "bd": (203, 213, 225)},
    {"dia": 1, "h_idx": 1.7, "dur": 0.8, "tit": "Coordinación", "sub": "Fija • 45m", "bg": (241, 245, 249), "bd": (203, 213, 225)},
    {"dia": 2, "h_idx": 0.8, "dur": 0.8, "tit": "Soporte", "sub": "Fija • 40m", "bg": (241, 245, 249), "bd": (203, 213, 225)},
    {"dia": 3, "h_idx": 0.5, "dur": 0.9, "tit": "Demo Interna", "sub": "Fija • 1h", "bg": (241, 245, 249), "bd": (203, 213, 225)},
    {"dia": 4, "h_idx": 2.2, "dur": 0.7, "tit": "Cierre Semanal", "sub": "Fija • 30m", "bg": (241, 245, 249), "bd": (203, 213, 225)},
]

TAREAS_AUTO_AGENDADAS = [
    {"dia": 0, "h_idx": 1.0, "dur": 1.1, "tit": "Propuesta", "sub": "Auto-fit • 1h 30m", "bg": (255, 241, 242), "bd": (244, 63, 94), "aparece_etapa": 0},
    {"dia": 0, "h_idx": 2.2, "dur": 0.8, "tit": "Proveedor", "sub": "Auto-fit • 45m", "bg": (254, 243, 199), "bd": (245, 158, 11), "aparece_etapa": 1},
    {"dia": 1, "h_idx": 0.4, "dur": 1.0, "tit": "Informe", "sub": "Auto-fit • 1h 00m", "bg": (224, 242, 254), "bd": (14, 165, 233), "aparece_etapa": 0},
    {"dia": 2, "h_idx": 1.7, "dur": 0.8, "tit": "Responder", "sub": "Auto-fit • 30m", "bg": (243, 232, 255), "bd": (168, 85, 247), "aparece_etapa": 1},
    {"dia": 3, "h_idx": 1.6, "dur": 1.1, "tit": "Presentación", "sub": "Auto-fit • 1h 15m", "bg": (238, 242, 255), "bd": (99, 102, 241), "aparece_etapa": 2},
    {"dia": 4, "h_idx": 0.6, "dur": 0.8, "tit": "Base datos", "sub": "Auto-fit • 45m", "bg": (209, 250, 229), "bd": (16, 185, 129), "aparece_etapa": 2},
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el calendario con bloques que encajan dinámicamente cada <= 3s."""
    etapa, p_etapa = evaluar_etapa_visual(tiempo_segundos, duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0))

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Lista Andes",
        subtitulo="Calendario Semanal IA",
        tipo_mockup=tipo_mockup
    )

    f_bold_13 = obtener_fuente(13, bold=True)
    f_reg_11 = obtener_fuente(11, bold=False)
    f_bold_10 = obtener_fuente(10, bold=True)
    f_horas = obtener_fuente(10, bold=False)

    # 1. Chip superior derecho (ubicado a la izquierda del sello ilustrativo)
    chip_x = ancho - 395
    chip_y = 12
    draw.rounded_rectangle([chip_x, chip_y, chip_x + 190, chip_y + 34], radius=8, fill=(236, 253, 245), outline=(16, 185, 129))
    dibujar_chispa_ia(draw, chip_x + 16, chip_y + 17, 6, (16, 185, 129))
    draw.text((chip_x + 30, chip_y + 8), "Auto-Agendado en Huecos", fill=(6, 95, 70), font=f_bold_10)

    # 2. Encabezado de columnas (Días de la semana)
    col_w = (iw - 60) // 5
    header_y = iy + 4
    x_offset = ix + 55

    for d_idx, dia in enumerate(DIAS_SEMANA):
        dx = x_offset + d_idx * col_w
        if d_idx == 0:
            draw.rounded_rectangle([dx + 2, header_y - 2, dx + col_w - 2, header_y + 24], radius=6, fill=(241, 245, 249))
        draw.text((dx + 16, header_y + 2), dia, fill=(15, 23, 42) if d_idx == 0 else (100, 116, 139), font=f_bold_13)

    # 3. Filas de horas y cuadrícula
    cal_top = header_y + 32
    cal_h = ih - 42
    h_step = cal_h // 4

    for h_idx, hora in enumerate(HORAS[:-1]):
        hy = cal_top + h_idx * h_step
        draw.text((ix + 4, hy - 6), hora, fill=(148, 163, 184), font=f_horas)
        draw.line([(x_offset, hy), (ix + iw - 10, hy)], fill=(241, 245, 249), width=1)

    for d_idx in range(6):
        dx = x_offset + d_idx * col_w
        draw.line([(dx, cal_top - 4), (dx, cal_top + cal_h)], fill=(241, 245, 249), width=1)

    # 4. Dibujar eventos fijos
    for ev in EVENTOS_FIJOS:
        bx = x_offset + ev["dia"] * col_w + 4
        by = cal_top + int(ev["h_idx"] * h_step)
        bw = col_w - 8
        bh = max(24, int(ev["dur"] * h_step))

        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=6, fill=ev["bg"], outline=ev["bd"], width=1)
        draw.text((bx + 6, by + 4), ev["tit"], fill=(30, 41, 59), font=f_bold_10)
        draw.text((bx + 6, by + 18), ev["sub"], fill=(148, 163, 184), font=f_horas)

    # 5. Dibujar tareas auto-agendadas (con aparición secuencial según etapa <= 3s)
    for t_idx, ta in enumerate(TAREAS_AUTO_AGENDADAS):
        if etapa < ta["aparece_etapa"]:
            continue

        bx = x_offset + ta["dia"] * col_w + 4
        by = cal_top + int(ta["h_idx"] * h_step)
        bw = col_w - 8
        bh = max(26, int(ta["dur"] * h_step))

        # Efecto snap / pop si acaba de aparecer en la etapa actual
        if etapa == ta["aparece_etapa"] and p_etapa < 0.35:
            scale_pop = 1.0 + 0.08 * math.sin(p_etapa / 0.35 * math.pi)
            bw = int(bw * scale_pop)

        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=6, fill=ta["bg"], outline=ta["bd"], width=2)
        draw.text((bx + 6, by + 4), ta["tit"], fill=(30, 41, 59), font=f_bold_10)
        draw.text((bx + 6, by + 18), ta["sub"], fill=ta["bd"], font=f_horas)

    # Toast animado de confirmación en etapa 1 o 2
    if etapa >= 1:
        toast_w = 260
        tx = x_offset + 10
        ty = cal_top + 10
        draw.rounded_rectangle([tx, ty, tx + toast_w, ty + 24], radius=6, fill=(240, 253, 250), outline=(13, 148, 136), width=1)
        dibujar_chispa_ia(draw, tx + 10, ty + 12, 4, (13, 148, 136))
        draw.text((tx + 20, ty + 4), "Ajuste Inteligente (Snap)", fill=(15, 118, 110), font=f_bold_10)

    return img

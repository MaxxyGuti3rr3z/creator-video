"""
plantillas/correo_hilo_resumen.py
---------------------------------
Plantilla para Video 4 (correo):
Mobile-First / Alta Legibilidad:
- Letras grandes (20px a 26px) para lectura instantánea en smartphones.
- Máximo aprovechamiento del espacio sin márgenes muertos.
- Frases concisas y contundentes: Hilo -> Resumen IA -> Borrador listo.
"""

from typing import List, Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
from src.mockups.motor import (
    dibujar_ventana_base,
    obtener_fuente,
    dibujar_chispa_ia,
    dibujar_icono_check,
    evaluar_etapa_visual
)

textos_permitidos: List[str] = [
    "Correo",
    "Hilo de Conversación",
    "Lucas Ferrero",
    "Sofía Bianchi",
    "Re: Propuesta Comercial y Alcance Q3",
    "Adjunto las modificaciones solicitadas al cronograma.",
    "Revisamos los puntos pendientes y tenemos acuerdo en tarifas.",
    "Resumen en 1 línea (IA): Cliente aprueba propuesta con entrega el viernes.",
    "Asistente IA",
    "Borrador sugerido",
    "Confirmar entrega viernes",
    "Hola Lucas, confirmamos la entrega para este viernes según lo acordado. Saludos.",
    "Enviar respuesta",
    "Copiar borrador"
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el mockup de correo con tipografía grande y alta legibilidad móvil."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Correo",
        subtitulo="Hilo de Conversación",
        tipo_mockup=tipo_mockup
    )

    # Tipografías Mobile-First escaladas (20px - 26px)
    f_tit_26 = obtener_fuente(26, bold=True)
    f_bold_22 = obtener_fuente(22, bold=True)
    f_reg_21 = obtener_fuente(21, bold=False)
    f_badge_19 = obtener_fuente(19, bold=True)
    f_btn_21 = obtener_fuente(21, bold=True)

    cur_y = iy + 4

    # 1. TARJETA SUPERIOR: Encabezado del Hilo (Grande y claro)
    h_hilo = 118
    draw.rounded_rectangle(
        [ix, cur_y, ix + iw, cur_y + h_hilo],
        radius=12,
        fill=(255, 255, 255),
        outline=(226, 232, 240),
        width=2
    )

    # Badge '12 mensajes' a la derecha
    bw, bh = 150, 34
    bx = ix + iw - bw - 16
    by = cur_y + 16
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((bx + 16, by + 6), "12 mensajes", fill=(71, 85, 105), font=f_badge_19)

    # Avatar grande
    av_r = 22
    av_cx = ix + 36
    av_cy = cur_y + 36
    draw.ellipse([av_cx - av_r, av_cy - av_r, av_cx + av_r, av_cy + av_r], fill=(37, 99, 235))
    draw.text((av_cx - 13, av_cy - 12), "LF", fill=(255, 255, 255), font=f_bold_22)

    # Asunto y remitente
    draw.text((ix + 72, cur_y + 14), "Lucas Ferrero • Propuesta Q3", fill=(15, 23, 42), font=f_tit_26)
    draw.text((ix + 72, cur_y + 48), "Revisamos los puntos pendientes y tenemos acuerdo en tarifas", fill=(100, 116, 139), font=f_reg_21)

    # Estado del hilo
    draw.line([(ix + 72, cur_y + 82), (ix + iw - 16, cur_y + 82)], fill=(241, 245, 249), width=1)
    draw.text((ix + 72, cur_y + 88), "Hilo largo con múltiples respuestas y cambios de fecha", fill=(148, 163, 184), font=f_reg_21)

    cur_y += h_hilo + 14

    # 2. TARJETA CENTRAL: Resumen Inteligente de 1 Línea (Aparece en etapa >= 1)
    if etapa >= 1:
        h_sum = 120
        draw.rounded_rectangle(
            [ix, cur_y, ix + iw, cur_y + h_sum],
            radius=12,
            fill=(240, 249, 255),
            outline=(14, 165, 233),
            width=2
        )
        dibujar_chispa_ia(draw, ix + 28, cur_y + 28, 9, (14, 165, 233))
        draw.text((ix + 46, cur_y + 16), "Resumen en 1 línea (IA):", fill=(3, 105, 161), font=f_bold_22)
        draw.text(
            (ix + 28, cur_y + 54),
            "Cliente aprueba propuesta con entrega el viernes",
            fill=(12, 74, 110),
            font=f_tit_26
        )
        draw.text(
            (ix + 28, cur_y + 86),
            "Sin necesidad de leer los 12 correos anteriores",
            fill=(14, 165, 233),
            font=f_reg_21
        )
        cur_y += h_sum + 14

    # 3. TARJETA INFERIOR: Borrador Automático Sugerido (Aparece en etapa >= 2)
    if etapa >= 2:
        h_draft = ih - (cur_y - iy)
        draw.rounded_rectangle(
            [ix, cur_y, ix + iw, cur_y + h_draft],
            radius=12,
            fill=(255, 255, 255),
            outline=(16, 185, 129),
            width=2
        )

        # Header del borrador
        dibujar_chispa_ia(draw, ix + 28, cur_y + 26, 8, (16, 185, 129))
        draw.text((ix + 46, cur_y + 14), "Borrador sugerido listo:", fill=(5, 150, 105), font=f_bold_22)

        # Texto del borrador
        txt_draft = "Hola Lucas, confirmamos la entrega para este viernes según lo acordado"
        draw.text((ix + 28, cur_y + 48), txt_draft, fill=(15, 23, 42), font=f_bold_22)

        # Botón Enviar Respuesta
        btn_w = 320
        btn_h = 44
        btn_x = ix + iw - btn_w - 18
        btn_y = cur_y + h_draft - btn_h - 16
        draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=8, fill=(16, 185, 129))
        dibujar_icono_check(draw, btn_x + 22, btn_y + 14, (255, 255, 255), tam=16, grosor=3)
        draw.text((btn_x + 50, btn_y + 10), "Confirmar entrega viernes", fill=(255, 255, 255), font=f_btn_21)

    return img

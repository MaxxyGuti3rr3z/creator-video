"""
plantillas/correo_chat_generico.py
----------------------------------
Plantilla para Video 4 (correo):
Mobile-First / Alta Legibilidad:
- Letras grandes (21px a 26px) para lectura clara e inmediata en video vertical.
- Aprovechamiento completo de la ventana sin espacios muertos.
- Flujo: Pedido del usuario -> Puntos clave extraídos -> Borrador listo para enviar.
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
    "Asistente",
    "Chat de Productividad",
    "Vos",
    "Leé este correo y armame un borrador confirmando la entrega del viernes:",
    "Adjunto el cronograma revisado con acuerdo en tarifas para el viernes.",
    "Puntos clave extraídos",
    "Propuesta y tarifas aprobadas",
    "Entrega confirmada para el viernes",
    "Borrador de respuesta listo",
    "Hola Lucas, confirmamos la entrega para este viernes en el horario acordado.",
    "Copiar respuesta"
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el chat de productividad con textos grandes y lectura instantánea."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Asistente",
        subtitulo="Chat de Productividad",
        tipo_mockup=tipo_mockup
    )

    # Tipografías Mobile-First escaladas (20px - 26px)
    f_tit_26 = obtener_fuente(26, bold=True)
    f_bold_22 = obtener_fuente(22, bold=True)
    f_reg_21 = obtener_fuente(21, bold=False)
    f_btn_21 = obtener_fuente(21, bold=True)

    cur_y = iy + 4

    # 1. PEDIDO DEL USUARIO (Tarjeta superior destacada)
    h_user = 110
    draw.rounded_rectangle(
        [ix, cur_y, ix + iw, cur_y + h_user],
        radius=12,
        fill=(248, 250, 252),
        outline=(203, 213, 225),
        width=2
    )

    # Tag de Usuario
    draw.rounded_rectangle([ix + 20, cur_y + 14, ix + 85, cur_y + 44], radius=6, fill=(226, 232, 240))
    draw.text((ix + 30, cur_y + 18), "Vos", fill=(51, 65, 85), font=f_bold_22)

    draw.text(
        (ix + 100, cur_y + 16),
        "Leé este correo y armame un borrador confirmando la entrega del viernes:",
        fill=(15, 23, 42),
        font=f_reg_21
    )

    # Cita destacada del mail
    draw.rounded_rectangle([ix + 20, cur_y + 54, ix + iw - 20, cur_y + 96], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((ix + 34, cur_y + 64), "• Adjunto el cronograma revisado con acuerdo en tarifas para el viernes.", fill=(100, 116, 139), font=f_reg_21)

    cur_y += h_user + 14

    # 2. PUNTOS CLAVE EXTRAÍDOS (Aparece en etapa >= 1)
    if etapa >= 1:
        h_pts = 126
        draw.rounded_rectangle(
            [ix, cur_y, ix + iw, cur_y + h_pts],
            radius=12,
            fill=(240, 249, 255),
            outline=(14, 165, 233),
            width=2
        )

        dibujar_chispa_ia(draw, ix + 28, cur_y + 26, 8, (14, 165, 233))
        draw.text((ix + 46, cur_y + 14), "Puntos clave extraídos:", fill=(3, 105, 161), font=f_bold_22)

        # Check 1
        dibujar_icono_check(draw, ix + 28, cur_y + 54, (14, 165, 233), tam=16, grosor=3)
        draw.text((ix + 54, cur_y + 50), "Propuesta y tarifas aprobadas", fill=(15, 23, 42), font=f_bold_22)

        # Check 2
        dibujar_icono_check(draw, ix + 28, cur_y + 88, (14, 165, 233), tam=16, grosor=3)
        draw.text((ix + 54, cur_y + 84), "Entrega confirmada para el viernes", fill=(15, 23, 42), font=f_bold_22)

        cur_y += h_pts + 14

    # 3. BORRADOR DE RESPUESTA LISTO (Aparece en etapa >= 2)
    if etapa >= 2:
        h_draft = ih - (cur_y - iy)
        draw.rounded_rectangle(
            [ix, cur_y, ix + iw, cur_y + h_draft],
            radius=12,
            fill=(255, 255, 255),
            outline=(16, 185, 129),
            width=2
        )

        dibujar_chispa_ia(draw, ix + 28, cur_y + 26, 8, (16, 185, 129))
        draw.text((ix + 46, cur_y + 14), "Borrador de respuesta listo:", fill=(5, 150, 105), font=f_bold_22)

        txt_res = "Hola Lucas, confirmamos la entrega para este viernes en el horario acordado."
        draw.text((ix + 28, cur_y + 50), txt_res, fill=(15, 23, 42), font=f_bold_22)

        # Botón Copiar respuesta
        btn_w = 260
        btn_h = 44
        btn_x = ix + iw - btn_w - 20
        btn_y = cur_y + h_draft - btn_h - 16
        draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=8, fill=(16, 185, 129))
        dibujar_icono_check(draw, btn_x + 20, btn_y + 14, (255, 255, 255), tam=16, grosor=3)
        draw.text((btn_x + 48, btn_y + 10), "Copiar respuesta", fill=(255, 255, 255), font=f_btn_21)

    return img

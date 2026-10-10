"""
plantillas/presentaciones_problema.py
------------------------------------
Plantilla para Video 5 (Presentaciones):
Escena de Caos / Problema:
- Horas armando informes y diapositivas en blanco sin diseño.
- Mobile-First: Letras grandes (20px a 26px) y alto impacto visual.
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
    "Presentaciones",
    "Borrador de Informe",
    "Sin formato",
    "Diapositiva 1 de 15 (En blanco)",
    "Pegando datos de tablas dispersas...",
    "Alineando cajas de texto a mano...",
    "Buscando tipografías y colores...",
    "Horas invertidas sin avanzar",
    "Caos de formato"
]


def renderizar_frame(
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Renderiza el caos de armar diapositivas a mano."""
    etapa, p_etapa = evaluar_etapa_visual(
        tiempo_segundos,
        duracion_total=max(3.0, tiempo_segundos / max(0.01, progreso) if progreso > 0 else 6.0),
        num_etapas=3
    )

    img, draw, (ix, iy, iw, ih) = dibujar_ventana_base(
        ancho, alto,
        titulo="Presentaciones",
        subtitulo="Borrador de Informe",
        tipo_mockup=tipo_mockup
    )

    f_tit_26 = obtener_fuente(26, bold=True)
    f_sub_21 = obtener_fuente(21, bold=False)
    f_badge_19 = obtener_fuente(19, bold=True)

    # 1. Badge superior de advertencia
    chip_w = 200
    chip_h = 36
    chip_x = ancho - chip_w - 205
    chip_y = (66 - chip_h) // 2
    draw.rounded_rectangle([chip_x, chip_y, chip_x + chip_w, chip_y + chip_h], radius=8, fill=(254, 226, 226), outline=(244, 63, 94))
    draw.ellipse([chip_x + 14, chip_y + 13, chip_x + 24, chip_y + 23], fill=(225, 29, 72))
    draw.text((chip_x + 32, chip_y + 7), "Caos de formato", fill=(153, 27, 27), font=f_badge_19)

    cur_y = iy + 4

    # 2. Lienzo de Diapositiva en blanco (con guías desordenadas)
    h_slide = 160
    draw.rounded_rectangle(
        [ix, cur_y, ix + iw, cur_y + h_slide],
        radius=12,
        fill=(255, 255, 255),
        outline=(244, 63, 94) if etapa >= 1 else (226, 232, 240),
        width=2
    )

    # Header de la diapositiva vacía
    draw.rounded_rectangle([ix + 20, cur_y + 18, ix + 240, cur_y + 54], radius=6, fill=(254, 242, 242))
    draw.text((ix + 32, cur_y + 23), "Slide 1 de 15 • En blanco", fill=(225, 29, 72), font=f_badge_19)

    draw.text((ix + 20, cur_y + 70), "Pasás horas acomodando cuadros y buscando datos", fill=(15, 23, 42), font=f_tit_26)
    draw.text((ix + 20, cur_y + 110), "Textos desalineados, gráficos rotos y sin diseño", fill=(100, 116, 139), font=f_sub_21)

    cur_y += h_slide + 14

    # 3. Tarjetas de dolor / tareas manuales trabadas
    bloques_dolor = [
        ("Alineando cajas de texto a mano", "Más de 40 minutos ajustando fuentes y márgenes"),
        ("Pegando tablas y métricas dispersas", "Copiar y pegar números sin orden visual"),
    ]

    h_card = 100
    for idx_b, (tit_b, sub_b) in enumerate(bloques_dolor):
        ry = cur_y + idx_b * (h_card + 12)
        if ry + h_card > alto - 10:
            break

        resaltar = (etapa >= 1 and idx_b == 0) or (etapa >= 2 and idx_b == 1)
        bg_c = (255, 241, 242) if resaltar else (248, 250, 252)
        bd_c = (251, 113, 133) if resaltar else (226, 232, 240)

        draw.rounded_rectangle([ix, ry, ix + iw, ry + h_card], radius=12, fill=bg_c, outline=bd_c, width=2)
        draw.rounded_rectangle([ix, ry, ix + 8, ry + h_card], radius=4, fill=(225, 29, 72) if resaltar else (203, 213, 225))

        # Indicador de traba
        draw.ellipse([ix + 28, ry + (h_card - 32) // 2, ix + 60, ry + (h_card - 32) // 2 + 32], fill=(254, 226, 226) if resaltar else (241, 245, 249))
        draw.text((ix + 40, ry + 36), "!", fill=(225, 29, 72) if resaltar else (148, 163, 184), font=f_tit_26)

        draw.text((ix + 80, ry + 18), tit_b, fill=(15, 23, 42), font=f_tit_26)
        draw.text((ix + 80, ry + 54), sub_b, fill=(100, 116, 139), font=f_sub_21)

    return img

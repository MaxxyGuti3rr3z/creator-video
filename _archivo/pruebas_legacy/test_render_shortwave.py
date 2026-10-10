import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Optional, Tuple

import generar_animacion_solucion as gas

def dibujar_chispa_ia(draw: ImageDraw.Draw, x: int, y: int, tam: int, color: Tuple[int, ...]):
    """Dibuja una estrella / chispa vectorial de 4 puntas estilo IA."""
    puntos = [
        (x, y - tam),
        (x + int(tam * 0.28), y - int(tam * 0.28)),
        (x + tam, y),
        (x + int(tam * 0.28), y + int(tam * 0.28)),
        (x, y + tam),
        (x - int(tam * 0.28), y + int(tam * 0.28)),
        (x - tam, y),
        (x - int(tam * 0.28), y - int(tam * 0.28)),
    ]
    draw.polygon(puntos, fill=color)

def dibujar_rayo(draw: ImageDraw.Draw, x: int, y: int, tam: int, color: Tuple[int, ...]):
    """Dibuja un rayo / flash vectorial."""
    puntos = [
        (x + int(tam * 0.2), y - tam),
        (x - int(tam * 0.5), y),
        (x, y),
        (x - int(tam * 0.2), y + tam),
        (x + int(tam * 0.5), y),
        (x, y),
    ]
    draw.polygon(puntos, fill=color)


def renderizar_frame_lectura_shortwave(
    ancho: int = 940,
    alto: int = 700,
    cursor_pos: Optional[Tuple[int, int]] = None,
    cursor_ripple: int = 0,
    boton_ia_activo: bool = False,
    panel_resumen_progreso: float = 0.0,
    borrador_progreso: float = 0.0,
    btn_enviar_activo: bool = False
) -> Image.Image:
    """
    Renderiza la vista de lectura de correo y resumen inteligente de Shortwave:
    - Lectura de correo realista de Martín Rossi con dudas sobre plazos/servidores.
    - Botón de acción 'Resumir con IA' con hover/click interactivo.
    - Panel de resumen IA con 3 viñetas clave desplegadas dinámicamente.
    - Tarjeta de borrador automático con tono natural empático y chip de confirmación.
    """
    img = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    scale = max(1.0, ancho / 560.0)

    f_top = gas.obtener_fuente(int(13 * scale), bold=True)
    f_asunto = gas.obtener_fuente(int(14.5 * scale), bold=True)
    f_btn_ia = gas.obtener_fuente(int(11.5 * scale), bold=True)
    f_remitente = gas.obtener_fuente(int(13 * scale), bold=True)
    f_subrem = gas.obtener_fuente(int(10.5 * scale), bold=False)
    f_cuerpo = gas.obtener_fuente(int(11 * scale), bold=False)
    f_card_title = gas.obtener_fuente(int(12 * scale), bold=True)
    f_bullet = gas.obtener_fuente(int(11 * scale), bold=False)
    f_bullet_bold = gas.obtener_fuente(int(11 * scale), bold=True)
    f_pill = gas.obtener_fuente(int(10 * scale), bold=True)
    f_draft_text = gas.obtener_fuente(int(11.5 * scale), bold=False)

    radio_v = int(18 * scale)

    # 1. Contenedor Ventana (Fondo blanco #FFFFFF, esquinas redondeadas)
    draw.rounded_rectangle(
        [0, 0, ancho - 1, alto - 1],
        radius=radio_v,
        fill=(255, 255, 255, 255),
        outline=(203, 213, 225, 255),
        width=max(2, int(2 * scale))
    )

    # 2. Barra Superior (#F8FAFC)
    h_top = int(44 * scale)
    mask_top = Image.new("L", (ancho, h_top), 0)
    d_top_mask = ImageDraw.Draw(mask_top)
    d_top_mask.rounded_rectangle([0, 0, ancho - 1, alto - 1], radius=radio_v, fill=255)
    top_bar = Image.new("RGBA", (ancho, h_top), (248, 250, 252, 255))
    img.paste(top_bar, (0, 0), mask_top)
    draw.line([(0, h_top), (ancho, h_top)], fill=(226, 232, 240, 255), width=max(1, int(1 * scale)))

    # Puntos decorativos estilo Byte
    dot_y = h_top // 2
    r_dot = int(4.5 * scale)
    draw.ellipse([int(16 * scale) - r_dot, dot_y - r_dot, int(16 * scale) + r_dot, dot_y + r_dot], fill=(255, 111, 97, 220))
    draw.ellipse([int(32 * scale) - r_dot, dot_y - r_dot, int(32 * scale) + r_dot, dot_y + r_dot], fill=(240, 196, 70, 220))
    draw.ellipse([int(48 * scale) - r_dot, dot_y - r_dot, int(48 * scale) + r_dot, dot_y + r_dot], fill=(0, 229, 255, 220))

    # Título MailFlow • Correo
    draw.text((int(70 * scale), dot_y - int(10 * scale)), "MailFlow", fill=(15, 23, 42, 255), font=f_top)
    draw.text((int(145 * scale), dot_y - int(10 * scale)), "•  Bandeja de Entrada  >  Mensaje", fill=(100, 116, 139, 255), font=f_subrem)

    # Pill derecha: Prioridad / Proyecto
    badge_w = int(105 * scale)
    badge_h = int(22 * scale)
    badge_x0 = ancho - badge_w - int(16 * scale)
    draw.rounded_rectangle([badge_x0, dot_y - badge_h // 2, badge_x0 + badge_w, dot_y + badge_h // 2], radius=int(6 * scale), fill=(238, 242, 255, 255), outline=(199, 210, 254, 255), width=1)
    draw.text((badge_x0 + int(12 * scale), dot_y - int(8 * scale)), "Proyecto Q3", fill=(67, 56, 202, 255), font=f_pill)

    # 3. Sub-barra: Asunto grande y Botón de Resumen con IA
    h_sub = int(48 * scale)
    y_sub = h_top
    draw.rectangle([0, y_sub, ancho, y_sub + h_sub], fill=(255, 255, 255, 255))
    draw.line([(0, y_sub + h_sub), (ancho, y_sub + h_sub)], fill=(241, 245, 249, 255), width=max(1, int(1 * scale)))

    # Asunto destacado
    draw.text((int(20 * scale), y_sub + int(12 * scale)), "Propuesta técnica de API y servidores", fill=(15, 23, 42, 255), font=f_asunto)

    # Botón 'Resumir con IA' en la esquina derecha
    btn_w = int(160 * scale)
    btn_h = int(32 * scale)
    btn_x0 = ancho - btn_w - int(16 * scale)
    btn_y0 = y_sub + (h_sub - btn_h) // 2

    if boton_ia_activo:
        btn_bg = (0, 229, 255, 255)
        btn_border = (0, 180, 216, 255)
        btn_fg = (15, 23, 42, 255)
    else:
        btn_bg = (248, 250, 252, 255)
        btn_border = (203, 213, 225, 255)
        btn_fg = (30, 41, 59, 255)

    draw.rounded_rectangle([btn_x0, btn_y0, btn_x0 + btn_w, btn_y0 + btn_h], radius=int(8 * scale), fill=btn_bg, outline=btn_border, width=max(1, int(1.5 * scale)))
    dibujar_chispa_ia(draw, btn_x0 + int(18 * scale), btn_y0 + btn_h // 2, int(6 * scale), btn_fg)
    draw.text((btn_x0 + int(30 * scale), btn_y0 + int(6 * scale)), "Resumir con IA", fill=btn_fg, font=f_btn_ia)

    # 4. Bloque del Remitente (Avatar + Nombre + Fecha)
    y_rem = y_sub + h_sub + int(8 * scale)
    av_r = int(16 * scale)
    av_cx = int(36 * scale)
    av_cy = y_rem + av_r
    draw.ellipse([av_cx - av_r, av_cy - av_r, av_cx + av_r, av_cy + av_r], fill=(37, 99, 235, 255))
    draw.text((av_cx - int(6 * scale), av_cy - int(9 * scale)), "M", fill=(255, 255, 255, 255), font=f_top)

    draw.text((int(62 * scale), y_rem + int(1 * scale)), "Martín Rossi", fill=(15, 23, 42, 255), font=f_remitente)
    draw.text((int(150 * scale), y_rem + int(3 * scale)), "<martin@andescorp.com>", fill=(100, 116, 139, 255), font=f_subrem)
    draw.text((int(62 * scale), y_rem + int(18 * scale)), "Para: vos, equipo-dev@startup.io  •  Hoy, 10:45 AM", fill=(148, 163, 184, 255), font=f_subrem)

    draw.line([(int(20 * scale), y_rem + int(38 * scale)), (ancho - int(20 * scale), y_rem + int(38 * scale))], fill=(241, 245, 249, 255), width=1)

    # Si borrador_progreso es alto, contraemos suavemente el cuerpo para dar lugar al borrador
    cuerpo_opacidad = max(0.2, 1.0 - 0.7 * borrador_progreso)
    y_cuerpo = y_rem + int(46 * scale)

    # 5. Cuerpo del correo original
    if borrador_progreso < 0.95:
        linea1 = "Hola equipo, estuvimos analizando la propuesta para integrar la API de Shortwave en Q3."
        linea2 = "La arquitectura es viable, pero preocupan los plazos y el costo de servidores dedicados."
        linea3 = "¿Podrían enviarnos el desglose detallado y coordinamos una llamada de 20 minutos mañana?"

        c_col = (int(51 * cuerpo_opacidad + 255 * (1 - cuerpo_opacidad)),
                 int(65 * cuerpo_opacidad + 255 * (1 - cuerpo_opacidad)),
                 int(85 * cuerpo_opacidad + 255 * (1 - cuerpo_opacidad)), 255)

        draw.text((int(22 * scale), y_cuerpo), linea1, fill=c_col, font=f_cuerpo)
        draw.text((int(22 * scale), y_cuerpo + int(18 * scale)), linea2, fill=c_col, font=f_cuerpo)
        draw.text((int(22 * scale), y_cuerpo + int(36 * scale)), linea3, fill=c_col, font=f_cuerpo)

    # 6. Panel de Resumen Inteligente de Shortwave
    if panel_resumen_progreso > 0.05:
        p = min(1.0, panel_resumen_progreso)
        p_card_x0 = int(18 * scale)
        p_card_w = ancho - 2 * p_card_x0
        
        # Desplazamiento dinámico si entra el borrador
        if borrador_progreso > 0.0:
            p_card_y0 = y_cuerpo + int(58 * scale) - int(38 * scale * borrador_progreso)
            p_card_h = int(162 * scale)
        else:
            p_card_y0 = y_cuerpo + int(60 * scale)
            p_card_h = int(166 * scale)

        # Marco con fondo cyan muy claro y borde cyan brillante
        draw.rounded_rectangle(
            [p_card_x0, p_card_y0, p_card_x0 + p_card_w, p_card_y0 + p_card_h],
            radius=int(12 * scale),
            fill=(240, 253, 250, 255),
            outline=(0, 229, 255, 255),
            width=max(2, int(2 * scale))
        )

        # Header del panel de IA
        dibujar_chispa_ia(draw, p_card_x0 + int(24 * scale), p_card_y0 + int(20 * scale), int(6 * scale), (0, 180, 216))
        draw.text((p_card_x0 + int(36 * scale), p_card_y0 + int(11 * scale)), "Resumen Inteligente (Shortwave AI)", fill=(15, 23, 42, 255), font=f_card_title)
        
        # Badge verde "Listo en 0.4s"
        chip_w = int(130 * scale)
        chip_h = int(22 * scale)
        chip_x0 = p_card_x0 + p_card_w - chip_w - int(14 * scale)
        chip_y0 = p_card_y0 + int(10 * scale)
        draw.rounded_rectangle([chip_x0, chip_y0, chip_x0 + chip_w, chip_y0 + chip_h], radius=int(6 * scale), fill=(220, 252, 231, 255), outline=(134, 239, 172, 255), width=1)
        gas.dibujar_icono_check(draw, chip_x0 + int(10 * scale), chip_y0 + int(6 * scale), (22, 101, 52), tam=int(10 * scale), grosor=2)
        draw.text((chip_x0 + int(26 * scale), chip_y0 + int(3 * scale)), "Listo en 0.4s", fill=(22, 101, 52, 255), font=f_pill)

        # Viñetas de resumen
        bullets = [
            ("•", (16, 185, 129), "Arquitectura viable:", " Propuesta técnica aceptada por el cliente."),
            ("•", (245, 158, 11), "Puntos de atención:", " Plazo límite en octubre y costo de servidores."),
            ("•", (0, 229, 255), "Acción requerida:", " Enviar desglose de costos y agendar llamada de 20 min."),
        ]

        b_y = p_card_y0 + int(42 * scale)
        for i, (sym, sym_col, b_title, b_desc) in enumerate(bullets):
            if p >= (i + 1) * 0.28:
                draw.text((p_card_x0 + int(16 * scale), b_y), sym, fill=sym_col, font=f_bullet_bold)
                draw.text((p_card_x0 + int(30 * scale), b_y), b_title, fill=(15, 23, 42, 255), font=f_bullet_bold)
                bbox_bt = draw.textbbox((0, 0), b_title, font=f_bullet_bold)
                tw_bt = bbox_bt[2] - bbox_bt[0]
                draw.text((p_card_x0 + int(30 * scale) + tw_bt, b_y), b_desc, fill=(71, 85, 105, 255), font=f_bullet)
            b_y += int(33 * scale)

    # 7. Tarjeta de Borrador Automático (Aparece con borrador_progreso)
    if borrador_progreso > 0.05:
        p_d = min(1.0, borrador_progreso)
        d_x0 = int(18 * scale)
        d_w = ancho - 2 * d_x0
        d_y0 = p_card_y0 + p_card_h + int(12 * scale)
        d_h = alto - d_y0 - int(16 * scale)

        # Marco blanco con borde cyan brillante y fondo blanco puro
        draw.rounded_rectangle(
            [d_x0, d_y0, d_x0 + d_w, d_y0 + d_h],
            radius=int(12 * scale),
            fill=(255, 255, 255, 255),
            outline=(0, 229, 255, 255),
            width=max(2, int(2 * scale))
        )

        # Header del borrador
        dibujar_rayo(draw, d_x0 + int(24 * scale), d_y0 + int(18 * scale), int(7 * scale), (2, 132, 199))
        draw.text((d_x0 + int(36 * scale), d_y0 + int(10 * scale)), "Borrador Automático (Shortwave Draft)", fill=(15, 23, 42, 255), font=f_card_title)

        # Chip 'Tono natural, no robótico ✓'
        chip_d_w = int(195 * scale)
        chip_d_h = int(22 * scale)
        chip_dx0 = d_x0 + d_w - chip_d_w - int(14 * scale)
        chip_dy0 = d_y0 + int(9 * scale)
        draw.rounded_rectangle([chip_dx0, chip_dy0, chip_dx0 + chip_d_w, chip_dy0 + chip_d_h], radius=int(6 * scale), fill=(240, 253, 244, 255), outline=(187, 247, 208, 255), width=1)
        gas.dibujar_icono_check(draw, chip_dx0 + int(10 * scale), chip_dy0 + int(6 * scale), (22, 101, 52), tam=int(10 * scale), grosor=2)
        draw.text((chip_dx0 + int(26 * scale), chip_dy0 + int(3 * scale)), "Tono natural, no robótico", fill=(22, 101, 52, 255), font=f_pill)

        # Texto del borrador generado
        txt_b1 = "“¡Hola Martín! Totalmente de acuerdo con los puntos."
        txt_b2 = "Ya te preparé el desglose de servidores para que lo veas claro."
        txt_b3 = "¿Te queda bien vernos mañana a las 10:30? Abrazo.”"

        d_txt_y = d_y0 + int(38 * scale)
        draw.text((d_x0 + int(18 * scale), d_txt_y), txt_b1, fill=(15, 23, 42, 255), font=f_draft_text)
        draw.text((d_x0 + int(18 * scale), d_txt_y + int(20 * scale)), txt_b2, fill=(15, 23, 42, 255), font=f_draft_text)
        draw.text((d_x0 + int(18 * scale), d_txt_y + int(40 * scale)), txt_b3, fill=(15, 23, 42, 255), font=f_draft_text)

        # Botón Enviar Borrador
        b_send_w = int(160 * scale)
        b_send_h = int(30 * scale)
        b_send_x0 = d_x0 + d_w - b_send_w - int(16 * scale)
        b_send_y0 = d_y0 + d_h - b_send_h - int(12 * scale)

        if btn_enviar_activo:
            b_col = (0, 229, 255, 255)
            b_txt = (15, 23, 42, 255)
        else:
            b_col = (15, 23, 42, 255)
            b_txt = (255, 255, 255, 255)

        draw.rounded_rectangle([b_send_x0, b_send_y0, b_send_x0 + b_send_w, b_send_y0 + b_send_h], radius=int(6 * scale), fill=b_col)
        draw.text((b_send_x0 + int(16 * scale), b_send_y0 + int(6 * scale)), "Enviar Borrador  →", fill=b_txt, font=f_btn_ia)

    # 8. Cursor de mouse y ripple
    if cursor_pos is not None:
        gas.dibujar_cursor(draw, cursor_pos[0], cursor_pos[1], ripple_radio=cursor_ripple, escala=scale)

    return img


if __name__ == "__main__":
    out_dir = Path("test_shortwave_frames")
    out_dir.mkdir(exist_ok=True)

    # Frame 1: Leyendo correo, cursor entra
    f1 = renderizar_frame_lectura_shortwave(cursor_pos=(750, 70))
    f1.save(out_dir / "frame1_lectura.png")

    # Frame 2: Clic en 'Resumir con IA' con ripple
    f2 = renderizar_frame_lectura_shortwave(cursor_pos=(750, 70), cursor_ripple=18, boton_ia_activo=True)
    f2.save(out_dir / "frame2_click_ia.png")

    # Frame 3: Resumen desplegado
    f3 = renderizar_frame_lectura_shortwave(boton_ia_activo=True, panel_resumen_progreso=1.0)
    f3.save(out_dir / "frame3_resumen.png")

    # Frame 4: Borrador sugerido completo
    f4 = renderizar_frame_lectura_shortwave(
        boton_ia_activo=True,
        panel_resumen_progreso=1.0,
        borrador_progreso=1.0,
        btn_enviar_activo=True,
        cursor_pos=(800, 640),
        cursor_ripple=12
    )
    f4.save(out_dir / "frame4_borrador.png")

    print("Frames de prueba actualizados con vectores limpios y layout dinámico.")

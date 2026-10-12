"""
src.mockups.planos.arquetipos
---------------------------------------------------------------------------
Arquetipos cinematograficos base (compartidos por varios videos).
Codigo movido desde src/mockups/director_escena.py sin cambios de comportamiento.
"""

from typing import Dict, Any, Optional, Tuple, List, Union
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFilter

from src.mockups.motor import (
    obtener_fuente,
    dibujar_chispa_ia,
    dibujar_icono_check,
    dibujar_ventana_base,
    generar_fondo_tech_base,
)
from src.mockups.estilos.animaciones_fondo import obtener_lienzo_dinamico_fondo
from src.rutas import DIR_BYTE_TRANSPARENTES, DIR_BYTE_ILUSTRACIONES

from src.mockups.planos.comunes import (
    dibujar_icono_alerta,
    dibujar_icono_cruz,
    dibujar_icono_candado,
    dibujar_icono_lupa,
)




# ---------------------------------------------------------------------------
# 1. PLANO_HERO_CAOS: Byte protagonista al frente con elementos desordenados
# ---------------------------------------------------------------------------
def renderizar_plano_hero_caos(
    ancho: int,
    alto: int,
    t_sec: float,
    duracion: float,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Byte en primer plano rodeado de elementos caóticos flotando sin ventanas de software."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.45)
    draw = ImageDraw.Draw(frame)

    f_tit = obtener_fuente(34, bold=True)
    f_sub = obtener_fuente(24, bold=False)
    f_badge = obtener_fuente(20, bold=True)

    # 1. Fondo con resplandor rojo de alerta
    prog = min(1.0, t_sec / max(0.01, duracion))
    pulso_alerta = 0.5 + 0.5 * math.sin(t_sec * 4.0)

    # Círculo radial de alerta
    r_glow = 480
    cx_glow = ancho // 2
    cy_glow = int(alto * 0.45)
    glow_img = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_glow = ImageDraw.Draw(glow_img)
    alpha_alerta = int(35 + 30 * pulso_alerta)
    d_glow.ellipse([cx_glow - r_glow, cy_glow - r_glow, cx_glow + r_glow, cy_glow + r_glow], fill=(225, 29, 72, alpha_alerta))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(80))
    frame = Image.alpha_composite(frame, glow_img)
    draw = ImageDraw.Draw(frame)

    cfg = config or {}
    badge_txt = cfg.get("badge", "CAOS DE INFORMES Y SLIDES")

    # 2. Elementos temáticos de dolor flotando (solo franja y=250..780, x=100..980)
    elementos = cfg.get("elementos", [
        {"x": 100, "y": 330, "w": 300, "h": 150, "rot": -10, "tit": "Slide 1 • En blanco", "sub": "Falta formato", "col": (225, 29, 72)},
        {"x": 650, "y": 330, "w": 310, "h": 150, "rot": 12, "tit": "Slide 2 • Datos rotos", "sub": "Tablas desalineadas", "col": (225, 29, 72)},
        {"x": 100, "y": 600, "w": 330, "h": 150, "rot": 7, "tit": "Métricas Q3", "sub": "Sin orden visual", "col": (245, 158, 11)},
        {"x": 650, "y": 600, "w": 330, "h": 150, "rot": -7, "tit": "Borrador interminable", "sub": "Horas perdidas", "col": (225, 29, 72)},
    ])

    for it in elementos:
        # Movimiento flotante senoidal
        drift_y = int(8 * math.sin(t_sec * 2.0 + it["rot"]))
        el_img = Image.new("RGBA", (it["w"], it["h"]), (0, 0, 0, 0))
        d_el = ImageDraw.Draw(el_img)
        d_el.rounded_rectangle([0, 0, it["w"], it["h"]], radius=14, fill=(255, 241, 242, 240), outline=it["col"], width=2)
        d_el.text((18, 16), it["tit"], fill=(15, 23, 42), font=obtener_fuente(28, bold=True))
        d_el.text((18, 56), it["sub"], fill=it["col"], font=obtener_fuente(22, bold=False))
        # Líneas simuladas de texto roto
        d_el.line([(18, 100), (it["w"] - 20, 100)], fill=(251, 113, 133), width=3)
        d_el.line([(18, 120), (it["w"] - 60, 120)], fill=(254, 205, 211), width=3)

        el_rot = el_img.rotate(it["rot"], resample=Image.Resampling.BILINEAR, expand=True)
        frame.paste(el_rot, (it["x"], it["y"] + drift_y), el_rot)

    # 3. Título de Alerta Superior (inicia en y=250, zona muerta 0..240 vacía)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=f_badge)
    alerta_w = max(420, bbox_b[2] - bbox_b[0] + 90)
    alerta_h = 52
    ax = (ancho - alerta_w) // 2
    ay = 250
    draw.rounded_rectangle([ax, ay, ax + alerta_w, ay + alerta_h], radius=26, fill=(225, 29, 72, 235), outline=(254, 205, 211), width=2)
    # Icono de alerta !
    draw.ellipse([ax + 18, ay + 12, ax + 46, ay + 40], fill=(255, 255, 255))
    draw.text((ax + 28, ay + 13), "!", fill=(225, 29, 72), font=obtener_fuente(20, bold=True))
    draw.text((ax + 58, ay + 13), badge_txt, fill=(255, 255, 255), font=f_badge)

    # 4. Byte Protagonista en la Zona Superior (y: 380 a 880, dejando libre 900..1160 para subtítulos)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        for cand in ["hook_guion_07_transparente.png", "escena_problema_guion_06_transparente.png", "escena_problema_guion_05_transparente.png"]:
            if (DIR_BYTE_TRANSPARENTES / cand).exists():
                p_byte = DIR_BYTE_TRANSPARENTES / cand
                break

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_rgba = img_b.convert("RGBA")
            bbox = b_rgba.getbbox()
            if bbox:
                b_rgba = b_rgba.crop(bbox)
            bw = 540
            aspect = b_rgba.height / max(1, b_rgba.width)
            bh = int(bw * aspect)
            if bh > 540:
                bh = 540
                bw = int(bh / aspect)
            b_resized = b_rgba.resize((bw, bh), Image.Resampling.LANCZOS)
            # Pequeño temblor (shake) de estrés en segundos 0 a 3
            shake_x = int(4 * math.sin(t_sec * 25.0)) if t_sec < 3.0 else 0
            bx = (ancho - bw) // 2 + shake_x
            by = 400
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 2. PLANO_SHOWCASE_PANORAMICO: Gran diapositiva + Byte comentarista lateral
# ---------------------------------------------------------------------------
def renderizar_plano_showcase_panoramico(
    ancho: int,
    alto: int,
    t_sec: float,
    duracion: float,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """La diapositiva generada ocupa casi toda la pantalla y Byte aparece en la esquina."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.45)
    draw = ImageDraw.Draw(frame)

    # 1. Gran Contenedor Panorámico Showcase (franja y=250..780, ancho 880 centrado)
    sw = 880
    sh = 530
    sx = (ancho - sw) // 2
    sy = 250

    # Sombra del showcase
    sombra = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_s = ImageDraw.Draw(sombra)
    d_s.rounded_rectangle([sx + 8, sy + 14, sx + sw - 8, sy + sh + 8], radius=24, fill=(14, 165, 233, 60))
    sombra = sombra.filter(ImageFilter.GaussianBlur(24))
    frame = Image.alpha_composite(frame, sombra)
    draw = ImageDraw.Draw(frame)

    cfg = config or {}
    header_txt = cfg.get("header", "Gamma • Presentación generada desde una idea")
    badge_txt = cfg.get("badge", "⚡ Generación IA")
    tit_principal = cfg.get("titulo", "Estrategia Q3: Crecimiento y Resultados")
    sub_principal = cfg.get("subtitulo", "Estructura completa de informe armada en 10 segundos sin tocar plantillas")
    items_showcase = cfg.get("items", [
        ("01 • Objetivos", "Alineación de equipo y metas claras", (37, 99, 235), (239, 246, 255)),
        ("02 • Métricas", "Gráficos de ventas y retención ordenados", (5, 150, 105), (236, 253, 245)),
        ("03 • Próximos Pasos", "Cronograma de entregas confirmado", (124, 58, 237), (245, 243, 255))
    ])
    footer_txt = cfg.get("footer", "Diapositivas listas para exponer en un clic")

    # Tarjeta Diapositiva Principal
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=24, fill=(255, 255, 255, 255), outline=(14, 165, 233), width=3)

    # Barra superior de la diapositiva en Gamma
    h_bar = 70
    draw.rounded_rectangle([sx, sy, sx + sw, sy + h_bar], radius=24, fill=(240, 249, 255))
    draw.line([(sx, sy + h_bar), (sx + sw, sy + h_bar)], fill=(186, 230, 253), width=2)

    dibujar_chispa_ia(draw, sx + 32, sy + 35, 10, (14, 165, 233))
    draw.text((sx + 54, sy + 22), header_txt, fill=(3, 105, 161), font=obtener_fuente(24, bold=True))

    # Badge de estado a la derecha
    bbox_badge = draw.textbbox((0, 0), badge_txt, font=obtener_fuente(20, bold=True))
    bw_badge = bbox_badge[2] - bbox_badge[0] + 30
    draw.rounded_rectangle([sx + sw - bw_badge - 20, sy + 16, sx + sw - 20, sy + 54], radius=8, fill=(224, 242, 254))
    draw.text((sx + sw - bw_badge - 5, sy + 24), badge_txt, fill=(2, 132, 199), font=obtener_fuente(20, bold=True))

    # Contenido de la Diapositiva Ejecutiva
    draw.text((sx + 36, sy + 105), tit_principal, fill=(15, 23, 42), font=obtener_fuente(30, bold=True))
    draw.text((sx + 36, sy + 155), sub_principal, fill=(100, 116, 139), font=obtener_fuente(24, bold=False))

    # 3 Tarjetas de contenido con métricas visuales dentro de la slide
    w_card = (sw - 72 - 32) // max(1, len(items_showcase))
    h_card = 190
    y_cards = sy + 220

    for i, (tit_c, desc_c, col_c, bg_c) in enumerate(items_showcase):
        cx0 = sx + 36 + i * (w_card + 16)
        cx1 = cx0 + w_card
        draw.rounded_rectangle([cx0, y_cards, cx1, y_cards + h_card], radius=14, fill=bg_c, outline=(*col_c[:3], 90), width=2)
        draw.rounded_rectangle([cx0, y_cards, cx0 + 8, y_cards + h_card], radius=4, fill=col_c)
        draw.text((cx0 + 20, y_cards + 26), tit_c, fill=col_c, font=obtener_fuente(23, bold=True))
        # Descripción
        palabras = desc_c.split(" ")
        l1 = " ".join(palabras[:3])
        l2 = " ".join(palabras[3:])
        draw.text((cx0 + 20, y_cards + 75), l1, fill=(30, 41, 59), font=obtener_fuente(21, bold=False))
        if l2:
            draw.text((cx0 + 20, y_cards + 108), l2, fill=(30, 41, 59), font=obtener_fuente(21, bold=False))

    # Barra de confirmación inferior de la diapositiva
    draw.rounded_rectangle([sx + 36, sy + sh - 90, sx + sw - 36, sy + sh - 30], radius=10, fill=(240, 249, 255), outline=(186, 230, 253))
    dibujar_icono_check(draw, sx + 56, sy + sh - 68, (14, 165, 233), tam=18, grosor=3)
    draw.text((sx + 88, sy + sh - 72), footer_txt, fill=(3, 105, 161), font=obtener_fuente(22, bold=True))

    # 2. Byte Comentarista / Streamer en la esquina inferior derecha
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        for cand in ["punto_1_guion_06_transparente.png", "punto_1_guion_05_transparente.png", "punto_1_guion_04_transparente.png"]:
            if (DIR_BYTE_TRANSPARENTES / cand).exists():
                p_byte = DIR_BYTE_TRANSPARENTES / cand
                break

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_rgba = img_b.convert("RGBA")
            bw, bh = 420, 420
            b_rgba = b_rgba.resize((bw, bh), Image.Resampling.LANCZOS)
            # Abajo a la derecha con base en y=1650 (zona sagrada de Byte)
            bx = ancho - bw - 100
            by = 1650 - bh
            frame.paste(b_rgba, (bx, by), b_rgba)

    return frame


# ---------------------------------------------------------------------------
# 3. PLANO_SPLIT_BEFORE_AFTER: Comparativa Antes vs. Después (Glow-Up Canva)
# ---------------------------------------------------------------------------
def renderizar_plano_split_before_after(
    ancho: int,
    alto: int,
    t_sec: float,
    duracion: float,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Pantalla dividida dinámica: Antes (aburrido) vs Después (pulido con IA)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.45)
    draw = ImageDraw.Draw(frame)

    f_tit = obtener_fuente(26, bold=True)
    f_badge = obtener_fuente(22, bold=True)

    cfg = config or {}
    antes_tag = cfg.get("antes_tag", "ANTES")
    antes_tit = cfg.get("antes_tit", "Diseño manual plano y desordenado")
    antes_items = cfg.get("antes_items", [
        "• Tipografías genéricas sin jerarquía",
        "• Colores apagados que no retienen la atención",
        "• Formato rígido que cuesta leer"
    ])
    separador_txt = cfg.get("separador", "CANVA MAGIC AI")
    despues_tag = cfg.get("despues_tag", "DESPUÉS")
    despues_tit = cfg.get("despues_tit", "Pulido estético profesional")
    pills_despues = cfg.get("pills_despues", [
        ("Paleta de Marca", "Colores armónicos automáticos", (124, 58, 237), (245, 243, 255)),
        ("Jerarquía Visual", "Tipografía moderna que impacta", (14, 165, 233), (240, 249, 255)),
        ("Presentación Lista", "Material impecable para proyectar", (16, 185, 129), (236, 253, 245)),
    ])

    # 1. Dos Tarjetas Gigantes Comparativas (Arriba: Antes / Abajo: Después) — franja y=250..780
    card_w = 880
    card_x = (ancho - card_w) // 2

    # TARJETA 1 (ANTES - Manual / Plano)
    y_antes = 250
    h_antes = 210
    draw.rounded_rectangle([card_x, y_antes, card_x + card_w, y_antes + h_antes], radius=18, fill=(241, 245, 249), outline=(203, 213, 225), width=2)
    # Tag 'ANTES'
    bbox_at = draw.textbbox((0, 0), antes_tag, font=f_badge)
    at_w = bbox_at[2] - bbox_at[0] + 32
    draw.rounded_rectangle([card_x + 24, y_antes + 20, card_x + 24 + at_w, y_antes + 60], radius=8, fill=(226, 232, 240))
    draw.text((card_x + 40, y_antes + 26), antes_tag, fill=(100, 116, 139), font=f_badge)
    draw.text((card_x + 40 + at_w + 14, y_antes + 26), antes_tit, fill=(71, 85, 105), font=f_tit)

    for idx_it, it_txt in enumerate(antes_items[:3]):
        draw.text((card_x + 30, y_antes + 90 + idx_it * 45), it_txt, fill=(100, 116, 139), font=obtener_fuente(22, bold=False))

    # SEPARADOR CON CHISPA IA
    y_sep = y_antes + h_antes + 16
    draw.line([(card_x, y_sep + 12), (card_x + card_w, y_sep + 12)], fill=(147, 51, 234), width=2)
    bbox_sep = draw.textbbox((0, 0), separador_txt, font=obtener_fuente(18, bold=True))
    sep_w = bbox_sep[2] - bbox_sep[0] + 70
    draw.rounded_rectangle([ancho // 2 - sep_w // 2, y_sep - 6, ancho // 2 + sep_w // 2, y_sep + 30], radius=18, fill=(147, 51, 234))
    dibujar_chispa_ia(draw, ancho // 2 - sep_w // 2 + 20, y_sep + 12, 8, (255, 255, 255))
    draw.text((ancho // 2 - sep_w // 2 + 40, y_sep + 2), separador_txt, fill=(255, 255, 255), font=obtener_fuente(18, bold=True))

    # TARJETA 2 (DESPUÉS - Glow-Up con IA)
    y_despues = y_sep + 46
    h_despues = 258
    draw.rounded_rectangle([card_x, y_despues, card_x + card_w, y_despues + h_despues], radius=18, fill=(255, 255, 255), outline=(147, 51, 234), width=3)
    # Tag 'DESPUÉS'
    bbox_dt = draw.textbbox((0, 0), despues_tag, font=f_badge)
    dt_w = bbox_dt[2] - bbox_dt[0] + 32
    draw.rounded_rectangle([card_x + 24, y_despues + 20, card_x + 24 + dt_w, y_despues + 64], radius=8, fill=(245, 243, 255), outline=(147, 51, 234))
    draw.text((card_x + 40, y_despues + 28), despues_tag, fill=(124, 58, 237), font=f_badge)
    draw.text((card_x + 40 + dt_w + 14, y_despues + 28), despues_tit, fill=(15, 23, 42), font=f_tit)

    # Badges de Glow-Up con iconos dibujados limpios
    for idx_p, (t_p, d_p, c_p, bg_p) in enumerate(pills_despues[:3]):
        py = y_despues + 80 + idx_p * 58
        draw.rounded_rectangle([card_x + 24, py, card_x + card_w - 24, py + 54], radius=10, fill=bg_p, outline=(*c_p[:3], 90), width=1)
        # Bullet / chispa
        dibujar_chispa_ia(draw, card_x + 46, py + 27, 7, c_p)
        f_tp = obtener_fuente(22, bold=True)
        bbox_tp = draw.textbbox((0, 0), t_p, font=f_tp)
        tp_w = bbox_tp[2] - bbox_tp[0]
        draw.text((card_x + 64, py + 14), t_p, fill=c_p, font=f_tp)
        desc_x = max(card_x + 330, card_x + 64 + tp_w + 18)
        draw.text((desc_x, py + 16), d_p, fill=(51, 65, 85), font=obtener_fuente(20, bold=False))

    # Byte en laptop en la parte inferior central
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        for cand in ["punto_2_guion_06_transparente.png", "punto_2_guion_05_transparente.png", "punto_2_guion_04_transparente.png"]:
            if (DIR_BYTE_TRANSPARENTES / cand).exists():
                p_byte = DIR_BYTE_TRANSPARENTES / cand
                break

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_rgba = img_b.convert("RGBA")
            bw, bh = 460, 460
            b_rgba = b_rgba.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            by = 1650 - bh
            frame.paste(b_rgba, (bx, by), b_rgba)

    return frame


# ---------------------------------------------------------------------------
# 4. PLANO_DECK_3D: Abanico de diapositivas terminadas + Byte Zen
# ---------------------------------------------------------------------------
def renderizar_plano_deck_3d(
    ancho: int,
    alto: int,
    t_sec: float,
    duracion: float,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Muro o abanico de diapositivas completas con sensación de victoria y alivio."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.45)
    draw = ImageDraw.Draw(frame)

    f_big = obtener_fuente(34, bold=True)
    f_sub = obtener_fuente(24, bold=False)
    f_badge = obtener_fuente(22, bold=True)

    # 1. Aura verde esmeralda en el fondo
    cx, cy = ancho // 2, int(alto * 0.45)
    r_aura = 420
    aura = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_aura = ImageDraw.Draw(aura)
    d_aura.ellipse([cx - r_aura, cy - r_aura, cx + r_aura, cy + r_aura], fill=(16, 185, 129, 45))
    aura = aura.filter(ImageFilter.GaussianBlur(80))
    frame = Image.alpha_composite(frame, aura)
    draw = ImageDraw.Draw(frame)

    # 2. Gran Badge Circular de Victoria (inicia en y=250, zona muerta vacía)
    r_circ = 46
    draw.ellipse([cx - r_circ - 10, 310 - r_circ - 10, cx + r_circ + 10, 310 + r_circ + 10], fill=(236, 253, 245))
    draw.ellipse([cx - r_circ, 310 - r_circ, cx + r_circ, 310 + r_circ], fill=(16, 185, 129))
    dibujar_icono_check(draw, cx - 18, 310 - 20, (255, 255, 255), tam=38, grosor=4)

    cfg = config or {}
    tit_txt = cfg.get("titulo", "¡Presentación 100% Lista!")
    sub_txt = cfg.get("subtitulo", "Material presentable, ordenado y visual para compartir")
    cards_deck = cfg.get("cards", [
        {"x_off": -180, "y": 500, "tit": "01 • Introducción", "rot": -7, "col": (37, 99, 235)},
        {"x_off": 180, "y": 500, "tit": "03 • Conclusiones", "rot": 7, "col": (124, 58, 237)},
        {"x_off": 0, "y": 480, "tit": "02 • Estrategia Q3", "rot": 0, "col": (16, 185, 129)},
    ])
    pills = cfg.get("pills", [("Presentable", (16, 185, 129)), ("Ordenado", (14, 165, 233)), ("Visual", (124, 58, 237))])

    # Títulos
    bbox_t = draw.textbbox((0, 0), tit_txt, font=f_big)
    tw = bbox_t[2] - bbox_t[0]
    draw.text((cx - tw // 2, 390), tit_txt, fill=(255, 255, 255), font=f_big)

    bbox_s = draw.textbbox((0, 0), sub_txt, font=f_sub)
    sw = bbox_s[2] - bbox_s[0]
    draw.text((cx - sw // 2, 440), sub_txt, fill=(167, 243, 208), font=f_sub)

    # 3. Muro / Abanico 3D de Diapositivas Terminadas
    dw, dh = 320, 200
    for cd in cards_deck:
        c_img = Image.new("RGBA", (dw, dh), (0, 0, 0, 0))
        d_cd = ImageDraw.Draw(c_img)
        d_cd.rounded_rectangle([0, 0, dw, dh], radius=14, fill=(255, 255, 255, 250), outline=cd["col"], width=3)
        d_cd.rounded_rectangle([0, 0, dw, 48], radius=14, fill=(248, 250, 252))
        d_cd.text((20, 14), cd["tit"], fill=(15, 23, 42), font=obtener_fuente(20, bold=True))
        # Contenido simulado
        d_cd.rounded_rectangle([18, 64, dw - 18, 120], radius=8, fill=(241, 245, 249))
        c_desc = cd.get("desc", "Diseño visual profesional")
        d_cd.text((26, 78), c_desc, fill=cd["col"], font=obtener_fuente(20, bold=True))
        dibujar_icono_check(d_cd, dw - 44, dh - 36, cd["col"], tam=16, grosor=3)

        c_rot = c_img.rotate(cd["rot"], resample=Image.Resampling.BILINEAR, expand=True)
        pos_x = cx + cd["x_off"] - c_rot.width // 2
        frame.paste(c_rot, (pos_x, cd["y"]), c_rot)

    # 4. Badges de Alivio Cualitativo al pie (y=720..772, dentro de la franja UI)
    pw = 260
    ph = 52
    y_p = 720
    gap_p = (880 - pw * 3) // 2
    start_x = (ancho - 880) // 2

    for i, (txt_p, col_p) in enumerate(pills[:3]):
        px = start_x + i * (pw + gap_p)
        draw.rounded_rectangle([px, y_p, px + pw, y_p + ph], radius=12, fill=(255, 255, 255), outline=col_p, width=2)
        dibujar_chispa_ia(draw, px + 24, y_p + 26, 8, col_p)
        draw.text((px + 44, y_p + 14), txt_p, fill=col_p, font=f_badge)

    # 5. Byte Zen Meditando
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        for cand in ["resultado_guion_06_transparente.png", "resultado_guion_05_transparente.png", "resultado_guion_04_transparente.png"]:
            if (DIR_BYTE_TRANSPARENTES / cand).exists():
                p_byte = DIR_BYTE_TRANSPARENTES / cand
                break

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_rgba = img_b.convert("RGBA")
            bw, bh = 510, 510
            b_rgba = b_rgba.resize((bw, bh), Image.Resampling.LANCZOS)
            # Levita suavemente con base en y=1650 (zona sagrada de Byte)
            flotacion = int(5 * math.sin(t_sec * 2.5))
            bx = (ancho - bw) // 2
            by = 1135 + flotacion
            frame.paste(b_rgba, (bx, by), b_rgba)

    return frame


# ---------------------------------------------------------------------------
# 5. PLANO_HOST_COMMUNITY: Byte host con stickers gigantes de encuesta
# ---------------------------------------------------------------------------
def renderizar_plano_host_community(
    ancho: int,
    alto: int,
    t_sec: float,
    duracion: float,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.45)
    draw = ImageDraw.Draw(frame)

    f_tit = obtener_fuente(32, bold=True)
    f_op = obtener_fuente(24, bold=True)
    f_badge = obtener_fuente(20, bold=True)

    cfg = config or {}
    pregunta_tit = cfg.get("pregunta_tit", "PREGUNTA A LA COMUNIDAD:")
    pregunta_l1 = cfg.get("pregunta_l1", "¿Cuál parte de tus informes")
    pregunta_l2 = cfg.get("pregunta_l2", "automatizarías primero?")
    opciones = cfg.get("opciones", [
        ("A", "Búsqueda y extracción de datos", (37, 99, 235), (239, 246, 255)),
        ("B", "Diseño y formateo de diapositivas", (124, 58, 237), (245, 243, 255)),
        ("C", "Redacción de resúmenes y notas", (16, 185, 129), (236, 253, 245)),
    ])
    txt_com = cfg.get("callout", "Dejámelo en los comentarios")

    # 1. Gran Pregunta Central Superior (Estilo Sticker de TikTok/Instagram) — inicia en y=250
    qw = 880
    qx = (ancho - qw) // 2
    qy = 250
    qh = 160
    draw.rounded_rectangle([qx, qy, qx + qw, qy + qh], radius=20, fill=(240, 249, 255), outline=(14, 165, 233), width=3)
    dibujar_chispa_ia(draw, qx + 36, qy + 36, 12, (14, 165, 233))
    draw.text((qx + 60, qy + 24), pregunta_tit, fill=(3, 105, 161), font=f_badge)
    draw.text((qx + 36, qy + 75), pregunta_l1, fill=(15, 23, 42), font=f_tit)
    draw.text((qx + 36, qy + 115), pregunta_l2, fill=(14, 165, 233), font=f_tit)

    ow = qw
    oh = 85
    start_oy = qy + qh + 24
    etapa = int(t_sec * 1.5) % max(1, len(opciones))

    for idx, opt in enumerate(opciones[:3]):
        letra = opt[0]
        texto_op = opt[1]
        col_op = opt[2] if len(opt) > 2 else (37, 99, 235)
        bg_op = opt[3] if len(opt) > 3 else (239, 246, 255)

        oy = start_oy + idx * (oh + 16)
        resaltar = (idx == etapa)
        bd_c = col_op if resaltar else (226, 232, 240)
        bg_c = bg_op if resaltar else (255, 255, 255)

        draw.rounded_rectangle([qx, oy, qx + ow, oy + oh], radius=16, fill=bg_c, outline=bd_c, width=3 if resaltar else 1)

        # Círculo de opción A / B / C
        draw.ellipse([qx + 24, oy + 16, qx + 76, oy + 68], fill=col_op)
        draw.text((qx + 40, oy + 26), letra, fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

        draw.text((qx + 95, oy + 28), texto_op, fill=(15, 23, 42), font=f_op)

    # 3. Byte Host saltando feliz abajo
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        for cand in ["cierre_guion_06_transparente.png", "cierre_guion_05_transparente.png", "cierre_guion_04_transparente.png"]:
            if (DIR_BYTE_TRANSPARENTES / cand).exists():
                p_byte = DIR_BYTE_TRANSPARENTES / cand
                break

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_rgba = img_b.convert("RGBA")
            bbox = b_rgba.getbbox()
            if bbox:
                b_rgba = b_rgba.crop(bbox)
            bw = 520
            aspect = b_rgba.height / max(1, b_rgba.width)
            bh = int(bw * aspect)
            if bh > 520:
                bh = 520
                bw = int(bh / aspect)
            b_resized = b_rgba.resize((bw, bh), Image.Resampling.LANCZOS)
            # Rebote alegre con base en y=1650 (zona sagrada de Byte)
            rebote = int(10 * abs(math.sin(t_sec * 3.0)))
            bx = (ancho - bw) // 2
            by = 1650 - bh - rebote
            frame.paste(b_resized, (bx, by), b_resized)

    # 4. Única píldora flotante de callout en y=790..860 (franja permitida)
    f_com = obtener_fuente(30, bold=True)
    bbox_com = draw.textbbox((0, 0), txt_com, font=f_com)
    cw = min(bbox_com[2] - bbox_com[0] + 120, 880)
    cx = (ancho - cw) // 2
    cy = 790
    draw.rounded_rectangle([cx, cy, cx + cw, cy + 70], radius=35, fill=(15, 23, 42, 245), outline=(14, 165, 233), width=2)
    dibujar_chispa_ia(draw, cx + 34, cy + 35, 10, (14, 165, 233))
    draw.text((cx + 70, cy + 17), txt_com, fill=(255, 255, 255), font=f_com)

    return frame


def renderizar_plano_panico_reloj(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 3.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.45)
    badge_txt = cfg.get("badge", "VIERNES • 17:59 HS")
    hora_txt = cfg.get("hora", "17:59")
    sub_reloj = cfg.get("sub_reloj", "TIEMPO LÍMITE: 1 MINUTO PARA EL CIERRE")

    # 1. Glow rojo de alerta en el fondo
    pulso_alerta = math.sin(t_sec * 8.0) * 0.5 + 0.5
    r_glow = 520
    cx_glow = ancho // 2
    cy_glow = 430
    glow_img = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_glow = ImageDraw.Draw(glow_img)
    alpha_alerta = int(45 + 35 * pulso_alerta)
    d_glow.ellipse([cx_glow - r_glow, cy_glow - r_glow, cx_glow + r_glow, cy_glow + r_glow], fill=(225, 29, 72, alpha_alerta))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(90))
    frame = Image.alpha_composite(frame, glow_img)
    draw = ImageDraw.Draw(frame)

    # 2. Badge superior de alerta (tipografía grande y clara)
    f_badge = obtener_fuente(24, bold=True)
    ax, ay, aw, ah = (ancho - 420) // 2, 80, 420, 56
    draw.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=28, fill=(225, 29, 72, 245), outline=(254, 205, 211), width=2)
    draw.ellipse([ax + 16, ay + 12, ax + 46, ay + 42], fill=(255, 255, 255))
    draw.text((ax + 27, ay + 14), "!", fill=(225, 29, 72), font=obtener_fuente(22, bold=True))
    draw.text((ax + 60, ay + 14), badge_txt, fill=(255, 255, 255), font=f_badge)

    # 3. Reloj digital de alta tensión
    cw, ch = 760, 210
    cx, cy = (ancho - cw) // 2, 160
    neon_col = (239, 68, 68) if pulso_alerta > 0.4 else (225, 29, 72)
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(17, 24, 39, 240), outline=neon_col, width=4)

    f_hora = obtener_fuente(106, bold=True)
    sec_blink = ":" if int(t_sec * 2.0) % 2 == 0 else " "
    hora_display = f"17{sec_blink}59"
    bbox_h = draw.textbbox((0, 0), hora_display, font=f_hora)
    hx = cx + (cw - (bbox_h[2] - bbox_h[0])) // 2
    draw.text((hx, cy + 24), hora_display, fill=(248, 113, 113), font=f_hora)

    f_sub = obtener_fuente(22, bold=True)
    bbox_s = draw.textbbox((0, 0), sub_reloj, font=f_sub)
    sx = cx + (cw - (bbox_s[2] - bbox_s[0])) // 2
    draw.text((sx, cy + 150), sub_reloj, fill=(254, 202, 202), font=f_sub)

    # 4. Byte Protagonista en el Centro Superior (Recortado al bbox real para máxima escala y presencia)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        for cand in ["cold_open_guion_07_transparente.png", "byte_cortocircuito_transparente.png"]:
            if (DIR_BYTE_TRANSPARENTES / cand).exists():
                p_byte = DIR_BYTE_TRANSPARENTES / cand
                break

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_rgba = img_b.convert("RGBA")
            bbox = b_rgba.getbbox()
            b_cropped = b_rgba.crop(bbox) if bbox else b_rgba
            aspect = b_cropped.width / b_cropped.height
            bh = 460
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            shake_x = int(4 * math.sin(t_sec * 28.0))
            bx = (ancho - bw) // 2 + shake_x
            by = 390
            frame.paste(b_resized, (bx, by), b_resized)

    # 5. ZONA CENTRAL DE SUBTÍTULOS: y = 880 a 1080 (100% LIBRE PARA SUBTÍTULOS KARAOKE)

    # 6. ZONA INFERIOR: Meme Windows Crash Dialog con tipografías GRANDES para móvil
    dw, dh = 860, 340
    dx, dy = (ancho - dw) // 2, 1100
    draw.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=18, fill=(255, 255, 255), outline=(203, 213, 225), width=3)
    # Barra de título de la ventana
    draw.rounded_rectangle([dx, dy, dx + dw, dy + 64], radius=18, fill=(241, 245, 249))
    draw.line([(dx, dy + 64), (dx + dw, dy + 64)], fill=(226, 232, 240), width=2)

    # Icono X rojo
    draw.ellipse([dx + 22, dy + 18, dx + 50, dy + 46], fill=(225, 29, 72))
    draw.text((dx + 30, dy + 20), "X", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.text((dx + 62, dy + 18), "Microsoft Excel — No responde", fill=(15, 23, 42), font=obtener_fuente(26, bold=True))

    # Cuerpo del diálogo en 34px y 26px (100% legible en cualquier pantalla chica)
    draw.text((dx + 36, dy + 95), "¡El programa se tildó a las 17:59!", fill=(15, 23, 42), font=obtener_fuente(34, bold=True))
    draw.text((dx + 36, dy + 150), "Si cerrás ahora, perdés 3 horas de fórmulas sin guardar.", fill=(225, 29, 72), font=obtener_fuente(26, bold=False))

    # Botones meme grandes (360x68 con texto de 26px)
    btn_w, btn_h = 360, 68
    b1_x, b1_y = dx + 36, dy + 235
    draw.rounded_rectangle([b1_x, b1_y, b1_x + btn_w, b1_y + btn_h], radius=12, fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((b1_x + 55, b1_y + 18), "Esperar un milagro", fill=(71, 85, 105), font=obtener_fuente(26, bold=True))

    b2_x, b2_y = dx + dw - btn_w - 36, dy + 235
    draw.rounded_rectangle([b2_x, b2_y, b2_x + btn_w, b2_y + btn_h], radius=12, fill=(225, 29, 72), outline=(190, 18, 60), width=1)
    draw.text((b2_x + 90, b2_y + 18), "Cerrar y llorar", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # 7. Card inferior grande de error en planilla (30px / 25px)
    cx_b, cy_b, cw_b, ch_b = (ancho - 860) // 2, 1480, 860, 140
    draw.rounded_rectangle([cx_b, cy_b, cx_b + cw_b, cy_b + ch_b], radius=18, fill=(255, 241, 242, 245), outline=(225, 29, 72), width=3)
    draw.text((cx_b + 32, cy_b + 26), "Error en celda #¡REF! — Fórmula rota", fill=(15, 23, 42), font=obtener_fuente(30, bold=True))
    draw.text((cx_b + 32, cy_b + 78), "Faltan datos de ventas y la planilla sigue en blanco", fill=(225, 29, 72), font=obtener_fuente(25, bold=False))

    # Badge inferior de remate
    bx_m, by_m, bw_m, bh_m = (ancho - 640) // 2, 1660, 640, 66
    draw.rounded_rectangle([bx_m, by_m, bx_m + bw_m, by_m + bh_m], radius=16, fill=(225, 29, 72, 45), outline=(225, 29, 72), width=2)
    dibujar_chispa_ia(draw, bx_m + 32, by_m + 33, 12, (251, 113, 133))
    draw.text((bx_m + 60, by_m + 16), "ALERTA: FIN DE SEMANA EN RIESGO", fill=(254, 205, 211), font=obtener_fuente(24, bold=True))

    return frame

"""
director_escena.py
------------------
Motor de Dirección Visual y Composición de Escenas Cinematográficas para Byte el Zorrito.
Implementa el catálogo de arquetipos visuales:
1. PLANO_HERO_CAOS (Gancho / Dolor)
2. PLANO_SHOWCASE_PANORAMICO (Herramienta principal / Gran formato)
3. PLANO_SPLIT_BEFORE_AFTER (Transformación / Glow-Up estético)
4. PLANO_DECK_3D (Resultado / Alivio cualitativo)
5. PLANO_HOST_COMMUNITY (Cierre / Interacción comunitaria)
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
    generar_fondo_tech_base
)
from src.mockups.estilos.animaciones_fondo import obtener_lienzo_dinamico_fondo
from src.rutas import DIR_BYTE_TRANSPARENTES, DIR_BYTE_ILUSTRACIONES


def dibujar_icono_alerta(draw: ImageDraw.Draw, cx: int, cy: int, tam: int = 14, color: Tuple[int, ...] = (255, 255, 255)):
    """Dibuja un triángulo de advertencia con signo de exclamación vectorial nítido."""
    pts = [
        (cx, cy - tam),
        (cx + tam, cy + tam),
        (cx - tam, cy + tam)
    ]
    draw.polygon(pts, fill=color)
    draw.line([(cx, cy - int(tam * 0.35)), (cx, cy + int(tam * 0.25))], fill=(15, 23, 42), width=max(2, tam // 5))
    draw.ellipse([cx - max(1, tam // 7), cy + int(tam * 0.55) - max(1, tam // 7), cx + max(1, tam // 7), cy + int(tam * 0.55) + max(1, tam // 7)], fill=(15, 23, 42))


def dibujar_icono_cruz(draw: ImageDraw.Draw, cx: int, cy: int, tam: int = 8, color: Tuple[int, ...] = (244, 63, 94), grosor: int = 2):
    """Dibuja una cruz X vectorial nítida."""
    draw.line([(cx - tam, cy - tam), (cx + tam, cy + tam)], fill=color, width=grosor)
    draw.line([(cx - tam, cy + tam), (cx + tam, cy - tam)], fill=color, width=grosor)


def dibujar_icono_candado(draw: ImageDraw.Draw, cx: int, cy: int, tam: int = 14, color: Tuple[int, ...] = (16, 185, 129)):
    """Dibuja un candado de seguridad vectorial nítido."""
    arco_r = int(tam * 0.7)
    draw.arc([cx - arco_r, cy - tam - arco_r // 2, cx + arco_r, cy], start=180, end=0, fill=color, width=max(2, tam // 4))
    draw.rounded_rectangle([cx - tam, cy - int(tam * 0.2), cx + tam, cy + tam], radius=max(2, tam // 4), fill=color)
    draw.ellipse([cx - max(1, tam // 6), cy + int(tam * 0.1), cx + max(1, tam // 6), cy + int(tam * 0.4)], fill=(15, 23, 42))
    draw.line([(cx, cy + int(tam * 0.3)), (cx, cy + int(tam * 0.65))], fill=(15, 23, 42), width=max(2, tam // 5))


def dibujar_icono_lupa(draw: ImageDraw.Draw, cx: int, cy: int, r: int = 12, color: Tuple[int, ...] = (148, 163, 184)):
    """Dibuja una lupa de búsqueda vectorial nítida."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=max(2, r // 4))
    dx = int(r * 0.65)
    dy = int(r * 0.65)
    largo = int(r * 0.8)
    draw.line([(cx + dx, cy + dy), (cx + dx + largo, cy + dy + largo)], fill=color, width=max(3, r // 3))


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
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.35, atenuacion_oscura=0.45)
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

    # 2. Elementos temáticos de dolor flotando y rotando (zonas y < 880 e y > 1160)
    elementos = cfg.get("elementos", [
        {"x": 70, "y": 250, "w": 300, "h": 150, "rot": -10, "tit": "Slide 1 • En blanco", "sub": "Falta formato", "col": (225, 29, 72)},
        {"x": 680, "y": 240, "w": 310, "h": 150, "rot": 12, "tit": "Slide 2 • Datos rotos", "sub": "Tablas desalineadas", "col": (225, 29, 72)},
        {"x": 50, "y": 1200, "w": 330, "h": 150, "rot": 7, "tit": "Métricas Q3", "sub": "Sin orden visual", "col": (245, 158, 11)},
        {"x": 680, "y": 1220, "w": 330, "h": 150, "rot": -7, "tit": "Borrador interminable", "sub": "Horas perdidas", "col": (225, 29, 72)},
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

    # 3. Título de Alerta Superior (Safe Zone)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=f_badge)
    alerta_w = max(420, bbox_b[2] - bbox_b[0] + 90)
    alerta_h = 52
    ax = (ancho - alerta_w) // 2
    ay = 110
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
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.35, atenuacion_oscura=0.45)
    draw = ImageDraw.Draw(frame)

    # 1. Gran Contenedor Panorámico Showcase (Ocupa 92% del ancho y 50% de alto)
    sw = int(ancho * 0.92)
    sh = 720
    sx = (ancho - sw) // 2
    sy = 160

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
    draw.text((sx + 36, sy + 155), sub_principal, fill=(100, 116, 139), font=obtener_fuente(22, bold=False))

    # 3 Tarjetas de contenido con métricas visuales dentro de la slide
    w_card = (sw - 72 - 32) // max(1, len(items_showcase))
    h_card = 260
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
            # Ubicado abajo a la derecha asomándose
            bx = ancho - bw - 20
            by = alto - bh - 60
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
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.35, atenuacion_oscura=0.45)
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

    # 1. Dos Tarjetas Gigantes Comparativas (Arriba: Antes / Abajo: Después)
    card_w = int(ancho * 0.92)
    card_x = (ancho - card_w) // 2

    # TARJETA 1 (ANTES - Manual / Plano)
    y_antes = 150
    h_antes = 260
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
    h_despues = 300
    draw.rounded_rectangle([card_x, y_despues, card_x + card_w, y_despues + h_despues], radius=18, fill=(255, 255, 255), outline=(147, 51, 234), width=3)
    # Tag 'DESPUÉS'
    bbox_dt = draw.textbbox((0, 0), despues_tag, font=f_badge)
    dt_w = bbox_dt[2] - bbox_dt[0] + 32
    draw.rounded_rectangle([card_x + 24, y_despues + 20, card_x + 24 + dt_w, y_despues + 64], radius=8, fill=(245, 243, 255), outline=(147, 51, 234))
    draw.text((card_x + 40, y_despues + 28), despues_tag, fill=(124, 58, 237), font=f_badge)
    draw.text((card_x + 40 + dt_w + 14, y_despues + 28), despues_tit, fill=(15, 23, 42), font=f_tit)

    # Badges de Glow-Up con iconos dibujados limpios
    for idx_p, (t_p, d_p, c_p, bg_p) in enumerate(pills_despues[:3]):
        py = y_despues + 90 + idx_p * 64
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
            by = alto - bh - 50
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
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.35, atenuacion_oscura=0.45)
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

    # 2. Gran Badge Circular de Victoria
    r_circ = 46
    draw.ellipse([cx - r_circ - 10, 190 - r_circ - 10, cx + r_circ + 10, 190 + r_circ + 10], fill=(236, 253, 245))
    draw.ellipse([cx - r_circ, 190 - r_circ, cx + r_circ, 190 + r_circ], fill=(16, 185, 129))
    dibujar_icono_check(draw, cx - 18, 190 - 20, (255, 255, 255), tam=38, grosor=4)

    cfg = config or {}
    tit_txt = cfg.get("titulo", "¡Presentación 100% Lista!")
    sub_txt = cfg.get("subtitulo", "Material presentable, ordenado y visual para compartir")
    cards_deck = cfg.get("cards", [
        {"x_off": -180, "y": 380, "tit": "01 • Introducción", "rot": -7, "col": (37, 99, 235)},
        {"x_off": 180, "y": 380, "tit": "03 • Conclusiones", "rot": 7, "col": (124, 58, 237)},
        {"x_off": 0, "y": 360, "tit": "02 • Estrategia Q3", "rot": 0, "col": (16, 185, 129)},
    ])
    pills = cfg.get("pills", [("Presentable", (16, 185, 129)), ("Ordenado", (14, 165, 233)), ("Visual", (124, 58, 237))])

    # Títulos
    bbox_t = draw.textbbox((0, 0), tit_txt, font=f_big)
    tw = bbox_t[2] - bbox_t[0]
    draw.text((cx - tw // 2, 260), tit_txt, fill=(255, 255, 255), font=f_big)

    bbox_s = draw.textbbox((0, 0), sub_txt, font=f_sub)
    sw = bbox_s[2] - bbox_s[0]
    draw.text((cx - sw // 2, 310), sub_txt, fill=(167, 243, 208), font=f_sub)

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
        d_cd.text((26, 78), c_desc, fill=cd["col"], font=obtener_fuente(18, bold=True))
        dibujar_icono_check(d_cd, dw - 44, dh - 36, cd["col"], tam=16, grosor=3)

        c_rot = c_img.rotate(cd["rot"], resample=Image.Resampling.BILINEAR, expand=True)
        pos_x = cx + cd["x_off"] - c_rot.width // 2
        frame.paste(c_rot, (pos_x, cd["y"]), c_rot)

    # 4. Badges de Alivio Cualitativo al pie
    pw = 260
    ph = 52
    y_p = 610
    gap_p = (int(ancho * 0.92) - pw * 3) // 2
    start_x = (ancho - int(ancho * 0.92)) // 2

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
            bw, bh = 540, 540
            b_rgba = b_rgba.resize((bw, bh), Image.Resampling.LANCZOS)
            # Levita suavemente
            flotacion = int(8 * math.sin(t_sec * 2.5))
            bx = (ancho - bw) // 2
            by = alto - bh - 60 + flotacion
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
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.35, atenuacion_oscura=0.45)
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

    # 1. Gran Pregunta Central Superior (Estilo Sticker de TikTok/Instagram)
    qw = int(ancho * 0.92)
    qx = (ancho - qw) // 2
    qy = 150
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
            # Rebote alegre
            rebote = int(10 * abs(math.sin(t_sec * 3.0)))
            bx = (ancho - bw) // 2
            by = alto - bh - 40 - rebote
            frame.paste(b_resized, (bx, by), b_resized)

    # 4. Indicador hacia los comentarios limpio y elegante
    f_com = obtener_fuente(22, bold=True)
    bbox_com = draw.textbbox((0, 0), txt_com, font=f_com)
    cw = bbox_com[2] - bbox_com[0]
    cx = (ancho - cw) // 2
    cy = alto - 75
    draw.text((cx, cy), txt_com, fill=(255, 255, 255), font=f_com)
    # Flecha chevron hacia abajo dibujada
    arr_x = cx + cw + 18
    arr_y = cy + 10
    draw.polygon([(arr_x, arr_y), (arr_x + 12, arr_y), (arr_x + 6, arr_y + 8)], fill=(255, 255, 255))

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
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.35, atenuacion_oscura=0.45)
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


# ---------------------------------------------------------------------------
# 6. PLANO_JULIUS_DASHBOARD: Dashboard Analítico Completo con Gráficos Neón
# ---------------------------------------------------------------------------
def renderizar_plano_julius_dashboard(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.35, atenuacion_oscura=0.50)

    # 1. Aura de datos cyan/azul en el fondo
    cx, cy = ancho // 2, 550
    aura = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_aura = ImageDraw.Draw(aura)
    d_aura.ellipse([cx - 450, cy - 400, cx + 450, cy + 400], fill=(6, 182, 212, 35))
    aura = aura.filter(ImageFilter.GaussianBlur(90))
    frame = Image.alpha_composite(frame, aura)
    draw = ImageDraw.Draw(frame)

    # 2. Barra de ventana superior (3 puntos neutros)
    wx, wy, ww, wh = 50, 70, ancho - 100, 75
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=16, fill=(17, 24, 39, 230), outline=(30, 41, 59), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 20 + idx_dot * 22, wy + 28, wx + 34 + idx_dot * 22, wy + 42], fill=(148, 163, 184))

    dibujar_chispa_ia(draw, wx + 110, wy + 37, 10, (6, 182, 212))
    header_tit = cfg.get("header", "JULIUS AI • Analista de Datos Inteligente")
    draw.text((wx + 130, wy + 24), header_tit, fill=(241, 245, 249), font=obtener_fuente(24, bold=True))

    b_txt = cfg.get("badge", "Gráficos en 1 Frase")
    draw.rounded_rectangle([wx + ww - 260, wy + 14, wx + ww - 16, wy + wh - 14], radius=10, fill=(6, 182, 212, 40), outline=(6, 182, 212), width=1)
    draw.text((wx + ww - 245, wy + 23), b_txt, fill=(6, 182, 212), font=obtener_fuente(20, bold=True))

    # 3. Prompt Bar interactivo con tipografía grande (24px)
    px, py, pw, ph = 50, 165, ancho - 100, 100
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=18, fill=(15, 23, 42, 240), outline=(56, 189, 248), width=2)
    dibujar_chispa_ia(draw, px + 24, py + 30, 10, (56, 189, 248))
    draw.text((px + 44, py + 18), "Prompt:", fill=(56, 189, 248), font=obtener_fuente(24, bold=True))
    prompt_txt = cfg.get("titulo", "Analizá las ventas de la semana y armá gráficos")
    draw.text((px + 145, py + 18), f'"{prompt_txt}"', fill=(255, 255, 255), font=obtener_fuente(23, bold=False))

    # Status chip
    draw.rounded_rectangle([px + 24, py + 58, px + 390, py + 90], radius=8, fill=(16, 185, 129, 35))
    dibujar_icono_check(draw, px + 36, py + 74, (16, 185, 129), tam=14, grosor=2)
    draw.text((px + 58, py + 64), "Planilla Excel procesada en 0.8s", fill=(52, 211, 153), font=obtener_fuente(18, bold=True))

    # 4. DASHBOARD VISUAL CON GRÁFICO DE BARRAS REAL (Tipografía 28px y 20px)
    dx, dy, dw, dh = 50, 280, ancho - 100, 580
    draw.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=22, fill=(17, 24, 39, 240), outline=(30, 41, 59), width=2)

    draw.text((dx + 30, dy + 25), "Rendimiento y Ventas Semanales", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))
    draw.text((dx + 30, dy + 66), "Generado automáticamente sin fórmulas manuales", fill=(148, 163, 184), font=obtener_fuente(20, bold=False))

    draw.rounded_rectangle([dx + dw - 240, dy + 22, dx + dw - 25, dy + 74], radius=10, fill=(16, 185, 129, 30), outline=(16, 185, 129), width=1)
    draw.text((dx + dw - 222, dy + 34), "+84% Crecimiento", fill=(52, 211, 153), font=obtener_fuente(22, bold=True))

    # Área de dibujo de barras
    gx, gy, gw, gh = dx + 40, dy + 110, dw - 80, 430

    for l_idx in range(4):
        ly = gy + l_idx * (gh // 4)
        draw.line([(gx, ly), (gx + gw, ly)], fill=(31, 41, 55), width=1)
        val_txt = f"${(4 - l_idx) * 2}k"
        draw.text((gx - 35, ly - 10), val_txt, fill=(100, 116, 139), font=obtener_fuente(16, bold=False))

    datos = [
        ("Lun", 130, "$1.4k", (6, 182, 212)),
        ("Mar", 180, "$2.1k", (6, 182, 212)),
        ("Mié", 250, "$3.2k", (56, 189, 248)),
        ("Jue", 310, "$4.0k", (56, 189, 248)),
        ("Vie", 370, "$5.8k", (16, 185, 129)),
        ("Total", 400, "+84%", (234, 179, 8))
    ]

    col_w = 70
    gap = (gw - col_w * len(datos)) // (len(datos) + 1)
    puntos_tendencia = []

    for i, (dia, alt_bar, val_s, col_bar) in enumerate(datos):
        bx0 = gx + gap + i * (col_w + gap)
        bx1 = bx0 + col_w
        by1 = gy + gh
        by0 = by1 - alt_bar

        draw.rounded_rectangle([bx0, by0, bx1, by1], radius=8, fill=(*col_bar[:3], 230))
        draw.rounded_rectangle([bx0, by0, bx1, by0 + 8], radius=4, fill=(255, 255, 255, 220))
        draw.text((bx0 + 6, by0 - 32), val_s, fill=col_bar, font=obtener_fuente(20, bold=True))
        draw.text((bx0 + 14, by1 + 10), dia, fill=(148, 163, 184), font=obtener_fuente(20, bold=True))
        puntos_tendencia.append((bx0 + col_w // 2, by0 + 4))

    for p_idx in range(len(puntos_tendencia) - 1):
        pt1 = puntos_tendencia[p_idx]
        pt2 = puntos_tendencia[p_idx + 1]
        draw.line([pt1, pt2], fill=(255, 245, 0), width=4)
        draw.ellipse([pt1[0] - 5, pt1[1] - 5, pt1[0] + 5, pt1[1] + 5], fill=(255, 245, 0))
    draw.ellipse([puntos_tendencia[-1][0] - 5, puntos_tendencia[-1][1] - 5, puntos_tendencia[-1][0] + 5, puntos_tendencia[-1][1] + 5], fill=(255, 245, 0))

    # 5. SUBTITLE SAFE ZONE: y = 880 a 1120 (100% LIBRE PARA SUBTÍTULOS KARAOKE)

    # 6. ZONA INFERIOR: Byte Protagonista Recortado (Derecha) + Cards Grandes (Izquierda)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        for cand in ["punto_1_guion_07_transparente.png", "byte_computadora_feliz_transparente.png", "punto_1_guion_06_transparente.png"]:
            if (DIR_BYTE_TRANSPARENTES / cand).exists():
                p_byte = DIR_BYTE_TRANSPARENTES / cand
                break

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_rgba = img_b.convert("RGBA")
            bbox = b_rgba.getbbox()
            b_cropped = b_rgba.crop(bbox) if bbox else b_rgba
            aspect = b_cropped.width / b_cropped.height
            bh = 580
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = ancho - bw - 10
            by = 1240
            frame.paste(b_resized, (bx, by), b_resized)

    # Cards a la izquierda con tipografía GRANDE (28px / 23px)
    c1_x, c1_y, c1_w, c1_h = 50, 1260, 450, 150
    draw.rounded_rectangle([c1_x, c1_y, c1_x + c1_w, c1_y + c1_h], radius=16, fill=(15, 23, 42, 230), outline=(6, 182, 212), width=2)
    dibujar_chispa_ia(draw, c1_x + 30, c1_y + 35, 12, (6, 182, 212))
    draw.text((c1_x + 56, c1_y + 22), "Cero Fórmulas", fill=(6, 182, 212), font=obtener_fuente(28, bold=True))
    draw.text((c1_x + 24, c1_y + 68), "Julius genera el script de", fill=(241, 245, 249), font=obtener_fuente(23, bold=False))
    draw.text((c1_x + 24, c1_y + 102), "análisis con solo pedírselo", fill=(148, 163, 184), font=obtener_fuente(21, bold=False))

    c2_x, c2_y, c2_w, c2_h = 50, 1440, 450, 150
    draw.rounded_rectangle([c2_x, c2_y, c2_x + c2_w, c2_y + c2_h], radius=16, fill=(15, 23, 42, 230), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, c2_x + 30, c2_y + 35, (16, 185, 129), tam=18, grosor=3)
    draw.text((c2_x + 60, c2_y + 22), "Gráficos Listos", fill=(52, 211, 153), font=obtener_fuente(28, bold=True))
    draw.text((c2_x + 24, c2_y + 68), "Barras, tortas y métricas", fill=(241, 245, 249), font=obtener_fuente(23, bold=False))
    draw.text((c2_x + 24, c2_y + 102), "listas para exportar", fill=(148, 163, 184), font=obtener_fuente(21, bold=False))

    b_inf_x, b_inf_y, b_inf_w, b_inf_h = 50, 1620, 450, 68
    draw.rounded_rectangle([b_inf_x, b_inf_y, b_inf_x + b_inf_w, b_inf_y + b_inf_h], radius=14, fill=(234, 179, 8, 30), outline=(234, 179, 8), width=2)
    dibujar_chispa_ia(draw, b_inf_x + 30, b_inf_y + 34, 12, (255, 245, 0))
    draw.text((b_inf_x + 56, b_inf_y + 18), "AHORRO: TODA LA TARDE", fill=(255, 245, 0), font=obtener_fuente(23, bold=True))

    return frame


# ---------------------------------------------------------------------------
# 7. PLANO_GAMMA_SLIDES: Diapositiva Ejecutiva Panorámica Real
# ---------------------------------------------------------------------------
def renderizar_plano_gamma_slides(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.35, atenuacion_oscura=0.50)

    # Glow violeta en el fondo
    cx, cy = ancho // 2, 500
    aura = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_aura = ImageDraw.Draw(aura)
    d_aura.ellipse([cx - 450, cy - 380, cx + 450, cy + 380], fill=(139, 92, 246, 35))
    aura = aura.filter(ImageFilter.GaussianBlur(90))
    frame = Image.alpha_composite(frame, aura)
    draw = ImageDraw.Draw(frame)

    # 1. Barra de ventana superior
    wx, wy, ww, wh = 50, 70, ancho - 100, 75
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=16, fill=(17, 24, 39, 230), outline=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 20 + idx_dot * 22, wy + 28, wx + 34 + idx_dot * 22, wy + 42], fill=(148, 163, 184))

    dibujar_chispa_ia(draw, wx + 110, wy + 37, 10, (168, 85, 247))
    header_tit = cfg.get("header", "GAMMA • Diapositivas Generadas con IA")
    draw.text((wx + 130, wy + 24), header_tit, fill=(241, 245, 249), font=obtener_fuente(24, bold=True))

    draw.rounded_rectangle([wx + ww - 240, wy + 16, wx + ww - 16, wy + wh - 16], radius=10, fill=(168, 85, 247, 40), outline=(168, 85, 247), width=1)
    draw.text((wx + ww - 220, wy + 25), "De Idea a Slides", fill=(192, 132, 252), font=obtener_fuente(20, bold=True))

    # 2. DIAPOSITIVA EJECUTIVA PANORÁMICA REAL (y = 165 a 850)
    sx, sy, sw, sh = 50, 165, ancho - 100, 680
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=22, fill=(255, 255, 255), outline=(139, 92, 246), width=3)

    # Barra superior de la slide
    draw.rounded_rectangle([sx, sy, sx + sw, sy + 64], radius=22, fill=(245, 243, 255))
    draw.line([(sx, sy + 64), (sx + sw, sy + 64)], fill=(233, 213, 255), width=2)
    draw.text((sx + 30, sy + 18), "REPORTE SEMANAL • RESULTADOS Q3", fill=(124, 58, 237), font=obtener_fuente(20, bold=True))
    draw.text((sx + sw - 260, sy + 18), "Página 1 de 8 • Lista para enviar", fill=(100, 116, 139), font=obtener_fuente(18, bold=False))

    draw.text((sx + 36, sy + 92), "Estrategia y Crecimiento del Negocio", fill=(15, 23, 42), font=obtener_fuente(32, bold=True))
    draw.text((sx + 36, sy + 140), "Estructura completa armada en segundos sin tocar plantillas", fill=(100, 116, 139), font=obtener_fuente(22, bold=False))

    col_w = (sw - 72 - 32) // 3
    col_h = 320
    col_y = sy + 185
    cards_slide = [
        ("01 • Objetivos", "Métricas semanales alcanzadas y alineadas", (37, 99, 235), (239, 246, 255)),
        ("02 • Datos Julius", "Gráficos de ventas insertados con éxito", (124, 58, 237), (245, 243, 255)),
        ("03 • Próximos Pasos", "Cronograma confirmado listo para mandar", (5, 150, 105), (236, 253, 245)),
    ]
    for i, (tit_c, desc_c, col_c, bg_c) in enumerate(cards_slide):
        cx0 = sx + 36 + i * (col_w + 16)
        cx1 = cx0 + col_w
        draw.rounded_rectangle([cx0, col_y, cx1, col_y + col_h], radius=14, fill=bg_c, outline=(*col_c[:3], 90), width=2)
        draw.rounded_rectangle([cx0, col_y, cx0 + 8, col_y + col_h], radius=4, fill=col_c)
        draw.text((cx0 + 20, col_y + 26), tit_c, fill=col_c, font=obtener_fuente(24, bold=True))

        palabras = desc_c.split(" ")
        l1 = " ".join(palabras[:3])
        l2 = " ".join(palabras[3:6])
        l3 = " ".join(palabras[6:])
        draw.text((cx0 + 20, col_y + 80), l1, fill=(30, 41, 59), font=obtener_fuente(20, bold=False))
        if l2:
            draw.text((cx0 + 20, col_y + 115), l2, fill=(30, 41, 59), font=obtener_fuente(20, bold=False))
        if l3:
            draw.text((cx0 + 20, col_y + 150), l3, fill=(30, 41, 59), font=obtener_fuente(20, bold=False))

        dibujar_icono_check(draw, cx1 - 40, col_y + col_h - 36, col_c, tam=18, grosor=3)

    draw.rounded_rectangle([sx + 36, sy + sh - 95, sx + sw - 36, sy + sh - 25], radius=12, fill=(245, 243, 255), outline=(233, 213, 255), width=2)
    dibujar_chispa_ia(draw, sx + 58, sy + sh - 60, 12, (124, 58, 237))
    draw.text((sx + 84, sy + sh - 72), "Presentación exportable a PDF o diapositivas con un clic", fill=(109, 40, 217), font=obtener_fuente(22, bold=True))

    # 3. ZONA CENTRAL DE SUBTÍTULOS: y = 870 a 1120 (100% LIBRE)

    # 4. ZONA INFERIOR: Byte Hacker (Izquierda) + Cards Grandes (Derecha)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        for cand in ["punto_2_guion_07_transparente.png", "byte_computadora_feliz_transparente.png", "punto_2_guion_06_transparente.png"]:
            if (DIR_BYTE_TRANSPARENTES / cand).exists():
                p_byte = DIR_BYTE_TRANSPARENTES / cand
                break

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_rgba = img_b.convert("RGBA")
            bbox = b_rgba.getbbox()
            b_cropped = b_rgba.crop(bbox) if bbox else b_rgba
            aspect = b_cropped.width / b_cropped.height
            bh = 560
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = 20
            by = 1240
            frame.paste(b_resized, (bx, by), b_resized)

    rc_x, rc_w = 540, ancho - 540 - 50
    draw.rounded_rectangle([rc_x, 1260, rc_x + rc_w, 1410], radius=16, fill=(17, 24, 39, 230), outline=(139, 92, 246), width=2)
    dibujar_chispa_ia(draw, rc_x + 28, 1295, 12, (168, 85, 247))
    draw.text((rc_x + 54, 1282), "Diseño Pro en Minutos", fill=(192, 132, 252), font=obtener_fuente(28, bold=True))
    draw.text((rc_x + 24, 1328), "Convierte texto e ideas en", fill=(241, 245, 249), font=obtener_fuente(22, bold=False))
    draw.text((rc_x + 24, 1362), "diapositivas bien armadas", fill=(148, 163, 184), font=obtener_fuente(20, bold=False))

    draw.rounded_rectangle([rc_x, 1440, rc_x + rc_w, 1590], radius=16, fill=(17, 24, 39, 230), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, rc_x + 28, 1475, (16, 185, 129), tam=18, grosor=3)
    draw.text((rc_x + 58, 1462), "Listo para Enviar", fill=(52, 211, 153), font=obtener_fuente(28, bold=True))
    draw.text((rc_x + 24, 1508), "Compartilo con tu jefe", fill=(241, 245, 249), font=obtener_fuente(22, bold=False))
    draw.text((rc_x + 24, 1542), "antes de las 18:00 hs", fill=(148, 163, 184), font=obtener_fuente(20, bold=False))

    draw.rounded_rectangle([rc_x, 1620, rc_x + rc_w, 1686], radius=12, fill=(124, 58, 237, 35), outline=(139, 92, 246), width=1)
    dibujar_chispa_ia(draw, rc_x + 24, 1653, 10, (216, 180, 254))
    draw.text((rc_x + 46, 1638), "CERO COPY-PASTE MANUAL", fill=(216, 180, 254), font=obtener_fuente(22, bold=True))

    return frame


# ---------------------------------------------------------------------------
# 8. PLANO_LAPTOP_CERRADA: Finde Libre, Laptop Cerrada y Reporte Enviado
# ---------------------------------------------------------------------------
def renderizar_plano_laptop_finde(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.35, atenuacion_oscura=0.45)

    cx, cy = ancho // 2, 450
    aura = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_aura = ImageDraw.Draw(aura)
    d_aura.ellipse([cx - 450, cy - 380, cx + 450, cy + 380], fill=(16, 185, 129, 35))
    aura = aura.filter(ImageFilter.GaussianBlur(90))
    frame = Image.alpha_composite(frame, aura)
    draw = ImageDraw.Draw(frame)

    # 1. Badge superior de victoria
    badge_txt = cfg.get("badge", "VIERNES 18:00 • INFORME ENVIADO")
    f_badge = obtener_fuente(24, bold=True)
    ax, ay, aw, ah = (ancho - 520) // 2, 80, 520, 56
    draw.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=28, fill=(16, 185, 129, 230), outline=(167, 243, 208), width=2)
    dibujar_icono_check(draw, ax + 32, ay + 28, (255, 255, 255), tam=20, grosor=3)
    draw.text((ax + 64, ay + 14), badge_txt, fill=(255, 255, 255), font=f_badge)

    # 2. GRÁFICO DE LAPTOP CERRADA ELEGANTE (y = 170 a 640)
    lx, ly, lw, lh = 170, 180, 740, 430

    draw.rounded_rectangle([lx - 40, ly + lh - 25, lx + lw + 40, ly + lh + 15], radius=14, fill=(51, 65, 85), outline=(71, 85, 105), width=2)
    draw.rounded_rectangle([lx + lw // 2 - 50, ly + lh - 24, lx + lw // 2 + 50, ly + lh - 14], radius=4, fill=(15, 23, 42))
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh - 20], radius=20, fill=(30, 41, 59), outline=(71, 85, 105), width=3)
    draw.line([(lx + 40, ly + 20), (lx + lw - 40, ly + 20)], fill=(71, 85, 105, 120), width=2)

    logo_cx, logo_cy = lx + lw // 2, ly + (lh - 20) // 2 - 20
    draw.ellipse([logo_cx - 35, logo_cy - 35, logo_cx + 35, logo_cy + 35], fill=(51, 65, 85))
    dibujar_chispa_ia(draw, logo_cx, logo_cy, 20, (56, 189, 248))

    # SELLO VERDE GIGANTE: "✓ REPORTE ENVIADO • 18:00 HS"
    stamp_w, stamp_h = 600, 120
    stamp_img = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
    d_st = ImageDraw.Draw(stamp_img)
    d_st.rounded_rectangle([0, 0, stamp_w, stamp_h], radius=18, fill=(16, 185, 129, 230), outline=(255, 255, 255), width=4)
    d_st.rounded_rectangle([8, 8, stamp_w - 8, stamp_h - 8], radius=12, fill=None, outline=(255, 255, 255), width=2)
    dibujar_icono_check(d_st, 45, stamp_h // 2, (255, 255, 255), tam=32, grosor=4)
    d_st.text((88, 24), "REPORTE ENVIADO • 18:00 HS", fill=(255, 255, 255), font=obtener_fuente(32, bold=True))
    d_st.text((128, 72), "VIERNES CERRADO A TIEMPO", fill=(209, 250, 229), font=obtener_fuente(20, bold=True))

    stamp_rot = stamp_img.rotate(-7, resample=Image.Resampling.BILINEAR, expand=True)
    frame.paste(stamp_rot, (lx + 50, ly + 130), stamp_rot)

    # Tarjetas de alivio
    draw.rounded_rectangle([50, 670, 480, 810], radius=16, fill=(15, 23, 42, 230), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, 75, 705, (52, 211, 153), tam=18, grosor=3)
    draw.text((104, 690), "Modo Fin de Semana", fill=(52, 211, 153), font=obtener_fuente(26, bold=True))
    draw.text((75, 735), "Cero pendientes ni horas extra", fill=(241, 245, 249), font=obtener_fuente(22, bold=False))
    draw.text((75, 768), "sin deberle nada a nadie", fill=(148, 163, 184), font=obtener_fuente(20, bold=False))

    draw.rounded_rectangle([540, 670, ancho - 50, 810], radius=16, fill=(15, 23, 42, 230), outline=(56, 189, 248), width=2)
    dibujar_chispa_ia(draw, 565, 705, 12, (56, 189, 248))
    draw.text((594, 690), "Cabeza en Paz", fill=(56, 189, 248), font=obtener_fuente(26, bold=True))
    draw.text((565, 735), "La tarde no se perdió en Excel", fill=(241, 245, 249), font=obtener_fuente(22, bold=False))
    draw.text((565, 768), "y el reporte quedó impecable", fill=(148, 163, 184), font=obtener_fuente(20, bold=False))

    # 3. ZONA CENTRAL DE SUBTÍTULOS: y = 870 a 1120 (100% LIBRE)

    # 4. ZONA INFERIOR: Byte Zen Protagonista (Centrado y Grande, Recortado a Bbox)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        for cand in ["resultado_guion_07_transparente.png", "resultado_guion_06_transparente.png"]:
            if (DIR_BYTE_TRANSPARENTES / cand).exists():
                p_byte = DIR_BYTE_TRANSPARENTES / cand
                break

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_rgba = img_b.convert("RGBA")
            bbox = b_rgba.getbbox()
            b_cropped = b_rgba.crop(bbox) if bbox else b_rgba
            aspect = b_cropped.width / b_cropped.height
            bh = 580
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            flotacion = int(8 * math.sin(t_sec * 2.5))
            bx = (ancho - bw) // 2
            by = 1240 + flotacion
            frame.paste(b_resized, (bx, by), b_resized)

    # Floating pills de relax
    draw.rounded_rectangle([60, 1550, 310, 1618], radius=16, fill=(16, 185, 129, 35), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, 88, 1584, (110, 231, 183), tam=16, grosor=2)
    draw.text((116, 1568), "Finde Libre", fill=(110, 231, 183), font=obtener_fuente(24, bold=True))

    draw.rounded_rectangle([ancho - 310 - 60, 1550, ancho - 60, 1618], radius=16, fill=(56, 189, 248, 35), outline=(56, 189, 248), width=2)
    dibujar_chispa_ia(draw, ancho - 310 - 32, 1584, 12, (125, 211, 252))
    draw.text((ancho - 310 - 4, 1568), "Cero Estrés", fill=(125, 211, 252), font=obtener_fuente(24, bold=True))

    return frame


# ---------------------------------------------------------------------------
# 9. PLANO_PERPLEXITY_SEARCH: Hero UI 1040px con Búsqueda en Vivo y Citas Reales
# ---------------------------------------------------------------------------
def renderizar_plano_perplexity_search(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "viaje_espacial")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)

    # 1. Aura cian/azul eléctrica en el fondo
    cx, cy = ancho // 2, 520
    aura = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_aura = ImageDraw.Draw(aura)
    d_aura.ellipse([cx - 460, cy - 380, cx + 460, cy + 380], fill=(6, 182, 212, 35))
    aura = aura.filter(ImageFilter.GaussianBlur(90))
    frame = Image.alpha_composite(frame, aura)
    draw = ImageDraw.Draw(frame)

    # 2. Hero UI: Ventana Maximizada (1040px de ancho, 20px margen)
    wx, wy, ww, wh = 20, 70, ancho - 40, 75
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=16, fill=(15, 23, 42, 235), outline=(30, 41, 59), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 22, wy + 28, wx + 36 + idx_dot * 22, wy + 42], fill=(148, 163, 184))

    dibujar_chispa_ia(draw, wx + 110, wy + 37, 10, (6, 182, 212))
    header_tit = cfg.get("header", "PERPLEXITY AI • Motor de Respuestas en Tiempo Real")
    draw.text((wx + 130, wy + 24), header_tit, fill=(241, 245, 249), font=obtener_fuente(24, bold=True))

    b_txt = cfg.get("badge", "⚡ En Vivo")
    draw.rounded_rectangle([wx + ww - 180, wy + 16, wx + ww - 18, wy + wh - 16], radius=10, fill=(6, 182, 212, 40), outline=(6, 182, 212), width=1)
    draw.text((wx + ww - 162, wy + 24), b_txt, fill=(6, 182, 212), font=obtener_fuente(20, bold=True))

    # 3. Prompt Bar prominente
    px, py, pw, ph = 20, 165, ancho - 40, 105
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=18, fill=(15, 23, 42, 240), outline=(6, 182, 212), width=2)
    dibujar_chispa_ia(draw, px + 26, py + 32, 10, (56, 189, 248))
    draw.text((px + 48, py + 20), "Prompt:", fill=(56, 189, 248), font=obtener_fuente(24, bold=True))
    prompt_txt = cfg.get("titulo", "Buscá datos verificados de mercado y citá fuentes")
    draw.text((px + 150, py + 20), f'"{prompt_txt}"', fill=(255, 255, 255), font=obtener_fuente(23, bold=False))

    draw.rounded_rectangle([px + 26, py + 62, px + 390, py + 95], radius=8, fill=(16, 185, 129, 35))
    dibujar_icono_check(draw, px + 38, py + 78, (16, 185, 129), tam=14, grosor=2)
    draw.text((px + 60, py + 68), "Fuentes verificadas al instante", fill=(52, 211, 153), font=obtener_fuente(18, bold=True))

    # 4. Contenedor de Fuentes Verificadas
    fx, fy, fw, fh = 20, 285, ancho - 40, 75
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=14, fill=(17, 24, 39, 230), outline=(30, 41, 59), width=1)
    draw.text((fx + 24, fy + 26), "FUENTES:", fill=(148, 163, 184), font=obtener_fuente(18, bold=True))

    fuentes = [("[1] Bloomberg", (6, 182, 212)), ("[2] Reuters", (14, 165, 233)), ("[3] Nature", (16, 185, 129)), ("[4] ArXiv", (168, 85, 247))]
    fx_chip = fx + 130
    for f_txt, f_col in fuentes:
        bbox_f = draw.textbbox((0, 0), f_txt, font=obtener_fuente(18, bold=True))
        w_chip = bbox_f[2] - bbox_f[0] + 24
        draw.rounded_rectangle([fx_chip, fy + 16, fx_chip + w_chip, fy + fh - 16], radius=8, fill=(*f_col[:3], 35), outline=f_col, width=1)
        draw.text((fx_chip + 12, fy + 24), f_txt, fill=f_col, font=obtener_fuente(18, bold=True))
        fx_chip += w_chip + 12

    # 5. Tarjeta de Respuesta Estructurada (Limpia y legible en 1 segundo)
    rx, ry, rw, rh = 20, 375, ancho - 40, 325
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=20, fill=(15, 23, 42, 245), outline=(30, 41, 59), width=2)
    draw.text((rx + 30, ry + 26), "Respuesta Verificada:", fill=(56, 189, 248), font=obtener_fuente(24, bold=True))

    draw.text((rx + 30, ry + 75), "Síntesis directa basada en fuentes oficiales [1][2]", fill=(255, 255, 255), font=obtener_fuente(27, bold=True))
    draw.text((rx + 30, ry + 130), "Cada dato incluye enlace a la cita original [3][4]", fill=(226, 232, 240), font=obtener_fuente(25, bold=False))

    draw.rounded_rectangle([rx + 30, ry + 205, rx + 480, ry + 265], radius=12, fill=(6, 182, 212, 35), outline=(6, 182, 212), width=1)
    dibujar_chispa_ia(draw, rx + 52, ry + 235, 10, (6, 182, 212))
    draw.text((rx + 75, ry + 220), "Información respaldada por fuentes", fill=(56, 189, 248), font=obtener_fuente(22, bold=True))

    # 6. Hero UI: Píldora Única de Alto Impacto (Zona media-alta: NO tapa a Byte)
    pill_w = ancho - 80
    draw.rounded_rectangle([40, 720, 40 + pill_w, 795], radius=24, fill=(6, 182, 212, 45), outline=(6, 182, 212), width=2)
    dibujar_chispa_ia(draw, 72, 757, 14, (6, 182, 212))
    draw.text((105, 739), "⚡ Citas reales con fuentes verificadas", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))

    # 7. Sprite de Byte en esquina inferior derecha (100% visible, sin banners encima)
    p_byte = cfg.get("sprite_byte")
    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 600
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = ancho - bw - 10
            by = alto - bh - 110 + int(6 * math.sin(t_sec * 3.0))
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 10. PLANO_NOTEBOOKLM_DOCS: Hero UI 1040px con Documentos Subidos y Cero Alucinación
# ---------------------------------------------------------------------------
def renderizar_plano_notebooklm_docs(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "viaje_espacial")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)

    # 1. Aura verde esmeralda en el fondo
    cx, cy = ancho // 2, 520
    aura = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_aura = ImageDraw.Draw(aura)
    d_aura.ellipse([cx - 460, cy - 380, cx + 460, cy + 380], fill=(16, 185, 129, 35))
    aura = aura.filter(ImageFilter.GaussianBlur(90))
    frame = Image.alpha_composite(frame, aura)
    draw = ImageDraw.Draw(frame)

    # 2. Hero UI: Ventana Maximizada (1040px de ancho)
    wx, wy, ww, wh = 20, 70, ancho - 40, 75
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=16, fill=(15, 23, 42, 235), outline=(30, 41, 59), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 22, wy + 28, wx + 36 + idx_dot * 22, wy + 42], fill=(148, 163, 184))

    dibujar_chispa_ia(draw, wx + 110, wy + 37, 10, (16, 185, 129))
    header_tit = cfg.get("header", "GOOGLE NOTEBOOKLM • Asistente de tus Propios Archivos")
    draw.text((wx + 130, wy + 24), header_tit, fill=(241, 245, 249), font=obtener_fuente(24, bold=True))

    b_txt = cfg.get("badge", "✓ Tus Datos")
    draw.rounded_rectangle([wx + ww - 180, wy + 16, wx + ww - 18, wy + wh - 16], radius=10, fill=(16, 185, 129, 40), outline=(16, 185, 129), width=1)
    draw.text((wx + ww - 162, wy + 24), b_txt, fill=(52, 211, 153), font=obtener_fuente(20, bold=True))

    # 3. Documentos Subidos Panel
    fx, fy, fw, fh = 20, 165, ancho - 40, 85
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=16, fill=(17, 24, 39, 235), outline=(30, 41, 59), width=1)
    draw.text((fx + 24, fy + 30), "FUENTES SUBIDAS:", fill=(148, 163, 184), font=obtener_fuente(18, bold=True))

    docs = [("📄 informe_q3.pdf", (52, 211, 153)), ("📊 balance_anual.xlsx", (56, 189, 248)), ("📝 notas_estrategia.docx", (168, 85, 247))]
    dx_chip = fx + 200
    for d_txt, d_col in docs:
        bbox_d = draw.textbbox((0, 0), d_txt, font=obtener_fuente(18, bold=True))
        w_chip = bbox_d[2] - bbox_d[0] + 24
        draw.rounded_rectangle([dx_chip, fy + 20, dx_chip + w_chip, fy + fh - 20], radius=8, fill=(*d_col[:3], 35), outline=d_col, width=1)
        draw.text((dx_chip + 12, fy + 30), d_txt, fill=d_col, font=obtener_fuente(18, bold=True))
        dx_chip += w_chip + 12

    # 4. Prompt Bar interactivo
    px, py, pw, ph = 20, 265, ancho - 40, 95
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=18, fill=(15, 23, 42, 240), outline=(16, 185, 129), width=2)
    dibujar_chispa_ia(draw, px + 26, py + 30, 10, (16, 185, 129))
    draw.text((px + 48, py + 18), "Prompt:", fill=(52, 211, 153), font=obtener_fuente(24, bold=True))
    prompt_txt = cfg.get("titulo", "Resumí las obligaciones del contrato y los plazos")
    draw.text((px + 150, py + 18), f'"{prompt_txt}"', fill=(255, 255, 255), font=obtener_fuente(23, bold=False))

    draw.rounded_rectangle([px + 26, py + 56, px + 390, py + 86], radius=8, fill=(16, 185, 129, 35))
    dibujar_icono_check(draw, px + 38, py + 71, (16, 185, 129), tam=14, grosor=2)
    draw.text((px + 60, py + 62), "Respuesta restringida a tus documentos", fill=(52, 211, 153), font=obtener_fuente(18, bold=True))

    # 5. Tarjeta de Respuesta Estructurada (Limpia y legible en 1 segundo)
    rx, ry, rw, rh = 20, 375, ancho - 40, 325
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=20, fill=(15, 23, 42, 245), outline=(30, 41, 59), width=2)
    draw.text((rx + 30, ry + 26), "Extracción de tus Documentos:", fill=(52, 211, 153), font=obtener_fuente(24, bold=True))

    draw.text((rx + 30, ry + 75), "Resumen exacto sin inventar información", fill=(255, 255, 255), font=obtener_fuente(27, bold=True))
    draw.text((rx + 30, ry + 130), "Cita página y párrafo de cada archivo subido", fill=(226, 232, 240), font=obtener_fuente(25, bold=False))

    draw.rounded_rectangle([rx + 30, ry + 205, rx + 480, ry + 265], radius=12, fill=(16, 185, 129, 35), outline=(16, 185, 129), width=1)
    dibujar_icono_check(draw, rx + 52, ry + 235, (52, 211, 153), tam=14, grosor=2)
    draw.text((rx + 75, ry + 220), "Respuestas ancladas a tus archivos", fill=(52, 211, 153), font=obtener_fuente(22, bold=True))

    # 6. Hero UI: Píldora Única de Alto Impacto (Zona media-alta: NO tapa a Byte)
    pill_w = ancho - 80
    draw.rounded_rectangle([40, 720, 40 + pill_w, 795], radius=24, fill=(16, 185, 129, 45), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, 72, 757, (52, 211, 153), tam=16, grosor=3)
    draw.text((105, 739), "✓ Respuestas basadas 100% en tus archivos", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))

    # 7. Sprite de Byte en esquina inferior derecha (100% visible, sin banners encima)
    p_byte = cfg.get("sprite_byte")
    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 600
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = ancho - bw - 10
            by = alto - bh - 110 + int(6 * math.sin(t_sec * 3.0))
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 11. PLANO_BROWSER_TABS_CAOS: Navegador Real Saturado de 10 Pestañas, Popups y Cookies
# ---------------------------------------------------------------------------
def renderizar_plano_browser_tabs_caos(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "viaje_espacial")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)

    # 1. Alerta roja sutil de fondo
    pulso_alerta = math.sin(t_sec * 6.0) * 0.5 + 0.5
    r_glow = 460
    glow_img = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_glow = ImageDraw.Draw(glow_img)
    alpha_alerta = int(35 + 25 * pulso_alerta)
    d_glow.ellipse([ancho // 2 - r_glow, 450 - r_glow, ancho // 2 + r_glow, 450 + r_glow], fill=(225, 29, 72, alpha_alerta))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(90))
    frame = Image.alpha_composite(frame, glow_img)
    draw = ImageDraw.Draw(frame)

    # 2. Hero UI: Ventana del Navegador Web Saturado (1040px ancho)
    wx, wy, ww, wh = 20, 70, ancho - 40, 800
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=18, fill=(15, 23, 42, 245), outline=(225, 29, 72), width=2)

    # Barra de ventana superior con 3 puntos neutros
    draw.rounded_rectangle([wx, wy, wx + ww, wy + 55], radius=18, fill=(17, 24, 39))
    draw.line([(wx, wy + 55), (wx + ww, wy + 55)], fill=(30, 41, 59), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 20, wy + 18, wx + 34 + idx_dot * 20, wy + 30], fill=(148, 163, 184))

    # Barra de 10 Pestañas diminutas y colapsadas (Tab Overload)
    ty = wy + 56
    th = 48
    tab_w = (ww - 20) // 10
    nombres_tabs = ["Google", "Error 404", "Stack...", "Cookie...", "Blog 1", "Foro...", "Wiki", "Doc...", "Precios", "Lenta..."]
    for i, t_name in enumerate(nombres_tabs):
        tx = wx + 10 + i * tab_w
        is_active = (i == 3)
        tab_bg = (30, 41, 59) if not is_active else (225, 29, 72, 80)
        tab_border = (51, 65, 85) if not is_active else (225, 29, 72)
        draw.rounded_rectangle([tx, ty + 4, tx + tab_w - 4, ty + th], radius=6, fill=tab_bg, outline=tab_border, width=1)
        if i % 3 == 0:
            spin_rad = (t_sec * 8.0 + i) % (2 * math.pi)
            cx_s, cy_s = tx + 14, ty + 24
            draw.ellipse([cx_s - 5, cy_s - 5, cx_s + 5, cy_s + 5], outline=(245, 158, 11), width=2)
            draw.line([(cx_s, cy_s), (cx_s + int(5 * math.cos(spin_rad)), cy_s + int(5 * math.sin(spin_rad)))], fill=(245, 158, 11), width=2)
        elif i % 2 == 1:
            draw.text((tx + 8, ty + 15), "!", fill=(239, 68, 68), font=obtener_fuente(14, bold=True))
        else:
            draw.ellipse([tx + 10, ty + 20, tx + 18, ty + 28], fill=(56, 189, 248))
        draw.text((tx + 22, ty + 16), t_name[:5], fill=(226, 232, 240), font=obtener_fuente(13, bold=False))
        draw.text((tx + tab_w - 15, ty + 15), "×", fill=(148, 163, 184), font=obtener_fuente(14, bold=True))

    # Barra de URL del navegador
    uy = ty + th + 10
    draw.rounded_rectangle([wx + 20, uy, wx + ww - 20, uy + 48], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    draw.text((wx + 36, uy + 12), "🔒 https://www.google.com/search?q=como+resolver+esto+urgente", fill=(148, 163, 184), font=obtener_fuente(18, bold=False))

    # 3. Viewport Caótico de Búsqueda
    vy = uy + 65
    draw.rounded_rectangle([wx + 40, vy, wx + ww - 40, vy + 55], radius=10, fill=(225, 29, 72, 45), outline=(225, 29, 72), width=1)
    draw.text((wx + 60, vy + 14), "⚠️ ALERTA DE MEMORIA: 10 pestañas consumiendo 99% de RAM", fill=(254, 205, 211), font=obtener_fuente(20, bold=True))

    cy_pop = vy + 75
    draw.rounded_rectangle([wx + 40, cy_pop, wx + ww - 40, cy_pop + 130], radius=14, fill=(17, 24, 39, 250), outline=(245, 158, 11), width=2)
    draw.text((wx + 65, cy_pop + 20), "🍪 ACEPTAR COOKIES PARA VER EL ARTÍCULO", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.text((wx + 65, cy_pop + 55), "Para continuar leyendo debe aceptar 184 socios de rastreo y publicidad.", fill=(148, 163, 184), font=obtener_fuente(18, bold=False))
    draw.rounded_rectangle([wx + 65, cy_pop + 85, wx + 260, cy_pop + 120], radius=6, fill=(245, 158, 11))
    draw.text((wx + 85, cy_pop + 92), "ACEPTAR TODO", fill=(15, 23, 42), font=obtener_fuente(16, bold=True))
    draw.rounded_rectangle([wx + 280, cy_pop + 85, wx + 440, cy_pop + 120], radius=6, fill=(51, 65, 85))
    draw.text((wx + 300, cy_pop + 92), "CONFIGURAR", fill=(255, 255, 255), font=obtener_fuente(16, bold=False))

    ry = cy_pop + 150
    draw.rounded_rectangle([wx + 40, ry, wx + ww - 40, ry + 110], radius=12, fill=(30, 41, 59, 180), outline=(71, 85, 105), width=1)
    draw.text((wx + 65, ry + 16), "Anuncio • Patrocinado", fill=(100, 116, 139), font=obtener_fuente(16, bold=True))
    draw.text((wx + 65, ry + 42), "Comprá este software para arreglar tus errores de oficina", fill=(56, 189, 248), font=obtener_fuente(22, bold=True))
    draw.text((wx + 65, ry + 75), "Página con 15 banners publicitarios y ninguna respuesta concreta...", fill=(148, 163, 184), font=obtener_fuente(18, bold=False))

    badge_txt = cfg.get("badge", "POV: 10 PESTAÑAS ABIERTAS")
    f_badge = obtener_fuente(22, bold=True)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=f_badge)
    bw_badge = max(400, bbox_b[2] - bbox_b[0] + 80)
    draw.rounded_rectangle([(ancho - bw_badge) // 2, 10, (ancho + bw_badge) // 2, 58], radius=24, fill=(225, 29, 72, 235), outline=(254, 205, 211), width=2)
    draw.text(((ancho - bw_badge) // 2 + 40, 20), badge_txt, fill=(255, 255, 255), font=f_badge)

    # 4. Byte Protagonista Abajo en el Centro
    p_byte = cfg.get("sprite_byte")
    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 650
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            shake_x = int(3 * math.sin(t_sec * 30.0))
            by = 1200 + shake_x
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 12. PLANO_SINGLE_TAB_ZEN: Resultado con 1 Sola Pestaña Limpia y Cero Pestañas Perdidas
# ---------------------------------------------------------------------------
def renderizar_plano_single_tab_zen(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "viaje_espacial")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)

    # 1. Aura verde esmeralda y cian de alivio y victoria
    cx, cy = ancho // 2, 520
    aura = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_aura = ImageDraw.Draw(aura)
    d_aura.ellipse([cx - 460, cy - 380, cx + 460, cy + 380], fill=(16, 185, 129, 40))
    aura = aura.filter(ImageFilter.GaussianBlur(95))
    frame = Image.alpha_composite(frame, aura)
    draw = ImageDraw.Draw(frame)

    # 2. Navegador Web Zen: EXACTAMENTE UNA SOLA PESTAÑA LIMPIA (Compactado a 580px)
    wx, wy, ww, wh = 20, 70, ancho - 40, 580
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=20, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)

    # Barra superior con 3 puntos neutros
    draw.rounded_rectangle([wx, wy, wx + ww, wy + 52], radius=20, fill=(17, 24, 39))
    draw.line([(wx, wy + 52), (wx + ww, wy + 52)], fill=(30, 41, 59), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 24 + idx_dot * 22, wy + 19, wx + 38 + idx_dot * 22, wy + 33], fill=(148, 163, 184))

    # LA ÚNICA PESTAÑA (Elegante y destacada)
    tab_w = 440
    draw.rounded_rectangle([wx + 100, wy + 8, wx + 100 + tab_w, wy + 51], radius=10, fill=(16, 185, 129, 45), outline=(16, 185, 129), width=1)
    dibujar_icono_check(draw, wx + 120, wy + 30, (52, 211, 153), tam=14, grosor=2)
    draw.text((wx + 145, wy + 17), "✓ 1 Pestaña • Respuesta Encontrada", fill=(255, 255, 255), font=obtener_fuente(20, bold=True))

    # Barra de búsqueda limpia
    uy = wy + 68
    draw.rounded_rectangle([wx + 30, uy, wx + ww - 30, uy + 48], radius=12, fill=(30, 41, 59), outline=(16, 185, 129), width=1)
    draw.text((wx + 55, uy + 12), "🔒 https://perplexity.ai/search/respuesta-verificada", fill=(52, 211, 153), font=obtener_fuente(19, bold=True))

    # Contenedor central de victoria
    vy = uy + 62
    draw.rounded_rectangle([wx + 30, vy, wx + ww - 30, vy + 375], radius=18, fill=(17, 24, 39, 230), outline=(30, 41, 59), width=1)

    # Gran Checkmark animado
    pulso_ok = math.sin(t_sec * 3.0) * 0.1 + 0.95
    r_c = int(38 * pulso_ok)
    cx_c, cy_c = ancho // 2, vy + 58
    draw.ellipse([cx_c - r_c, cy_c - r_c, cx_c + r_c, cy_c + r_c], fill=(16, 185, 129, 40), outline=(16, 185, 129), width=3)
    dibujar_icono_check(draw, cx_c - 14, cy_c - 2, (52, 211, 153), tam=24, grosor=4)

    draw.text((ancho // 2 - 245, vy + 112), "RESPUESTA RESUELTA AL TOQUE", fill=(255, 255, 255), font=obtener_fuente(27, bold=True))
    draw.text((ancho // 2 - 200, vy + 152), "Cero pestañas acumuladas • Cero anuncios", fill=(148, 163, 184), font=obtener_fuente(20, bold=False))

    draw.rounded_rectangle([wx + 50, vy + 190, wx + ww - 50, vy + 295], radius=12, fill=(30, 41, 59, 200), outline=(52, 211, 153), width=1)
    dibujar_chispa_ia(draw, wx + 80, vy + 242, 12, (52, 211, 153))
    draw.text((wx + 105, vy + 210), "Búsqueda precisa y directa con Perplexity", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.text((wx + 105, vy + 248), "Tus documentos sintetizados con NotebookLM", fill=(148, 163, 184), font=obtener_fuente(19, bold=False))

    draw.rounded_rectangle([wx + 50, vy + 315, wx + 380, vy + 358], radius=10, fill=(16, 185, 129, 35))
    draw.text((wx + 75, vy + 325), "✓ Tarde salvada sin rodeos", fill=(52, 211, 153), font=obtener_fuente(19, bold=True))

    # 3. Hero UI: Píldora Única de Alto Impacto (Ubicada en y=675..750, arriba de los subtítulos)
    pill_w = ancho - 80
    draw.rounded_rectangle([40, 675, 40 + pill_w, 750], radius=24, fill=(16, 185, 129, 45), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, 75, 712, (52, 211, 153), tam=16, grosor=3)
    draw.text((110, 694), "✓ De 10 pestañas caóticas a 1 sola respuesta", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))

    # 4. Byte Zen / Victorioso (100% visible y libre de banners)
    p_byte = cfg.get("sprite_byte")
    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 650
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            by = 1180 + int(8 * math.sin(t_sec * 2.0))
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 13. PLANO_BATTLE_VS: Battle Card de Enfrentamiento (Team 50 Pestañas vs Team 1 Clic)
# ---------------------------------------------------------------------------
def renderizar_plano_battle_vs(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "viaje_espacial")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. Título Superior Estilo Debate
    # 1. Título Superior Estilo Debate
    draw.rounded_rectangle([40, 70, ancho - 40, 190], radius=20, fill=(15, 23, 42, 240), outline=(56, 189, 248), width=2)
    dibujar_chispa_ia(draw, 75, 115, 12, (56, 189, 248))
    tit_debate = cfg.get("header_debate", "DEBATE A LA COMUNIDAD:")
    draw.text((105, 95), tit_debate, fill=(56, 189, 248), font=obtener_fuente(22, bold=True))
    preg_debate = cfg.get("pregunta_debate", "¿Sos Team 50 pestañas o Team 1 clic?")
    draw.text((60, 135), preg_debate, fill=(255, 255, 255), font=obtener_fuente(28, bold=True))

    # 2. Las Dos Tarjetas de Batalla Lado a Lado (Card VS)
    y_card = 220
    h_card = 460
    w_card = (ancho - 100) // 2

    # Lado Izquierdo: Rojo
    x_izq = 40
    tit_izq = cfg.get("titulo_izq", "TEAM 50 PESTAÑAS")
    draw.rounded_rectangle([x_izq, y_card, x_izq + w_card, y_card + h_card], radius=22, fill=(15, 23, 42, 245), outline=(225, 29, 72), width=2)
    draw.rounded_rectangle([x_izq + 15, y_card + 15, x_izq + w_card - 15, y_card + 75], radius=12, fill=(225, 29, 72))
    draw.text((x_izq + 30, y_card + 28), tit_izq, fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    items_izq = cfg.get("items_izq", [
        "• Mil pestañas abiertas",
        "• Saltando de link en link",
        "• Publicidad invasiva",
        "• Horas buscando sin fin"
    ])
    for idx_i, txt_i in enumerate(items_izq):
        draw.text((x_izq + 25, y_card + 115 + idx_i * 74), txt_i, fill=(254, 205, 211), font=obtener_fuente(22, bold=False))

    # Lado Derecho: Verde
    x_der = x_izq + w_card + 20
    tit_der = cfg.get("titulo_der", "TEAM 1 CLIC")
    draw.rounded_rectangle([x_der, y_card, x_der + w_card, y_card + h_card], radius=22, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    draw.rounded_rectangle([x_der + 15, y_card + 15, x_der + w_card - 15, y_card + 75], radius=12, fill=(16, 185, 129))
    draw.text((x_der + 30, y_card + 28), tit_der, fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    items_der = cfg.get("items_der", [
        "• Perplexity directo",
        "• Citas verificadas",
        "• NotebookLM con tus notas",
        "• Menos alucinaciones"
    ])
    for idx_d, txt_d in enumerate(items_der):
        draw.text((x_der + 25, y_card + 115 + idx_d * 74), txt_d, fill=(167, 243, 208), font=obtener_fuente(22, bold=False))

    # Escudo Central "VS"
    cx_vs, cy_vs = ancho // 2, y_card + h_card // 2
    r_vs = 48
    draw.ellipse([cx_vs - r_vs, cy_vs - r_vs, cx_vs + r_vs, cy_vs + r_vs], fill=(15, 23, 42), outline=(234, 179, 8), width=3)
    draw.text((cx_vs - 24, cy_vs - 20), "VS", fill=(234, 179, 8), font=obtener_fuente(34, bold=True))

    # 3. Floating Callout (Ubicado en y=710..785, debajo de las cards y encima de los subtítulos)
    draw.rounded_rectangle([ancho // 2 - 280, 710, ancho // 2 + 280, 785], radius=24, fill=(15, 23, 42, 245), outline=(234, 179, 8), width=2)
    dibujar_chispa_ia(draw, ancho // 2 - 250, 747, 10, (234, 179, 8))
    draw.text((ancho // 2 - 225, 732), "¿De qué lado estás? Votá en comentarios", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # 4. Byte Host en el Centro Señalando (100% visible, sin banners encima)
    p_byte = cfg.get("sprite_byte")
    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 620
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            by = 1180 + int(6 * math.sin(t_sec * 3.0))
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 14. PLANO_FLYER_PAINT_CAOS: Gancho de Alerta y Flyer Amateur Satírico (Paint/Word)
# ---------------------------------------------------------------------------
def renderizar_plano_flyer_paint_caos(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. STICKER TITULAR HOOK (Pattern Interrupt en los primeros 2 segundos para Facebook/TikTok)
    pulso_alerta = 0.5 + 0.5 * math.sin(t_sec * 6.0)
    col_borde = (255, 255, 255) if pulso_alerta > 0.5 else (244, 63, 94)

    # Pastilla superior Alerta
    draw.rounded_rectangle([ancho // 2 - 240, 70, ancho // 2 + 240, 118], radius=12, fill=(225, 29, 72), outline=col_borde, width=2)
    dibujar_icono_alerta(draw, ancho // 2 - 180, 94, tam=10, color=(255, 255, 255))
    draw.text((ancho // 2 - 158, 82), "ALERTA DE DISEÑO URGENTE", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    # Titular Hook prominente en mayúsculas
    badge_txt = cfg.get("badge", "POV: NECESITÁS UN FLYER YA")
    draw.rounded_rectangle([40, 130, ancho - 40, 205], radius=16, fill=(15, 23, 42, 250), outline=(225, 29, 72), width=2)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=obtener_fuente(28, bold=True))
    bw_txt = bbox_b[2] - bbox_b[0]
    draw.text(((ancho - bw_txt) // 2, 150), badge_txt, fill=(255, 245, 0), font=obtener_fuente(28, bold=True))

    # 2. VENTANA DEL FLYER AMATEUR (El dolor relatable de oficina / Paint)
    wx, wy, ww, wh = 20, 220, ancho - 40, 480
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=18, fill=(30, 41, 59, 245), outline=(71, 85, 105), width=2)

    # Barra de título de programa antiguo
    draw.rounded_rectangle([wx, wy, wx + ww, wy + 45], radius=18, fill=(15, 23, 42))
    draw.line([(wx, wy + 45), (wx + ww, wy + 45)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 20, wy + 16, wx + 34 + idx_dot * 20, wy + 28], fill=(148, 163, 184))
    draw.text((wx + 100, wy + 14), "ProgramaDeDiseño_SinTitulo.exe (No responde)", fill=(203, 213, 225), font=obtener_fuente(18, bold=True))

    # Lienzo del flyer cómico
    lx, ly, lw, lh = wx + 30, wy + 65, ww - 60, wh - 85
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=12, fill=(254, 240, 138), outline=(234, 179, 8), width=2)

    # Texto cómico amateur desalineado
    draw.text((lx + 40, ly + 25), "GRAN EVENTO IMPERDIBLE", fill=(225, 29, 72), font=obtener_fuente(32, bold=True))
    draw.text((lx + 40, ly + 75), "Comprá acá las mejores cosas de la vida", fill=(30, 58, 138), font=obtener_fuente(22, bold=True))
    draw.text((lx + 40, ly + 115), "Vení con tu familia • Traé a tus amigos • No faltes", fill=(71, 85, 105), font=obtener_fuente(20, bold=False))

    # Cartel de explosión / WordArt falso
    draw.rounded_rectangle([lx + lw - 260, ly + 160, lx + lw - 30, ly + 250], radius=10, fill=(239, 68, 68), outline=(255, 255, 255), width=2)
    draw.text((lx + lw - 240, ly + 175), "¡¡SUPER OFERTA!!", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))
    draw.text((lx + lw - 225, ly + 210), "100% GARANTIZADO", fill=(254, 240, 138), font=obtener_fuente(18, bold=True))

    # Error sticker / aviso de colapso
    draw.rounded_rectangle([lx + 30, ly + 175, lx + 390, ly + 250], radius=10, fill=(15, 23, 42, 240), outline=(225, 29, 72), width=2)
    dibujar_icono_cruz(draw, lx + 48, ly + 200, tam=7, color=(244, 63, 94), grosor=2)
    draw.text((lx + 65, ly + 188), "Error: Tipografía desalineada", fill=(244, 63, 94), font=obtener_fuente(18, bold=True))
    dibujar_icono_cruz(draw, lx + 48, ly + 227, tam=7, color=(244, 63, 94), grosor=2)
    draw.text((lx + 65, ly + 215), "Foto pixelada con fondo blanco", fill=(244, 63, 94), font=obtener_fuente(18, bold=True))

    # SELLO ROJO EN DIAGONAL: "POR FAVOR DEJÁ DE HACER ESTO"
    stamp_w, stamp_h = 620, 95
    stamp = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
    d_s = ImageDraw.Draw(stamp)
    d_s.rounded_rectangle([0, 0, stamp_w, stamp_h], radius=14, fill=(225, 29, 72, 240), outline=(255, 255, 255), width=3)
    d_s.text((28, 26), "POR FAVOR DEJÁ DE HACER ESTO", fill=(255, 255, 255), font=obtener_fuente(30, bold=True))
    stamp_rot = stamp.rotate(-6, resample=Image.Resampling.BILINEAR, expand=True)
    frame.paste(stamp_rot, (ancho // 2 - stamp_rot.width // 2, wy + 260), stamp_rot)

    # 3. PÍLDORA FLOTANTE (Zona y = 720..795, justo debajo de ventana y arriba de subtítulos)
    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(225, 29, 72), width=2)
    dibujar_icono_alerta(draw, 75, 757, tam=14, color=(225, 29, 72))
    draw.text((105, 742), "El diseño amateur espanta a tus clientes", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # 4. BYTE CORTOCIRCUITO (100% libre en y = 1180..1850)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 600
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            shake_x = int(4 * math.sin(t_sec * 28.0))
            by = 1200 + shake_x
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 15. PLANO_CANVA_MAGIC_DESIGN: Canva AI con Prompt y Generación de Flyers
# ---------------------------------------------------------------------------
def renderizar_plano_canva_magic_design(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. Ventana Canva Hero UI (1040px)
    wx, wy, ww, wh = 20, 70, ancho - 40, 75
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=16, fill=(15, 23, 42, 235), outline=(139, 92, 246), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 22, wy + 28, wx + 36 + idx_dot * 22, wy + 42], fill=(148, 163, 184))

    dibujar_chispa_ia(draw, wx + 110, wy + 37, 10, (139, 92, 246))
    draw.text((wx + 130, wy + 24), "CANVA • Magic Design con Inteligencia Artificial", fill=(241, 245, 249), font=obtener_fuente(23, bold=True))

    draw.rounded_rectangle([wx + ww - 180, wy + 16, wx + ww - 18, wy + wh - 16], radius=10, fill=(139, 92, 246, 40), outline=(139, 92, 246), width=1)
    dibujar_chispa_ia(draw, wx + ww - 158, wy + 37, 8, (192, 132, 252))
    draw.text((wx + ww - 142, wy + 24), "Generador IA", fill=(192, 132, 252), font=obtener_fuente(20, bold=True))

    # 2. Prompt Bar interactivo
    px, py, pw, ph = 20, 165, ancho - 40, 105
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=18, fill=(15, 23, 42, 240), outline=(139, 92, 246), width=2)
    dibujar_chispa_ia(draw, px + 26, py + 32, 10, (192, 132, 252))
    draw.text((px + 48, py + 20), "Prompt:", fill=(192, 132, 252), font=obtener_fuente(24, bold=True))
    draw.text((px + 150, py + 20), '"Flyer moderno para evento de café especial"', fill=(255, 255, 255), font=obtener_fuente(23, bold=False))

    draw.rounded_rectangle([px + 26, py + 62, px + 520, py + 95], radius=8, fill=(139, 92, 246, 35))
    dibujar_icono_check(draw, px + 38, py + 78, (192, 132, 252), tam=14, grosor=2)
    draw.text((px + 60, py + 68), "Generando 3 propuestas de diseño automáticas", fill=(216, 180, 254), font=obtener_fuente(18, bold=True))

    # 3. Dos propuestas de Flyers Profesionales lado a lado (Resultados de Canva)
    cx_card = 20
    cy_card = 285
    cw_card = (ancho - 60) // 2
    ch_card = 415

    # Propuesta 1: Espresso Minimal
    draw.rounded_rectangle([cx_card, cy_card, cx_card + cw_card, cy_card + ch_card], radius=18, fill=(26, 18, 14, 245), outline=(217, 119, 6), width=2)
    draw.rounded_rectangle([cx_card + 15, cy_card + 15, cx_card + cw_card - 15, cy_card + 190], radius=12, fill=(45, 27, 21))
    draw.text((cx_card + 35, cy_card + 50), "SPECIALTY", fill=(251, 191, 36), font=obtener_fuente(24, bold=True))
    draw.text((cx_card + 35, cy_card + 85), "COFFEE FEST", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))
    draw.text((cx_card + 35, cy_card + 140), "VIERNES 18 HS • ENTRADA LIBRE", fill=(214, 211, 209), font=obtener_fuente(17, bold=False))
    draw.text((cx_card + 20, cy_card + 220), "• Layout y tipografías pro", fill=(245, 245, 244), font=obtener_fuente(20, bold=False))
    draw.text((cx_card + 20, cy_card + 265), "• Paleta café y ámbar lista", fill=(245, 245, 244), font=obtener_fuente(20, bold=False))
    draw.rounded_rectangle([cx_card + 20, cy_card + 330, cx_card + cw_card - 20, cy_card + 385], radius=10, fill=(217, 119, 6, 40), outline=(217, 119, 6), width=1)
    dibujar_icono_check(draw, cx_card + 45, cy_card + 355, (251, 191, 36), tam=14, grosor=2)
    draw.text((cx_card + 70, cy_card + 345), "Opción 1 (Elegante)", fill=(251, 191, 36), font=obtener_fuente(20, bold=True))

    # Propuesta 2: Neon Latte Art
    cx2 = cx_card + cw_card + 20
    draw.rounded_rectangle([cx2, cy_card, cx2 + cw_card, cy_card + ch_card], radius=18, fill=(19, 21, 38, 245), outline=(139, 92, 246), width=2)
    draw.rounded_rectangle([cx2 + 15, cy_card + 15, cx2 + cw_card - 15, cy_card + 190], radius=12, fill=(35, 28, 66))
    draw.text((cx2 + 35, cy_card + 50), "COFFEE & CODE", fill=(236, 72, 153), font=obtener_fuente(24, bold=True))
    draw.text((cx2 + 35, cy_card + 85), "WORKSHOP 2026", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))
    draw.text((cx2 + 35, cy_card + 140), "CUPOS LIMITADOS • REGISTRATE", fill=(226, 232, 240), font=obtener_fuente(17, bold=False))
    draw.text((cx2 + 20, cy_card + 220), "• Formato para historias y feed", fill=(245, 245, 244), font=obtener_fuente(20, bold=False))
    draw.text((cx2 + 20, cy_card + 265), "• Gráficos vectoriales IA", fill=(245, 245, 244), font=obtener_fuente(20, bold=False))
    draw.rounded_rectangle([cx2 + 20, cy_card + 330, cx2 + cw_card - 20, cy_card + 385], radius=10, fill=(139, 92, 246, 40), outline=(139, 92, 246), width=1)
    dibujar_icono_check(draw, cx2 + 45, cy_card + 355, (192, 132, 252), tam=14, grosor=2)
    draw.text((cx2 + 70, cy_card + 345), "Opción 2 (Moderno)", fill=(192, 132, 252), font=obtener_fuente(20, bold=True))

    # 4. PÍLDORA FLOTANTE (Zona media-alta: NO tapa a Byte)
    pill_w = ancho - 80
    draw.rounded_rectangle([40, 720, 40 + pill_w, 795], radius=24, fill=(15, 23, 42, 245), outline=(139, 92, 246), width=2)
    dibujar_chispa_ia(draw, 72, 757, 14, (192, 132, 252))
    draw.text((105, 739), "De una simple idea a flyer listo", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))

    # 5. Sprite de Byte en esquina inferior derecha
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 600
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = ancho - bw - 10
            by = alto - bh - 110 + int(6 * math.sin(t_sec * 3.0))
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 16. PLANO_REMOVE_BG: Recorte Inteligente de Fondos en 1 Segundo
# ---------------------------------------------------------------------------
def renderizar_plano_remove_bg(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. Ventana Remove.bg Hero UI
    wx, wy, ww, wh = 20, 70, ancho - 40, 75
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=16, fill=(15, 23, 42, 235), outline=(56, 189, 248), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 22, wy + 28, wx + 36 + idx_dot * 22, wy + 42], fill=(148, 163, 184))

    dibujar_chispa_ia(draw, wx + 110, wy + 37, 10, (56, 189, 248))
    draw.text((wx + 130, wy + 24), "REMOVE.BG • Recorte Automático de Fotos con IA", fill=(241, 245, 249), font=obtener_fuente(23, bold=True))

    draw.rounded_rectangle([wx + ww - 180, wy + 16, wx + ww - 18, wy + wh - 16], radius=10, fill=(56, 189, 248, 40), outline=(56, 189, 248), width=1)
    dibujar_icono_check(draw, wx + ww - 160, wy + 32, (56, 189, 248), tam=12, grosor=2)
    draw.text((wx + ww - 140, wy + 24), "1 Segundo", fill=(56, 189, 248), font=obtener_fuente(20, bold=True))

    # 2. Before / After Split Panel (Foto con fondo caótico vs PNG Transparente)
    bx, by, bw, bh = 20, 165, ancho - 40, 535
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=(15, 23, 42, 245), outline=(30, 41, 59), width=2)

    half_w = (bw - 30) // 2

    # Lado Izquierdo: ANTES (Foto con fondo molesto)
    x_izq = bx + 15
    draw.rounded_rectangle([x_izq, by + 15, x_izq + half_w, by + bh - 15], radius=14, fill=(45, 55, 72))
    draw.rounded_rectangle([x_izq + 20, by + 30, x_izq + half_w - 20, by + 80], radius=8, fill=(225, 29, 72, 40), outline=(225, 29, 72), width=1)
    dibujar_icono_cruz(draw, x_izq + 38, by + 55, tam=8, color=(244, 63, 94), grosor=2)
    draw.text((x_izq + 55, by + 42), "ANTES: Fondo desordenado", fill=(244, 63, 94), font=obtener_fuente(20, bold=True))

    # Dibujar taza de café con fondo feo simulado
    cx_taza_izq = x_izq + half_w // 2
    cy_taza = by + bh // 2 + 10
    draw.rectangle([x_izq + 30, cy_taza - 120, x_izq + half_w - 30, cy_taza + 120], fill=(71, 85, 105))
    draw.ellipse([cx_taza_izq - 80, cy_taza - 40, cx_taza_izq + 80, cy_taza + 70], fill=(180, 83, 9))
    draw.ellipse([cx_taza_izq - 60, cy_taza - 30, cx_taza_izq + 60, cy_taza + 10], fill=(251, 191, 36))
    draw.text((x_izq + 50, by + bh - 70), "Fondo gris difícil de borrar", fill=(203, 213, 225), font=obtener_fuente(18, bold=False))

    # Lado Derecho: DESPUÉS (Cuadrícula de ajedrez PNG transparente y taza limpia)
    x_der = x_izq + half_w + 10
    draw.rounded_rectangle([x_der, by + 15, x_der + half_w, by + bh - 15], radius=14, fill=(255, 255, 255))

    # Cuadrícula PNG de ajedrez
    tam_check = 16
    for gx in range(x_der, x_der + half_w, tam_check):
        for gy in range(by + 15, by + bh - 15, tam_check):
            if ((gx - x_der) // tam_check + (gy - (by + 15)) // tam_check) % 2 == 0:
                draw.rectangle([gx, gy, min(gx + tam_check, x_der + half_w), min(gy + tam_check, by + bh - 15)], fill=(226, 232, 240))

    # Taza nítida sin fondo
    cx_taza_der = x_der + half_w // 2
    draw.ellipse([cx_taza_der - 80, cy_taza - 40, cx_taza_der + 80, cy_taza + 70], fill=(180, 83, 9))
    draw.ellipse([cx_taza_der - 60, cy_taza - 30, cx_taza_der + 60, cy_taza + 10], fill=(251, 191, 36))
    draw.ellipse([cx_taza_der - 70, cy_taza + 60, cx_taza_der + 70, cy_taza + 85], fill=(100, 116, 139, 90))

    draw.rounded_rectangle([x_der + 20, by + 30, x_der + half_w - 20, by + 80], radius=8, fill=(16, 185, 129, 230))
    dibujar_icono_check(draw, x_der + 40, by + 55, (255, 255, 255), tam=16, grosor=2)
    draw.text((x_der + 65, by + 42), "DESPUÉS: PNG Transparente", fill=(255, 255, 255), font=obtener_fuente(20, bold=True))
    draw.text((x_der + 50, by + bh - 70), "Listo para soltar en tu flyer", fill=(15, 23, 42), font=obtener_fuente(18, bold=True))

    # Haz láser divisor vertical en escaneo
    x_laser = x_der - 5
    pulso_laser = 0.5 + 0.5 * math.sin(t_sec * 5.0)
    alpha_l = int(180 + pulso_laser * 75)
    draw.line([(x_laser, by + 15), (x_laser, by + bh - 15)], fill=(56, 189, 248, alpha_l), width=4)

    # 3. PÍLDORA FLOTANTE (Zona media-alta: NO tapa a Byte)
    pill_w = ancho - 80
    draw.rounded_rectangle([40, 720, 40 + pill_w, 795], radius=24, fill=(15, 23, 42, 245), outline=(56, 189, 248), width=2)
    dibujar_icono_check(draw, 72, 757, (56, 189, 248), tam=16, grosor=3)
    draw.text((105, 739), "Recorte automático con fondo transparente", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))

    # 4. Byte Mago Zen en esquina inferior derecha
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 600
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = ancho - bw - 10
            by = alto - bh - 110 + int(6 * math.sin(t_sec * 3.0))
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 17. PLANO_FLYER_SHOWCASE_ZEN: Flyer Profesional Terminado y Alivio Total
# ---------------------------------------------------------------------------
def renderizar_plano_flyer_showcase_zen(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. Aura verde esmeralda y violeta de victoria y alivio
    cx, cy = ancho // 2, 520
    aura = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_aura = ImageDraw.Draw(aura)
    d_aura.ellipse([cx - 460, cy - 380, cx + 460, cy + 380], fill=(16, 185, 129, 35))
    aura = aura.filter(ImageFilter.GaussianBlur(95))
    frame = Image.alpha_composite(frame, aura)
    draw = ImageDraw.Draw(frame)

    # 2. Showcase del Flyer Final (580px de alto, y = 70..650)
    wx, wy, ww, wh = 40, 70, ancho - 80, 580
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=22, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)

    # Flyer interior enmarcado
    fx, fy, fw, fh = wx + 30, wy + 25, ww - 60, wh - 110
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=16, fill=(28, 20, 16), outline=(251, 191, 36), width=2)

    # Encabezado del flyer final
    draw.text((fx + 40, fy + 35), "COFFEE & CODE FESTIVAL", fill=(251, 191, 36), font=obtener_fuente(30, bold=True))
    draw.text((fx + 40, fy + 80), "VIERNES • 18:00 HS • CENTRO TECH", fill=(245, 245, 244), font=obtener_fuente(22, bold=False))

    # Badge destacado
    draw.rounded_rectangle([fx + 40, fy + 125, fx + 260, fy + 175], radius=10, fill=(16, 185, 129))
    draw.text((fx + 55, fy + 138), "ENTRADA GRATUITA", fill=(255, 255, 255), font=obtener_fuente(20, bold=True))

    # Taza nítida integrada
    draw.ellipse([fx + fw - 220, fy + 180, fx + fw - 60, fy + 300], fill=(217, 119, 6))
    draw.ellipse([fx + fw - 200, fy + 195, fx + fw - 80, fy + 240], fill=(254, 240, 138))

    # Sello Verde Gigante de Éxito
    stamp_w, stamp_h = 560, 85
    stamp = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
    d_s = ImageDraw.Draw(stamp)
    d_s.rounded_rectangle([0, 0, stamp_w, stamp_h], radius=14, fill=(16, 185, 129, 240), outline=(255, 255, 255), width=3)
    dibujar_icono_check(d_s, 40, 42, (255, 255, 255), tam=24, grosor=4)
    d_s.text((80, 24), "FLYER LISTO PARA PUBLICAR", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))
    stamp_rot = stamp.rotate(-4, resample=Image.Resampling.BILINEAR, expand=True)
    frame.paste(stamp_rot, (ancho // 2 - stamp_rot.width // 2, wy + 320), stamp_rot)

    # Badges de alivio
    draw.rounded_rectangle([wx + 30, wy + wh - 70, wx + 310, wy + wh - 18], radius=12, fill=(30, 41, 59, 220), outline=(52, 211, 153), width=1)
    dibujar_icono_check(draw, wx + 45, wy + wh - 48, (52, 211, 153), tam=12, grosor=2)
    draw.text((wx + 65, wy + wh - 55), "Sin programas difíciles", fill=(52, 211, 153), font=obtener_fuente(20, bold=True))

    draw.rounded_rectangle([wx + ww - 310, wy + wh - 70, wx + ww - 30, wy + wh - 18], radius=12, fill=(30, 41, 59, 220), outline=(56, 189, 248), width=1)
    dibujar_chispa_ia(draw, wx + ww - 290, wy + wh - 45, 8, (56, 189, 248))
    draw.text((wx + ww - 272, wy + wh - 55), "Armado en 3 minutos", fill=(56, 189, 248), font=obtener_fuente(20, bold=True))

    # 3. PÍLDORA FLOTANTE (y = 675..750)
    pill_w = ancho - 80
    draw.rounded_rectangle([40, 675, 40 + pill_w, 750], radius=24, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, 75, 712, (52, 211, 153), tam=16, grosor=3)
    draw.text((110, 694), "Diseño listo sin pagar de más ni perder la tarde", fill=(255, 255, 255), font=obtener_fuente(27, bold=True))

    # 4. Byte Zen flotando en paz
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "resultado_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 650
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            flotacion = int(8 * math.sin(t_sec * 2.0))
            by = 1180 + flotacion
            frame.paste(b_resized, (bx, by), b_resized)

    return frame



# ---------------------------------------------------------------------------
# 18. PLANO_CHAT_FLYER_URGENTE: Notificación Urgente de Cliente (WhatsApp/Slack)
# ---------------------------------------------------------------------------
def renderizar_plano_chat_flyer_urgente(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 3.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    pulso = 0.5 + 0.5 * math.sin(t_sec * 6.0)
    col_borde = (255, 255, 255) if pulso > 0.5 else (244, 63, 94)
    draw.rounded_rectangle([ancho // 2 - 250, 70, ancho // 2 + 250, 118], radius=12, fill=(225, 29, 72), outline=col_borde, width=2)
    dibujar_icono_alerta(draw, ancho // 2 - 190, 94, tam=10, color=(255, 255, 255))
    draw.text((ancho // 2 - 168, 82), "PEDIDO URGENTE • 17:59 HS", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    badge_txt = cfg.get("badge", "POV: NECESITÁS UN FLYER URGENTE")
    draw.rounded_rectangle([40, 130, ancho - 40, 205], radius=16, fill=(15, 23, 42, 250), outline=(225, 29, 72), width=2)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=obtener_fuente(28, bold=True))
    bw_txt = bbox_b[2] - bbox_b[0]
    draw.text(((ancho - bw_txt) // 2, 150), badge_txt, fill=(255, 245, 0), font=obtener_fuente(28, bold=True))

    wx, wy, ww, wh = 30, 225, ancho - 60, 475
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=20, fill=(15, 23, 42, 245), outline=(71, 85, 105), width=2)

    draw.rounded_rectangle([wx, wy, wx + ww, wy + 65], radius=20, fill=(30, 41, 59))
    draw.line([(wx, wy + 65), (wx + ww, wy + 65)], fill=(51, 65, 85), width=2)
    draw.ellipse([wx + 25, wy + 12, wx + 67, wy + 54], fill=(225, 29, 72))
    draw.text((wx + 34, wy + 20), "JM", fill=(255, 255, 255), font=obtener_fuente(20, bold=True))
    draw.text((wx + 80, wy + 14), "Jefe de Marketing • Cliente", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))
    draw.ellipse([wx + 82, wy + 42, wx + 92, wy + 52], fill=(34, 197, 94))
    draw.text((wx + 100, wy + 38), "En línea • Escribiendo...", fill=(148, 163, 184), font=obtener_fuente(16, bold=False))

    bx, by, bw, bh = wx + 35, wy + 90, ww - 70, 185
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=16, fill=(20, 83, 45, 240), outline=(34, 197, 94), width=2)
    draw.text((bx + 25, by + 20), "Che Max, ¿tenés el flyer para el evento de hoy?", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))
    draw.text((bx + 25, by + 65), "¡Lo necesito urgente antes de las 18:00 hs!", fill=(254, 240, 138), font=obtener_fuente(24, bold=True))
    draw.text((bx + 25, by + 110), "Tiene que verse profesional y con las fotos sin fondo.", fill=(220, 252, 231), font=obtener_fuente(20, bold=False))
    draw.text((bx + bw - 145, by + bh - 32), "17:58 hs • Leído", fill=(134, 239, 172), font=obtener_fuente(16, bold=True))

    tx, ty, tw, th = wx + 35, wy + 295, ww - 70, 155
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=14, fill=(30, 41, 59, 240), outline=(239, 68, 68), width=2)
    dibujar_icono_alerta(draw, tx + 40, ty + 45, tam=18, color=(239, 68, 68))
    draw.text((tx + 75, ty + 25), "TIEMPO LÍMITE: MENOS DE 1 HORA", fill=(248, 113, 113), font=obtener_fuente(22, bold=True))
    draw.text((tx + 75, ty + 65), "Estado: 0% diseñado • Bloqueo total", fill=(203, 213, 225), font=obtener_fuente(20, bold=False))
    draw.rounded_rectangle([tx + 75, ty + 105, tx + tw - 40, ty + 125], radius=8, fill=(15, 23, 42), outline=(71, 85, 105), width=1)
    draw.rounded_rectangle([tx + 75, ty + 105, tx + 140, ty + 125], radius=8, fill=(239, 68, 68))

    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(225, 29, 72), width=2)
    dibujar_icono_alerta(draw, 75, 757, tam=14, color=(225, 29, 72))
    draw.text((105, 742), "El tiempo vuela y no tenés nada listo para publicar", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "byte_agotado_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 580
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1220 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 19. PLANO_PHOTOSHOP_FREEZE: Programa Pesado y Máquina Colapsada
# ---------------------------------------------------------------------------
def renderizar_plano_photoshop_freeze(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 3.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    draw.rounded_rectangle([ancho // 2 - 250, 70, ancho // 2 + 250, 118], radius=12, fill=(234, 88, 12), outline=(255, 255, 255), width=2)
    dibujar_icono_cruz(draw, ancho // 2 - 190, 94, tam=10, color=(255, 255, 255), grosor=3)
    draw.text((ancho // 2 - 168, 82), "PROGRAMAS PESADOS", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    badge_txt = cfg.get("badge", "DEJÁ DE PELEAR CON EL DISEÑO")
    draw.rounded_rectangle([40, 130, ancho - 40, 205], radius=16, fill=(15, 23, 42, 250), outline=(234, 88, 12), width=2)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=obtener_fuente(28, bold=True))
    bw_txt = bbox_b[2] - bbox_b[0]
    draw.text(((ancho - bw_txt) // 2, 150), badge_txt, fill=(255, 245, 0), font=obtener_fuente(28, bold=True))

    wx, wy, ww, wh = 30, 225, ancho - 60, 475
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=20, fill=(15, 23, 42, 245), outline=(239, 68, 68), width=3)

    draw.rounded_rectangle([wx, wy, wx + ww, wy + 55], radius=20, fill=(30, 41, 59))
    draw.line([(wx, wy + 55), (wx + ww, wy + 55)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 20, wy + 20, wx + 34 + idx_dot * 20, wy + 32], fill=(148, 163, 184))
    draw.text((wx + 95, wy + 16), "Adobe_Photoshop_2026.exe (No responde)", fill=(248, 113, 113), font=obtener_fuente(20, bold=True))

    cx_card = wx + 40
    cy_card = wy + 85
    cw_card = ww - 80
    ch_card = wh - 110
    draw.rounded_rectangle([cx_card, cy_card, cx_card + cw_card, cy_card + ch_card], radius=16, fill=(2, 6, 23, 240), outline=(71, 85, 105), width=2)

    sp_x, sp_y = cx_card + cw_card // 2, cy_card + 75
    draw.ellipse([sp_x - 35, sp_y - 35, sp_x + 35, sp_y + 35], outline=(100, 116, 139), width=6)
    angulo_rad = t_sec * 6.0
    ax1 = sp_x + int(35 * math.cos(angulo_rad))
    ay1 = sp_y + int(35 * math.sin(angulo_rad))
    draw.ellipse([ax1 - 6, ay1 - 6, ax1 + 6, ay1 + 6], fill=(239, 68, 68))

    draw.text((cx_card + 50, cy_card + 130), "Iniciando motor de gráficos...", fill=(241, 245, 249), font=obtener_fuente(24, bold=True))
    draw.text((cx_card + 50, cy_card + 175), "Cargando 4.280 pinceles, fuentes y plugins... (1%)", fill=(148, 163, 184), font=obtener_fuente(20, bold=False))

    draw.rounded_rectangle([cx_card + 50, cy_card + 225, cx_card + cw_card - 50, cy_card + 250], radius=10, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.rounded_rectangle([cx_card + 50, cy_card + 225, cx_card + 80, cy_card + 250], radius=10, fill=(239, 68, 68))

    stamp_w, stamp_h = 580, 75
    stamp = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
    d_s = ImageDraw.Draw(stamp)
    d_s.rounded_rectangle([0, 0, stamp_w, stamp_h], radius=12, fill=(225, 29, 72, 245), outline=(255, 255, 255), width=2)
    dibujar_icono_cruz(d_s, 35, 37, tam=10, color=(255, 255, 255), grosor=3)
    d_s.text((60, 20), "PROGRAMA PESADO Y TRABADO", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))
    stamp_rot = stamp.rotate(-4, resample=Image.Resampling.BILINEAR, expand=True)
    frame.paste(stamp_rot, (ancho // 2 - stamp_rot.width // 2, wy + 395), stamp_rot)

    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(234, 88, 12), width=2)
    dibujar_icono_cruz(draw, 75, 757, tam=12, color=(234, 88, 12), grosor=3)
    draw.text((105, 742), "50 capas sin nombrar y la máquina congelada", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_2_guion_04_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 600
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            shake_x = int(5 * math.sin(t_sec * 32.0))
            by = 1200 + shake_x
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 20. PLANO_LIENZO_BLANCO_BLOQUEO: El Miedo a la Hoja en Blanco
# ---------------------------------------------------------------------------
def renderizar_plano_lienzo_blanco_bloqueo(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 3.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    draw.rounded_rectangle([ancho // 2 - 250, 70, ancho // 2 + 250, 118], radius=12, fill=(185, 28, 28), outline=(255, 255, 255), width=2)
    dibujar_icono_alerta(draw, ancho // 2 - 190, 94, tam=10, color=(255, 255, 255))
    draw.text((ancho // 2 - 168, 82), "BLOQUEO CREATIVO TOTAL", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    badge_txt = cfg.get("badge", "ABRÍS Y NO SABÉS QUÉ HACER")
    draw.rounded_rectangle([40, 130, ancho - 40, 205], radius=16, fill=(15, 23, 42, 250), outline=(185, 28, 28), width=2)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=obtener_fuente(28, bold=True))
    bw_txt = bbox_b[2] - bbox_b[0]
    draw.text(((ancho - bw_txt) // 2, 150), badge_txt, fill=(255, 245, 0), font=obtener_fuente(28, bold=True))

    wx, wy, ww, wh = 30, 225, ancho - 60, 475
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=20, fill=(30, 41, 59, 245), outline=(71, 85, 105), width=2)

    draw.rounded_rectangle([wx, wy, wx + ww, wy + 55], radius=20, fill=(15, 23, 42))
    draw.line([(wx, wy + 55), (wx + ww, wy + 55)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 20, wy + 20, wx + 34 + idx_dot * 20, wy + 32], fill=(148, 163, 184))
    draw.text((wx + 95, wy + 16), "Lienzo_Sin_Titulo.psd • 1080x1920 (0% creado)", fill=(203, 213, 225), font=obtener_fuente(20, bold=True))

    sx, sy, sw, sh = wx + 15, wy + 70, 75, wh - 85
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    tool_letters = ["P", "T", "V", "M", "C", "A"]
    for i, ico in enumerate(tool_letters):
        draw.rounded_rectangle([sx + 15, sy + 15 + i * 50, sx + sw - 15, sy + 50 + i * 50], radius=6, fill=(30, 41, 59))
        draw.text((sx + 28, sy + 20 + i * 50), ico, fill=(148, 163, 184), font=obtener_fuente(20, bold=True))

    lx, ly, lw, lh = wx + 105, wy + 70, ww - 120, wh - 85
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=14, fill=(248, 250, 252), outline=(148, 163, 184), width=2)

    for gx in range(lx + 40, lx + lw, 60):
        draw.line([(gx, ly), (gx, ly + lh)], fill=(226, 232, 240), width=1)
    for gy in range(ly + 40, ly + lh, 60):
        draw.line([(lx, gy), (lx + lw, gy)], fill=(226, 232, 240), width=1)

    alpha_q = 0.5 + 0.5 * math.sin(t_sec * 6.0)
    col_q = (225, 29, 72) if alpha_q > 0.5 else (100, 116, 139)
    draw.text((lx + lw // 2 - 40, ly + 60), "?", fill=col_q, font=obtener_fuente(110, bold=True))
    draw.text((lx + lw // 2 - 160, ly + 210), "¿POR DÓNDE EMPIEZO?", fill=(15, 23, 42), font=obtener_fuente(28, bold=True))
    draw.text((lx + lw // 2 - 180, ly + 260), "Sin ideas • Sin plantilla • Sin tiempo", fill=(100, 116, 139), font=obtener_fuente(20, bold=False))

    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(185, 28, 28), width=2)
    dibujar_icono_alerta(draw, 75, 757, tam=14, color=(185, 28, 28))
    draw.text((105, 742), "Abrís una pantalla en blanco y te quedás congelado", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 600
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            shake_x = int(4 * math.sin(t_sec * 28.0))
            by = 1200 + shake_x
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 21. PLANO_REMOVE_BG_LASER: Escáner Láser de Recorte Before/After
# ---------------------------------------------------------------------------
def renderizar_plano_remove_bg_laser(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.5,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    wx, wy, ww, wh = 20, 70, ancho - 40, 630
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=18, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)

    draw.rounded_rectangle([wx, wy, wx + ww, wy + 45], radius=18, fill=(2, 6, 23))
    draw.line([(wx, wy + 45), (wx + ww, wy + 45)], fill=(30, 41, 59), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 20, wy + 16, wx + 34 + idx_dot * 20, wy + 28], fill=(148, 163, 184))
    draw.text((wx + 95, wy + 14), "REMOVE.BG • Recorte Instantáneo de Fondo con Inteligencia Artificial", fill=(241, 245, 249), font=obtener_fuente(18, bold=True))

    draw.rounded_rectangle([wx + ww - 200, wy + 8, wx + ww - 15, wy + 38], radius=8, fill=(16, 185, 129))
    dibujar_icono_check(draw, wx + ww - 185, wy + 23, tam=7, color=(255, 255, 255))
    draw.text((wx + ww - 170, wy + 12), "100% Automático", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    card_y = wy + 65
    cw = (ww - 60) // 2
    ch = wh - 85

    c1_x = wx + 20
    draw.rounded_rectangle([c1_x, card_y, c1_x + cw, card_y + ch], radius=14, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    draw.rounded_rectangle([c1_x + 15, card_y + 15, c1_x + 185, card_y + 50], radius=8, fill=(225, 29, 72))
    dibujar_icono_cruz(draw, cx=c1_x + 30, cy=card_y + 32, tam=6, color=(255, 255, 255), grosor=2)
    draw.text((c1_x + 45, card_y + 20), "ANTES • Con Fondo", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    fx, fy, fw, fh = c1_x + 20, card_y + 65, cw - 40, ch - 120
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=10, fill=(71, 85, 105))
    for rx in range(fx + 20, fx + fw - 20, 40):
        draw.line([(rx, fy + 20), (rx + 20, fy + fh - 20)], fill=(100, 116, 139), width=3)
    draw.ellipse([fx + fw // 2 - 70, fy + fh // 2 - 50, fx + fw // 2 + 70, fy + fh // 2 + 70], fill=(217, 119, 6), outline=(255, 255, 255), width=3)
    draw.text((fx + fw // 2 - 45, fy + fh // 2), "OBJETO", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.text((c1_x + 20, card_y + ch - 40), "Fondo sucio que arruina el diseño", fill=(244, 63, 94), font=obtener_fuente(16, bold=True))

    c2_x = wx + 40 + cw
    draw.rounded_rectangle([c2_x, card_y, c2_x + cw, card_y + ch], radius=14, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    draw.rounded_rectangle([c2_x + 15, card_y + 15, c2_x + 205, card_y + 50], radius=8, fill=(16, 185, 129))
    dibujar_icono_check(draw, c2_x + 30, card_y + 32, tam=7, color=(255, 255, 255))
    draw.text((c2_x + 45, card_y + 20), "DESPUÉS • PNG Limpio", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    px, py, pw, ph = c2_x + 20, card_y + 65, cw - 40, ch - 120
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=10, fill=(30, 41, 59))
    sq = 18
    for row in range(py, py + ph, sq):
        for col in range(px, px + pw, sq):
            if ((col - px) // sq + (row - py) // sq) % 2 == 0:
                draw.rectangle([col, row, min(col + sq, px + pw), min(row + sq, py + ph)], fill=(51, 65, 85))
    draw.ellipse([px + pw // 2 - 70, py + ph // 2 - 50, px + pw // 2 + 70, py + ph // 2 + 70], fill=(217, 119, 6), outline=(52, 211, 153), width=4)
    draw.text((px + pw // 2 - 45, py + ph // 2), "OBJETO", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.text((c2_x + 20, card_y + ch - 40), "Bordes perfectos en 1 segundo", fill=(52, 211, 153), font=obtener_fuente(16, bold=True))

    laser_x = ancho // 2 + int(60 * math.sin(t_sec * 4.0))
    draw.line([(laser_x, card_y + 10), (laser_x, card_y + ch - 10)], fill=(56, 189, 248), width=4)
    draw.ellipse([laser_x - 12, card_y + ch // 2 - 12, laser_x + 12, card_y + ch // 2 + 12], fill=(255, 255, 255), outline=(56, 189, 248), width=3)

    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, 75, 757, tam=14, color=(16, 185, 129))
    draw.text((105, 742), "Recorta cualquier foto en un segundo sin tocar nada", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "cierre_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 600
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            by = 1200
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 22. PLANO_SMARTPHONE_INSTAGRAM_FEED: Mockup de Celular con Post Terminado
# ---------------------------------------------------------------------------
def renderizar_plano_smartphone_instagram_feed(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.5,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    draw.rounded_rectangle([ancho // 2 - 250, 70, ancho // 2 + 250, 118], radius=12, fill=(16, 185, 129), outline=(255, 255, 255), width=2)
    dibujar_icono_check(draw, ancho // 2 - 190, 94, tam=10, color=(255, 255, 255))
    draw.text((ancho // 2 - 168, 82), "RESULTADO PROFESIONAL", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    ph_w, ph_h = 580, 570
    ph_x, ph_y = (ancho - ph_w) // 2, 135

    draw.rounded_rectangle([ph_x, ph_y, ph_x + ph_w, ph_y + ph_h], radius=38, fill=(15, 23, 42), outline=(71, 85, 105), width=4)
    draw.rounded_rectangle([ph_x + ph_w // 2 - 60, ph_y + 12, ph_x + ph_w // 2 + 60, ph_y + 30], radius=8, fill=(2, 6, 23))

    sx, sy, sw, sh = ph_x + 18, ph_y + 42, ph_w - 36, ph_h - 60
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=24, fill=(2, 6, 23))

    draw.ellipse([sx + 20, sy + 15, sx + 50, sy + 45], fill=(225, 29, 72))
    draw.text((sx + 26, sy + 20), "BT", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))
    draw.text((sx + 60, sy + 16), "byte_tech_studio", fill=(255, 255, 255), font=obtener_fuente(18, bold=True))
    draw.text((sx + 60, sy + 38), "Publicidad • Hace 5 min", fill=(148, 163, 184), font=obtener_fuente(14, bold=False))
    draw.text((sx + sw - 45, sy + 20), "•••", fill=(148, 163, 184), font=obtener_fuente(18, bold=True))

    fx, fy, fw, fh = sx + 15, sy + 65, sw - 30, sh - 150
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=14, fill=(24, 24, 27), outline=(217, 119, 6), width=2)
    draw.text((fx + 30, fy + 25), "SPECIALTY COFFEE FEST", fill=(251, 191, 36), font=obtener_fuente(24, bold=True))
    draw.text((fx + 30, fy + 65), "VIERNES 18 HS • ENTRADA LIBRE", fill=(241, 245, 249), font=obtener_fuente(18, bold=False))
    draw.ellipse([fx + fw // 2 - 50, fy + fh // 2 - 20, fx + fw // 2 + 50, fy + fh // 2 + 70], fill=(217, 119, 6), outline=(251, 191, 36), width=3)
    draw.text((fx + fw // 2 - 38, fy + fh // 2 + 15), "COFFEE", fill=(255, 255, 255), font=obtener_fuente(18, bold=True))
    draw.rounded_rectangle([fx + 30, fy + fh - 55, fx + fw - 30, fy + fh - 20], radius=8, fill=(217, 119, 6))
    draw.text((fx + fw // 2 - 75, fy + fh - 48), "REGISTRATE GRATIS", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    iy = fy + fh + 15
    draw.rounded_rectangle([sx + 20, iy, sx + 95, iy + 30], radius=6, fill=(225, 29, 72))
    draw.text((sx + 30, iy + 6), "LIKE", fill=(255, 255, 255), font=obtener_fuente(14, bold=True))
    draw.rounded_rectangle([sx + 105, iy, sx + 225, iy + 30], radius=6, fill=(30, 41, 59))
    draw.text((sx + 115, iy + 6), "COMENTAR", fill=(255, 255, 255), font=obtener_fuente(14, bold=True))
    draw.text((sx + 20, iy + 38), "1.480 Me gusta • Diseño listo en 3 minutos", fill=(254, 240, 138), font=obtener_fuente(16, bold=True))

    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, 75, 757, tam=14, color=(16, 185, 129))
    draw.text((105, 742), "Te queda un diseño prolijo sin pagar de más", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "cierre_guion_04_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 600
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            salto = int(12 * abs(math.sin(t_sec * 4.0)))
            by = 1200 - salto
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# 24. Funciones de Escena para Video 10 (Cotización Automática de Pedidos)
# ---------------------------------------------------------------------------

def renderizar_plano_whatsapp_pedido_remeras(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 3.5,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """
    Arquetipo: Smartphone Native POV (Safe Zone Móvil Estricta: y >= 250).
    Muestra un marco de teléfono moderno centrado (880px de ancho) con WhatsApp real.
    """
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.5, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    alerta_calculo = cfg.get("alerta_calculo", False)

    # 1. Contenedor de Smartphone Centrado (Safe Zone: y=250..780, ancho=880, x=100)
    pw, ph = 880, 530
    px = (ancho - pw) // 2  # 100
    py = 250

    # Sombra difusa del teléfono
    sombra = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_s = ImageDraw.Draw(sombra)
    glow_col = (239, 68, 68, 60) if alerta_calculo else (37, 211, 102, 50)
    d_s.rounded_rectangle([px + 10, py + 12, px + pw - 10, py + ph + 12], radius=28, fill=glow_col)
    sombra = sombra.filter(ImageFilter.GaussianBlur(22))
    frame = Image.alpha_composite(frame, sombra)
    draw = ImageDraw.Draw(frame)

    # Chasis del teléfono
    border_col = (239, 68, 68) if alerta_calculo else (37, 211, 102)
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=28, fill=(11, 20, 26, 252), outline=border_col, width=3)

    # Dynamic Island / Notch superior del smartphone
    notch_w = 160
    notch_x = (ancho - notch_w) // 2
    draw.rounded_rectangle([notch_x, py + 12, notch_x + notch_w, py + 34], radius=11, fill=(2, 6, 23, 240))
    draw.ellipse([notch_x + notch_w - 28, py + 18, notch_x + notch_w - 18, py + 28], fill=(30, 41, 59))

    # Barra de WhatsApp Header
    hy = py + 42
    draw.rounded_rectangle([px + 16, hy, px + pw - 16, hy + 66], radius=14, fill=(32, 44, 51))
    av_cx, av_cy = px + 52, hy + 33
    draw.ellipse([av_cx - 20, av_cy - 20, av_cx + 20, av_cy + 20], fill=(0, 168, 132))
    draw.text((av_cx - 13, av_cy - 12), "CL", fill=(255, 255, 255), font=obtener_fuente(18, bold=True))
    draw.text((px + 86, hy + 10), "Cliente • Textil & Merchandising", fill=(233, 237, 239), font=obtener_fuente(20, bold=True))
    draw.text((px + 86, hy + 36), "En línea • Escribió hace un instante", fill=(37, 211, 102), font=obtener_fuente(15, bold=False))

    # Burbuja verde de WhatsApp con el pedido real
    bx, by, bw, bh = px + 25, py + 122, pw - 50, 265
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=18, fill=(0, 92, 75), outline=(0, 168, 132), width=2)

    linea1 = "“Hola, necesito 20 remeras negras,"
    linea2 = "talle M y L, con mi logo."
    linea3 = "¿Cuánto me saldría?”"
    draw.text((bx + 26, by + 24), linea1, fill=(255, 255, 255), font=obtener_fuente(28, bold=True))
    draw.text((bx + 26, by + 72), linea2, fill=(255, 255, 255), font=obtener_fuente(28, bold=True))
    draw.text((bx + 26, by + 120), linea3, fill=(254, 240, 138), font=obtener_fuente(28, bold=True))
    draw.text((bx + bw - 190, by + bh - 40), "14:32 hs • Leído ✓✓", fill=(134, 150, 160), font=obtener_fuente(16, bold=False))

    # Tarjeta inferior dentro del smartphone
    iy = py + 405
    if alerta_calculo:
        draw.rounded_rectangle([px + 25, iy, px + pw - 25, iy + 100], radius=14, fill=(225, 29, 72, 240), outline=(255, 255, 255), width=2)
        dibujar_icono_cruz(draw, px + 65, iy + 50, tam=12, color=(255, 255, 255), grosor=3)
        draw.text((px + 95, iy + 18), "¡NO PIENSO CALCULAR ESTO A MANO!", fill=(255, 255, 255), font=obtener_fuente(23, bold=True))
        draw.text((px + 95, iy + 52), "Calcular a mano te hace perder tiempo y clientes", fill=(254, 226, 226), font=obtener_fuente(18, bold=False))
    else:
        draw.rounded_rectangle([px + 25, iy, px + pw - 25, iy + 100], radius=14, fill=(15, 23, 42, 240), outline=(37, 211, 102), width=1)
        dibujar_icono_check(draw, px + 65, iy + 50, tam=12, color=(37, 211, 102))
        draw.text((px + 95, iy + 18), "PEDIDO ENTRANTE DE UN CLIENTE", fill=(255, 245, 0), font=obtener_fuente(22, bold=True))
        draw.text((px + 95, iy + 52), "Mensaje real sin ordenar esperando cotización rápida", fill=(226, 232, 240), font=obtener_fuente(18, bold=False))

    # Píldora de llamada clave (Safe Zone: y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=border_col, width=2)
    if alerta_calculo:
        dibujar_icono_cruz(draw, px + 40, py_pill + 35, tam=12, color=(239, 68, 68), grosor=3)
        draw.text((px + 70, py_pill + 20), "Hacer cuentas manuales = Clientes perdidos", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))
    else:
        dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(37, 211, 102))
        draw.text((px + 70, py_pill + 20), "De mensaje informal a presupuesto automático", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / ("punto_2_guion_04_transparente.png" if alerta_calculo else "cierre_transparente.png")

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_byte_pase_ia(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 3.5,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Bento Transfer / Pipeline Automático (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.6, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    # Tarjeta principal
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 248), outline=(59, 130, 246), width=3)

    # Cabecera de la tarjeta
    draw.rounded_rectangle([px, py, px + pw, py + 60], radius=24, fill=(30, 41, 59))
    draw.line([(px, py + 60), (px + pw, py + 60)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([px + 25 + idx_dot * 20, py + 23, px + 37 + idx_dot * 20, py + 35], fill=(148, 163, 184))
    draw.text((px + 100, py + 18), "Asistente_Cotizaciones_IA • Input Activo", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))

    # Caja del prompt pegado
    qx, qy, qw, qh = px + 30, py + 85, pw - 60, 260
    draw.rounded_rectangle([qx, qy, qx + qw, qy + qh], radius=16, fill=(2, 6, 23, 245), outline=(71, 85, 105), width=2)
    draw.text((qx + 25, qy + 20), "PROMPT PEGADO:", fill=(148, 163, 184), font=obtener_fuente(16, bold=True))
    draw.text((qx + 25, qy + 60), "“Extraer detalles del pedido y cotizar:", fill=(248, 250, 252), font=obtener_fuente(22, bold=True))
    draw.text((qx + 25, qy + 105), "  20 remeras negras (M y L) con logo impreso", fill=(96, 165, 250), font=obtener_fuente(22, bold=True))
    draw.text((qx + 25, qy + 150), "  Generar tabla con precios unitarios y total”", fill=(248, 250, 252), font=obtener_fuente(22, bold=True))

    # Cursor titilante
    if int(t_sec * 4) % 2 == 0:
        draw.line([(qx + 25 + 500, qy + 150), (qx + 25 + 500, qy + 175)], fill=(96, 165, 250), width=3)

    # Chip de estado IA
    draw.rounded_rectangle([px + 30, py + 370, px + pw - 30, py + 480], radius=16, fill=(30, 58, 138, 240), outline=(59, 130, 246), width=2)
    dibujar_chispa_ia(draw, px + 65, py + 425, tam=14, color=(96, 165, 250))
    draw.text((px + 95, py + 400), "IA procesando texto y estructurando datos...", fill=(255, 255, 255), font=obtener_fuente(23, bold=True))
    draw.text((px + 95, py + 435), "Detectando prendas, cantidades y estampados requeridos", fill=(191, 219, 254), font=obtener_fuente(18, bold=False))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(59, 130, 246), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(59, 130, 246))
    draw.text((px + 70, py_pill + 20), "De mensaje informal a instrucciones claras", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "byte_computadora_feliz_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            shake_x = int(3 * math.sin(t_sec * 16.0))
            by = 1120 + shake_x
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_tabla_presupuesto_extraccion(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Bento Grid Modular 3D de Extracción (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.6, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    # Tarjeta Bento principal
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 248), outline=(16, 185, 129), width=3)

    # Cabecera Bento
    draw.rounded_rectangle([px, py, px + pw, py + 60], radius=24, fill=(30, 41, 59))
    draw.line([(px, py + 60), (px + pw, py + 60)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([px + 25 + idx_dot * 20, py + 23, px + 37 + idx_dot * 20, py + 35], fill=(148, 163, 184))
    draw.text((px + 100, py + 18), "Estructura_Pedido_Detectada.json", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))

    filas = [
        ("Producto", "Remeras Negras Lisas", "✓ Detectado", (16, 185, 129)),
        ("Cantidad", "20 unidades (10 M + 10 L)", "✓ Desglosado", (59, 130, 246)),
        ("Personalización", "Estampado Logo Pecho", "✓ Identificado", (168, 85, 247)),
        ("Precio Estimado", "$4.500 c/u • Subtotal $90.000", "✓ Calculado", (245, 158, 11)),
    ]

    rx, ry, rw, rh = px + 30, py + 80, pw - 60, 92
    for idx_f, (campo, valor, badge, col) in enumerate(filas):
        curr_y = ry + idx_f * 105
        draw.rounded_rectangle([rx, curr_y, rx + rw, curr_y + rh], radius=14, fill=(2, 6, 23, 245), outline=(51, 65, 85), width=1)
        draw.text((rx + 22, curr_y + 16), campo.upper(), fill=(148, 163, 184), font=obtener_fuente(16, bold=True))
        draw.text((rx + 22, curr_y + 46), valor, fill=(248, 250, 252), font=obtener_fuente(23, bold=True))

        draw.rounded_rectangle([rx + rw - 180, curr_y + 26, rx + rw - 20, curr_y + 68], radius=10, fill=(col[0]//4, col[1]//4, col[2]//4), outline=col, width=1)
        draw.text((rx + rw - 165, curr_y + 35), badge, fill=col, font=obtener_fuente(17, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(16, 185, 129))
    draw.text((px + 70, py_pill + 20), "Cantidades, talles y logo detectados al instante", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_1_guion_04_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            salto = int(8 * abs(math.sin(t_sec * 3.5)))
            by = 1120 - salto
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_tabla_cotizar_ordenada(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Invoice / Tarjeta de Presupuesto Limpia (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.6, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 248), outline=(16, 185, 129), width=3)

    # Cabecera de la calculadora
    draw.rounded_rectangle([px, py, px + pw, py + 60], radius=24, fill=(30, 41, 59))
    draw.line([(px, py + 60), (px + pw, py + 60)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([px + 25 + idx_dot * 20, py + 23, px + 37 + idx_dot * 20, py + 35], fill=(148, 163, 184))
    draw.text((px + 100, py + 18), "Calculadora_Automatica_Costos", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))

    cx, cy, cw, ch = px + 30, py + 80, pw - 60, 210
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=16, fill=(2, 6, 23, 245), outline=(51, 65, 85), width=1)
    draw.text((cx + 25, cy + 22), "• 20 Remeras Negras (10 M + 10 L):", fill=(241, 245, 249), font=obtener_fuente(22, bold=False))
    draw.text((cx + cw - 150, cy + 22), "$70.000", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.text((cx + 25, cy + 70), "• 20 Estampados de Logo en Pecho:", fill=(241, 245, 249), font=obtener_fuente(22, bold=False))
    draw.text((cx + cw - 150, cy + 70), "$20.000", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.line([(cx + 20, cy + 125), (cx + cw - 20, cy + 125)], fill=(71, 85, 105), width=1)
    draw.text((cx + 25, cy + 148), "TIEMPO DE PRODUCCIÓN:", fill=(148, 163, 184), font=obtener_fuente(18, bold=True))
    draw.text((cx + cw - 220, cy + 148), "4 a 5 días hábiles", fill=(52, 211, 153), font=obtener_fuente(18, bold=True))

    tx, ty, tw, th = px + 30, py + 310, pw - 60, 185
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=18, fill=(6, 78, 59, 250), outline=(16, 185, 129), width=3)
    draw.text((tx + 30, ty + 25), "TOTAL ESTIMADO A COBRAR:", fill=(167, 243, 208), font=obtener_fuente(20, bold=True))
    draw.text((tx + 30, ty + 70), "$90.000", fill=(255, 255, 255), font=obtener_fuente(56, bold=True))
    draw.rounded_rectangle([tx + tw - 240, ty + 70, tx + tw - 30, ty + 130], radius=12, fill=(16, 185, 129))
    draw.text((tx + tw - 215, ty + 86), "✓ LISTO AL TOQUE", fill=(255, 255, 255), font=obtener_fuente(18, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(16, 185, 129))
    draw.text((px + 70, py_pill + 20), "Cálculos matemáticos y desglose sin errores", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_cotizacion_formal_pdf(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Envío Formal WhatsApp PDF (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.6, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 248), outline=(16, 185, 129), width=3)

    # Cabecera del PDF
    draw.rounded_rectangle([px, py, px + pw, py + 60], radius=24, fill=(30, 41, 59))
    draw.line([(px, py + 60), (px + pw, py + 60)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([px + 25 + idx_dot * 20, py + 23, px + 37 + idx_dot * 20, py + 35], fill=(148, 163, 184))
    draw.text((px + 100, py + 18), "Presupuesto_Santiago_20Remeras.pdf", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))

    dx, dy, dw, dh = px + 30, py + 85, pw - 60, 275
    draw.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=18, fill=(2, 6, 23, 245), outline=(16, 185, 129), width=2)
    draw.text((dx + 30, dy + 28), "PRESUPUESTO FORMAL #1042", fill=(16, 185, 129), font=obtener_fuente(20, bold=True))
    draw.text((dx + 30, dy + 72), "Cliente: Santiago • 20 Remeras negras (10M + 10L)", fill=(241, 245, 249), font=obtener_fuente(23, bold=True))
    draw.text((dx + 30, dy + 118), "Detalle: Estampado con logo • Entrega 5 días", fill=(148, 163, 184), font=obtener_fuente(20, bold=False))
    draw.text((dx + 30, dy + 165), "TOTAL: $90.000 (Validez 7 días)", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))

    bx_btn, by_btn, bw_btn, bh_btn = px + 30, py + 390, pw - 60, 105
    draw.rounded_rectangle([bx_btn, by_btn, bx_btn + bw_btn, by_btn + bh_btn], radius=18, fill=(37, 211, 102), outline=(255, 255, 255), width=2)
    draw.text((bx_btn + 110, by_btn + 34), "ENVIAR COTIZACIÓN POR WHATSAPP ➔", fill=(11, 20, 26), font=obtener_fuente(24, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(16, 185, 129))
    draw.text((px + 70, py_pill + 20), "Respuesta impecable enviada en menos de 1 minuto", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "cierre_guion_04_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            salto = int(12 * abs(math.sin(t_sec * 4.0)))
            by = 1120 - salto
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_cierre_pregunta_automatizar(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Encuesta Comunitaria A / B / C (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_creativo")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.5, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(245, 158, 11), width=3)

    draw.text((px + 40, py + 30), "¿QUÉ TAREA DE TU NEGOCIO", fill=(255, 245, 0), font=obtener_fuente(34, bold=True))
    draw.text((px + 40, py + 75), "AUTOMATIZARÍAS PRIMERO?", fill=(255, 245, 0), font=obtener_fuente(34, bold=True))

    opciones = [
        ("A", "Presupuestos y cotizaciones de clientes", (16, 185, 129)),
        ("B", "Respuestas repetitivas de WhatsApp", (59, 130, 246)),
        ("C", "Control de pedidos y stock diario", (168, 85, 247)),
    ]

    for idx_o, (letra, texto, col) in enumerate(opciones):
        oy = py + 145 + idx_o * 120
        draw.rounded_rectangle([px + 30, oy, px + pw - 30, oy + 98], radius=16, fill=(2, 6, 23, 245), outline=col, width=2)
        draw.ellipse([px + 50, oy + 22, px + 102, oy + 74], fill=col)
        draw.text((px + 65, oy + 32), letra, fill=(255, 255, 255), font=obtener_fuente(26, bold=True))
        draw.text((px + 120, oy + 35), texto, fill=(248, 250, 252), font=obtener_fuente(22, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(245, 158, 11), width=2)
    draw.text((px + 90, py_pill + 20), "👇 Votá A, B o C en los comentarios", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(4 * math.sin(t_sec * 3.0))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_cincuenta_archivos_caos(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Hero Caos con cascada de 50 archivos PDF flotantes (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.5, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw = 880
    px = (ancho - pw) // 2

    # 1. Cabecera superior elegante (y = 250..325)
    py_hdr = 250
    draw.rounded_rectangle([px, py_hdr, px + pw, py_hdr + 75], radius=20, fill=(15, 23, 42, 248), outline=(59, 130, 246), width=2)
    # Dibujar icono carpeta estilizado
    draw.rounded_rectangle([px + 28, py_hdr + 22, px + 68, py_hdr + 52], radius=6, fill=(245, 158, 11))
    draw.rectangle([px + 28, py_hdr + 18, px + 48, py_hdr + 24], fill=(245, 158, 11))
    draw.text((px + 82, py_hdr + 22), "CARPETA: FACTURAS_PROVEEDORES/", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.rounded_rectangle([px + pw - 230, py_hdr + 16, px + pw - 25, py_hdr + 59], radius=14, fill=(225, 29, 72), outline=(254, 205, 211), width=1)
    draw.text((px + pw - 210, py_hdr + 24), "50 ARCHIVOS PDF", fill=(255, 255, 255), font=obtener_fuente(18, bold=True))

    # 2. Cascada de PDFs flotantes (y = 345..785)
    archivos_grid = [
        ("Factura_01.pdf", "1.2 MB", 0),
        ("Factura_02.pdf", "850 KB", 1),
        ("Factura_07.pdf", "2.1 MB", 2),
        ("Factura_14.pdf", "940 KB", 3),
        ("Factura_22.pdf", "1.5 MB", 4),
        ("Factura_29.pdf", "3.2 MB", 5),
        ("Factura_33.pdf", "620 KB", 6),
        ("Factura_38.pdf", "1.8 MB", 7),
        ("Factura_42.pdf", "780 KB", 8),
        ("Factura_47.pdf", "1.1 MB", 9),
        ("Factura_49.pdf", "2.4 MB", 10),
        ("Factura_50.pdf", "910 KB", 11),
    ]

    cols = 3
    card_w = 275
    card_h = 95
    col_gap = 15
    row_gap = 15
    start_y = 345

    for idx, (nombre_pdf, tam_str, seed) in enumerate(archivos_grid):
        c = idx % cols
        r = idx // cols
        cx = px + c * (card_w + col_gap)
        cy = start_y + r * (card_h + row_gap)
        
        oleaje = int(6 * math.sin(t_sec * 2.5 + seed * 0.8))
        curr_cy = cy + oleaje

        draw.rounded_rectangle([cx, curr_cy, cx + card_w, curr_cy + card_h], radius=14, fill=(15, 23, 42, 240), outline=(239, 68, 68), width=1)
        draw.rounded_rectangle([cx + 15, curr_cy + 18, cx + 62, curr_cy + 52], radius=8, fill=(225, 29, 72))
        draw.text((cx + 22, curr_cy + 24), "PDF", fill=(255, 255, 255), font=obtener_fuente(14, bold=True))
        draw.text((cx + 72, curr_cy + 22), nombre_pdf, fill=(248, 250, 252), font=obtener_fuente(17, bold=True))
        draw.text((cx + 72, curr_cy + 55), f"Septiembre • {tam_str}", fill=(148, 163, 184), font=obtener_fuente(14, bold=False))

    # 3. Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(239, 68, 68), width=2)
    draw.text((px + 55, py_pill + 20), "• Necesito encontrar un dato en estos 50 archivos...", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # 4. Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "escena_problema_guion_03_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(6 * math.sin(t_sec * 3.0))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_byte_rechazo_manual(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Visor de PDF denso / Rechazo absoluto a abrir 50 archivos a mano (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.5, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 248), outline=(239, 68, 68), width=3)

    # Cabecera de ventana gris neutra
    draw.rounded_rectangle([px, py, px + pw, py + 60], radius=24, fill=(30, 41, 59))
    draw.line([(px, py + 60), (px + pw, py + 60)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([px + 25 + idx_dot * 20, py + 23, px + 37 + idx_dot * 20, py + 35], fill=(148, 163, 184))
    draw.text((px + 100, py + 18), "Factura_01.pdf - Visor Manual de Documentos", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))

    # Hoja de documento denso simulado
    doc_x, doc_y, doc_w, doc_h = px + 40, py + 85, pw - 80, 290
    draw.rounded_rectangle([doc_x, doc_y, doc_x + doc_w, doc_y + doc_h], radius=16, fill=(241, 245, 249), outline=(203, 213, 225), width=2)
    
    draw.text((doc_x + 30, doc_y + 20), "FACTURA COMERCIAL 'A' #0042-9912", fill=(30, 41, 59), font=obtener_fuente(18, bold=True))
    draw.text((doc_x + doc_w - 180, doc_y + 20), "Fecha: 12/09/2026", fill=(100, 116, 139), font=obtener_fuente(16, bold=False))
    draw.line([(doc_x + 25, doc_y + 55), (doc_x + doc_w - 25, doc_y + 55)], fill=(203, 213, 225), width=2)

    filas_doc = [
        ("Item 01: Servicios de mantenimiento técnico", "$ 45.200"),
        ("Item 02: Licencias de software y servidores", "$ 12.800"),
        ("Item 03: Insumos de papelería y suministros", "$ 8.400"),
    ]
    for idx_f, (it, pr) in enumerate(filas_doc):
        fy = doc_y + 75 + idx_f * 45
        draw.text((doc_x + 30, fy), it, fill=(51, 65, 85), font=obtener_fuente(16, bold=False))
        draw.text((doc_x + doc_w - 150, fy), pr, fill=(15, 23, 42), font=obtener_fuente(16, bold=True))
        draw.line([(doc_x + 25, fy + 32), (doc_x + doc_w - 25, fy + 32)], fill=(226, 232, 240), width=1)

    # Sello grande rojo cruzado: DESCARTADO
    draw.rounded_rectangle([doc_x + 80, doc_y + 205, doc_x + doc_w - 80, doc_y + 265], radius=12, fill=(225, 29, 72, 240), outline=(255, 255, 255), width=2)
    draw.text((doc_x + 110, doc_y + 218), "[ REVISIÓN MANUAL DESCARTADA ]", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    # Tarjeta de alerta inferior en la ventana
    tx, ty, tw, th = px + 40, py + 395, pw - 80, 105
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=16, fill=(69, 10, 10, 240), outline=(239, 68, 68), width=2)
    draw.text((tx + 30, ty + 20), "TIEMPO ESTIMADO REVISANDO 50 DOCUMENTOS:", fill=(254, 205, 211), font=obtener_fuente(18, bold=True))
    draw.text((tx + 30, ty + 55), "• Más de 2 horas abriendo PDFs uno por uno", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(239, 68, 68), width=2)
    draw.text((px + 60, py_pill + 20), "• No. Definitivamente no pienso abrir uno por uno.", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_2_guion_10_cotizacion_automatica_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(4 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_drag_drop_ia_analisis(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Drag & Drop masivo a Asistente IA + Pregunta Semántica (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.6, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 248), outline=(6, 182, 212), width=3)

    # Cabecera de ventana
    draw.rounded_rectangle([px, py, px + pw, py + 60], radius=24, fill=(30, 41, 59))
    draw.line([(px, py + 60), (px + pw, py + 60)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([px + 25 + idx_dot * 20, py + 23, px + 37 + idx_dot * 20, py + 35], fill=(148, 163, 184))
    draw.text((px + 100, py + 18), "Asistente_Documental_IA // RAG Analyzer", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))

    # Zona Drag & Drop masivo
    zx, zy, zw, zh = px + 30, py + 80, pw - 60, 180
    draw.rounded_rectangle([zx, zy, zx + zw, zy + zh], radius=18, fill=(8, 47, 73, 240), outline=(6, 182, 212), width=2)
    
    dibujar_icono_check(draw, zx + 40, zy + 34, tam=10, color=(103, 232, 249))
    draw.text((zx + 65, zy + 22), "50 ARCHIVOS PDF CARGADOS", fill=(103, 232, 249), font=obtener_fuente(22, bold=True))
    draw.text((zx + zw - 190, zy + 24), "100% INDEXADO", fill=(52, 211, 153), font=obtener_fuente(18, bold=True))
    
    bar_y = zy + 65
    draw.rounded_rectangle([zx + 30, bar_y, zx + zw - 30, bar_y + 16], radius=8, fill=(15, 23, 42))
    draw.rounded_rectangle([zx + 30, bar_y, zx + zw - 30, bar_y + 16], radius=8, fill=(6, 182, 212))
    
    chips_arch = ["Factura_01.pdf", "Factura_14.pdf", "Factura_29.pdf", "+47 más"]
    for idx_c, chip_t in enumerate(chips_arch):
        cx_chip = zx + 30 + idx_c * 185
        cy_chip = zy + 105
        draw.rounded_rectangle([cx_chip, cy_chip, cx_chip + 170, cy_chip + 48], radius=10, fill=(15, 23, 42, 230), outline=(51, 65, 85), width=1)
        draw.text((cx_chip + 15, cy_chip + 14), chip_t, fill=(226, 232, 240), font=obtener_fuente(16, bold=False))

    # Burbuja de Pregunta del Usuario
    bx_msg, by_msg, bw_msg, bh_msg = px + 30, py + 285, pw - 60, 215
    draw.rounded_rectangle([bx_msg, by_msg, bx_msg + bw_msg, by_msg + bh_msg], radius=18, fill=(30, 27, 75, 245), outline=(99, 102, 241), width=2)
    draw.text((bx_msg + 25, by_msg + 18), "TU PREGUNTA A LA INTELIGENCIA ARTIFICIAL:", fill=(165, 180, 252), font=obtener_fuente(16, bold=True))
    draw.text((bx_msg + 25, by_msg + 55), "• ¿Cuánto gastamos en proveedores", fill=(255, 255, 255), font=obtener_fuente(27, bold=True))
    draw.text((bx_msg + 45, by_msg + 95), "durante septiembre?", fill=(255, 255, 255), font=obtener_fuente(27, bold=True))
    
    draw.line([(bx_msg + 25, by_msg + 145), (bx_msg + bw_msg - 25, by_msg + 145)], fill=(67, 56, 202), width=1)
    draw.text((bx_msg + 25, by_msg + 162), "• Escaneando 50 documentos en lenguaje natural...", fill=(129, 140, 248), font=obtener_fuente(19, bold=False))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(6, 182, 212), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(6, 182, 212))
    draw.text((px + 70, py_pill + 20), "50 documentos indexados y analizados al instante", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "byte_computadora_feliz_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            salto = int(8 * abs(math.sin(t_sec * 3.5)))
            by = 1120 - salto
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_rag_resultado_citas(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Total Consolidado + Fuentes y Citas de Origen Verificadas (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.6, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 248), outline=(16, 185, 129), width=3)

    # Cabecera de ventana
    draw.rounded_rectangle([px, py, px + pw, py + 60], radius=24, fill=(30, 41, 59))
    draw.line([(px, py + 60), (px + pw, py + 60)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([px + 25 + idx_dot * 20, py + 23, px + 37 + idx_dot * 20, py + 35], fill=(148, 163, 184))
    draw.text((px + 100, py + 18), "Respuesta_IA // Fuentes_Verificadas.rag", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))

    # Banner del Total Calculado
    rx, ry, rw, rh = px + 30, py + 80, pw - 60, 160
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=18, fill=(6, 78, 59, 240), outline=(16, 185, 129), width=2)
    draw.text((rx + 25, ry + 20), "GASTO TOTAL EN PROVEEDORES (SEPTIEMBRE):", fill=(167, 243, 208), font=obtener_fuente(18, bold=True))
    draw.text((rx + 25, ry + 55), "$ 148.500 ARS", fill=(255, 255, 255), font=obtener_fuente(50, bold=True))
    
    draw.rounded_rectangle([rx + rw - 240, ry + 60, rx + rw - 25, ry + 115], radius=12, fill=(16, 185, 129))
    draw.text((rx + rw - 215, ry + 75), "3 FACTURAS CLAVE", fill=(255, 255, 255), font=obtener_fuente(17, bold=True))

    # Mosaico de Citas de Origen
    citas = [
        ("[1] Factura_14.pdf", "Servicios Cloud y Hosting", "$ 62.000", (6, 182, 212)),
        ("[2] Factura_29.pdf", "Insumos de Oficina y Librería", "$ 41.500", (59, 130, 246)),
        ("[3] Factura_47.pdf", "Mantenimiento Técnico Hardware", "$ 45.000", (168, 85, 247)),
    ]

    for idx_c, (doc_name, concepto, monto, col) in enumerate(citas):
        cy_c = py + 260 + idx_c * 75
        draw.rounded_rectangle([px + 30, cy_c, px + pw - 30, cy_c + 65], radius=14, fill=(2, 6, 23, 245), outline=col, width=1)
        draw.text((px + 50, cy_c + 20), doc_name, fill=col, font=obtener_fuente(20, bold=True))
        draw.text((px + 280, cy_c + 22), concepto, fill=(226, 232, 240), font=obtener_fuente(18, bold=False))
        draw.text((px + pw - 180, cy_c + 20), monto, fill=(255, 255, 255), font=obtener_fuente(20, bold=True))

    draw.text((px + 45, py + 495), "• Cada dato incluye enlace directo al PDF original (Sin adivinar)", fill=(110, 231, 183), font=obtener_fuente(17, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(16, 185, 129))
    draw.text((px + 70, py_pill + 20), "Respuesta exacta + documentos de origen verificados", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "resultado_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_humor_sufrir_gratis(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Balanza comparativa / Humor reflexivo (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.5, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 248), outline=(245, 158, 11), width=3)

    # Cabecera de ventana
    draw.rounded_rectangle([px, py, px + pw, py + 60], radius=24, fill=(30, 41, 59))
    draw.line([(px, py + 60), (px + pw, py + 60)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([px + 25 + idx_dot * 20, py + 23, px + 37 + idx_dot * 20, py + 35], fill=(148, 163, 184))
    draw.text((px + 100, py + 18), "Comparativa // Qué manera de complicarse solo", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))

    col_w = (pw - 80) // 2
    
    # Columna Izquierda: A MANO (Rojo/Gris)
    c1_x = px + 30
    c1_y = py + 85
    draw.rounded_rectangle([c1_x, c1_y, c1_x + col_w, c1_y + 415], radius=18, fill=(69, 10, 10, 240), outline=(239, 68, 68), width=2)
    draw.text((c1_x + 25, c1_y + 25), "MÉTODO MANUAL", fill=(254, 205, 211), font=obtener_fuente(24, bold=True))
    
    items_mano = [
        "• Abrir 50 PDFs 1 por 1",
        "• Revisar tablas con la vista",
        "• Sumar con calculadora",
        "• 2 horas perdidas",
    ]
    for idx_m, it_m in enumerate(items_mano):
        draw.text((c1_x + 25, c1_y + 85 + idx_m * 55), it_m, fill=(241, 245, 249), font=obtener_fuente(20, bold=False))
    
    draw.rounded_rectangle([c1_x + 25, c1_y + 325, c1_x + col_w - 25, c1_y + 385], radius=12, fill=(225, 29, 72))
    draw.text((c1_x + 35, c1_y + 342), "Complicarse solo", fill=(255, 255, 255), font=obtener_fuente(20, bold=True))

    # Columna Derecha: CON IA (Verde/Cian)
    c2_x = px + 50 + col_w
    c2_y = py + 85
    draw.rounded_rectangle([c2_x, c2_y, c2_x + col_w, c2_y + 415], radius=18, fill=(6, 78, 59, 240), outline=(16, 185, 129), width=2)
    draw.text((c2_x + 25, c2_y + 25), "CON ASISTENTE IA", fill=(167, 243, 208), font=obtener_fuente(24, bold=True))
    
    items_ia = [
        "• Arrastrar los 50 archivos",
        "• Preguntar en 1 línea",
        "• Total calculado al toque",
        "• Citas de origen exactas",
    ]
    for idx_ia, it_ia in enumerate(items_ia):
        draw.text((c2_x + 25, c2_y + 85 + idx_ia * 55), it_ia, fill=(241, 245, 249), font=obtener_fuente(20, bold=False))

    draw.rounded_rectangle([c2_x + 25, c2_y + 325, c2_x + col_w - 25, c2_y + 385], radius=12, fill=(16, 185, 129))
    draw.text((c2_x + 35, c2_y + 342), "Resuelto en 5 seg", fill=(255, 255, 255), font=obtener_fuente(20, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(245, 158, 11), width=2)
    draw.text((px + 60, py_pill + 20), "• Y pensar que iba a abrirlos uno por uno...", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "cierre_guion_07_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.0))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_cierre_archivos_acumulados(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Encuesta de Catarsis Comunitaria (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.5, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(245, 158, 11), width=3)

    draw.text((px + 40, py + 30), "¿CUÁNTOS ARCHIVOS TENÉS", fill=(255, 245, 0), font=obtener_fuente(34, bold=True))
    draw.text((px + 40, py + 75), "ACUMULADOS EN TU COMPU?", fill=(255, 245, 0), font=obtener_fuente(34, bold=True))

    opciones = [
        ("A", "Menos de 20 (Todo limpio y ordenado)", (16, 185, 129)),
        ("B", "Entre 20 y 100 (Un caos pero sobrevivo)", (59, 130, 246)),
        ("C", "Más de 500 (No abro la carpeta por miedo)", (168, 85, 247)),
    ]

    for idx_o, (letra, texto, col) in enumerate(opciones):
        oy = py + 145 + idx_o * 120
        draw.rounded_rectangle([px + 30, oy, px + pw - 30, oy + 98], radius=16, fill=(2, 6, 23, 245), outline=col, width=2)
        draw.ellipse([px + 50, oy + 22, px + 102, oy + 74], fill=col)
        draw.text((px + 65, oy + 32), letra, fill=(255, 255, 255), font=obtener_fuente(26, bold=True))
        draw.text((px + 120, oy + 35), texto, fill=(248, 250, 252), font=obtener_fuente(22, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(245, 158, 11), width=2)
    draw.text((px + 70, py_pill + 20), "• Dejame tu número en los comentarios", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            salto = int(12 * abs(math.sin(t_sec * 4.0)))
            by = 1120 - salto
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


# ---------------------------------------------------------------------------
# Router Central del Director de Escena
# ---------------------------------------------------------------------------


def renderizar_plano_google_ads_busqueda_trampa(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Mockup de Búsqueda de Google con resultado patrocinado malicioso (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    # Tarjeta principal Google Search Container
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 248), outline=(59, 130, 246), width=2)

    # 1. Barra de Búsqueda Google (y = py + 25..py + 95)
    by_s = py + 25
    draw.rounded_rectangle([px + 30, by_s, px + pw - 30, by_s + 68], radius=34, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    dibujar_icono_lupa(draw, px + 65, by_s + 34, r=13, color=(148, 163, 184))
    draw.text((px + 95, by_s + 20), "Banco Rio Online login", fill=(241, 245, 249), font=obtener_fuente(23, bold=False))
    if int(t_sec * 3) % 2 == 0:
        draw.line([(px + 355, by_s + 18), (px + 355, by_s + 50)], fill=(96, 165, 250), width=2)
    draw.text((px + pw - 130, by_s + 22), "Google", fill=(148, 163, 184), font=obtener_fuente(18, bold=True))

    # 2. Tarjeta Resultado #1 Patrocinado (y = py + 115..py + 495)
    ry = py + 115
    rw = pw - 60
    rh = 380
    draw.rounded_rectangle([px + 30, ry, px + 30 + rw, ry + rh], radius=18, fill=(2, 6, 23, 245), outline=(245, 158, 11), width=2)

    # Badge 'Patrocinado' + URL sospechosa
    draw.rounded_rectangle([px + 55, ry + 25, px + 195, ry + 62], radius=8, fill=(245, 158, 11))
    draw.text((px + 68, ry + 32), "Patrocinado", fill=(15, 23, 42), font=obtener_fuente(17, bold=True))
    draw.text((px + 215, ry + 33), "https://www.banc0-online-seguro.xyz", fill=(148, 163, 184), font=obtener_fuente(18, bold=False))

    # Título del enlace falso
    draw.text((px + 55, ry + 80), "Banco Río - Acceso Oficial Home Banking", fill=(96, 165, 250), font=obtener_fuente(28, bold=True))
    draw.line([(px + 55, ry + 118), (px + 640, ry + 118)], fill=(96, 165, 250), width=1)

    # Snippet de descripción
    draw.text((px + 55, ry + 135), "Ingresá a tu cuenta personal para consultar saldos,", fill=(203, 213, 225), font=obtener_fuente(21, bold=False))
    draw.text((px + 55, ry + 168), "transferencias y pagar servicios de forma inmediata.", fill=(203, 213, 225), font=obtener_fuente(21, bold=False))
    draw.text((px + 55, ry + 205), "Acceso rápido y seguro las 24 horas del día...", fill=(148, 163, 184), font=obtener_fuente(19, bold=False))

    # Caja de alerta sutil del primer puesto
    draw.rounded_rectangle([px + 55, ry + 260, px + rw + 5, ry + 345], radius=12, fill=(30, 41, 59, 220), outline=(71, 85, 105), width=1)
    draw.text((px + 75, ry + 275), "[ ! ] Primer resultado en la pantalla", fill=(245, 158, 11), font=obtener_fuente(18, bold=True))
    draw.text((px + 75, ry + 305), "El usuario suele cliquear acá automáticamente sin mirar", fill=(241, 245, 249), font=obtener_fuente(19, bold=False))

    # Cursor de mouse vectorial apuntando al título
    mx = px + 680
    my = ry + 85
    pts_cursor = [(mx, my), (mx + 18, my + 18), (mx + 8, my + 18), (mx + 13, my + 30), (mx + 7, my + 32), (mx + 2, my + 20), (mx - 6, my + 25)]
    draw.polygon(pts_cursor, fill=(255, 255, 255), outline=(0, 0, 0))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(59, 130, 246), width=2)
    draw.text((px + 45, py_pill + 20), "• Buscás tu banco en Google y tocás el primer enlace...", fill=(255, 255, 255), font=obtener_fuente(23, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(4 * math.sin(t_sec * 3.0))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_alerta_sitio_clonado(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Alerta roja dramática de sitio clonado y phishing (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.40)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    # Tarjeta principal con borde rojo brillante
    pulso_rojo = 0.7 + 0.3 * math.sin(t_sec * 6.0)
    borde_col = (int(239 * pulso_rojo), 68, 68)
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=borde_col, width=3)

    # 1. Cabecera roja de advertencia
    draw.rounded_rectangle([px + 30, py + 25, px + pw - 30, py + 105], radius=16, fill=(225, 29, 72))
    dibujar_icono_alerta(draw, px + 75, py + 65, tam=18, color=(255, 255, 255))
    draw.text((px + 120, py + 45), "¡ALERTA CRÍTICA: SITIO CLONADO!", fill=(255, 255, 255), font=obtener_fuente(27, bold=True))

    # 2. Panel central: Inspección del dominio falso
    uy = py + 125
    draw.rounded_rectangle([px + 30, uy, px + pw - 30, uy + 175], radius=18, fill=(2, 6, 23, 245), outline=(239, 68, 68), width=2)
    draw.text((px + 55, uy + 20), "DIRECCIÓN WEB SOSPECHOSA DETECTADA:", fill=(148, 163, 184), font=obtener_fuente(18, bold=True))

    # Texto con el '0' destacado
    draw.text((px + 55, uy + 60), "https://www.banc", fill=(255, 255, 255), font=obtener_fuente(30, bold=True))
    draw.rounded_rectangle([px + 335, uy + 55, px + 375, uy + 105], radius=8, fill=(225, 29, 72))
    draw.text((px + 342, uy + 58), "0", fill=(255, 255, 255), font=obtener_fuente(34, bold=True))
    draw.text((px + 385, uy + 60), "-online.xyz/login", fill=(255, 255, 255), font=obtener_fuente(30, bold=True))

    draw.text((px + 335, uy + 120), "^ ¡CAMBIARON LA 'O' POR UN CERO!", fill=(254, 205, 211), font=obtener_fuente(18, bold=True))

    # 3. Panel inferior: Consecuencias del engaño
    py_c = py + 320
    draw.rounded_rectangle([px + 30, py_c, px + pw - 30, py_c + 180], radius=18, fill=(2, 6, 23, 245), outline=(71, 85, 105), width=1)
    draw.text((px + 55, py_c + 20), "PELIGROS DE ESTE TIPO DE ESTAFA:", fill=(245, 158, 11), font=obtener_fuente(18, bold=True))
    draw.text((px + 55, py_c + 58), "• Roban usuario y clave cuando intentás entrar", fill=(241, 245, 249), font=obtener_fuente(20, bold=False))
    draw.text((px + 55, py_c + 96), "• Solicitan tokens y códigos de seguridad falsos", fill=(241, 245, 249), font=obtener_fuente(20, bold=False))
    draw.text((px + 55, py_c + 134), "• No es la web institucional de tu banco", fill=(239, 68, 68), font=obtener_fuente(20, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(239, 68, 68), width=2)
    dibujar_icono_alerta(draw, px + 40, py_pill + 35, tam=13, color=(239, 68, 68))
    draw.text((px + 65, py_pill + 20), "Cuidado: Podrías regalar tus claves en una web clonada", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "hook_estresado_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            shake_x = int(3 * math.sin(t_sec * 18.0))
            by = 1120 + shake_x
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_mecanica_anuncio_pagado(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Explicación de la compra de anuncios patrocinados en Google (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(245, 158, 11), width=3)

    # Cabecera
    draw.text((px + 40, py + 25), "¿CÓMO LLEGA UNA ESTAFA AL #1 DE GOOGLE?", fill=(255, 245, 0), font=obtener_fuente(26, bold=True))

    pasos = [
        ("1", "Los estafadores clonan la web del banco", "Copia Visual Idéntica", (59, 130, 246)),
        ("2", "Pagan una campaña en Google Ads", "Publicidad Patrocinada", (245, 158, 11)),
        ("3", "Google los pone primeros por encima del oficial", "El primer puesto se compra", (239, 68, 68)),
    ]

    for idx_p, (num, titulo_p, badge_p, col_p) in enumerate(pasos):
        cy = py + 80 + idx_p * 135
        draw.rounded_rectangle([px + 30, cy, px + pw - 30, cy + 120], radius=16, fill=(2, 6, 23, 245), outline=col_p, width=2)
        # Círculo numerado
        draw.ellipse([px + 50, cy + 25, px + 105, cy + 80], fill=col_p)
        draw.text((px + 68, cy + 34), num, fill=(255, 255, 255), font=obtener_fuente(28, bold=True))

        draw.text((px + 125, cy + 28), titulo_p, fill=(248, 250, 252), font=obtener_fuente(22, bold=True))
        draw.rounded_rectangle([px + 125, cy + 68, px + 440, cy + 102], radius=8, fill=(col_p[0]//4, col_p[1]//4, col_p[2]//4), outline=col_p, width=1)
        draw.text((px + 140, cy + 74), f"• {badge_p}", fill=col_p, font=obtener_fuente(16, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(245, 158, 11), width=2)
    draw.text((px + 45, py_pill + 20), "• Los estafadores pagan anuncios para ponerse arriba", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_inspeccion_url_lupa(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Detección visual letra por letra y regla de patrocinado (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(6, 182, 212), width=3)

    # Cabecera
    draw.text((px + 40, py + 25), "REGLAS DE ORO DE INSPECCIÓN VISUAL", fill=(6, 182, 212), font=obtener_fuente(26, bold=True))

    # Regla 1: Etiqueta Patrocinado
    r1_y = py + 80
    draw.rounded_rectangle([px + 30, r1_y, px + pw - 30, r1_y + 190], radius=16, fill=(2, 6, 23, 245), outline=(245, 158, 11), width=2)
    draw.rounded_rectangle([px + 50, r1_y + 20, px + 200, r1_y + 60], radius=8, fill=(245, 158, 11))
    draw.text((px + 65, r1_y + 28), "Patrocinado", fill=(15, 23, 42), font=obtener_fuente(18, bold=True))
    draw.text((px + 220, r1_y + 26), "<-- SI DICE ESTO EN TU BANCO: ¡FRENA!", fill=(255, 245, 0), font=obtener_fuente(20, bold=True))
    draw.text((px + 50, r1_y + 80), "Un banco casi nunca necesita pagar anuncios para aparecer", fill=(203, 213, 225), font=obtener_fuente(20, bold=False))
    draw.text((px + 50, r1_y + 115), "cuando vos buscás su propio nombre oficial en Google.", fill=(203, 213, 225), font=obtener_fuente(20, bold=False))
    draw.text((px + 50, r1_y + 150), "Desconfianza inmediata ante cualquier tag de anuncio.", fill=(245, 158, 11), font=obtener_fuente(18, bold=True))

    # Regla 2: Inspección de Dominio
    r2_y = py + 290
    draw.rounded_rectangle([px + 30, r2_y, px + pw - 30, r2_y + 210], radius=16, fill=(2, 6, 23, 245), outline=(239, 68, 68), width=2)
    dibujar_icono_lupa(draw, px + 65, r2_y + 35, r=14, color=(239, 68, 68))
    draw.text((px + 95, r2_y + 22), "MIRÁ LA DIRECCIÓN WEB ANTES DE ENTRAR", fill=(239, 68, 68), font=obtener_fuente(21, bold=True))
    draw.text((px + 50, r2_y + 70), "[X] Dominio Falso: www.banc0-online.xyz (Usa cero y .xyz)", fill=(254, 205, 211), font=obtener_fuente(19, bold=False))
    draw.text((px + 50, r2_y + 110), "[X] Dominio Trucho: www.banco-soporte-oficial.net", fill=(254, 205, 211), font=obtener_fuente(19, bold=False))
    draw.text((px + 50, r2_y + 155), "[OK] Los bancos usan .com, .com.ar y dominios oficiales", fill=(52, 211, 153), font=obtener_fuente(18, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(245, 158, 11), width=2)
    dibujar_icono_alerta(draw, px + 40, py_pill + 35, tam=13, color=(245, 158, 11))
    draw.text((px + 65, py_pill + 20), "Si dice Patrocinado, mirá bien la dirección web", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(4 * math.sin(t_sec * 3.0))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_split_anuncio_vs_organico(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Split / Desplazamiento al resultado orgánico oficial verificado (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(16, 185, 129), width=3)

    # 1. Bloque Superior: Anuncio clon tachado (y = py + 20..py + 215)
    ay = py + 20
    draw.rounded_rectangle([px + 25, ay, px + pw - 25, ay + 195], radius=16, fill=(30, 20, 25, 230), outline=(239, 68, 68), width=2)
    draw.rounded_rectangle([px + 45, ay + 18, px + 210, ay + 52], radius=6, fill=(225, 29, 72))
    draw.text((px + 58, ay + 24), "[X] ANUNCIO CLON", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))
    draw.text((px + 225, ay + 24), "www.banc0-online-seguro.xyz", fill=(244, 114, 182), font=obtener_fuente(18, bold=False))
    draw.text((px + 45, ay + 68), "Banco Río - Ingreso Clientes (Falso)", fill=(148, 163, 184), font=obtener_fuente(24, bold=True))
    draw.text((px + 45, ay + 105), "Sitio malicioso creado para capturar claves privadas.", fill=(203, 213, 225), font=obtener_fuente(18, bold=False))
    draw.text((px + 45, ay + 145), "[X] NO TOCAR ESTE ENLACE", fill=(239, 68, 68), font=obtener_fuente(20, bold=True))
    # Línea tachada suave
    draw.line([(px + 35, ay + 35), (px + pw - 35, ay + 175)], fill=(239, 68, 68, 180), width=3)

    # Separador con flecha de scroll
    sy = py + 225
    draw.text((px + pw // 2 - 190, sy), "vv SCROLLEÁ UN SEGUNDO HACIA ABAJO vv", fill=(255, 245, 0), font=obtener_fuente(18, bold=True))

    # 2. Bloque Inferior: Enlace Oficial Orgánico Verificado (y = py + 260..py + 505)
    oy = py + 260
    draw.rounded_rectangle([px + 25, oy, px + pw - 25, oy + 245], radius=16, fill=(6, 78, 59, 250), outline=(16, 185, 129), width=3)
    draw.rounded_rectangle([px + 45, oy + 20, px + 230, oy + 58], radius=8, fill=(16, 185, 129))
    draw.text((px + 58, oy + 27), "[OK] RESULTADO OFICIAL", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    dibujar_icono_candado(draw, px + 260, oy + 38, tam=13, color=(52, 211, 153))
    draw.text((px + 285, oy + 26), "https://www.bancorio.com.ar", fill=(167, 243, 208), font=obtener_fuente(20, bold=True))

    draw.text((px + 45, oy + 75), "Banco Río Oficial • Portal Institucional", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))
    draw.text((px + 45, oy + 118), "Operá con seguridad. Sitio web verificado con cifrado SSL.", fill=(209, 250, 229), font=obtener_fuente(19, bold=False))

    # Badges de seguridad
    badges_seg = ["Candado Verde", "Sin Anuncios", "Sitio Oficial"]
    for idx_b, b_txt in enumerate(badges_seg):
        bx_b = px + 45 + idx_b * 190
        draw.rounded_rectangle([bx_b, oy + 165, bx_b + 175, oy + 205], radius=8, fill=(4, 120, 87), outline=(52, 211, 153), width=1)
        draw.text((bx_b + 20, oy + 174), f"[OK] {b_txt}", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(16, 185, 129))
    draw.text((px + 65, py_pill + 20), "El enlace oficial está más abajo y tiene el dominio real", fill=(255, 255, 255), font=obtener_fuente(23, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_escudo_ciberseguridad(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Hábitos de oro y alivio de ciberseguridad (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(16, 185, 129), width=3)

    # Cabecera
    draw.text((px + 45, py + 30), "ESCUDO DE CIBERSEGURIDAD ACTIVO", fill=(16, 185, 129), font=obtener_fuente(28, bold=True))

    consejos = [
        ("1", "Guardá tu home banking en Favoritos", "No lo busques en Google cada vez, entrás directo y seguro.", (16, 185, 129)),
        ("2", "Scrolleá 2 segundos antes de hacer clic", "Salteá los primeros resultados patrocinados y buscá el oficial.", (59, 130, 246)),
    ]

    for idx_c, (num_c, tit_c, sub_c, col_c) in enumerate(consejos):
        cy = py + 95 + idx_c * 175
        draw.rounded_rectangle([px + 30, cy, px + pw - 30, cy + 155], radius=18, fill=(2, 6, 23, 245), outline=col_c, width=2)
        draw.ellipse([px + 50, cy + 30, px + 115, cy + 95], fill=col_c)
        draw.text((px + 73, cy + 42), num_c, fill=(255, 255, 255), font=obtener_fuente(30, bold=True))

        draw.text((px + 135, cy + 35), tit_c, fill=(255, 255, 255), font=obtener_fuente(24, bold=True))
        draw.text((px + 135, cy + 85), sub_c, fill=(203, 213, 225), font=obtener_fuente(20, bold=False))

    draw.text((px + 45, py + ph - 55), "[OK] Tus claves y cuentas a salvo con 2 segundos de atención", fill=(255, 245, 0), font=obtener_fuente(20, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(16, 185, 129))
    draw.text((px + 65, py_pill + 20), "Mirar la dirección web te salva de dolores de cabeza", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "resultado_guion_10_cotizacion_automatica_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_cierre_debate_estafas(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Encuesta comunitaria sobre estafas y phishing (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "ciudad_cyberpunk")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(245, 158, 11), width=3)

    draw.text((px + 40, py + 30), "¿ALGUNA VEZ CASI CAÉS EN UN", fill=(255, 245, 0), font=obtener_fuente(34, bold=True))
    draw.text((px + 40, py + 75), "LINK TRAMPA DE ESTOS?", fill=(255, 245, 0), font=obtener_fuente(34, bold=True))

    opciones = [
        ("A", "Casi caigo una vez en un link trampa", (239, 68, 68)),
        ("B", "Siempre miro la URL antes de entrar", (16, 185, 129)),
        ("C", "No sabía que pagaban anuncios para estafar", (168, 85, 247)),
    ]

    for idx_o, (letra, texto, col) in enumerate(opciones):
        oy = py + 145 + idx_o * 120
        draw.rounded_rectangle([px + 30, oy, px + pw - 30, oy + 98], radius=16, fill=(2, 6, 23, 245), outline=col, width=2)
        draw.ellipse([px + 50, oy + 22, px + 102, oy + 74], fill=col)
        draw.text((px + 65, oy + 32), letra, fill=(255, 255, 255), font=obtener_fuente(26, bold=True))
        draw.text((px + 120, oy + 35), texto, fill=(248, 250, 252), font=obtener_fuente(22, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(245, 158, 11), width=2)
    draw.text((px + 70, py_pill + 20), "• Dejame tu historia en los comentarios", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            salto = int(12 * abs(math.sin(t_sec * 4.0)))
            by = 1120 - salto
            frame.paste(b_resized, (bx, by), b_resized)

    return frame




def renderizar_plano_noticias_mito_chat(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Portal de Noticias Tech en Vivo (Flash Tech / Byte News) (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    # Tarjeta principal Noticias Container
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(59, 130, 246), width=2)

    # 1. Cabecera del Noticiero (y = py + 25..py + 85)
    draw.rounded_rectangle([px + 30, py + 25, px + 170, py + 65], radius=8, fill=(225, 29, 72))
    draw.ellipse([px + 45, py + 40, px + 55, py + 50], fill=(255, 255, 255))
    draw.text((px + 65, py + 33), "EN VIVO", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))
    draw.text((px + 190, py + 33), "BYTE TECH NEWS • FLASH ESPECIAL", fill=(241, 245, 249), font=obtener_fuente(19, bold=True))
    draw.text((px + pw - 140, py + 33), "20:00 HS", fill=(148, 163, 184), font=obtener_fuente(17, bold=False))

    # 2. Caja Central: El mito del chatbot (y = py + 95..py + 490)
    cy = py + 95
    cw = pw - 60
    ch = 390
    draw.rounded_rectangle([px + 30, cy, px + 30 + cw, cy + ch], radius=18, fill=(2, 6, 23, 245), outline=(71, 85, 105), width=2)

    draw.rounded_rectangle([px + 55, cy + 25, px + 260, cy + 62], radius=8, fill=(245, 158, 11))
    draw.text((px + 70, cy + 32), "PERCEPCIÓN PÚBLICA", fill=(15, 23, 42), font=obtener_fuente(16, bold=True))

    draw.text((px + 55, cy + 85), "¿La IA es solo para pedirle textos a un chat?", fill=(255, 255, 255), font=obtener_fuente(28, bold=True))
    draw.text((px + 55, cy + 130), "Muchos creen que la inteligencia artificial empieza y termina", fill=(203, 213, 225), font=obtener_fuente(20, bold=False))
    draw.text((px + 55, cy + 165), "en pedirle un resumen a un chatbot o generar un meme.", fill=(203, 213, 225), font=obtener_fuente(20, bold=False))

    # Burbuja de chat simulada
    draw.rounded_rectangle([px + 55, cy + 220, px + cw + 5, cy + 305], radius=14, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    draw.text((px + 75, cy + 235), "Usuario: 'Escribime un correo formal para mi jefe...'", fill=(148, 163, 184), font=obtener_fuente(19, bold=False))
    draw.text((px + 75, cy + 268), "IA: 'Estimado, por medio de la presente le informo...'", fill=(59, 130, 246), font=obtener_fuente(19, bold=True))

    draw.text((px + 55, cy + 335), "[ ! ] La punta del iceberg de una revolución mucho más profunda", fill=(245, 158, 11), font=obtener_fuente(18, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(59, 130, 246), width=2)
    draw.text((px + 45, py_pill + 20), "• Muchos creen que la IA es solo para chatear...", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "cold_open_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(4 * math.sin(t_sec * 3.0))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_noticias_breaking_impacto(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Placa de Último Momento / Breaking News (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.40)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    pulso_borde = 0.7 + 0.3 * math.sin(t_sec * 6.0)
    col_borde = (int(239 * pulso_borde), 68, 68)
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=col_borde, width=3)

    # 1. Cabecera BREAKING NEWS
    draw.rounded_rectangle([px + 30, py + 25, px + pw - 30, py + 105], radius=16, fill=(225, 29, 72))
    dibujar_icono_alerta(draw, px + 75, py + 65, tam=18, color=(255, 255, 255))
    draw.text((px + 120, py + 45), "BREAKING NEWS • IMPACTO GLOBAL", fill=(255, 255, 255), font=obtener_fuente(27, bold=True))

    # 2. Titular de impacto
    ty = py + 130
    draw.rounded_rectangle([px + 30, ty, px + pw - 30, ty + 175], radius=18, fill=(2, 6, 23, 245), outline=(239, 68, 68), width=2)
    draw.text((px + 50, ty + 25), "LO QUE ESTÁ PASANDO FUERA DE LAS REDES", fill=(255, 245, 0), font=obtener_fuente(25, bold=True))
    draw.text((px + 50, ty + 70), "La verdadera revolución no está en chatear con bots,", fill=(241, 245, 249), font=obtener_fuente(21, bold=False))
    draw.text((px + 50, ty + 105), "sino en laboratorios, hospitales y centros científicos.", fill=(203, 213, 225), font=obtener_fuente(21, bold=False))

    # 3. Badges de sectores
    by_s = py + 330
    sectores = [
        ("Salud & Medicina", (225, 29, 72)),
        ("Modelos Climáticos", (6, 182, 212)),
        ("Ciencia de Materiales", (16, 185, 129)),
    ]
    for idx_s, (sec_nom, sec_col) in enumerate(sectores):
        bx_s = px + 30 + idx_s * 275
        draw.rounded_rectangle([bx_s, by_s, bx_s + 260, by_s + 155], radius=14, fill=(2, 6, 23, 245), outline=sec_col, width=2)
        draw.rounded_rectangle([bx_s + 15, by_s + 18, bx_s + 60, by_s + 48], radius=6, fill=sec_col)
        draw.text((bx_s + 26, by_s + 24), str(idx_s + 1), fill=(255, 255, 255), font=obtener_fuente(16, bold=True))
        draw.text((bx_s + 15, by_s + 65), sec_nom, fill=(255, 255, 255), font=obtener_fuente(19, bold=True))
        draw.text((bx_s + 15, by_s + 105), "Avances en tiempo real", fill=(148, 163, 184), font=obtener_fuente(15, bold=False))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(239, 68, 68), width=2)
    dibujar_icono_alerta(draw, px + 40, py_pill + 35, tam=13, color=(239, 68, 68))
    draw.text((px + 65, py_pill + 20), "En el mundo real está pasando algo mucho más grande", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto1_feliz_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_noticias_transformacion_silenciosa(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Bento Grid Comparativo ("Lo visible" vs "Lo que avanza") (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(59, 130, 246), width=3)

    # Cabecera
    draw.text((px + 40, py + 25), "EL MAPA REAL DE LA TRANSFORMACIÓN", fill=(59, 130, 246), font=obtener_fuente(26, bold=True))

    # Columna Izquierda: Lo visible en redes
    col_w = (pw - 80) // 2
    cx1 = px + 30
    cy = py + 80
    ch = 410
    draw.rounded_rectangle([cx1, cy, cx1 + col_w, cy + ch], radius=16, fill=(2, 6, 23, 245), outline=(71, 85, 105), width=2)
    draw.rounded_rectangle([cx1 + 20, cy + 20, cx1 + 220, cy + 55], radius=6, fill=(51, 65, 85))
    draw.text((cx1 + 30, cy + 27), "LO QUE SE VE EN REDES", fill=(203, 213, 225), font=obtener_fuente(15, bold=True))

    items_izq = [
        "• Asistentes de chat para tareas",
        "• Generadores de fotos y memes",
        "• Debates sobre si reemplaza humanos",
        "• Filtros y herramientas virales",
    ]
    for idx_i, it_txt in enumerate(items_izq):
        draw.text((cx1 + 20, cy + 85 + idx_i * 65), it_txt, fill=(148, 163, 184), font=obtener_fuente(18, bold=False))

    # Columna Derecha: Lo que avanza en silencio
    cx2 = px + 50 + col_w
    draw.rounded_rectangle([cx2, cy, cx2 + col_w, cy + ch], radius=16, fill=(2, 6, 23, 245), outline=(16, 185, 129), width=2)
    draw.rounded_rectangle([cx2 + 20, cy + 20, cx2 + 250, cy + 55], radius=6, fill=(16, 185, 129))
    draw.text((cx2 + 30, cy + 27), "LO QUE AVANZA EN SILENCIO", fill=(255, 255, 255), font=obtener_fuente(15, bold=True))

    items_der = [
        "[OK] Diagnósticos médicos tempranos",
        "[OK] Predicción de tormentas extremas",
        "[OK] Diseño de nuevos materiales",
        "[OK] Automatización de flujos pesados",
    ]
    for idx_d, dt_txt in enumerate(items_der):
        draw.text((cx2 + 20, cy + 85 + idx_d * 65), dt_txt, fill=(255, 255, 255), font=obtener_fuente(18, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(59, 130, 246), width=2)
    draw.text((px + 45, py_pill + 20), "• Transformando la ciencia y el trabajo en silencio...", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(4 * math.sin(t_sec * 3.0))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_noticias_medicina_diagnostico(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Noticia Médica de Vanguardia (Health Tech Scanner) (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(16, 185, 129), width=3)

    # Cabecera
    draw.rounded_rectangle([px + 30, py + 22, px + 280, py + 58], radius=8, fill=(16, 185, 129))
    draw.text((px + 45, py + 28), "NOTICIA 01 • MEDICINA", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))
    draw.text((px + 300, py + 28), "AVANCES PUBLICADOS EN NATURE", fill=(52, 211, 153), font=obtener_fuente(17, bold=True))

    # Visor de escáner médico
    sy = py + 75
    draw.rounded_rectangle([px + 30, sy, px + pw - 30, sy + 395], radius=18, fill=(6, 30, 25, 245), outline=(16, 185, 129), width=2)

    draw.text((px + 55, sy + 25), "DETECCIÓN TEMPRANA DE PATRONES CELULARES", fill=(255, 255, 255), font=obtener_fuente(25, bold=True))

    # Retícula de diagnóstico
    dy = sy + 75
    draw.rounded_rectangle([px + 55, dy, px + pw - 55, dy + 185], radius=14, fill=(2, 6, 23, 245), outline=(16, 185, 129), width=1)
    draw.text((px + 80, dy + 22), "• Estudios analizados: Tomografías, resonancias y biopsias", fill=(209, 250, 229), font=obtener_fuente(20, bold=False))
    draw.text((px + 80, dy + 62), "• Capacidad técnica: Reconoce anomalías a nivel microscópico", fill=(209, 250, 229), font=obtener_fuente(20, bold=False))
    draw.text((px + 80, dy + 102), "• Factor clave: Alerta temprana meses antes de síntomas graves", fill=(255, 245, 0), font=obtener_fuente(20, bold=True))
    draw.text((px + 80, dy + 142), "• Impacto real: Asistencia directa para médicos especialistas", fill=(52, 211, 153), font=obtener_fuente(19, bold=True))

    # Badges de rigor científico
    badges_med = ["Asistencia Diagnóstica", "Detección Precoz", "Verificado por Especialistas"]
    for idx_m, bm_txt in enumerate(badges_med):
        bx_m = px + 55 + idx_m * 255
        draw.rounded_rectangle([bx_m, sy + 285, bx_m + 240, sy + 325], radius=8, fill=(4, 120, 87), outline=(52, 211, 153), width=1)
        draw.text((bx_m + 20, sy + 294), f"[OK] {bm_txt}", fill=(255, 255, 255), font=obtener_fuente(15, bold=True))

    draw.text((px + 55, sy + 350), "* Complemento de alta precisión, jamás reemplazo de criterio médico", fill=(148, 163, 184), font=obtener_fuente(16, bold=False))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(16, 185, 129))
    draw.text((px + 65, py_pill + 20), "En medicina detecta patrones antes que el ojo humano", fill=(255, 255, 255), font=obtener_fuente(23, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_noticias_ciencia_clima_materiales(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Noticia Científica (Clima y Nuevos Materiales) (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(6, 182, 212), width=3)

    # Cabecera
    draw.rounded_rectangle([px + 30, py + 22, px + 280, py + 58], radius=8, fill=(6, 182, 212))
    draw.text((px + 45, py + 28), "NOTICIA 02 • CIENCIA", fill=(15, 23, 42), font=obtener_fuente(16, bold=True))
    draw.text((px + 300, py + 28), "DEEPMIND • GRAPHCAST Y GNOME", fill=(34, 211, 238), font=obtener_fuente(17, bold=True))

    # Bloque 1: Predicción Climática (y = py + 75)
    c1_y = py + 75
    draw.rounded_rectangle([px + 30, c1_y, px + pw - 30, c1_y + 185], radius=16, fill=(2, 6, 23, 245), outline=(59, 130, 246), width=2)
    draw.text((px + 55, c1_y + 20), "PREDICCIÓN DE CLIMA EXTREMO (GRAPHCAST)", fill=(96, 165, 250), font=obtener_fuente(22, bold=True))
    draw.text((px + 55, c1_y + 60), "• Pronostica ciclones y tormentas con 10 días de anticipación", fill=(241, 245, 249), font=obtener_fuente(19, bold=False))
    draw.text((px + 55, c1_y + 95), "• Calcula trayectorias meteorológicas en menos de 1 minuto", fill=(241, 245, 249), font=obtener_fuente(19, bold=False))
    draw.text((px + 55, c1_y + 135), "[OK] Más rápido y preciso que supercomputadoras tradicionales", fill=(52, 211, 153), font=obtener_fuente(18, bold=True))

    # Bloque 2: Nuevos Materiales (y = py + 280)
    c2_y = py + 280
    draw.rounded_rectangle([px + 30, c2_y, px + pw - 30, c2_y + 195], radius=16, fill=(2, 6, 23, 245), outline=(16, 185, 129), width=2)
    draw.text((px + 55, c2_y + 20), "DESCUBRIMIENTO DE NUEVOS MATERIALES (GNOME)", fill=(52, 211, 153), font=obtener_fuente(22, bold=True))
    draw.text((px + 55, c2_y + 60), "• Diseñó más de 380.000 estructuras cristalinas estables", fill=(241, 245, 249), font=obtener_fuente(19, bold=False))
    draw.text((px + 55, c2_y + 95), "• Equivale a 800 años de investigación experimental humana", fill=(255, 245, 0), font=obtener_fuente(19, bold=True))
    draw.text((px + 55, c2_y + 135), "[OK] Aplicado a nuevas baterías, celdas solares y chips", fill=(34, 211, 238), font=obtener_fuente(18, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(6, 182, 212), width=2)
    dibujar_icono_check(draw, px + 40, py_pill + 35, tam=12, color=(6, 182, 212))
    draw.text((px + 65, py_pill + 20), "Predice el clima y descubre materiales en cuestión de horas", fill=(255, 255, 255), font=obtener_fuente(23, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_noticias_aceleracion_editorial(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Editorial / Salto histórico de productividad (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.35)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(245, 158, 11), width=3)

    # Cabecera
    draw.text((px + 45, py + 25), "EDITORIAL BYTE NEWS • CONCLUSIÓN", fill=(245, 158, 11), font=obtener_fuente(24, bold=True))

    # Titular gigante
    draw.text((px + 45, py + 75), "LA MAYOR ACELERACIÓN TÉCNICA", fill=(255, 255, 255), font=obtener_fuente(34, bold=True))
    draw.text((px + 45, py + 120), "DE NUESTRA ÉPOCA", fill=(255, 245, 0), font=obtener_fuente(34, bold=True))

    # 3 Puntos editoriales
    ey = py + 185
    puntos_edit = [
        ("No es una moda pasajera", "Multiplica la velocidad de resolución en todas las disciplinas."),
        ("No es solo texto o imágenes", "Resuelve cálculos y patrones masivos que eran imposibles."),
        ("El futuro ya está acá", "Quien aprende a integrarla hoy, da un salto cuántico mañana."),
    ]
    for idx_pe, (tit_pe, desc_pe) in enumerate(puntos_edit):
        py_pe = ey + idx_pe * 85
        draw.rounded_rectangle([px + 30, py_pe, px + pw - 30, py_pe + 72], radius=14, fill=(2, 6, 23, 245), outline=(71, 85, 105), width=1)
        dibujar_icono_check(draw, px + 55, py_pe + 36, tam=10, color=(16, 185, 129))
        draw.text((px + 80, py_pe + 16), tit_pe, fill=(255, 255, 255), font=obtener_fuente(20, bold=True))
        draw.text((px + 80, py_pe + 42), desc_pe, fill=(148, 163, 184), font=obtener_fuente(16, bold=False))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(245, 158, 11), width=2)
    draw.text((px + 40, py_pill + 20), "• No es una moda, es la mayor aceleración técnica de la era", fill=(255, 255, 255), font=obtener_fuente(23, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "resultado_guion_10_cotizacion_automatica_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            respira = int(5 * math.sin(t_sec * 3.5))
            by = 1120 + respira
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


def renderizar_plano_noticias_cierre_encuesta_futuro(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 4.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Arquetipo: Encuesta Comunitaria sobre el Impacto Futuro de la IA (Safe Zone: y >= 250)."""
    cfg = config or {}
    estilo_fondo = cfg.get("estilo_fondo", "estudio_tech")
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.45, atenuacion_oscura=0.30)
    draw = ImageDraw.Draw(frame)

    pw, ph = 880, 530
    px = (ancho - pw) // 2
    py = 250

    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(15, 23, 42, 250), outline=(168, 85, 247), width=3)

    draw.text((px + 40, py + 30), "¿EN QUÉ ÁREA CREÉS QUE VA A", fill=(255, 245, 0), font=obtener_fuente(34, bold=True))
    draw.text((px + 40, py + 75), "IMPACTAR MÁS FUERTE EN EL FUTURO?", fill=(255, 245, 0), font=obtener_fuente(32, bold=True))

    opciones = [
        ("A", "Medicina y Salud (Curar y diagnosticar)", (6, 182, 212)),
        ("B", "Ciencia, Energía y Clima (Descubrimientos)", (16, 185, 129)),
        ("C", "Automatización del Trabajo Diario", (168, 85, 247)),
    ]

    for idx_o, (letra, texto, col) in enumerate(opciones):
        oy = py + 145 + idx_o * 120
        draw.rounded_rectangle([px + 30, oy, px + pw - 30, oy + 98], radius=16, fill=(2, 6, 23, 245), outline=col, width=2)
        draw.ellipse([px + 50, oy + 22, px + 102, oy + 74], fill=col)
        draw.text((px + 65, oy + 32), letra, fill=(255, 255, 255), font=obtener_fuente(26, bold=True))
        draw.text((px + 120, oy + 35), texto, fill=(248, 250, 252), font=obtener_fuente(22, bold=True))

    # Píldora inferior (y = 805..875)
    py_pill = 805
    draw.rounded_rectangle([px, py_pill, px + pw, py_pill + 70], radius=22, fill=(15, 23, 42, 245), outline=(168, 85, 247), width=2)
    draw.text((px + 70, py_pill + 20), "• Dejame tu opinión en los comentarios abajo", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # Byte en Zona Exclusiva (y = 1120..1640)
    p_byte = cfg.get("sprite_byte")
    if not p_byte or not Path(p_byte).exists():
        p_byte = DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png"

    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 520
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            salto = int(12 * abs(math.sin(t_sec * 4.0)))
            by = 1120 - salto
            frame.paste(b_resized, (bx, by), b_resized)

    return frame


MAPA_ARQUETIPOS = {

    "PLANO_HERO_CAOS": renderizar_plano_hero_caos,
    "PLANO_SHOWCASE_PANORAMICO": renderizar_plano_showcase_panoramico,
    "PLANO_SPLIT_BEFORE_AFTER": renderizar_plano_split_before_after,
    "PLANO_DECK_3D": renderizar_plano_deck_3d,
    "PLANO_HOST_COMMUNITY": renderizar_plano_host_community,
    "PLANO_PANICO_RELOJ": renderizar_plano_panico_reloj,
    "PLANO_JULIUS_DASHBOARD": renderizar_plano_julius_dashboard,
    "PLANO_GAMMA_SLIDES": renderizar_plano_gamma_slides,
    "PLANO_LAPTOP_CERRADA": renderizar_plano_laptop_finde,
    "PLANO_PERPLEXITY_SEARCH": renderizar_plano_perplexity_search,
    "PLANO_NOTEBOOKLM_DOCS": renderizar_plano_notebooklm_docs,
    "PLANO_BROWSER_TABS_CAOS": renderizar_plano_browser_tabs_caos,
    "PLANO_SINGLE_TAB_ZEN": renderizar_plano_single_tab_zen,
    "PLANO_BATTLE_VS": renderizar_plano_battle_vs,
    "PLANO_FLYER_PAINT_CAOS": renderizar_plano_flyer_paint_caos,
    "PLANO_CANVA_MAGIC_DESIGN": renderizar_plano_canva_magic_design,
    "PLANO_REMOVE_BG": renderizar_plano_remove_bg,
    "PLANO_FLYER_SHOWCASE_ZEN": renderizar_plano_flyer_showcase_zen,
    "PLANO_CHAT_FLYER_URGENTE": renderizar_plano_chat_flyer_urgente,
    "PLANO_PHOTOSHOP_FREEZE": renderizar_plano_photoshop_freeze,
    "PLANO_LIENZO_BLANCO_BLOQUEO": renderizar_plano_lienzo_blanco_bloqueo,
    "PLANO_REMOVE_BG_LASER": renderizar_plano_remove_bg_laser,
    "PLANO_SMARTPHONE_INSTAGRAM_FEED": renderizar_plano_smartphone_instagram_feed,
    "PLANO_WHATSAPP_PEDIDO_REMERAS": renderizar_plano_whatsapp_pedido_remeras,
    "PLANO_BYTE_PASE_IA": renderizar_plano_byte_pase_ia,
    "PLANO_TABLA_PRESUPUESTO_EXTRACCION": renderizar_plano_tabla_presupuesto_extraccion,
    "PLANO_TABLA_COTIZAR_ORDENADA": renderizar_plano_tabla_cotizar_ordenada,
    "PLANO_COTIZACION_FORMAL_PDF": renderizar_plano_cotizacion_formal_pdf,
    "PLANO_CIERRE_PREGUNTA_AUTOMATIZAR": renderizar_plano_cierre_pregunta_automatizar,
    "PLANO_CINCUENTA_ARCHIVOS_CAOS": renderizar_plano_cincuenta_archivos_caos,
    "PLANO_BYTE_RECHAZO_MANUAL": renderizar_plano_byte_rechazo_manual,
    "PLANO_DRAG_DROP_IA_ANALISIS": renderizar_plano_drag_drop_ia_analisis,
    "PLANO_RAG_RESULTADO_CITAS": renderizar_plano_rag_resultado_citas,
    "PLANO_HUMOR_SUFRIR_GRATIS": renderizar_plano_humor_sufrir_gratis,
    "PLANO_CIERRE_ARCHIVOS_ACUMULADOS": renderizar_plano_cierre_archivos_acumulados,
    "PLANO_GOOGLE_ADS_BUSQUEDA_TRAMPA": renderizar_plano_google_ads_busqueda_trampa,
    "PLANO_ALERTA_SITIO_CLONADO": renderizar_plano_alerta_sitio_clonado,
    "PLANO_MECANICA_ANUNCIO_PAGADO": renderizar_plano_mecanica_anuncio_pagado,
    "PLANO_INSPECCION_URL_LUPA": renderizar_plano_inspeccion_url_lupa,
    "PLANO_SPLIT_ANUNCIO_VS_ORGANICO": renderizar_plano_split_anuncio_vs_organico,
    "PLANO_ESCUDO_CIBERSEGURIDAD": renderizar_plano_escudo_ciberseguridad,
    "PLANO_CIERRE_DEBATE_ESTAFAS": renderizar_plano_cierre_debate_estafas,
    "PLANO_NOTICIAS_MITO_CHAT": renderizar_plano_noticias_mito_chat,
    "PLANO_NOTICIAS_BREAKING_IMPACTO": renderizar_plano_noticias_breaking_impacto,
    "PLANO_NOTICIAS_TRANSFORMACION_SILENCIOSA": renderizar_plano_noticias_transformacion_silenciosa,
    "PLANO_NOTICIAS_MEDICINA_DIAGNOSTICO": renderizar_plano_noticias_medicina_diagnostico,
    "PLANO_NOTICIAS_CIENCIA_CLIMA_MATERIALES": renderizar_plano_noticias_ciencia_clima_materiales,
    "PLANO_NOTICIAS_ACELERACION_EDITORIAL": renderizar_plano_noticias_aceleracion_editorial,
    "PLANO_NOTICIAS_CIERRE_ENCUESTA_FUTURO": renderizar_plano_noticias_cierre_encuesta_futuro,
}


def renderizar_escena_por_arquetipo(
    arquetipo: str,
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Invoca la función del arquetipo cinematográfico correspondiente."""
    fn = MAPA_ARQUETIPOS.get(arquetipo)
    if not fn:
        # Fallback inteligente según nombre
        if "caos" in arquetipo.lower() or "problema" in arquetipo.lower():
            fn = renderizar_plano_hero_caos
        elif "showcase" in arquetipo.lower() or "gamma" in arquetipo.lower():
            fn = renderizar_plano_showcase_panoramico
        elif "split" in arquetipo.lower() or "canva" in arquetipo.lower():
            fn = renderizar_plano_split_before_after
        elif "3d" in arquetipo.lower() or "resultado" in arquetipo.lower():
            fn = renderizar_plano_deck_3d
        else:
            fn = renderizar_plano_host_community

    return fn(ancho=ancho, alto=alto, t_sec=t_sec, duracion=duracion, config=config)


# ---------------------------------------------------------------------------
# Generador de Video MP4 para Escenas Cinematográficas
# ---------------------------------------------------------------------------
import subprocess

def generar_video_cinematico_escena(
    arquetipo: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    config: Optional[Dict[str, Any]] = None,
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Renderiza un video animado completo en base a un arquetipo cinematográfico enviando frames a FFmpeg."""
    ruta_salida = Path(ruta_salida)
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    total_frames = max(1, int(duracion_segundos * fps))

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{ancho}x{alto}",
        "-pix_fmt", "rgba",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "18",
        str(ruta_salida)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for f_idx in range(total_frames):
            if f_idx % 60 == 0 or f_idx == total_frames - 1:
                print(f"  [{arquetipo}] Frame {f_idx + 1}/{total_frames} ({((f_idx + 1) / total_frames) * 100:.0f}%)...", flush=True)

            t_sec = f_idx / float(fps)
            frame_img = renderizar_escena_por_arquetipo(
                arquetipo=arquetipo,
                ancho=ancho,
                alto=alto,
                t_sec=t_sec,
                duracion=duracion_segundos,
                config=config
            )
            proc.stdin.write(frame_img.tobytes())
        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        raise e

    print(f"Video cinematográfico generado en: {ruta_salida} ({total_frames} frames)")
    return ruta_salida


# ---------------------------------------------------------------------------
# Mapeo y Wrapper para Video 06: Atención al Cliente con IA
# ---------------------------------------------------------------------------
CONFIGS_ATENCION_CLIENTES = {
    "escena_problema": ("PLANO_HERO_CAOS", {
        "badge": "MENSAJES REPETITIVOS A MANO",
        "elementos": [
            {"x": 60, "y": 240, "w": 330, "h": 160, "rot": -10, "tit": "¿Cuánto sale el envío?", "sub": "Pregunta #1 • Sin responder", "col": (225, 29, 72)},
            {"x": 660, "y": 230, "w": 330, "h": 170, "rot": 12, "tit": "¿Tienen stock disponible?", "sub": "Pregunta #2 • Esperando 2h", "col": (225, 29, 72)},
            {"x": 40, "y": 870, "w": 320, "h": 150, "rot": 8, "tit": "¿Cuáles son los horarios?", "sub": "Pregunta #3 • Clientes impacientes", "col": (245, 158, 11)},
            {"x": 690, "y": 910, "w": 330, "h": 160, "rot": -8, "tit": "¿Cómo hago para pagar?", "sub": "Pregunta #4 • Misma duda diaria", "col": (225, 29, 72)},
        ]
    }),
    "punto_1": ("PLANO_SHOWCASE_PANORAMICO", {
        "header": "Intercom Fin • Agente de IA Activo 24/7",
        "badge": "⚡ Soporte Autónomo",
        "titulo": "Consulta de Cliente: Envíos al Interior",
        "subtitulo": "Fin lee tu centro de ayuda y responde con precisión en 2 segundos",
        "items": [
            ("01 • Duda Cliente", "¿Hacen envíos al interior del país?", (37, 99, 235), (239, 246, 255)),
            ("02 • RAG en Docs", "Consultando base de conocimiento...", (124, 58, 237), (245, 243, 255)),
            ("03 • Respuesta Fin", "Sí, entregas en 24 a 48 hs hábiles", (5, 150, 105), (236, 253, 245))
        ],
        "footer": "Ticket resuelto al instante sin tocar el teclado"
    }),
    "punto_2": ("PLANO_SPLIT_BEFORE_AFTER", {
        "antes_tag": "ANTES",
        "antes_tit": "Soporte manual lento y con demoras",
        "antes_items": [
            "• Cliente esperando 4 horas fuera de horario",
            "• Mensajes repetidos colapsando la bandeja",
            "• Equipo saturado respondiendo siempre lo mismo"
        ],
        "separador": "TIDIO LYRO AI",
        "despues_tag": "DESPUÉS",
        "despues_tit": "Resolución automática las 24 horas",
        "pills_despues": [
            ("Cero Espera", "Respuestas en 3 segundos a las 03:00 AM", (124, 58, 237), (245, 243, 255)),
            ("Entrenado con FAQs", "Cita artículos oficiales sin alucinar", (14, 165, 233), (240, 249, 255)),
            ("Equipo Liberado", "Foco 100% en dudas complejas y ventas", (16, 185, 129), (236, 253, 245))
        ]
    }),
    "resultado": ("PLANO_DECK_3D", {
        "titulo": "¡Bandeja de Soporte en Cero!",
        "subtitulo": "Lo repetitivo resuelto, foco en lo que necesita atención humana",
        "cards": [
            {"x_off": -180, "y": 380, "tit": "Ticket #182 • Envíos", "desc": "Resuelto por IA al instante", "rot": -7, "col": (37, 99, 235)},
            {"x_off": 180, "y": 380, "tit": "Ticket #184 • Precios", "desc": "Resuelto por IA al instante", "rot": 7, "col": (124, 58, 237)},
            {"x_off": 0, "y": 360, "tit": "Ticket #183 • Caso VIP", "desc": "Derivado a atención humana", "rot": 0, "col": (16, 185, 129)}
        ],
        "pills": [
            ("Menos Caos", (16, 185, 129)),
            ("Más Liviano", (14, 165, 233)),
            ("Foco Humano", (124, 58, 237))
        ]
    }),
    "cierre": ("PLANO_HOST_COMMUNITY", {
        "pregunta_tit": "PREGUNTA A LA COMUNIDAD:",
        "pregunta_l1": "¿Cuántas horas al día perdés",
        "pregunta_l2": "respondiendo mensajes?",
        "opciones": [
            ("A", "1 a 2 horas respondiendo lo mismo", (37, 99, 235), (239, 246, 255)),
            ("B", "Medio día atado a contestar mensajes", (124, 58, 237), (245, 243, 255)),
            ("C", "Vivo contestando dudas todo el día", (16, 185, 129), (236, 253, 245)),
        ],
        "callout": "Contame abajo"
    }),
}

def generar_video_interactivo_atencion_clientes(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 06 (Atención al cliente con IA)."""
    mapa = {
        "escena_problema": "escena_problema",
        "hook": "escena_problema",
        "problema": "escena_problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "fin": "punto_1",
        "intercom": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "lyro": "punto_2",
        "tidio": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "escena_problema")
    arquetipo, cfg = CONFIGS_ATENCION_CLIENTES.get(clave, ("PLANO_HERO_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Mapeo y Wrapper para Video 07: Salir del Excel (Julius AI + Gamma)
# ---------------------------------------------------------------------------
CONFIGS_EXCEL_REPORTES = {
    "cold_open": ("PLANO_PANICO_RELOJ", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "VIERNES • 17:59 HS",
        "hora": "17:59",
        "sub_reloj": "TIEMPO LÍMITE: 1 MINUTO PARA EL CIERRE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png",
        "elementos": [
            {"x": 40, "y": 410, "w": 340, "h": 140, "rot": -10, "tit": "POV: Viernes 17:59", "sub": "El jefe pide el reporte", "col": (225, 29, 72)},
            {"x": 690, "y": 400, "w": 340, "h": 140, "rot": 12, "tit": "¡SIN REPORTE!", "sub": "Y con ganas de irte a casa", "col": (239, 68, 68)},
        ]
    }),
    "hook": ("PLANO_HERO_CAOS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "ESTO TE SACA DEL EXCEL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "hook_guion_07_transparente.png",
        "elementos": [
            {"x": 60, "y": 240, "w": 340, "h": 150, "rot": -9, "tit": "Error #¡REF!", "sub": "Fórmula rota en fila 420", "col": (225, 29, 72)},
            {"x": 660, "y": 230, "w": 340, "h": 150, "rot": 11, "tit": "4.280 filas", "sub": "Sin ordenar ni limpiar", "col": (225, 29, 72)},
            {"x": 50, "y": 1200, "w": 340, "h": 150, "rot": 7, "tit": "#¡VALOR!", "sub": "Faltan datos de ventas", "col": (245, 158, 11)},
            {"x": 670, "y": 1220, "w": 340, "h": 150, "rot": -7, "tit": "Cálculo infinito...", "sub": "Ventilador al máximo", "col": (225, 29, 72)},
        ]
    }),
    "problema": ("PLANO_HERO_CAOS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "EL INFORME TE COME LA TARDE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "problema_guion_07_transparente.png",
        "elementos": [
            {"x": 60, "y": 250, "w": 330, "h": 150, "rot": -8, "tit": "Copiar y pegar", "sub": "Celdas que no coinciden", "col": (225, 29, 72)},
            {"x": 670, "y": 240, "w": 330, "h": 150, "rot": 10, "tit": "Acomodar gráficos", "sub": "Tablas desalineadas", "col": (225, 29, 72)},
            {"x": 50, "y": 1200, "w": 340, "h": 150, "rot": 7, "tit": "Horas perdidas", "sub": "Un viernes a la tarde", "col": (245, 158, 11)},
            {"x": 680, "y": 1220, "w": 340, "h": 150, "rot": -8, "tit": "Borrador sin fin", "sub": "Todo por hacer a mano", "col": (225, 29, 72)},
        ]
    }),
    "punto_1": ("PLANO_JULIUS_DASHBOARD", {
        "estilo_fondo": "ciudad_cyberpunk",
        "header": "JULIUS AI • Analista de Datos Inteligente",
        "badge": "Gráficos en 1 Frase",
        "titulo": "Analizá las ventas de la semana y armá gráficos",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_07_transparente.png"
    }),
    "punto_2": ("PLANO_GAMMA_SLIDES", {
        "estilo_fondo": "ciudad_cyberpunk",
        "header": "GAMMA • Diapositivas Generadas con IA",
        "badge": "De Idea a Slides",
        "titulo": "Presentación Prolija en Minutos",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_07_transparente.png"
    }),
    "resultado": ("PLANO_LAPTOP_CERRADA", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "VIERNES 18:00 • INFORME ENVIADO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_07_transparente.png"
    }),
    "cierre": ("PLANO_HOST_COMMUNITY", {
        "estilo_fondo": "ciudad_cyberpunk",
        "pregunta_tit": "PREGUNTA A LA COMUNIDAD:",
        "pregunta_l1": "¿Vos cómo armás tus reportes",
        "pregunta_l2": "hoy en el trabajo?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_07_transparente.png",
        "opciones": [
            ("A", "Excel a mano y sufriendo hasta tarde", (225, 29, 72), (255, 241, 242)),
            ("B", "Copio y pego fórmulas rezando que anden", (124, 58, 237), (245, 243, 255)),
            ("C", "Ya uso IA y salgo a las 18:00 en punto", (16, 185, 129), (236, 253, 245)),
        ],
        "callout": "Contame abajo"
    }),
}

def generar_video_interactivo_excel_reportes(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 07 (Salir del Excel con Julius y Gamma)."""
    mapa = {
        "cold_open": "cold_open",
        "panico": "cold_open",
        "reloj": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "julius": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "gamma": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_EXCEL_REPORTES.get(clave, ("PLANO_HERO_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 08 (Búsqueda e Investigación: Perplexity y NotebookLM)
# ---------------------------------------------------------------------------
CONFIGS_BUSQUEDA_INVESTIGACION = {
    "cold_open": ("PLANO_BROWSER_TABS_CAOS", {
        "estilo_fondo": "viaje_espacial",
        "badge": "POV: 10 PESTAÑAS ABIERTAS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cold_open_guion_08_busqueda_investigacion_transparente.png",
    }),
    "hook": ("PLANO_BROWSER_TABS_CAOS", {
        "estilo_fondo": "viaje_espacial",
        "badge": "DEJÁ DE BUSCAR A CIEGAS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "hook_guion_08_busqueda_investigacion_transparente.png",
    }),
    "problema": ("PLANO_BROWSER_TABS_CAOS", {
        "estilo_fondo": "viaje_espacial",
        "badge": "NINGUNA DA LA RESPUESTA",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "problema_guion_08_busqueda_investigacion_transparente.png",
    }),
    "punto_1": ("PLANO_PERPLEXITY_SEARCH", {
        "estilo_fondo": "viaje_espacial",
        "header": "PERPLEXITY AI • Motor de Respuestas en Tiempo Real",
        "badge": "⚡ En Vivo",
        "titulo": "Buscá datos verificados de mercado y citá fuentes",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png"
    }),
    "punto_2": ("PLANO_NOTEBOOKLM_DOCS", {
        "estilo_fondo": "viaje_espacial",
        "header": "GOOGLE NOTEBOOKLM • Asistente de tus Propios Archivos",
        "badge": "✓ Tus Datos",
        "titulo": "Resumí las obligaciones del contrato y los plazos",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png"
    }),
    "resultado": ("PLANO_SINGLE_TAB_ZEN", {
        "estilo_fondo": "viaje_espacial",
        "badge": "RESPUESTA CORRECTA AL TOQUE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_08_busqueda_investigacion_transparente.png"
    }),
    "cierre": ("PLANO_BATTLE_VS", {
        "estilo_fondo": "viaje_espacial",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_08_busqueda_investigacion_transparente.png",
    }),
}

def generar_video_interactivo_busqueda_investigacion(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 08 (Búsqueda e Investigación con Perplexity y NotebookLM)."""
    mapa = {
        "cold_open": "cold_open",
        "panico": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "perplexity": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "notebooklm": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_BUSQUEDA_INVESTIGACION.get(clave, ("PLANO_HERO_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 09 (Diseño de Flyers: Canva y Remove.bg)
# ---------------------------------------------------------------------------
CONFIGS_DISENO_FLYERS = {
    "cold_open": ("PLANO_CHAT_FLYER_URGENTE", {
        "estilo_fondo": "estudio_creativo",
        "badge": "POV: NECESITÁS UN FLYER URGENTE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_agotado_transparente.png",
    }),
    "hook": ("PLANO_PHOTOSHOP_FREEZE", {
        "estilo_fondo": "estudio_creativo",
        "badge": "DEJÁ DE PELEAR CON EL DISEÑO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_04_transparente.png",
    }),
    "problema": ("PLANO_LIENZO_BLANCO_BLOQUEO", {
        "estilo_fondo": "estudio_creativo",
        "badge": "ABRÍS Y NO SABÉS QUÉ HACER",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png",
    }),
    "punto_1": ("PLANO_CANVA_MAGIC_DESIGN", {
        "estilo_fondo": "estudio_creativo",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_04_transparente.png",
    }),
    "punto_2": ("PLANO_REMOVE_BG_LASER", {
        "estilo_fondo": "estudio_creativo",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_transparente.png",
    }),
    "resultado": ("PLANO_SMARTPHONE_INSTAGRAM_FEED", {
        "estilo_fondo": "estudio_creativo",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_04_transparente.png",
    }),
    "cierre": ("PLANO_BATTLE_VS", {
        "estilo_fondo": "estudio_creativo",
        "header_debate": "DEBATE A LA COMUNIDAD:",
        "pregunta_debate": "¿Sos Team Canva o Team Photoshop?",
        "titulo_izq": "TEAM PHOTOSHOP",
        "titulo_der": "TEAM CANVA + IA",
        "items_izq": [
            "• Recortando a pluma",
            "• 50 capas sin nombrar",
            "• Programa pesado y caro",
            "• Tarde entera perdida"
        ],
        "items_der": [
            "• Magic Design en 1 clic",
            "• Remove.bg automático",
            "• Layouts pro al instante",
            "• Publicado en 3 minutos"
        ],
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_08_busqueda_investigacion_transparente.png",
    }),
}

def generar_video_interactivo_diseno_flyers(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 09 (Diseño de Flyers: Canva y Remove.bg)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "canva": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "remove_bg": "punto_2",
        "removebg": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_DISENO_FLYERS.get(clave, ("PLANO_FLYER_PAINT_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 10 (Cotización Automática de Pedidos)
# ---------------------------------------------------------------------------
CONFIGS_COTIZACION_AUTOMATICA = {
    "cold_open": ("PLANO_WHATSAPP_PEDIDO_REMERAS", {
        "estilo_fondo": "estudio_creativo",
        "badge": "PEDIDO ENTRANTE DE UN CLIENTE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_transparente.png",
    }),
    "hook": ("PLANO_WHATSAPP_PEDIDO_REMERAS", {
        "estilo_fondo": "estudio_creativo",
        "badge": "NO PIENSO CALCULAR ESTO A MANO",
        "alerta_calculo": True,
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_04_transparente.png",
    }),
    "problema": ("PLANO_BYTE_PASE_IA", {
        "estilo_fondo": "estudio_creativo",
        "badge": "LE PASO EL TEXTO DIRECTO A LA IA",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_computadora_feliz_transparente.png",
    }),
    "punto_1": ("PLANO_TABLA_PRESUPUESTO_EXTRACCION", {
        "estilo_fondo": "estudio_creativo",
        "badge": "EXTRAE CANTIDADES Y DETALLES EN SEGUNDOS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_04_transparente.png",
    }),
    "punto_2": ("PLANO_TABLA_COTIZAR_ORDENADA", {
        "estilo_fondo": "estudio_creativo",
        "badge": "TODO ORDENADO Y LISTO PARA COTIZAR",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png",
    }),
    "resultado": ("PLANO_COTIZACION_FORMAL_PDF", {
        "estilo_fondo": "estudio_creativo",
        "badge": "REVISO LOS PRECIOS Y SE LA MANDO AL CLIENTE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_04_transparente.png",
    }),
    "cierre": ("PLANO_CIERRE_PREGUNTA_AUTOMATIZAR", {
        "estilo_fondo": "estudio_creativo",
        "badge": "¿QUÉ TAREA AUTOMATIZARÍAS PRIMERO?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png",
    }),
}


def generar_video_interactivo_cotizacion_automatica(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 10 (Cotización Automática de Pedidos)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "extraccion": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "presupuesto": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_COTIZACION_AUTOMATICA.get(clave, ("PLANO_WHATSAPP_PEDIDO_REMERAS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 11 (50 Archivos - Análisis Documental IA)
# ---------------------------------------------------------------------------
CONFIGS_CINCUENTA_ARCHIVOS = {
    "cold_open": ("PLANO_CINCUENTA_ARCHIVOS_CAOS", {
        "estilo_fondo": "estudio_tech",
        "badge": "CARPETA: FACTURAS_PROVEEDORES/ (50 PDFs)",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "escena_problema_guion_03_transparente.png",
    }),
    "hook": ("PLANO_BYTE_RECHAZO_MANUAL", {
        "estilo_fondo": "estudio_tech",
        "badge": "NO PIENSO ABRIR UNA POR UNA",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_10_cotizacion_automatica_transparente.png",
    }),
    "problema": ("PLANO_BYTE_RECHAZO_MANUAL", {
        "estilo_fondo": "estudio_tech",
        "badge": "SI REVISO 1 POR 1 SE ME VA TODA LA TARDE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png",
    }),
    "punto_1": ("PLANO_DRAG_DROP_IA_ANALISIS", {
        "estilo_fondo": "estudio_tech",
        "badge": "CARGA MASIVA Y ANÁLISIS EN SEGUNDOS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_computadora_feliz_transparente.png",
    }),
    "punto_2": ("PLANO_RAG_RESULTADO_CITAS", {
        "estilo_fondo": "estudio_tech",
        "badge": "TOTAL EXTRAÍDO + DOCUMENTOS DE ORIGEN",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_08_busqueda_investigacion_transparente.png",
    }),
    "resultado": ("PLANO_HUMOR_SUFRIR_GRATIS", {
        "estilo_fondo": "estudio_tech",
        "badge": "QUÉ MANERA DE COMPLICARME SOLO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_07_transparente.png",
    }),
    "cierre": ("PLANO_CIERRE_ARCHIVOS_ACUMULADOS", {
        "estilo_fondo": "estudio_tech",
        "badge": "¿CUÁNTOS ARCHIVOS TENÉS ACUMULADOS?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png",
    }),
}


def generar_video_interactivo_cincuenta_archivos(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 11 (50 Archivos - Análisis Documental IA)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "extraccion": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "citas": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_CINCUENTA_ARCHIVOS.get(clave, ("PLANO_CINCUENTA_ARCHIVOS_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )

# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 12 (Ciberseguridad y Google Ads Maliciosos)
# ---------------------------------------------------------------------------
CONFIGS_CIBERSEGURIDAD_GOOGLE_ADS = {
    "cold_open": ("PLANO_GOOGLE_ADS_BUSQUEDA_TRAMPA", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "GOOGLE SEARCH • BANCO RÍO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png",
    }),
    "hook": ("PLANO_ALERTA_SITIO_CLONADO", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "ALERTA: SITIO CLONADO (PHISHING)",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "hook_estresado_transparente.png",
    }),
    "problema": ("PLANO_MECANICA_ANUNCIO_PAGADO", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "LOS ESTAFADORES PAGAN ANUNCIOS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png",
    }),
    "punto_1": ("PLANO_INSPECCION_URL_LUPA", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "SI DICE PATROCINADO, MIRÁ LA URL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png",
    }),
    "punto_2": ("PLANO_SPLIT_ANUNCIO_VS_ORGANICO", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "RESULTADO ORGÁNICO OFICIAL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png",
    }),
    "resultado": ("PLANO_ESCUDO_CIBERSEGURIDAD", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "ESCUDO DE NAVEGACIÓN ACTIVO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_10_cotizacion_automatica_transparente.png",
    }),
    "cierre": ("PLANO_CIERRE_DEBATE_ESTAFAS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "¿CASI CAÉS EN UN LINK TRAMPA?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png",
    }),
}


def generar_video_interactivo_ciberseguridad_google_ads(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 12 (Ciberseguridad y Google Ads Maliciosos)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "inspeccion": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "organico": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_CIBERSEGURIDAD_GOOGLE_ADS.get(clave, ("PLANO_GOOGLE_ADS_BUSQUEDA_TRAMPA", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )

# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 13 (Portal de Noticias de IA - Qué Hace Realmente la IA)
# ---------------------------------------------------------------------------
CONFIGS_NOTICIAS_IA_REALIDAD = {
    "cold_open": ("PLANO_NOTICIAS_MITO_CHAT", {
        "estilo_fondo": "estudio_tech",
        "badge": "BYTE TECH NEWS • FLASH ESPECIAL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_transparente.png",
    }),
    "hook": ("PLANO_NOTICIAS_BREAKING_IMPACTO", {
        "estilo_fondo": "estudio_tech",
        "badge": "BREAKING NEWS • IMPACTO REAL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto1_feliz_transparente.png",
    }),
    "problema": ("PLANO_NOTICIAS_TRANSFORMACION_SILENCIOSA", {
        "estilo_fondo": "estudio_tech",
        "badge": "TRANSFORMACIÓN EN SILENCIO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png",
    }),
    "punto_1": ("PLANO_NOTICIAS_MEDICINA_DIAGNOSTICO", {
        "estilo_fondo": "estudio_tech",
        "badge": "NOTICIA 01 • MEDICINA",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png",
    }),
    "punto_2": ("PLANO_NOTICIAS_CIENCIA_CLIMA_MATERIALES", {
        "estilo_fondo": "estudio_tech",
        "badge": "NOTICIA 02 • CIENCIA Y MATERIALES",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png",
    }),
    "resultado": ("PLANO_NOTICIAS_ACELERACION_EDITORIAL", {
        "estilo_fondo": "estudio_tech",
        "badge": "EDITORIAL FINAL • BYTE TECH NEWS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_10_cotizacion_automatica_transparente.png",
    }),
    "cierre": ("PLANO_NOTICIAS_CIERRE_ENCUESTA_FUTURO", {
        "estilo_fondo": "estudio_tech",
        "badge": "¿EN QUÉ ÁREA IMPACTARÁ MÁS?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png",
    }),
}


def generar_video_interactivo_noticias_ia_realidad(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 13 (Portal de Noticias de IA)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "medicina": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "ciencia": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_NOTICIAS_IA_REALIDAD.get(clave, ("PLANO_NOTICIAS_MITO_CHAT", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )

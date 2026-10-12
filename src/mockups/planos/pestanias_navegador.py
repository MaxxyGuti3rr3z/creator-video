"""
src.mockups.planos.pestanias_navegador
---------------------------------------------------------------------------
Planos de pestanas de navegador (compartidos videos 08/09).
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
    atenuacion = cfg.get("atenuacion_oscura", 0.25)
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=atenuacion)
    draw = ImageDraw.Draw(frame)

    # 1. Título Superior Estilo Debate (inicia en y=250, zona muerta 0..240 vacía)
    draw.rounded_rectangle([100, 250, ancho - 100, 360], radius=20, fill=(15, 23, 42, 240), outline=(56, 189, 248), width=2)
    dibujar_chispa_ia(draw, 135, 290, 12, (56, 189, 248))
    tit_debate = cfg.get("header_debate", "DEBATE A LA COMUNIDAD:")
    draw.text((165, 275), tit_debate, fill=(56, 189, 248), font=obtener_fuente(22, bold=True))
    preg_debate = cfg.get("pregunta_debate", "¿Sos Team 50 pestañas o Team 1 clic?")
    draw.text((130, 315), preg_debate, fill=(255, 255, 255), font=obtener_fuente(28, bold=True))

    # 2. Las Dos Tarjetas de Batalla Lado a Lado (Card VS) — franja y=380..780, x=100..980
    y_card = 380
    h_card = 400
    w_card = (880 - 20) // 2

    # Lado Izquierdo: Rojo
    x_izq = 100
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

    # 3. Floating Callout (única píldora flotante en y=790..860, franja permitida)
    txt_callout = cfg.get("callout", "¿De qué lado estás? Votá en comentarios")
    f_com = obtener_fuente(28, bold=True)
    bbox_com = draw.textbbox((0, 0), txt_callout, font=f_com)
    cw = min(bbox_com[2] - bbox_com[0] + 130, 860)
    cx_com = (ancho - cw) // 2
    draw.rounded_rectangle([cx_com, 790, cx_com + cw, 860], radius=35, fill=(15, 23, 42, 245), outline=(234, 179, 8), width=2)
    dibujar_chispa_ia(draw, cx_com + 34, 825, 10, (234, 179, 8))
    draw.text((cx_com + 72, 806), txt_callout, fill=(255, 255, 255), font=f_com)

    # 4. Byte Host en el Centro Señalando (base en y=1650, zona sagrada)
    p_byte = cfg.get("sprite_byte")
    if p_byte and Path(p_byte).exists():
        with Image.open(p_byte) as img_b:
            b_cropped = img_b.crop(img_b.convert("RGBA").getbbox())
            aspect = b_cropped.width / max(1, b_cropped.height)
            bh = 510
            bw = int(bh * aspect)
            b_resized = b_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            by = 1134 + int(6 * math.sin(t_sec * 3.0))
            frame.paste(b_resized, (bx, by), b_resized)

    return frame

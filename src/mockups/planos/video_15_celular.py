"""
src.mockups.planos.video_15_celular
---------------------------------------------------------------------------
Planos nativos del Video 15 (IA en tu celular): popup de sospecha,
wake word, Circle to Search, resumen de notificaciones, balance
celu/nube y cierre de pregunta-debate.

Safe zones respetadas (lint_zonas_seguras):
 - sin contenido brillante en y<250 ni y>1650 (base de Byte <= 1650)
 - en y=250..900 todo el contenido vive en x=90..990
 - UI en y=250..780, pildora en y=790..870, Byte en y>=1090
"""

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter

from src.mockups.motor import (
    dibujar_chispa_ia,
    dibujar_icono_check,
    obtener_fuente,
    pegar_byte_animado,
)
from src.mockups.motion import pop_scale, type_chars
from src.mockups.estilos.animaciones_fondo import obtener_lienzo_dinamico_fondo
from src.mockups.planos.comunes import dibujar_icono_lupa
from src.rutas import DIR_BYTE_TRANSPARENTES


def _fondo(cfg: Dict[str, Any], ancho: int, alto: int, t_sec: float) -> Image.Image:
    estilo = cfg.get("estilo_fondo", "viaje_espacial")
    # 0.7 (en vez del 0.45 de catálogo): la media RGB de las estrellas/nebulosa
    # del viaje_espacial superaba 110 en las zonas muertas y<250/y>1650 del
    # linter (0.65 pasaba justo; 0.7 deja margen ante el shift de yuv420p)
    return obtener_lienzo_dinamico_fondo(
        estilo=estilo, ancho=ancho, alto=alto, t_sec=t_sec,
        velocidad_lenta=0.85, atenuacion_oscura=0.7,
    )


def _badge(
    frame: Image.Image,
    ancho: int,
    texto: str,
    col: Tuple[int, int, int] = (225, 29, 72),
    col_borde: Tuple[int, int, int] = (254, 205, 211),
    t_sec: float = 0.0,
) -> None:
    # Pop-in con muelle anclado arriba-centro (y=252); ancho tope 860 para que
    # el overshoot (max 1.04) no roce las laterales x<70 / x>1011
    s = pop_scale(t_sec)
    if s <= 0.03:
        return
    f = obtener_fuente(20, bold=True)
    bb = ImageDraw.Draw(frame).textbbox((0, 0), texto, font=f)
    w = min(max(420, bb[2] - bb[0] + 90), 860)
    h = 52
    badge = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(badge)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=(*col, 235), outline=col_borde, width=2)
    d.ellipse([18, 12, 46, 40], fill=(255, 255, 255))
    d.text((28, 13), "!", fill=col, font=obtener_fuente(20, bold=True))
    d.text((58, 13), texto, fill=(255, 255, 255), font=f)
    # Shine: destello diagonal que cruza el badge una vez tras el pop
    u_shine = (t_sec - 0.30) / 0.45
    if 0.0 < u_shine < 1.0:
        glint = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        dg = ImageDraw.Draw(glint)
        bx0 = int(-50 + u_shine * (w + 100))
        dg.polygon([(bx0, 0), (bx0 + 34, 0), (bx0 - 22, h), (bx0 - 56, h)], fill=(255, 255, 255, 55))
        badge = Image.alpha_composite(badge, glint)
    if s < 0.999:
        badge = badge.resize((max(1, int(w * s)), max(1, int(h * s))), Image.Resampling.LANCZOS)
    frame.paste(badge, ((ancho - badge.width) // 2, 252), badge)


def _pildora(
    frame: Image.Image,
    ancho: int,
    texto: str,
    col: Tuple[int, int, int] = (14, 165, 233),
    t_sec: float = 0.0,
    t_tipo: Optional[float] = None,
) -> None:
    # Pop-in con muelle (ancho fijo = texto completo) + typing carácter a
    # carácter sincronizado con la voz (t_tipo = inicio hablado; default fijo)
    s = pop_scale(t_sec, t0=0.10)
    if s <= 0.03:
        return
    t0_tipo = 0.25 if t_tipo is None else t_tipo
    f = obtener_fuente(28, bold=True)
    bb = ImageDraw.Draw(frame).textbbox((0, 0), texto, font=f)
    w = min(bb[2] - bb[0] + 130, 880)
    h = 70
    pild = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(pild)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=35, fill=(15, 23, 42, 245), outline=col, width=2)
    dibujar_chispa_ia(d, 36, 35, 10, col)
    texto_tipo = type_chars(texto, t_sec, t0=t0_tipo, cps=30.0)
    if texto_tipo:
        d.text((74, 18), texto_tipo, fill=(255, 255, 255), font=f)
    # Caret de search bar: parpadea mientras escribe y un instante después
    fin_tipo = t0_tipo + len(texto) / 30.0
    if t_sec > t0_tipo and t_sec < fin_tipo + 0.9 and int(t_sec * 5.0) % 2 == 0:
        if texto_tipo:
            bb_t = d.textbbox((74, 18), texto_tipo, font=f)
            cx_c = bb_t[2] + 6
        else:
            cx_c = 74
        d.rectangle([cx_c, 20, cx_c + 3, 50], fill=(255, 255, 255, 235))
    if s < 0.999:
        pild = pild.resize((max(1, int(w * s)), max(1, int(h * s))), Image.Resampling.LANCZOS)
    frame.paste(pild, ((ancho - pild.width) // 2, int(825 - pild.height / 2)), pild)


def _pegar_byte(
    frame: Image.Image,
    cfg: Dict[str, Any],
    base_y: int = 1650,
    alto: int = 540,
    cx: Optional[int] = None,
    rebote: int = 0,
    candidatos: Tuple[str, ...] = (),
    t_sec: Optional[float] = None,
) -> None:
    p = cfg.get("sprite_byte")
    if not p or not Path(p).exists():
        for cand in candidatos:
            pc = DIR_BYTE_TRANSPARENTES / cand
            if pc.exists():
                p = pc
                break
    if not p or not Path(p).exists():
        return
    # Con t_sec: rebote + squash&stretch + wobble + micro-pulse autocalculados
    pegar_byte_animado(frame, Path(p), base_y=base_y, alto=alto, t_sec=t_sec, rebote=rebote, cx=cx)


def _chispas_pop(
    frame: Image.Image,
    cx: int,
    cy: int,
    t: float,
    t0: float,
    col: Tuple[int, int, int],
    dur: float = 0.45,
    n: int = 6,
    r_max: int = 130,
) -> None:
    """Chispas que estallan en radial al hacer pop un elemento (juice sutil,
    determinístico; radio acortado en Y para quedar dentro del slot UI)."""
    u = (t - t0) / dur
    if u <= 0.0 or u >= 1.0:
        return
    avance = 1.0 - (1.0 - u) ** 2
    radio = r_max * avance
    alfa = int(220 * (1.0 - u))
    ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    dov = ImageDraw.Draw(ov)
    for i in range(n):
        ang = 2.0 * math.pi * i / n + 0.4
        px = cx + int(radio * math.cos(ang))
        py = cy + int(radio * math.sin(ang) * 0.7)
        rr = max(1, int(5 * (1.0 - u) + 1))
        col_p = (255, 245, 0) if i % 2 == 0 else col
        dov.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(*col_p, alfa))
    frame.paste(ov, (0, 0), ov)


# ---------------------------------------------------------------------------
# 1. PLANO_CELU_POPUP_SOSPECHA: pantalla de bloqueo con notificacion rara
# ---------------------------------------------------------------------------
def renderizar_plano_celu_popup_sospecha(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None,
) -> Image.Image:
    """Pantalla de bloqueo del celular con una notificacion sospechosa."""
    cfg = config or {}
    frame = _fondo(cfg, ancho, alto, t_sec)
    draw = ImageDraw.Draw(frame)
    _badge(frame, ancho, cfg.get("badge", "DICEN QUE TU CELU TE ESCUCHA"), t_sec=t_sec)

    px, py, pw, ph = 100, 330, 880, 440
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=36, fill=(15, 23, 42, 250), outline=(71, 85, 105), width=4)
    draw.rounded_rectangle([ancho // 2 - 70, py + 14, ancho // 2 + 70, py + 32], radius=9, fill=(2, 6, 23))

    draw.text((ancho // 2 - 98, py + 52), "21:04", fill=(241, 245, 249), font=obtener_fuente(56, bold=True))
    draw.text((ancho // 2 - 148, py + 124), "lunes 12 de octubre", fill=(148, 163, 184), font=obtener_fuente(18))

    col_notif = cfg.get("notif_col", (225, 29, 72))
    pulse = 0.5 + 0.5 * math.sin(t_sec * 3.0)
    nx, ny = px + 40, py + 170
    nw, nh = pw - 80, 150
    # Sync de voz: si hay evento t_ui, la notificación hace pop cuando el
    # narrador dice la palabra clave; sin evento, visible desde el inicio
    ev = cfg.get("eventos") or {}
    t_ui = ev.get("t_ui")
    s_notif = 1.0 if t_ui is None else pop_scale(t_sec, t0=float(t_ui))
    if s_notif > 0.03:
        notif = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
        dn = ImageDraw.Draw(notif)
        dn.rounded_rectangle(
            [0, 0, nw - 1, nh - 1], radius=20, fill=(30, 41, 59, 252),
            outline=(*col_notif, 255), width=2 + int(2 * pulse),
        )
        dn.ellipse([22, 22, 62, 62], fill=col_notif)
        dn.text((37, 30), "!", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
        dn.text((80, 20), cfg.get("notif_tit", "Asistente IA"), fill=(255, 255, 255), font=obtener_fuente(24, bold=True))
        dn.text((nw - 78, 26), "ahora", fill=(148, 163, 184), font=obtener_fuente(16))

        lineas = cfg.get("notif_lineas", [
            "'¿Seguimos escuchando?' hace 1 min",
            "Se activó sola, sin que la tocaras",
        ])
        for i, linea in enumerate(lineas[:2]):
            dn.text((24, 72 + i * 36), linea, fill=(203, 213, 225), font=obtener_fuente(22))
        if s_notif < 0.999:
            notif = notif.resize((max(1, int(nw * s_notif)), max(1, int(nh * s_notif))), Image.Resampling.LANCZOS)
        frame.paste(notif, (nx + (nw - notif.width) // 2, ny), notif)
        if t_ui is not None:
            _chispas_pop(frame, nx + nw // 2, ny + nh // 2, t_sec, float(t_ui), col_notif)

    if cfg.get("pildora"):
        _pildora(frame, ancho, cfg["pildora"], t_sec=t_sec, t_tipo=ev.get("t_pildora"))

    _pegar_byte(
        frame, cfg, base_y=1650, alto=560, t_sec=t_sec,
        candidatos=("cold_open_guion_15_ia_celular_transparente.png", "byte_agotado_transparente.png"),
    )
    return frame


# ---------------------------------------------------------------------------
# 2. PLANO_WAKE_WORD: la asistente solo despierta con su palabra magica
# ---------------------------------------------------------------------------
def renderizar_plano_wake_word(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None,
) -> Image.Image:
    """Orbe de asistente con ondas de escucha y el flujo despertar -> procesar."""
    cfg = config or {}
    frame = _fondo(cfg, ancho, alto, t_sec)
    draw = ImageDraw.Draw(frame)
    _badge(frame, ancho, cfg.get("badge", "SOLO DESPIERTA CON SU PALABRA"), col=(37, 99, 235), col_borde=(191, 219, 254), t_sec=t_sec)

    cx, cy = ancho // 2, 470
    pulso = 0.5 + 0.5 * math.sin(t_sec * 3.2)
    r = 118 + int(12 * pulso)

    glow = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_glow = ImageDraw.Draw(glow)
    d_glow.ellipse([cx - r - 55, cy - r - 55, cx + r + 55, cy + r + 55], fill=(14, 165, 233, int(50 + 45 * pulso)))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    frame = Image.alpha_composite(frame, glow)
    draw = ImageDraw.Draw(frame)

    for i, rr in enumerate((r + 36, r + 72)):
        alfa = int(170 - i * 55 - 50 * pulso)
        if alfa > 12:
            draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=-55, end=55, fill=(14, 165, 233, alfa), width=5)
            draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=125, end=235, fill=(14, 165, 233, alfa), width=5)

    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(3, 105, 161, 255), outline=(165, 243, 252, 255), width=4)
    dibujar_chispa_ia(draw, cx, cy, 30, (255, 255, 255))

    chips = [
        (110, "1. Suena su palabra", "Hey Siri / OK Google", (16, 185, 129)),
        (560, "2. Recien ahi procesa", "lo que le pedis", (14, 165, 233)),
    ]
    for chx, l1, l2, col in chips:
        chy, chw, chh = 670, 410, 84
        draw.rounded_rectangle([chx, chy, chx + chw, chy + chh], radius=16, fill=(30, 41, 59, 252), outline=col, width=2)
        draw.text((chx + 24, chy + 14), l1, fill=(255, 255, 255), font=obtener_fuente(21, bold=True))
        draw.text((chx + 24, chy + 48), l2, fill=col, font=obtener_fuente(20, bold=False))

    draw.text((527, 692), ">>", fill=(255, 245, 0), font=obtener_fuente(34, bold=True))

    ev = cfg.get("eventos") or {}
    if cfg.get("pildora"):
        _pildora(frame, ancho, cfg["pildora"], t_sec=t_sec, t_tipo=ev.get("t_pildora"))

    _pegar_byte(
        frame, cfg, base_y=1650, alto=540, t_sec=t_sec,
        candidatos=("problema_guion_15_ia_celular_transparente.png",),
    )
    return frame


# ---------------------------------------------------------------------------
# 3. PLANO_CIRCLE_TO_SEARCH: circulo magico sobre la foto y resultados
# ---------------------------------------------------------------------------
def renderizar_plano_circle_to_search(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None,
) -> Image.Image:
    """Recorte de pantalla con la foto, el circulo animado y la hoja de resultados."""
    cfg = config or {}
    frame = _fondo(cfg, ancho, alto, t_sec)
    draw = ImageDraw.Draw(frame)
    _badge(frame, ancho, cfg.get("badge", "GEMINI EN ANDROID • BUSCA CIRCULANDO"), col=(14, 165, 233), col_borde=(186, 230, 253), t_sec=t_sec)

    sx, sy, sw, sh = 100, 326, 880, 444
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=34, fill=(2, 6, 23, 255), outline=(71, 85, 105), width=4)

    ix0, iy0, ix1, iy1 = sx + 16, sy + 44, sx + sw - 16, sy + sh - 16
    draw.rounded_rectangle([ix0, iy0, ix1, iy1], radius=22, fill=(17, 26, 46, 255))

    cx_obj = (ix0 + ix1) // 2
    cy_obj = iy0 + 150
    camiseta = [
        (cx_obj - 66, cy_obj - 74), (cx_obj - 124, cy_obj - 36),
        (cx_obj - 96, cy_obj + 6), (cx_obj - 66, cy_obj - 12),
        (cx_obj - 66, cy_obj + 76), (cx_obj + 66, cy_obj + 76),
        (cx_obj + 66, cy_obj - 12), (cx_obj + 96, cy_obj + 6),
        (cx_obj + 124, cy_obj - 36), (cx_obj + 66, cy_obj - 74),
    ]
    draw.polygon(camiseta, fill=(56, 132, 255, 255), outline=(147, 197, 253, 255))

    for esq_x, esq_y, dx, dy in (
        (ix0 + 20, iy0 + 20, 1, 1), (ix1 - 20, iy0 + 20, -1, 1),
        (ix0 + 20, iy1 - 20, 1, -1), (ix1 - 20, iy1 - 20, -1, -1),
    ):
        draw.line([(esq_x, esq_y), (esq_x + 34 * dx, esq_y)], fill=(255, 255, 255, 255), width=4)
        draw.line([(esq_x, esq_y), (esq_x, esq_y + 34 * dy)], fill=(255, 255, 255, 255), width=4)

    r_circ = 150
    # Sync de voz: el círculo se dibuja cuando el narrador dice la palabra
    # clave (ui_clave); sin evento, arranca a los 0.4s (comportamiento previo)
    ev = cfg.get("eventos") or {}
    t_circ = 0.4 if ev.get("t_ui") is None else float(ev["t_ui"])
    prog = min(1.0, max(0.0, t_sec - t_circ) * 1.1)
    if prog > 0.02:
        fin = -90 + 360 * prog
        draw.arc(
            [cx_obj - r_circ, cy_obj - r_circ, cx_obj + r_circ, cy_obj + r_circ],
            start=-90, end=fin, fill=(255, 245, 0, 255), width=7,
        )
        ang = math.radians(fin)
        lp_x = cx_obj + r_circ * math.cos(ang)
        lp_y = cy_obj + r_circ * math.sin(ang)
        draw.ellipse([lp_x - 9, lp_y - 9, lp_x + 9, lp_y + 9], fill=(255, 245, 0, 255), outline=(15, 23, 42, 255), width=2)

    prog_hoja = min(1.0, max(0.0, t_sec - (t_circ + 0.6)) * 1.3)
    if prog_hoja > 0.03:
        hoja_h = int(190 * prog_hoja)
        hoja_y = iy1 - hoja_h
        draw.rounded_rectangle([ix0, hoja_y, ix1, iy1], radius=20, fill=(248, 250, 252, 255))
        if hoja_h > 56:
            dibujar_icono_lupa(draw, ix0 + 42, hoja_y + 38, r=14, color=(14, 165, 233))
            draw.text((ix0 + 74, hoja_y + 18), "Resultados en la web", fill=(15, 23, 42, 255), font=obtener_fuente(23, bold=True))
        if hoja_h > 120:
            draw.rounded_rectangle([ix0 + 24, hoja_y + 66, ix0 + 52, hoja_y + 94], radius=8, fill=(16, 185, 129, 255))
            draw.text((ix0 + 66, hoja_y + 68), "Ficha del producto encontrada", fill=(51, 65, 85, 255), font=obtener_fuente(20))
        if hoja_h > 168:
            draw.rounded_rectangle([ix0 + 24, hoja_y + 114, ix0 + 52, hoja_y + 142], radius=8, fill=(14, 165, 233, 255))
            draw.text((ix0 + 66, hoja_y + 116), "Videos y reseñas del mismo producto", fill=(51, 65, 85, 255), font=obtener_fuente(20))

    if cfg.get("pildora"):
        _pildora(frame, ancho, cfg["pildora"], t_sec=t_sec, t_tipo=ev.get("t_pildora"))

    _pegar_byte(
        frame, cfg, base_y=1650, alto=520, cx=360, t_sec=t_sec,
        candidatos=("byte_computadora_feliz_transparente.png",),
    )
    return frame


# ---------------------------------------------------------------------------
# 4. PLANO_IOS_RESUMEN_NOTIF: pila de avisos que colapsa en un resumen
# ---------------------------------------------------------------------------
def renderizar_plano_ios_resumen_notif(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None,
) -> Image.Image:
    """Lock screen donde cinco avisos se fusionan en una tarjeta de resumen."""
    cfg = config or {}
    frame = _fondo(cfg, ancho, alto, t_sec)
    draw = ImageDraw.Draw(frame)
    _badge(frame, ancho, cfg.get("badge", "APPLE INTELLIGENCE • RESUMEN Y ESCRITURA"), col=(124, 58, 237), col_borde=(221, 214, 254), t_sec=t_sec)

    sx, sy, sw, sh = 100, 326, 880, 444
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=34, fill=(10, 14, 30, 255), outline=(71, 85, 105), width=4)
    draw.text((ancho // 2 - 78, sy + 26), "9:41", fill=(241, 245, 249, 255), font=obtener_fuente(58, bold=True))
    draw.text((ancho // 2 - 148, sy + 100), "lunes 12 de octubre", fill=(148, 163, 184, 255), font=obtener_fuente(18))

    items = [
        ((56, 132, 255), "Mensajes", "Reuniones y confirmaciones"),
        ((48, 203, 128), "Recordatorios", "Entregas de la semana"),
        ((245, 158, 11), "Calendario", "Avisos del dia"),
        ((225, 29, 72), "Noticias", "Resumen de la manana"),
    ]
    # Sync de voz: los avisos colapsan en resumen cuando el narrador dice
    # la palabra clave (ui_clave); sin evento, a los 1.7s (previo)
    ev = cfg.get("eventos") or {}
    t_merge = 1.7 if ev.get("t_ui") is None else float(ev["t_ui"])
    merge = min(1.0, max(0.0, t_sec - t_merge) * 1.1)

    overlay = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)
    alfa_chips = int(255 * (1.0 - merge))
    if alfa_chips > 8:
        for i, (col, titulo, texto) in enumerate(items):
            y_from = sy + 150 + i * 66
            y_to = sy + 250
            y = int(y_from + (y_to - y_from) * merge)
            nx0, nx1 = sx + 50, sx + sw - 50
            d_ov.rounded_rectangle([nx0, y, nx1, y + 56], radius=14, fill=(30, 41, 59, alfa_chips))
            d_ov.ellipse([nx0 + 16, y + 16, nx0 + 40, y + 40], fill=(*col, alfa_chips))
            d_ov.text((nx0 + 56, y + 8), titulo, fill=(255, 255, 255, alfa_chips), font=obtener_fuente(18, bold=True))
            d_ov.text((nx0 + 56, y + 30), texto, fill=(203, 213, 225, alfa_chips), font=obtener_fuente(17))
            d_ov.text((nx1 - 74, y + 18), "ahora", fill=(148, 163, 184, alfa_chips), font=obtener_fuente(15))

    alfa_res = int(255 * merge)
    if alfa_res > 8:
        rx0, rx1 = sx + 40, sx + sw - 40
        ry0, ry1 = sy + 190, sy + 340
        d_ov.rounded_rectangle([rx0, ry0, rx1, ry1], radius=18, fill=(30, 41, 59, alfa_res), outline=(48, 203, 128, alfa_res), width=2)
        d_ov.ellipse([rx0 + 22, ry0 + 22, rx0 + 54, ry0 + 54], fill=(48, 203, 128, alfa_res))
        d_ov.text((rx0 + 68, ry0 + 18), "Resumen inteligente", fill=(255, 255, 255, alfa_res), font=obtener_fuente(24, bold=True))
        d_ov.text((rx0 + 26, ry0 + 74), "Todos los avisos del dia agrupados", fill=(203, 213, 225, alfa_res), font=obtener_fuente(21))
        d_ov.text((rx0 + 26, ry0 + 108), "en una sola tarjeta clara", fill=(203, 213, 225, alfa_res), font=obtener_fuente(21))

    frame = Image.alpha_composite(frame, overlay)
    draw = ImageDraw.Draw(frame)

    if cfg.get("pildora"):
        _pildora(frame, ancho, cfg["pildora"], t_sec=t_sec, t_tipo=ev.get("t_pildora"))

    _pegar_byte(
        frame, cfg, base_y=1650, alto=520, cx=730, t_sec=t_sec,
        candidatos=("punto_2_guion_08_busqueda_investigacion_transparente.png",),
    )
    return frame


# ---------------------------------------------------------------------------
# 5. PLANO_CELU_PRIMERO_NUBE: en el celu primero, la nube si se la pide
# ---------------------------------------------------------------------------
def renderizar_plano_celu_primero_nube(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None,
) -> Image.Image:
    """Tarjeta de celular con procesamiento local y nube opcional conectada."""
    cfg = config or {}
    frame = _fondo(cfg, ancho, alto, t_sec)
    draw = ImageDraw.Draw(frame)
    _badge(frame, ancho, cfg.get("badge", "CELULAR PRIMERO • NUBE DESPUES"), col=(16, 185, 129), col_borde=(167, 243, 208), t_sec=t_sec)

    px0, py0, px1, py1 = 100, 360, 520, 770
    draw.rounded_rectangle([px0, py0, px1, py1], radius=30, fill=(15, 23, 42, 252), outline=(16, 185, 129), width=3)
    dibujar_chispa_ia(draw, px0 + 42, py0 + 40, 11, (52, 211, 153))
    draw.text((px0 + 70, py0 + 24), "EN TU CELU", fill=(52, 211, 153), font=obtener_fuente(26, bold=True))

    lineas = cfg.get("lineas_celu", [
        "Procesamiento en el dispositivo",
        "Sin depender de la nube",
        "Respuestas rapidas del dia a dia",
    ])
    for i, linea in enumerate(lineas[:3]):
        ly = py0 + 108 + i * 78
        dibujar_icono_check(draw, px0 + 44, ly + 14, (52, 211, 153), tam=16, grosor=3)
        draw.text((px0 + 76, ly), linea, fill=(226, 232, 240), font=obtener_fuente(21, bold=False))

    cx0, cy0, cx1, cy1 = 620, 350, 980, 510
    draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=24, fill=(30, 41, 59, 252), outline=(148, 163, 184), width=2)
    ccx, ccy = cx0 + 76, cy0 + 66
    draw.ellipse([ccx - 44, ccy - 6, ccx - 4, ccy + 34], fill=(71, 85, 105, 255))
    draw.ellipse([ccx - 20, ccy - 24, ccx + 24, ccy + 20], fill=(71, 85, 105, 255))
    draw.ellipse([ccx + 6, ccy - 4, ccx + 46, ccy + 36], fill=(71, 85, 105, 255))
    draw.rounded_rectangle([ccx - 44, ccy + 12, ccx + 46, ccy + 34], radius=12, fill=(71, 85, 105, 255))
    draw.text((cx0 + 140, cy0 + 34), "EN LA NUBE", fill=(125, 211, 252), font=obtener_fuente(24, bold=True))
    draw.text((cx0 + 140, cy0 + 76), "solo si se la pide", fill=(203, 213, 225), font=obtener_fuente(20))
    draw.text((cx0 + 140, cy0 + 108), "cuando hace falta", fill=(148, 163, 184), font=obtener_fuente(18))

    for i in range(5):
        t_i = (t_sec * 0.9 + i * 0.2) % 1.0
        ax = 534 + int(70 * t_i)
        ay = 470 - int(60 * t_i)
        alfa = int(255 * (1.0 - abs(t_i - 0.5) * 1.4))
        if alfa > 16:
            draw.ellipse([ax - 5, ay - 5, ax + 5, ay + 5], fill=(255, 245, 0, alfa))
    draw.polygon([(616, 396), (590, 414), (614, 430)], fill=(255, 245, 0, 255))

    ev = cfg.get("eventos") or {}
    if cfg.get("pildora"):
        _pildora(frame, ancho, cfg["pildora"], t_sec=t_sec, t_tipo=ev.get("t_pildora"))

    _pegar_byte(
        frame, cfg, base_y=1650, alto=540, t_sec=t_sec,
        candidatos=("punto1_feliz_transparente.png",),
    )
    return frame


# ---------------------------------------------------------------------------
# 6. PLANO_CIERRE_RARA_FRASE: pregunta de debate con caja de comentario
# ---------------------------------------------------------------------------
def renderizar_plano_cierre_rara_frase(
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None,
) -> Image.Image:
    """Cierre estilo pregunta de debate con input de comentario y callout."""
    cfg = config or {}
    frame = _fondo(cfg, ancho, alto, t_sec)
    draw = ImageDraw.Draw(frame)
    _badge(frame, ancho, cfg.get("badge", "LA PREGUNTA DE BYTE PARA EL FEED"), col=(124, 58, 237), col_borde=(221, 214, 254), t_sec=t_sec)

    qw, qh = 880, 330
    s_caja = pop_scale(t_sec, t0=0.10)
    if s_caja > 0.03:
        caja = Image.new("RGBA", (qw, qh), (0, 0, 0, 0))
        dc = ImageDraw.Draw(caja)
        dc.rounded_rectangle([0, 0, qw - 1, qh - 1], radius=24, fill=(240, 249, 255, 252), outline=(14, 165, 233), width=3)
        dibujar_chispa_ia(dc, 40, 42, 12, (14, 165, 233))
        dc.text((70, 28), "PARA LOS COMENTARIOS:", fill=(3, 105, 161), font=obtener_fuente(20, bold=True))
        dc.text((36, 84), cfg.get("pregunta_l1", "¿Cuál es la cosa más rara"), fill=(15, 23, 42), font=obtener_fuente(36, bold=True))
        dc.text((36, 134), cfg.get("pregunta_l2", "que le dijiste a tu asistente?"), fill=(15, 23, 42), font=obtener_fuente(36, bold=True))

        ix0, iy0 = 36, 200
        iw, ih = qw - 72, 92
        dc.rounded_rectangle([ix0, iy0, ix0 + iw, iy0 + ih], radius=16, fill=(255, 255, 255, 255), outline=(203, 213, 225), width=2)
        f_input = obtener_fuente(24)
        dc.text((ix0 + 24, iy0 + 32), "escribi tu respuesta...", fill=(148, 163, 184), font=f_input)
        bb_input = dc.textbbox((0, 0), "escribi tu respuesta...", font=f_input)
        if int(t_sec * 2.0) % 2 == 0:
            cx_cur = ix0 + 34 + (bb_input[2] - bb_input[0])
            dc.rectangle([cx_cur, iy0 + 28, cx_cur + 4, iy0 + 64], fill=(14, 165, 233))
        if s_caja < 0.999:
            caja = caja.resize((max(1, int(qw * s_caja)), max(1, int(qh * s_caja))), Image.Resampling.LANCZOS)
        frame.paste(caja, ((ancho - caja.width) // 2, 330), caja)

    flecha_bob = int(6 * math.sin(t_sec * 4.0))
    fy = 700 + flecha_bob
    draw.polygon([(ancho // 2 - 22, fy), (ancho // 2 + 22, fy), (ancho // 2, fy + 38)], fill=(14, 165, 233, 255))

    ev = cfg.get("eventos") or {}
    if cfg.get("pildora"):
        _pildora(frame, ancho, cfg["pildora"], col=(14, 165, 233), t_sec=t_sec, t_tipo=ev.get("t_pildora"))

    _pegar_byte(
        frame, cfg, base_y=1650, alto=560, t_sec=t_sec,
        candidatos=("cierre_saltando_transparente.png",),
    )
    return frame

"""
src.mockups.planos.video_07_excel
---------------------------------------------------------------------------
Planos del Video 07 (Excel y Reportes con IA).
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
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.50)

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
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.50)

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
    frame = obtener_lienzo_dinamico_fondo(estilo=estilo_fondo, ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.45)

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

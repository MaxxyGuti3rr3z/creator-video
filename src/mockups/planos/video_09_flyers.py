"""
src.mockups.planos.video_09_flyers
---------------------------------------------------------------------------
Planos del Video 09 (Diseno de Flyers: Canva y Remove.bg).
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

"""
test_previews_video_09_v2.py
----------------------------
Prototipo y validación de las 7 escenas hiperdinámicas para el Video 09.
Cada escena cuenta con un mockup único, corte rápido (2-3s) y expresión distinta de Byte.
"""

import sys
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFilter

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.rutas import DIR_VIDEOS, DIR_BYTE_TRANSPARENTES
from src.mockups.motor import (
    obtener_fuente,
    dibujar_chispa_ia,
    dibujar_icono_check,
)
from src.mockups.estilos.animaciones_fondo import obtener_lienzo_dinamico_fondo
from src.mockups.director_escena import (
    dibujar_icono_alerta,
    dibujar_icono_cruz,
    renderizar_plano_canva_magic_design,
    renderizar_plano_battle_vs,
)

DIR_OUT = DIR_VIDEOS / "video_09_diseno_flyers" / "intermedios" / "previews_director_v2"
DIR_OUT.mkdir(parents=True, exist_ok=True)


# ===========================================================================
# 1. PLANO_CHAT_FLYER_URGENTE (Cold Open: 0.0s - 2.3s)
# ===========================================================================
def renderizar_plano_chat_flyer_urgente(ancho=1080, alto=1920, t_sec=1.0, duracion=2.5, config=None):
    cfg = config or {}
    frame = obtener_lienzo_dinamico_fondo(estilo="estudio_creativo", ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. Top sticker Alerta urgente
    pulso = 0.5 + 0.5 * math.sin(t_sec * 6.0)
    col_borde = (255, 255, 255) if pulso > 0.5 else (244, 63, 94)
    draw.rounded_rectangle([ancho // 2 - 250, 70, ancho // 2 + 250, 118], radius=12, fill=(225, 29, 72), outline=col_borde, width=2)
    dibujar_icono_alerta(draw, ancho // 2 - 190, 94, tam=10, color=(255, 255, 255))
    draw.text((ancho // 2 - 168, 82), "PEDIDO URGENTE • 17:59 HS", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    # Titular Hook
    badge_txt = cfg.get("badge", "POV: NECESITÁS UN FLYER URGENTE")
    draw.rounded_rectangle([40, 130, ancho - 40, 205], radius=16, fill=(15, 23, 42, 250), outline=(225, 29, 72), width=2)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=obtener_fuente(28, bold=True))
    bw_txt = bbox_b[2] - bbox_b[0]
    draw.text(((ancho - bw_txt) // 2, 150), badge_txt, fill=(255, 245, 0), font=obtener_fuente(28, bold=True))

    # 2. Mockup de Chat / Mensajería Urgente (WhatsApp / Slack)
    wx, wy, ww, wh = 30, 225, ancho - 60, 475
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=20, fill=(15, 23, 42, 245), outline=(71, 85, 105), width=2)

    # Header del chat
    draw.rounded_rectangle([wx, wy, wx + ww, wy + 65], radius=20, fill=(30, 41, 59))
    draw.line([(wx, wy + 65), (wx + ww, wy + 65)], fill=(51, 65, 85), width=2)
    # Avatar cliente
    draw.ellipse([wx + 25, wy + 12, wx + 67, wy + 54], fill=(225, 29, 72))
    draw.text((wx + 34, wy + 20), "JM", fill=(255, 255, 255), font=obtener_fuente(20, bold=True))
    # Nombre y estado
    draw.text((wx + 80, wy + 14), "Jefe de Marketing • Cliente", fill=(241, 245, 249), font=obtener_fuente(20, bold=True))
    draw.ellipse([wx + 82, wy + 42, wx + 92, wy + 52], fill=(34, 197, 94))
    draw.text((wx + 100, wy + 38), "En línea • Escribiendo...", fill=(148, 163, 184), font=obtener_fuente(16, bold=False))

    # Burbuja de mensaje entrante (Estilo WhatsApp verde oscuro / slate)
    bx, by, bw, bh = wx + 35, wy + 90, ww - 70, 185
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=16, fill=(20, 83, 45, 240), outline=(34, 197, 94), width=2)
    draw.text((bx + 25, by + 20), "Che Max, ¿tenés el flyer para el evento de hoy?", fill=(255, 255, 255), font=obtener_fuente(24, bold=True))
    draw.text((bx + 25, by + 65), "¡Lo necesito urgente antes de las 18:00 hs!", fill=(254, 240, 138), font=obtener_fuente(24, bold=True))
    draw.text((bx + 25, by + 110), "Tiene que verse profesional y con las fotos sin fondo.", fill=(220, 252, 231), font=obtener_fuente(20, bold=False))
    draw.text((bx + bw - 145, by + bh - 32), "17:58 hs • Leído", fill=(134, 239, 172), font=obtener_fuente(16, bold=True))

    # Tarjeta de alerta de tiempo límite (Reloj urgente)
    tx, ty, tw, th = wx + 35, wy + 295, ww - 70, 155
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=14, fill=(30, 41, 59, 240), outline=(239, 68, 68), width=2)
    dibujar_icono_alerta(draw, tx + 40, ty + 45, tam=18, color=(239, 68, 68))
    draw.text((tx + 75, ty + 25), "TIEMPO LÍMITE: MENOS DE 1 HORA", fill=(248, 113, 113), font=obtener_fuente(22, bold=True))
    draw.text((tx + 75, ty + 65), "Estado: 0% diseñado • Bloqueo total", fill=(203, 213, 225), font=obtener_fuente(20, bold=False))
    # Barra de progreso urgente en 0%
    draw.rounded_rectangle([tx + 75, ty + 105, tx + tw - 40, ty + 125], radius=8, fill=(15, 23, 42), outline=(71, 85, 105), width=1)
    draw.rounded_rectangle([tx + 75, ty + 105, tx + 140, ty + 125], radius=8, fill=(239, 68, 68))

    # 3. Píldora inferior (y = 720..795)
    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(225, 29, 72), width=2)
    dibujar_icono_alerta(draw, 75, 757, tam=14, color=(225, 29, 72))
    draw.text((105, 742), "El tiempo vuela y no tenés nada listo para publicar", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # 4. Byte Protagonista: BYTE AGOTADO / OJEROSO
    p_byte = DIR_BYTE_TRANSPARENTES / "byte_agotado_transparente.png"
    if p_byte.exists():
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


# ===========================================================================
# 2. PLANO_PHOTOSHOP_FREEZE (Hook: 2.3s - 4.5s)
# ===========================================================================
def renderizar_plano_photoshop_freeze(ancho=1080, alto=1920, t_sec=1.0, duracion=2.5, config=None):
    cfg = config or {}
    frame = obtener_lienzo_dinamico_fondo(estilo="estudio_creativo", ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. Top sticker
    draw.rounded_rectangle([ancho // 2 - 250, 70, ancho // 2 + 250, 118], radius=12, fill=(234, 88, 12), outline=(255, 255, 255), width=2)
    dibujar_icono_cruz(draw, ancho // 2 - 190, 94, tam=10, color=(255, 255, 255), grosor=3)
    draw.text((ancho // 2 - 168, 82), "PROGRAMAS PESADOS", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    # Titular Hook
    badge_txt = cfg.get("badge", "DEJÁ DE PELEAR CON EL DISEÑO")
    draw.rounded_rectangle([40, 130, ancho - 40, 205], radius=16, fill=(15, 23, 42, 250), outline=(234, 88, 12), width=2)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=obtener_fuente(28, bold=True))
    bw_txt = bbox_b[2] - bbox_b[0]
    draw.text(((ancho - bw_txt) // 2, 150), badge_txt, fill=(255, 245, 0), font=obtener_fuente(28, bold=True))

    # 2. Ventana congelada de Photoshop
    wx, wy, ww, wh = 30, 225, ancho - 60, 475
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=20, fill=(15, 23, 42, 245), outline=(239, 68, 68), width=3)

    # Barra de título con "(No responde)"
    draw.rounded_rectangle([wx, wy, wx + ww, wy + 55], radius=20, fill=(30, 41, 59))
    draw.line([(wx, wy + 55), (wx + ww, wy + 55)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 20, wy + 20, wx + 34 + idx_dot * 20, wy + 32], fill=(148, 163, 184))
    draw.text((wx + 95, wy + 16), "Adobe_Photoshop_2026.exe (No responde)", fill=(248, 113, 113), font=obtener_fuente(20, bold=True))

    # Cuerpo de congelamiento
    cx_card = wx + 40
    cy_card = wy + 85
    cw_card = ww - 80
    ch_card = wh - 110
    draw.rounded_rectangle([cx_card, cy_card, cx_card + cw_card, cy_card + ch_card], radius=16, fill=(2, 6, 23, 240), outline=(71, 85, 105), width=2)

    # Spinner / icono de espera trabado
    sp_x, sp_y = cx_card + cw_card // 2, cy_card + 75
    draw.ellipse([sp_x - 35, sp_y - 35, sp_x + 35, sp_y + 35], outline=(100, 116, 139), width=6)
    # Arco de giro
    angulo_rad = t_sec * 6.0
    ax1 = sp_x + int(35 * math.cos(angulo_rad))
    ay1 = sp_y + int(35 * math.sin(angulo_rad))
    draw.ellipse([ax1 - 6, ay1 - 6, ax1 + 6, ay1 + 6], fill=(239, 68, 68))

    # Textos de carga eterna
    draw.text((cx_card + 50, cy_card + 130), "Iniciando motor de gráficos...", fill=(241, 245, 249), font=obtener_fuente(24, bold=True))
    draw.text((cx_card + 50, cy_card + 175), "Cargando 4.280 pinceles, fuentes y plugins... (1%)", fill=(148, 163, 184), font=obtener_fuente(20, bold=False))

    # Barra de progreso congelada en 1%
    draw.rounded_rectangle([cx_card + 50, cy_card + 225, cx_card + cw_card - 50, cy_card + 250], radius=10, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.rounded_rectangle([cx_card + 50, cy_card + 225, cx_card + 80, cy_card + 250], radius=10, fill=(239, 68, 68))

    # Sello / Sticker rojo de alerta
    stamp_w, stamp_h = 580, 75
    stamp = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
    d_s = ImageDraw.Draw(stamp)
    d_s.rounded_rectangle([0, 0, stamp_w, stamp_h], radius=12, fill=(225, 29, 72, 245), outline=(255, 255, 255), width=2)
    dibujar_icono_cruz(d_s, 35, 37, tam=10, color=(255, 255, 255), grosor=3)
    d_s.text((60, 20), "PROGRAMA PESADO Y TRABADO", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))
    stamp_rot = stamp.rotate(-4, resample=Image.Resampling.BILINEAR, expand=True)
    frame.paste(stamp_rot, (ancho // 2 - stamp_rot.width // 2, wy + 395), stamp_rot)

    # 3. Píldora inferior (y = 720..795)
    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(234, 88, 12), width=2)
    dibujar_icono_cruz(draw, 75, 757, tam=12, color=(234, 88, 12), grosor=3)
    draw.text((105, 742), "50 capas sin nombrar y la máquina congelada", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # 4. Byte Protagonista: BYTE ENOJADO PELEANDO CON LA LAPTOP
    p_byte = DIR_BYTE_TRANSPARENTES / "punto_2_guion_04_transparente.png"
    if p_byte.exists():
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


# ===========================================================================
# 3. PLANO_LIENZO_BLANCO_BLOQUEO (Problema: 4.5s - 7.5s)
# ===========================================================================
def renderizar_plano_lienzo_blanco_bloqueo(ancho=1080, alto=1920, t_sec=1.0, duracion=3.0, config=None):
    cfg = config or {}
    frame = obtener_lienzo_dinamico_fondo(estilo="estudio_creativo", ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. Top sticker
    draw.rounded_rectangle([ancho // 2 - 250, 70, ancho // 2 + 250, 118], radius=12, fill=(185, 28, 28), outline=(255, 255, 255), width=2)
    dibujar_icono_alerta(draw, ancho // 2 - 190, 94, tam=10, color=(255, 255, 255))
    draw.text((ancho // 2 - 168, 82), "BLOQUEO CREATIVO TOTAL", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    # Titular Hook
    badge_txt = cfg.get("badge", "ABRÍS Y NO SABÉS QUÉ HACER")
    draw.rounded_rectangle([40, 130, ancho - 40, 205], radius=16, fill=(15, 23, 42, 250), outline=(185, 28, 28), width=2)
    bbox_b = draw.textbbox((0, 0), badge_txt, font=obtener_fuente(28, bold=True))
    bw_txt = bbox_b[2] - bbox_b[0]
    draw.text(((ancho - bw_txt) // 2, 150), badge_txt, fill=(255, 245, 0), font=obtener_fuente(28, bold=True))

    # 2. Ventana con Lienzo Blanco Intimidante
    wx, wy, ww, wh = 30, 225, ancho - 60, 475
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=20, fill=(30, 41, 59, 245), outline=(71, 85, 105), width=2)

    # Barra superior
    draw.rounded_rectangle([wx, wy, wx + ww, wy + 55], radius=20, fill=(15, 23, 42))
    draw.line([(wx, wy + 55), (wx + ww, wy + 55)], fill=(51, 65, 85), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 20, wy + 20, wx + 34 + idx_dot * 20, wy + 32], fill=(148, 163, 184))
    draw.text((wx + 95, wy + 16), "Lienzo_Sin_Titulo.psd • 1080x1920 (0% creado)", fill=(203, 213, 225), font=obtener_fuente(20, bold=True))

    # Barra lateral de herramientas técnicas vectoriales
    sx, sy, sw, sh = wx + 15, wy + 70, 75, wh - 85
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    tool_letters = ["P", "T", "V", "M", "C", "A"]
    for i, ico in enumerate(tool_letters):
        draw.rounded_rectangle([sx + 15, sy + 15 + i * 50, sx + sw - 15, sy + 50 + i * 50], radius=6, fill=(30, 41, 59))
        draw.text((sx + 28, sy + 20 + i * 50), ico, fill=(148, 163, 184), font=obtener_fuente(20, bold=True))

    # Lienzo Blanco intimidante
    lx, ly, lw, lh = wx + 105, wy + 70, ww - 120, wh - 85
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=14, fill=(248, 250, 252), outline=(148, 163, 184), width=2)

    # Cuadrícula tenue en el lienzo
    for gx in range(lx + 40, lx + lw, 60):
        draw.line([(gx, ly), (gx, ly + lh)], fill=(226, 232, 240), width=1)
    for gy in range(ly + 40, ly + lh, 60):
        draw.line([(lx, gy), (lx + lw, gy)], fill=(226, 232, 240), width=1)

    # Signo de interrogación gigante titilando
    alpha_q = 0.5 + 0.5 * math.sin(t_sec * 6.0)
    col_q = (225, 29, 72) if alpha_q > 0.5 else (100, 116, 139)
    draw.text((lx + lw // 2 - 40, ly + 60), "?", fill=col_q, font=obtener_fuente(110, bold=True))
    draw.text((lx + lw // 2 - 160, ly + 210), "¿POR DÓNDE EMPIEZO?", fill=(15, 23, 42), font=obtener_fuente(28, bold=True))
    draw.text((lx + lw // 2 - 180, ly + 260), "Sin ideas • Sin plantilla • Sin tiempo", fill=(100, 116, 139), font=obtener_fuente(20, bold=False))

    # 3. Píldora inferior (y = 720..795)
    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(185, 28, 28), width=2)
    dibujar_icono_alerta(draw, 75, 757, tam=14, color=(185, 28, 28))
    draw.text((105, 742), "Abrís una pantalla en blanco y te quedás congelado", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # 4. Byte Protagonista: BYTE EN CORTOCIRCUITO
    p_byte = DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png"
    if p_byte.exists():
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


# ===========================================================================
# 5. PLANO_REMOVE_BG_LASER (Herramienta 2: 13.0s - 17.5s)
# ===========================================================================
def renderizar_plano_remove_bg_laser(ancho=1080, alto=1920, t_sec=1.5, duracion=4.5, config=None):
    cfg = config or {}
    frame = obtener_lienzo_dinamico_fondo(estilo="estudio_creativo", ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. Ventana superior
    wx, wy, ww, wh = 20, 70, ancho - 40, 630
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=18, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)

    # Header
    draw.rounded_rectangle([wx, wy, wx + ww, wy + 45], radius=18, fill=(2, 6, 23))
    draw.line([(wx, wy + 45), (wx + ww, wy + 45)], fill=(30, 41, 59), width=2)
    for idx_dot in range(3):
        draw.ellipse([wx + 22 + idx_dot * 20, wy + 16, wx + 34 + idx_dot * 20, wy + 28], fill=(148, 163, 184))
    draw.text((wx + 95, wy + 14), "REMOVE.BG • Recorte Instantáneo de Fondo con Inteligencia Artificial", fill=(241, 245, 249), font=obtener_fuente(18, bold=True))

    # Badge IA verde
    draw.rounded_rectangle([wx + ww - 200, wy + 8, wx + ww - 15, wy + 38], radius=8, fill=(16, 185, 129))
    dibujar_icono_check(draw, wx + ww - 185, wy + 23, tam=7, color=(255, 255, 255))
    draw.text((wx + ww - 170, wy + 12), "100% Automático", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    # Comparativa Split Before / After interactiva
    card_y = wy + 65
    cw = (ww - 60) // 2
    ch = wh - 85

    # Card Izquierda: ANTES (Fondo ruidoso)
    c1_x = wx + 20
    draw.rounded_rectangle([c1_x, card_y, c1_x + cw, card_y + ch], radius=14, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    draw.rounded_rectangle([c1_x + 15, card_y + 15, c1_x + 185, card_y + 50], radius=8, fill=(225, 29, 72))
    dibujar_icono_cruz(draw, cx=c1_x + 30, cy=card_y + 32, tam=6, color=(255, 255, 255), grosor=2)
    draw.text((c1_x + 45, card_y + 20), "ANTES • Con Fondo", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    # Simulación de foto con fondo sucio
    fx, fy, fw, fh = c1_x + 20, card_y + 65, cw - 40, ch - 120
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=10, fill=(71, 85, 105))
    # Ruido de cocina/fondo desordenado
    for rx in range(fx + 20, fx + fw - 20, 40):
        draw.line([(rx, fy + 20), (rx + 20, fy + fh - 20)], fill=(100, 116, 139), width=3)
    # Sujeto (Taza de café)
    draw.ellipse([fx + fw // 2 - 70, fy + fh // 2 - 50, fx + fw // 2 + 70, fy + fh // 2 + 70], fill=(217, 119, 6), outline=(255, 255, 255), width=3)
    draw.text((fx + fw // 2 - 45, fy + fh // 2), "OBJETO", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.text((c1_x + 20, card_y + ch - 40), "Fondo sucio que arruina el diseño", fill=(244, 63, 94), font=obtener_fuente(16, bold=True))

    # Card Derecha: DESPUÉS (Transparencia perfecta PNG)
    c2_x = wx + 40 + cw
    draw.rounded_rectangle([c2_x, card_y, c2_x + cw, card_y + ch], radius=14, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    draw.rounded_rectangle([c2_x + 15, card_y + 15, c2_x + 205, card_y + 50], radius=8, fill=(16, 185, 129))
    dibujar_icono_check(draw, c2_x + 30, card_y + 32, tam=7, color=(255, 255, 255))
    draw.text((c2_x + 45, card_y + 20), "DESPUÉS • PNG Limpio", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    # Patrón de cuadrícula de transparencia PNG
    px, py, pw, ph = c2_x + 20, card_y + 65, cw - 40, ch - 120
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=10, fill=(30, 41, 59))
    sq = 18
    for row in range(py, py + ph, sq):
        for col in range(px, px + pw, sq):
            if ((col - px) // sq + (row - py) // sq) % 2 == 0:
                draw.rectangle([col, row, min(col + sq, px + pw), min(row + sq, py + ph)], fill=(51, 65, 85))
    # Sujeto aislado impecable
    draw.ellipse([px + pw // 2 - 70, py + ph // 2 - 50, px + pw // 2 + 70, py + ph // 2 + 70], fill=(217, 119, 6), outline=(52, 211, 153), width=4)
    draw.text((px + pw // 2 - 45, py + ph // 2), "OBJETO", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))
    draw.text((c2_x + 20, card_y + ch - 40), "Bordes perfectos en 1 segundo", fill=(52, 211, 153), font=obtener_fuente(16, bold=True))

    # Línea láser vertical interactiva que barre en el centro
    laser_x = ancho // 2 + int(60 * math.sin(t_sec * 4.0))
    draw.line([(laser_x, card_y + 10), (laser_x, card_y + ch - 10)], fill=(56, 189, 248), width=4)
    # Pulso láser
    draw.ellipse([laser_x - 12, card_y + ch // 2 - 12, laser_x + 12, card_y + ch // 2 + 12], fill=(255, 255, 255), outline=(56, 189, 248), width=3)

    # 3. Píldora inferior (y = 720..795)
    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, 75, 757, tam=14, color=(16, 185, 129))
    draw.text((105, 742), "Recorta cualquier foto en un segundo sin tocar nada", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # 4. Byte Protagonista: BYTE SEÑALANDO SERIO / CANCHERO
    p_byte = DIR_BYTE_TRANSPARENTES / "cierre_transparente.png"
    if p_byte.exists():
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


# ===========================================================================
# 6. PLANO_SMARTPHONE_INSTAGRAM_FEED (Resultado: 17.5s - 22.0s)
# ===========================================================================
def renderizar_plano_smartphone_instagram_feed(ancho=1080, alto=1920, t_sec=1.5, duracion=4.5, config=None):
    cfg = config or {}
    frame = obtener_lienzo_dinamico_fondo(estilo="estudio_creativo", ancho=ancho, alto=alto, t_sec=t_sec, velocidad_lenta=0.85, atenuacion_oscura=0.25)
    draw = ImageDraw.Draw(frame)

    # 1. Top sticker
    draw.rounded_rectangle([ancho // 2 - 250, 70, ancho // 2 + 250, 118], radius=12, fill=(16, 185, 129), outline=(255, 255, 255), width=2)
    dibujar_icono_check(draw, ancho // 2 - 190, 94, tam=10, color=(255, 255, 255))
    draw.text((ancho // 2 - 168, 82), "RESULTADO PROFESIONAL", fill=(255, 255, 255), font=obtener_fuente(22, bold=True))

    # 2. Mockup de SMARTPHONE con Instagram Feed
    ph_w, ph_h = 580, 570
    ph_x, ph_y = (ancho - ph_w) // 2, 135

    # Chasis de Smartphone moderno (Dark Titanium)
    draw.rounded_rectangle([ph_x, ph_y, ph_x + ph_w, ph_y + ph_h], radius=38, fill=(15, 23, 42), outline=(71, 85, 105), width=4)
    # Notch / Dynamic Island
    draw.rounded_rectangle([ph_x + ph_w // 2 - 60, ph_y + 12, ph_x + ph_w // 2 + 60, ph_y + 30], radius=8, fill=(2, 6, 23))

    # Pantalla interna de la app Instagram
    sx, sy, sw, sh = ph_x + 18, ph_y + 42, ph_w - 36, ph_h - 60
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=24, fill=(2, 6, 23))

    # Barra superior de Instagram
    draw.ellipse([sx + 20, sy + 15, sx + 50, sy + 45], fill=(225, 29, 72))
    draw.text((sx + 26, sy + 20), "BT", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))
    draw.text((sx + 60, sy + 16), "byte_tech_studio", fill=(255, 255, 255), font=obtener_fuente(18, bold=True))
    draw.text((sx + 60, sy + 38), "Publicidad • Hace 5 min", fill=(148, 163, 184), font=obtener_fuente(14, bold=False))
    draw.text((sx + sw - 45, sy + 20), "•••", fill=(148, 163, 184), font=obtener_fuente(18, bold=True))

    # El Flyer final en el Feed del teléfono
    fx, fy, fw, fh = sx + 15, sy + 65, sw - 30, sh - 150
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=14, fill=(24, 24, 27), outline=(217, 119, 6), width=2)
    # Contenido del flyer
    draw.text((fx + 30, fy + 25), "SPECIALTY COFFEE FEST", fill=(251, 191, 36), font=obtener_fuente(24, bold=True))
    draw.text((fx + 30, fy + 65), "VIERNES 18 HS • ENTRADA LIBRE", fill=(241, 245, 249), font=obtener_fuente(18, bold=False))
    # Taza destacada con fondo recortado impecable
    draw.ellipse([fx + fw // 2 - 50, fy + fh // 2 - 20, fx + fw // 2 + 50, fy + fh // 2 + 70], fill=(217, 119, 6), outline=(251, 191, 36), width=3)
    draw.text((fx + fw // 2 - 38, fy + fh // 2 + 15), "COFFEE", fill=(255, 255, 255), font=obtener_fuente(18, bold=True))
    draw.rounded_rectangle([fx + 30, fy + fh - 55, fx + fw - 30, fy + fh - 20], radius=8, fill=(217, 119, 6))
    draw.text((fx + fw // 2 - 75, fy + fh - 48), "REGISTRATE GRATIS", fill=(255, 255, 255), font=obtener_fuente(16, bold=True))

    # Barra inferior de interacción social
    iy = fy + fh + 15
    # Botones estilo Instagram limpios
    draw.rounded_rectangle([sx + 20, iy, sx + 95, iy + 30], radius=6, fill=(225, 29, 72))
    draw.text((sx + 30, iy + 6), "LIKE", fill=(255, 255, 255), font=obtener_fuente(14, bold=True))
    draw.rounded_rectangle([sx + 105, iy, sx + 225, iy + 30], radius=6, fill=(30, 41, 59))
    draw.text((sx + 115, iy + 6), "COMENTAR", fill=(255, 255, 255), font=obtener_fuente(14, bold=True))
    draw.text((sx + 20, iy + 38), "1.480 Me gusta • Diseño listo en 3 minutos", fill=(254, 240, 138), font=obtener_fuente(16, bold=True))

    # 3. Píldora inferior (y = 720..795)
    draw.rounded_rectangle([40, 720, ancho - 40, 795], radius=24, fill=(15, 23, 42, 245), outline=(16, 185, 129), width=2)
    dibujar_icono_check(draw, 75, 757, tam=14, color=(16, 185, 129))
    draw.text((105, 742), "Te queda un diseño prolijo sin pagar de más", fill=(255, 255, 255), font=obtener_fuente(26, bold=True))

    # 4. Byte Protagonista: BYTE SALTANDO FELIZ CON CONFETI
    p_byte = DIR_BYTE_TRANSPARENTES / "cierre_guion_04_transparente.png"
    if p_byte.exists():
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


def main():
    escenas = [
        ("01_cold_open_chat", renderizar_plano_chat_flyer_urgente),
        ("02_hook_ps_freeze", renderizar_plano_photoshop_freeze),
        ("03_problema_lienzo_blanco", renderizar_plano_lienzo_blanco_bloqueo),
        ("05_punto_2_removebg_laser", renderizar_plano_remove_bg_laser),
        ("06_resultado_smartphone_feed", renderizar_plano_smartphone_instagram_feed),
    ]
    print("=== RE-GENERANDO PREVIEWS HIPERDINÁMICAS PARA VIDEO 09 ===")
    for nombre, fn in escenas:
        print(f"Renderizando {nombre}...")
        img = fn()
        out_p = DIR_OUT / f"{nombre}.png"
        img.save(out_p, format="PNG")
        print(f"  -> Guardado: {out_p}")


if __name__ == "__main__":
    main()

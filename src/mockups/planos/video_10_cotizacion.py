"""
src.mockups.planos.video_10_cotizacion
---------------------------------------------------------------------------
Planos del Video 10 (Cotizacion Automatica de Pedidos).
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

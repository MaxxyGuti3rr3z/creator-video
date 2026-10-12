"""
src.mockups.planos.video_12_ciberseguridad
---------------------------------------------------------------------------
Planos del Video 12 (Ciberseguridad y Google Ads).
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

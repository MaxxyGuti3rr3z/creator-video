"""
src.mockups.planos.video_13_noticias
---------------------------------------------------------------------------
Planos del Video 13 (Portal de Noticias de IA).
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



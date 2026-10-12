"""
src.mockups.planos.video_11_archivos
---------------------------------------------------------------------------
Planos del Video 11 (50 Archivos - Analisis Documental IA).
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

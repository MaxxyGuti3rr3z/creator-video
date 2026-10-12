"""
src.mockups.planos.video_08_busqueda
---------------------------------------------------------------------------
Planos del Video 08 (Busqueda e Investigacion: Perplexity/NotebookLM).
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

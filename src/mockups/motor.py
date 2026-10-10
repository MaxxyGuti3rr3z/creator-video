"""
motor.py
--------
Motor unificado de renderizado de mockups vectoriales para 'Byte el Zorrito'.
Dibuja ventanas y elementos de interfaz con estándares estrictos:
- 3 puntos simples en gris neutro (#94A3B8, sin colores macOS semáforo).
- Estética limpia, moderna y clara (light-mode slate).
- Sello visible "Simulación ilustrativa" dentro de la zona segura.
- Soporte para notas visuales con cambios de estado dinámicos en intervalos <= 3 segundos.
- Fondos procedurales tech con paleta emocional temática y partículas vivas.
"""

from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any, Union, Callable
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import subprocess
import os

# ---------------------------------------------------------------------------
# Paletas Emocionales del Fondo por Escena
# ---------------------------------------------------------------------------
PALETAS_EMOCIONALES: Dict[str, Dict[str, Any]] = {
    "escena_problema": {
        "nombre": "Caos / Tensión",
        "top": (44, 12, 22),
        "bot": (18, 5, 10),
        "blob": (225, 29, 72, 105),
        "cuadricula": (225, 29, 72, 38),
        "particula": (244, 63, 94),
        "chip_bg": (254, 226, 226),
        "chip_txt": (153, 27, 27)
    },
    "punto_1": {
        "nombre": "Estructura / Orden Lógico",
        "top": (10, 28, 56),
        "bot": (6, 14, 32),
        "blob": (6, 182, 212, 105),
        "cuadricula": (6, 182, 212, 36),
        "particula": (6, 182, 212),
        "chip_bg": (224, 242, 254),
        "chip_txt": (3, 105, 161)
    },
    "punto_2": {
        "nombre": "Automatización IA",
        "top": (18, 20, 58),
        "bot": (8, 10, 34),
        "blob": (99, 102, 241, 100),
        "cuadricula": (99, 102, 241, 36),
        "particula": (129, 140, 248),
        "chip_bg": (238, 242, 255),
        "chip_txt": (67, 56, 202)
    },
    "resultado": {
        "nombre": "Alivio / Solucionado",
        "top": (8, 44, 28),
        "bot": (4, 22, 14),
        "blob": (16, 185, 129, 115),
        "cuadricula": (16, 185, 129, 38),
        "particula": (52, 211, 153),
        "chip_bg": (209, 250, 229),
        "chip_txt": (6, 95, 70)
    },
    "cierre": {
        "nombre": "Interacción / Pregunta",
        "top": (48, 34, 10),
        "bot": (22, 14, 5),
        "blob": (245, 158, 11, 110),
        "cuadricula": (245, 158, 11, 38),
        "particula": (251, 191, 36),
        "chip_bg": (254, 243, 199),
        "chip_txt": (146, 64, 14)
    }
}

# Alias comunes
PALETAS_EMOCIONALES["hook"] = PALETAS_EMOCIONALES["escena_problema"]
PALETAS_EMOCIONALES["tareas_problema"] = PALETAS_EMOCIONALES["escena_problema"]
PALETAS_EMOCIONALES["tareas_todoist"] = PALETAS_EMOCIONALES["punto_1"]
PALETAS_EMOCIONALES["tareas_calendario"] = PALETAS_EMOCIONALES["punto_2"]
PALETAS_EMOCIONALES["tareas_resultado"] = PALETAS_EMOCIONALES["resultado"]
PALETAS_EMOCIONALES["tareas_cierre"] = PALETAS_EMOCIONALES["cierre"]
PALETAS_EMOCIONALES["reunion_hook"] = PALETAS_EMOCIONALES["escena_problema"]
PALETAS_EMOCIONALES["reunion_transcripcion"] = PALETAS_EMOCIONALES["punto_1"]
PALETAS_EMOCIONALES["reunion_asistente"] = PALETAS_EMOCIONALES["punto_2"]
PALETAS_EMOCIONALES["reunion_cierre"] = PALETAS_EMOCIONALES["cierre"]
PALETAS_EMOCIONALES["correo_hilo_resumen"] = PALETAS_EMOCIONALES["punto_1"]
PALETAS_EMOCIONALES["correo_chat_generico"] = PALETAS_EMOCIONALES["punto_2"]
PALETAS_EMOCIONALES["presentaciones_problema"] = PALETAS_EMOCIONALES["escena_problema"]
PALETAS_EMOCIONALES["presentaciones_gamma"] = PALETAS_EMOCIONALES["punto_1"]
PALETAS_EMOCIONALES["presentaciones_canva"] = PALETAS_EMOCIONALES["punto_2"]
PALETAS_EMOCIONALES["presentaciones_resultado"] = PALETAS_EMOCIONALES["resultado"]
PALETAS_EMOCIONALES["presentaciones_cierre"] = PALETAS_EMOCIONALES["cierre"]


# ---------------------------------------------------------------------------
# Tipografía y Fallbacks
# ---------------------------------------------------------------------------

def obtener_fuente(tamanio: int, bold: bool = False) -> ImageFont.ImageFont:
    """Carga fuente Arial de Windows con fallback a default si no estuviera."""
    try:
        nombre = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(nombre, tamanio)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", tamanio)
        except Exception:
            return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Elementos Vectoriales Base
# ---------------------------------------------------------------------------

def dibujar_ventana_base(
    ancho: int,
    alto: int,
    titulo: str = "Aplicación",
    subtitulo: str = "",
    tipo_mockup: str = "ilustrativo",
    bg_color: Tuple[int, int, int] = (255, 255, 255),
    border_color: Tuple[int, int, int] = (226, 232, 240),
    radius: int = 24
) -> Tuple[Image.Image, ImageDraw.Draw, Tuple[int, int, int, int]]:
    """
    Crea el contenedor base de la ventana de aplicación:
    - 3 puntos simples en gris neutro (#94A3B8, sin colores macOS semáforo).
    - Encabezado sutil con título y subtítulo.
    - Sello pequeño 'Simulación ilustrativa' si tipo_mockup == 'ilustrativo'.
    - Retorna (imagen_rgba, draw, (interior_x, interior_y, interior_w, interior_h)).
    """
    img = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Sombra suave de la ventana
    sombra = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_s = ImageDraw.Draw(sombra)
    d_s.rounded_rectangle([6, 10, ancho - 6, alto - 4], radius=radius, fill=(0, 0, 0, 70))
    sombra = sombra.filter(ImageFilter.GaussianBlur(radius=14))
    img = Image.alpha_composite(img, sombra)
    draw = ImageDraw.Draw(img)

    # 2. Contenedor principal de la ventana
    draw.rounded_rectangle([0, 0, ancho, alto], radius=radius, fill=(*bg_color, 252), outline=border_color, width=2)

    # 3. Barra superior (Header)
    h_top = 66
    draw.rounded_rectangle([0, 0, ancho, h_top + 10], radius=radius, fill=(248, 250, 252, 255))
    draw.rectangle([0, h_top - 4, ancho, h_top], fill=(241, 245, 249, 255))
    draw.line([(0, h_top), (ancho, h_top)], fill=border_color, width=1)

    # 4. Los 3 puntos neutros (#94A3B8, tono gris uniforme, no macOS)
    col_dot = (148, 163, 184)
    dot_y = h_top // 2
    r_dot = 6
    for i, dx in enumerate([28, 48, 68]):
        draw.ellipse([dx - r_dot, dot_y - r_dot, dx + r_dot, dot_y + r_dot], fill=col_dot)

    # 5. Título y Breadcrumb (Escala Mobile-First grande y legible)
    f_titulo = obtener_fuente(22, bold=True)
    f_sub = obtener_fuente(18, bold=False)
    x_tit = 94
    draw.text((x_tit, dot_y - 13), titulo, fill=(30, 41, 59), font=f_titulo)

    if subtitulo:
        bbox_t = draw.textbbox((x_tit, dot_y - 13), titulo, font=f_titulo)
        x_sep = bbox_t[2] + 12
        draw.text((x_sep, dot_y - 11), "•", fill=(148, 163, 184), font=f_sub)
        draw.text((x_sep + 14, dot_y - 11), subtitulo, fill=(100, 116, 139), font=f_sub)

    # 6. Sello 'Simulación ilustrativa' (en zona segura superior derecha)
    if tipo_mockup.lower() == "ilustrativo":
        dibujar_sello_ilustrativo(img, ancho, alto)

    area_interior = (18, h_top + 10, ancho - 36, alto - h_top - 18)
    return img, draw, area_interior


def dibujar_icono_check(draw: ImageDraw.Draw, x: int, y: int, color: Tuple[int, ...], tam: int = 12, grosor: int = 2):
    """Dibuja un checkmark vectorial nítido sin emojis ni fuentes externas."""
    draw.line([(x, y + int(tam * 0.5)), (x + int(tam * 0.4), y + tam)], fill=color, width=grosor)
    draw.line([(x + int(tam * 0.4), y + tam), (x + tam, y)], fill=color, width=grosor)


def dibujar_chispa_ia(draw: ImageDraw.Draw, x: int, y: int, tam: int, color: Tuple[int, ...]):
    """Dibuja una estrella / chispa vectorial de 4 puntas de IA."""
    puntos = [
        (x, y - tam),
        (x + int(tam * 0.28), y - int(tam * 0.28)),
        (x + tam, y),
        (x + int(tam * 0.28), y + int(tam * 0.28)),
        (x, y + tam),
        (x - int(tam * 0.28), y + int(tam * 0.28)),
        (x - tam, y),
        (x - int(tam * 0.28), y - int(tam * 0.28)),
    ]
    draw.polygon(puntos, fill=color)


def dibujar_cursor_moderno(
    draw: ImageDraw.Draw,
    x: int,
    y: int,
    scale: float = 1.0,
    haciendo_click: bool = False,
    ripple_prog: float = 0.0,
    ripple_color: Tuple[int, ...] = (6, 182, 212)
):
    """Dibuja cursor de mouse hiper-estilizado con ondas expansivas de clic."""
    if 0.0 < ripple_prog <= 1.0:
        r_rip = int((10 + 38 * ripple_prog) * scale)
        alpha = int(220 * (1.0 - ripple_prog))
        col_rip = (ripple_color[0], ripple_color[1], ripple_color[2], alpha)
        draw.ellipse([x - r_rip, y - r_rip, x + r_rip, y + r_rip], outline=col_rip, width=max(2, int(3 * scale * (1.0 - ripple_prog))))

    cur_scale = scale * (0.84 if haciendo_click else 1.0)
    pts = [
        (0, 0),
        (0, int(22 * cur_scale)),
        (int(6 * cur_scale), int(17 * cur_scale)),
        (int(11 * cur_scale), int(27 * cur_scale)),
        (int(15 * cur_scale), int(25 * cur_scale)),
        (int(10 * cur_scale), int(15 * cur_scale)),
        (int(17 * cur_scale), int(15 * cur_scale))
    ]
    poly_pts = [(x + px, y + py) for px, py in pts]
    poly_sombra = [(x + px + int(2 * scale), y + py + int(2 * scale)) for px, py in pts]
    draw.polygon(poly_sombra, fill=(0, 0, 0, 80))
    draw.polygon(poly_pts, fill=(255, 255, 255), outline=(30, 41, 59))


def dibujar_banderin(draw: ImageDraw.Draw, x: int, y: int, tam: int, color: Tuple[int, ...]):
    """Dibuja un banderín de prioridad vectorial."""
    pts = [
        (x, y),
        (x + tam, y + int(tam * 0.35)),
        (x, y + int(tam * 0.7)),
    ]
    draw.polygon(pts, fill=color)
    draw.line([(x, y), (x, y + int(tam * 1.25))], fill=color, width=2)


def dibujar_icono_reloj(draw: ImageDraw.Draw, x: int, y: int, r: int, color: Tuple[int, ...]):
    """Dibuja un icono vectorial de reloj circular."""
    draw.ellipse([x - r, y - r, x + r, y + r], outline=color, width=max(1, r // 4))
    draw.line([(x, y), (x, y - int(r * 0.55))], fill=color, width=max(1, r // 4))
    draw.line([(x, y), (x + int(r * 0.45), y)], fill=color, width=max(1, r // 4))


# ---------------------------------------------------------------------------
# Control de Ritmo Visual (Regla: Ningún estado > 3 segundos)
# ---------------------------------------------------------------------------

def evaluar_etapa_visual(tiempo_segundos: float, duracion_total: float, num_etapas: int = 3) -> Tuple[int, float]:
    """
    Divide cualquier escena en micro-etapas de <= 3.0 segundos para garantizar dinamismo visual:
    Retorna (indice_etapa_actual, progreso_dentro_de_la_etapa_0_a_1).
    """
    # Si la escena dura más de num_etapas * 3, aumentamos etapas para que cada una dure <= 3.0s
    etapas = max(num_etapas, int(math.ceil(duracion_total / 2.8)))
    dur_etapa = duracion_total / float(etapas)
    
    idx = int(tiempo_segundos // dur_etapa)
    idx = max(0, min(etapas - 1, idx))
    
    t_en_etapa = tiempo_segundos - (idx * dur_etapa)
    prog_etapa = max(0.0, min(1.0, t_en_etapa / max(0.001, dur_etapa)))
    return idx, prog_etapa


# ---------------------------------------------------------------------------
# Generador de Fondo Tech con Paleta Emocional
# ---------------------------------------------------------------------------

def generar_fondo_tech_base(ancho: int, alto: int, tipo_escena: str) -> Image.Image:
    """Genera la imagen de fondo 1080x1920 con degradado emocional, cuadrícula y resplandor."""
    cfg = PALETAS_EMOCIONALES.get(tipo_escena, PALETAS_EMOCIONALES["escena_problema"])
    col_arriba = cfg["top"]
    col_abajo = cfg["bot"]
    col_blob = cfg["blob"]
    col_grid = cfg["cuadricula"]

    # 1. Degradado vertical
    base = Image.new("RGBA", (ancho, alto), (0, 0, 0, 255))
    d_base = ImageDraw.Draw(base)
    for y in range(alto):
        fac = y / float(alto)
        r = int(col_arriba[0] + fac * (col_abajo[0] - col_arriba[0]))
        g = int(col_arriba[1] + fac * (col_abajo[1] - col_arriba[1]))
        b = int(col_arriba[2] + fac * (col_abajo[2] - col_arriba[2]))
        d_base.line([(0, y), (ancho, y)], fill=(r, g, b, 255))

    # 2. Resplandor difuso suave
    blobs = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_b = ImageDraw.Draw(blobs)
    d_b.ellipse([ancho // 2 - 320, 160, ancho // 2 + 320, 800], fill=col_blob)
    d_b.ellipse([ancho // 2 - 280, alto - 620, ancho // 2 + 280, alto - 80], fill=(*col_blob[:3], int(col_blob[3] * 0.75)))
    blobs = blobs.filter(ImageFilter.GaussianBlur(radius=150))
    base = Image.alpha_composite(base, blobs)

    # 3. Cuadrícula tech suave
    grid = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_g = ImageDraw.Draw(grid)
    paso = 90
    for x in range(0, ancho, paso):
        d_g.line([(x, 0), (x, alto)], fill=col_grid, width=1)
    for y in range(0, alto, paso):
        d_g.line([(0, y), (ancho, y)], fill=col_grid, width=1)

    return Image.alpha_composite(base, grid)


# ---------------------------------------------------------------------------
# Orquestador de Video Interactivo (FFmpeg Pipe sin Deadlock)
# ---------------------------------------------------------------------------

def generar_video_interactivo(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    render_func: Callable[[int, int, float, float, Optional[Dict[str, Any]], str], Image.Image],
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo",
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """
    Genera un video MP4 animado de 1080x1920 con cámara dinámica y renderizado por frame.
    Garantiza que ningún estado visual supere los 3.0s y canaliza el stream sin OS buffer deadlock.
    """
    ruta_salida = Path(ruta_salida)
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    total_frames = max(1, int(duracion_segundos * fps))

    base_fondo = generar_fondo_tech_base(ancho, alto, tipo_escena)
    w_m, h_m = 940, 560
    x_m = (ancho - w_m) // 2
    y_m = 210

    # Partículas flotantes
    cfg_esc = PALETAS_EMOCIONALES.get(tipo_escena, PALETAS_EMOCIONALES["escena_problema"])
    col_p = cfg_esc.get("particula", (6, 182, 212))
    particulas = [
        (int((i * 197) % ancho), int((i * 313) % alto), 18 + (i % 14), 2 + (i % 3), (*col_p, 25 + (i * 7) % 35))
        for i in range(18)
    ]

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{ancho}x{alto}",
        "-pix_fmt", "rgba",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "18",
        str(ruta_salida)
    ]

    # Previene deadlock cerrando pipes no utilizados
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        for f_idx in range(total_frames):
            if f_idx % 60 == 0 or f_idx == total_frames - 1:
                print(f"  [{tipo_escena}] Frame {f_idx + 1}/{total_frames} ({((f_idx + 1) / total_frames) * 100:.0f}%)...", flush=True)

            t = f_idx / float(fps)
            prog = min(1.0, f_idx / float(max(1, total_frames - 1)))

            # Renderizado de la plantilla específica
            mockup = render_func(w_m, h_m, prog, t, notas_visuales, tipo_mockup)

            # Zoom suave de cámara (punch-in progresivo 4% a 8%)
            zoom = 1.0 + 0.05 * math.sin(prog * math.pi / 2.0)
            if abs(zoom - 1.0) > 0.005:
                nw = max(1, int(w_m * zoom))
                nh = max(1, int(h_m * zoom))
                mockup_to_paste = mockup.resize((nw, nh), Image.Resampling.BILINEAR)
                focal_x = x_m + w_m / 2.0
                focal_y = y_m + h_m / 2.0
                paste_x = int(focal_x - (focal_x - x_m) * zoom)
                paste_y = int(focal_y - (focal_y - y_m) * zoom)
            else:
                mockup_to_paste = mockup
                paste_x = x_m
                paste_y = y_m

            frame_img = base_fondo.copy()
            d_frame = ImageDraw.Draw(frame_img)

            # Partículas vivas
            for (p_x0, p_y0, p_v, p_r, p_col) in particulas:
                px = (p_x0 + int(20 * math.sin(t * 1.5 + p_x0))) % ancho
                py = (p_y0 - int(t * p_v)) % alto
                d_frame.ellipse([px - p_r, py - p_r, px + p_r, py + p_r], fill=p_col)

            # Pegar mockup sobre fondo
            frame_img.paste(mockup_to_paste, (paste_x, paste_y), mockup_to_paste)

            proc.stdin.write(frame_img.tobytes())

        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        raise e

    print(f"Video interactivo {tipo_escena} generado en: {ruta_salida} ({total_frames} frames)")
    return ruta_salida


# ---------------------------------------------------------------------------
# Generador de Frame Completo para Preview y Validación
# ---------------------------------------------------------------------------

def generar_frame_completo_escena(
    tipo_escena: str,
    mockup_img: Image.Image,
    ruta_byte_transparente: Path,
    texto_subtitulo: str,
    ruta_salida: Path,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Genera un frame completo (fondo + mockup + Byte + subtítulos) para previsualización."""
    ruta_salida = Path(ruta_salida)
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    frame = generar_fondo_tech_base(ancho, alto, tipo_escena)
    draw = ImageDraw.Draw(frame)

    m_w, m_h = mockup_img.size
    m_x = (ancho - m_w) // 2
    m_y = 190
    frame.paste(mockup_img, (m_x, m_y), mockup_img)

    # Chip superior opcional
    titulos_chip = {
        "escena_problema": "PRODUCTIVIDAD • CAOS DE TAREAS",
        "punto_1": "MÉTODO 1 • PRIORIDADES INTELIGENTES",
        "punto_2": "MÉTODO 2 • AUTO-SCHEDULE EN HUECOS",
        "resultado": "RESULTADO • BANDEJA EN CERO",
        "cierre": "ORGANIZACIÓN • DÍA COMPLETADO",
        "reunion_hook": "PRODUCTIVIDAD • REUNIONES LARGAS",
        "reunion_transcripcion": "MÉTODO 1 • TRANSCRIPCIÓN EN VIVO",
        "reunion_asistente": "MÉTODO 2 • ASISTENTE DE MINUTAS",
        "reunion_cierre": "ORGANIZACIÓN • REUNIÓN RESUELTA",
        "correo_hilo_resumen": "MÉTODO 1 • RESUMEN DE CORREO",
        "correo_chat_generico": "MÉTODO 2 • CHAT ASISTENTE",
    }
    txt_c = titulos_chip.get(tipo_escena)
    if txt_c:
        f_chip = obtener_fuente(16, bold=True)
        bbox_c = draw.textbbox((0, 0), txt_c, font=f_chip)
        tw_c = bbox_c[2] - bbox_c[0]
        chip_w = tw_c + 60
        chip_h = 42
        chip_x = (ancho - chip_w) // 2
        chip_y = 110
        cfg_chip = PALETAS_EMOCIONALES.get(tipo_escena, PALETAS_EMOCIONALES["escena_problema"])
        accent_col = cfg_chip.get("particula", (6, 182, 212))
        draw.rounded_rectangle([chip_x, chip_y, chip_x + chip_w, chip_y + chip_h], radius=21, fill=(15, 23, 42, 230), outline=accent_col, width=2)
        dibujar_chispa_ia(draw, chip_x + 20, chip_y + 21, 6, accent_col)
        draw.text((chip_x + 36, chip_y + 11), txt_c, fill=(255, 255, 255, 255), font=f_chip)

    # Sprite de Byte transparente
    if ruta_byte_transparente and ruta_byte_transparente.exists():
        with Image.open(ruta_byte_transparente) as img_byte:
            img_b = img_byte.convert("RGBA")
            bw, bh = 580, 580
            img_b = img_b.resize((bw, bh), Image.Resampling.LANCZOS)
            bx = (ancho - bw) // 2
            by = alto - bh - 50
            frame.paste(img_b, (bx, by), img_b)

    # Subtítulo en Amarillo puro #FFF500 con borde negro de 8px (Safe Zone: entre mockup y Byte)
    if texto_subtitulo:
        f_sub = obtener_fuente(54, bold=True)
        sub_y = 860  # Safe Zone óptima
        bbox_sub = draw.textbbox((0, 0), texto_subtitulo, font=f_sub)
        sub_w = bbox_sub[2] - bbox_sub[0]
        sub_x = (ancho - sub_w) // 2

        grosor = 8
        for dx in range(-grosor, grosor + 1):
            for dy in range(-grosor, grosor + 1):
                if dx * dx + dy * dy <= grosor * grosor:
                    draw.text((sub_x + dx, sub_y + dy), texto_subtitulo, fill=(0, 0, 0, 255), font=f_sub)
        draw.text((sub_x, sub_y), texto_subtitulo, fill=(255, 245, 0, 255), font=f_sub)

    frame.save(ruta_salida, format="PNG")
    print(f"[PREVIEW] Frame generado: {ruta_salida.name} -> {ruta_salida.resolve()}")
    return ruta_salida


# ---------------------------------------------------------------------------
# Enrutadores y Wrappers de Retrocompatibilidad
# ---------------------------------------------------------------------------

def dibujar_sello_ilustrativo(img: Image.Image, ancho: int, alto: int = 560):
    """Garantiza la presencia del sello 'Simulación ilustrativa' en la zona segura superior derecha."""
    draw = ImageDraw.Draw(img)
    f_sello = obtener_fuente(13, bold=True)
    txt_sello = "Simulación ilustrativa"
    bbox_s = draw.textbbox((0, 0), txt_sello, font=f_sello)
    sw = bbox_s[2] - bbox_s[0] + 18
    sh = bbox_s[3] - bbox_s[1] + 12
    sx = ancho - sw - 20
    sy = (66 - sh) // 2
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=1)
    draw.text((sx + 9, sy + 5), txt_sello, fill=(100, 116, 139), font=f_sello)


def renderizar_mockup_por_nombre(
    nombre_plantilla: str,
    ancho: int = 940,
    alto: int = 560,
    progreso: float = 0.0,
    tiempo_segundos: float = 0.0,
    notas_visuales: Optional[Dict[str, Any]] = None,
    tipo_mockup: str = "ilustrativo"
) -> Image.Image:
    """Invoca la función renderizar_frame del catálogo de plantillas y asegura el sello ilustrativo."""
    from src.mockups.plantillas import obtener_plantilla
    mod = obtener_plantilla(nombre_plantilla)
    img = mod.renderizar_frame(
        ancho=ancho,
        alto=alto,
        progreso=progreso,
        tiempo_segundos=tiempo_segundos,
        notas_visuales=notas_visuales,
        tipo_mockup=tipo_mockup
    )
    if tipo_mockup.lower() == "ilustrativo":
        dibujar_sello_ilustrativo(img, ancho, alto)
    return img


def generar_video_interactivo_tareas(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para compatibilidad con tareas (Video 3)."""
    mapa = {
        "escena_problema": "tareas_problema",
        "punto_1": "tareas_todoist",
        "punto_2": "tareas_calendario",
        "resultado": "tareas_resultado",
        "cierre": "tareas_cierre",
    }
    plantilla_key = mapa.get(tipo_escena, tipo_escena)
    
    def _render(w, h, prog, t, nv, tm):
        return renderizar_mockup_por_nombre(plantilla_key, w, h, prog, t, nv, tm)

    return generar_video_interactivo(
        tipo_escena=tipo_escena,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        render_func=_render,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


def generar_video_interactivo_reunion(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para compatibilidad con reuniones (Video 2)."""
    mapa = {
        "hook": "reunion_hook",
        "escena_problema": "reunion_hook",
        "punto_1": "reunion_transcripcion",
        "punto_2": "reunion_asistente",
        "cierre": "reunion_cierre",
        "resultado": "reunion_cierre"
    }
    plantilla_key = mapa.get(tipo_escena, tipo_escena)

    def _render(w, h, prog, t, nv, tm):
        return renderizar_mockup_por_nombre(plantilla_key, w, h, prog, t, nv, tm)

    return generar_video_interactivo(
        tipo_escena=tipo_escena,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        render_func=_render,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


def generar_video_interactivo_correo(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para Video 4 (correo)."""
    mapa = {
        "escena_problema": "tareas_problema",
        "hook": "tareas_problema",
        "punto_1": "correo_hilo_resumen",
        "punto_2": "correo_chat_generico",
        "resultado": "tareas_resultado",
        "cierre": "tareas_cierre",
    }
    plantilla_key = mapa.get(tipo_escena, tipo_escena)

    def _render(w, h, prog, t, nv, tm):
        return renderizar_mockup_por_nombre(plantilla_key, w, h, prog, t, nv, tm)

    return generar_video_interactivo(
        tipo_escena=tipo_escena,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        render_func=_render,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


def generar_video_interactivo_presentaciones(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para Video 5 (presentaciones e informes: Gamma y Canva)."""
    mapa = {
        "escena_problema": "presentaciones_problema",
        "hook": "presentaciones_problema",
        "problema": "presentaciones_problema",
        "punto_1": "presentaciones_gamma",
        "demostracion_1": "presentaciones_gamma",
        "gamma": "presentaciones_gamma",
        "punto_2": "presentaciones_canva",
        "demostracion_2": "presentaciones_canva",
        "canva": "presentaciones_canva",
        "resultado": "presentaciones_resultado",
        "cierre": "presentaciones_cierre",
    }
    plantilla_key = mapa.get(tipo_escena, tipo_escena)

    def _render(w, h, prog, t, nv, tm):
        return renderizar_mockup_por_nombre(plantilla_key, w, h, prog, t, nv, tm)

    return generar_video_interactivo(
        tipo_escena=tipo_escena,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        render_func=_render,
        fps=fps,
        ancho=ancho,
        alto=alto
    )



"""
fondos.py
---------
Librería de estilos de fondo atmosféricos y cinemáticos para Byte el Zorrito.
Ofrece variedad visual sin caer en una cuadrícula plana repetitiva:
- 'aurora_ambient': Ondas de luz suaves y orbes bokeh flotantes con glow y profundidad.
- 'cyber_spotlight': Cuadrícula tech moderna con haz de luz volumétrico y estelas de pulso.
- 'studio_minimal': Iluminación de estudio editorial con degradado radial y viñeta cinematográfica.
- 'nebula_waves': Ondas de energía etéreas ideales para IA y automatización.
"""

from typing import Tuple, List, Dict, Any
from PIL import Image, ImageDraw, ImageFilter
import math


def _crear_degradado_lineal(ancho: int, alto: int, col_arriba: Tuple[int, int, int], col_abajo: Tuple[int, int, int]) -> Image.Image:
    """Genera degradado vertical 24-bit RGB."""
    base = Image.new("RGBA", (ancho, alto), (0, 0, 0, 255))
    d = ImageDraw.Draw(base)
    for y in range(alto):
        f = y / float(alto)
        r = int(col_arriba[0] + f * (col_abajo[0] - col_arriba[0]))
        g = int(col_arriba[1] + f * (col_abajo[1] - col_arriba[1]))
        b = int(col_arriba[2] + f * (col_abajo[2] - col_arriba[2]))
        d.line([(0, y), (ancho, y)], fill=(r, g, b, 255))
    return base


def renderizar_fondo_aurora(
    ancho: int,
    alto: int,
    col_primario: Tuple[int, int, int],
    col_secundario: Tuple[int, int, int],
    progreso_t: float = 0.0
) -> Image.Image:
    """
    Estilo 'aurora_ambient':
    Luces de aurora orgánicas que respiran con ondas lentas y orbes bokeh de luz difusa.
    """
    # 1. Base oscura armónica
    bg_top = (int(col_primario[0] * 0.16), int(col_primario[1] * 0.16), int(col_primario[2] * 0.18))
    bg_bot = (int(col_secundario[0] * 0.06), int(col_secundario[1] * 0.06), int(col_secundario[2] * 0.08))
    canvas = _crear_degradado_lineal(ancho, alto, bg_top, bg_bot)

    # 2. Orbes de aurora vivos (resplandor que flota y respira con progreso_t)
    aurora = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_a = ImageDraw.Draw(aurora)

    cx1 = int(ancho * 0.35 + math.sin(progreso_t * math.pi * 2) * 90)
    cy1 = int(alto * 0.28 + math.cos(progreso_t * math.pi * 2) * 60)
    r1 = 440
    d_a.ellipse([cx1 - r1, cy1 - r1, cx1 + r1, cy1 + r1], fill=(*col_primario, 120))

    cx2 = int(ancho * 0.65 + math.cos(progreso_t * math.pi * 2) * 80)
    cy2 = int(alto * 0.42 + math.sin(progreso_t * math.pi * 2) * 70)
    r2 = 380
    d_a.ellipse([cx2 - r2, cy2 - r2, cx2 + r2, cy2 + r2], fill=(*col_secundario, 100))

    # Orbe inferior sutil detrás de Byte
    cx3 = int(ancho * 0.50)
    cy3 = int(alto * 0.78)
    r3 = 360
    d_a.ellipse([cx3 - r3, cy3 - r3, cx3 + r3, cy3 + r3], fill=(*col_primario, 80))

    aurora = aurora.filter(ImageFilter.GaussianBlur(radius=160))
    canvas = Image.alpha_composite(canvas, aurora)

    # 3. Partículas Bokeh flotantes a distintas profundidades
    particulas = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_p = ImageDraw.Draw(particulas)

    for i in range(24):
        fase = (i * 0.17 + progreso_t) % 1.0
        px = int((i * 181 + math.sin(fase * math.pi * 2 + i) * 50) % ancho)
        py = int((alto - (fase * alto * 1.1) + i * 40) % alto)
        radio = 3 + (i % 6)
        alpha = int(40 + (i % 5) * 28)
        color = col_primario if i % 2 == 0 else col_secundario

        # Halo suave
        d_p.ellipse([px - radio * 2, py - radio * 2, px + radio * 2, py + radio * 2], fill=(*color, alpha // 3))
        # Núcleo nítido
        d_p.ellipse([px - radio, py - radio, px + radio, py + radio], fill=(*color, alpha))

    canvas = Image.alpha_composite(canvas, particulas)
    return canvas


def renderizar_fondo_cyber_spotlight(
    ancho: int,
    alto: int,
    col_primario: Tuple[int, int, int],
    col_secundario: Tuple[int, int, int],
    progreso_t: float = 0.0
) -> Image.Image:
    """
    Estilo 'cyber_spotlight':
    Spotlight cenital volumétrico que enfoca el mockup con cuadrícula de alta precisión y pulsos.
    """
    # 1. Base muy profunda
    canvas = _crear_degradado_lineal(ancho, alto, (14, 17, 24), (6, 8, 12))

    # 2. Haz de luz / Spotlight cónico superior
    spotlight = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_s = ImageDraw.Draw(spotlight)
    # Cono de luz desde arriba al centro
    pts_cono = [
        (ancho // 2 - 120, -50),
        (ancho // 2 + 120, -50),
        (ancho // 2 + 480, 850),
        (ancho // 2 - 480, 850)
    ]
    d_s.polygon(pts_cono, fill=(*col_primario, 75))
    d_s.ellipse([ancho // 2 - 320, 200, ancho // 2 + 320, 720], fill=(*col_secundario, 95))
    spotlight = spotlight.filter(ImageFilter.GaussianBlur(radius=120))
    canvas = Image.alpha_composite(canvas, spotlight)

    # 3. Cuadrícula tech nítida con líneas de pulso activas
    grid = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_g = ImageDraw.Draw(grid)
    paso = 80
    col_g = (*col_primario, 28)
    for x in range(0, ancho, paso):
        d_g.line([(x, 0), (x, alto)], fill=col_g, width=1)
    for y in range(0, alto, paso):
        d_g.line([(0, y), (ancho, y)], fill=col_g, width=1)

    # Línea de barrido / data-pulse
    y_scan = int((progreso_t * alto * 1.5) % alto)
    d_g.line([(0, y_scan), (ancho, y_scan)], fill=(*col_secundario, 90), width=2)
    d_g.line([(0, y_scan - 2), (ancho, y_scan - 2)], fill=(*col_secundario, 35), width=4)

    canvas = Image.alpha_composite(canvas, grid)
    return canvas


def renderizar_fondo_studio_minimal(
    ancho: int,
    alto: int,
    col_primario: Tuple[int, int, int],
    col_secundario: Tuple[int, int, int],
    progreso_t: float = 0.0
) -> Image.Image:
    """
    Estilo 'studio_minimal':
    Degradado de estudio fotográfico suave con viñeta perimetral y halo central elegante.
    """
    top_col = (int(col_primario[0] * 0.22), int(col_primario[1] * 0.22), int(col_primario[2] * 0.24))
    bot_col = (12, 14, 18)
    canvas = _crear_degradado_lineal(ancho, alto, top_col, bot_col)

    # Halo radial sutil
    halo = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_h = ImageDraw.Draw(halo)
    d_h.ellipse([ancho // 2 - 380, 220, ancho // 2 + 380, 780], fill=(*col_primario, 85))
    d_h.ellipse([ancho // 2 - 250, alto - 550, ancho // 2 + 250, alto - 150], fill=(*col_secundario, 70))
    halo = halo.filter(ImageFilter.GaussianBlur(radius=180))
    canvas = Image.alpha_composite(canvas, halo)

    # Viñeta oscura perimetral
    vineta = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_v = ImageDraw.Draw(vineta)
    d_v.rectangle([0, 0, ancho, alto], outline=(0, 0, 0, 110), width=60)
    d_v.rectangle([40, 40, ancho - 40, alto - 40], outline=(0, 0, 0, 70), width=50)
    vineta = vineta.filter(ImageFilter.GaussianBlur(radius=80))
    canvas = Image.alpha_composite(canvas, vineta)
    return canvas


def renderizar_fondo_viaje_espacial(
    ancho: int,
    alto: int,
    col_primario: Tuple[int, int, int] = (99, 102, 241),
    col_secundario: Tuple[int, int, int] = (56, 189, 248),
    progreso_t: float = 0.0
) -> Image.Image:
    """
    Estilo 'viaje_espacial' / 'space_warp':
    Starfield hiperespacial con estelas de estrellas en velocidad luz y nebulosa cósmica.
    """
    # 1. Espacio profundo
    canvas = _crear_degradado_lineal(ancho, alto, (10, 10, 20), (4, 4, 10))

    # 2. Nebulosa cósmica difusa central
    nebulosa = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_neb = ImageDraw.Draw(nebulosa)
    cx_neb = ancho // 2
    cy_neb = int(alto * 0.38)
    d_neb.ellipse([cx_neb - 450, cy_neb - 350, cx_neb + 450, cy_neb + 350], fill=(*col_primario, 95))
    d_neb.ellipse([cx_neb - 280, cy_neb - 180, cx_neb + 280, cy_neb + 180], fill=(*col_secundario, 110))
    nebulosa = nebulosa.filter(ImageFilter.GaussianBlur(radius=160))
    canvas = Image.alpha_composite(canvas, nebulosa)

    # 3. Estrellas con estelas de velocidad 3D (Warp / Hiperespacio)
    warp_layer = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_w = ImageDraw.Draw(warp_layer)
    centro_x = ancho // 2
    centro_y = int(alto * 0.36)

    num_estrellas = 90
    for i in range(num_estrellas):
        # Ángulo radial y profundidad z
        ang = (i * 0.281) * (math.pi * 2)
        fase_z = ((i * 0.037 + progreso_t * 1.8) % 1.0)  # De 0 (lejos) a 1 (cerca)
        dist_actual = (fase_z ** 1.8) * (ancho * 0.85)
        dist_cola = max(0.0, dist_actual - (fase_z * 70.0 + 8.0))

        # Posiciones cabeza y cola del rayo de estrella
        x_head = int(centro_x + math.cos(ang) * dist_actual)
        y_head = int(centro_y + math.sin(ang) * dist_actual * 1.3)
        x_tail = int(centro_x + math.cos(ang) * dist_cola)
        y_tail = int(centro_y + math.sin(ang) * dist_cola * 1.3)

        if 0 <= x_head < ancho and 0 <= y_head < alto:
            alpha = int(min(255, fase_z * 280))
            grosor = max(1, int(fase_z * 3.5))
            color_estrella = (255, 255, 255, alpha) if i % 3 != 0 else (*col_secundario, alpha)
            d_w.line([(x_tail, y_tail), (x_head, y_head)], fill=color_estrella, width=grosor)
            if fase_z > 0.4:
                r_cabeza = max(1, int(fase_z * 2.5))
                d_w.ellipse([x_head - r_cabeza, y_head - r_cabeza, x_head + r_cabeza, y_head + r_cabeza], fill=(255, 255, 255, alpha))

    canvas = Image.alpha_composite(canvas, warp_layer)
    return canvas


def renderizar_fondo_ciudad_nocturna(
    ancho: int,
    alto: int,
    col_primario: Tuple[int, int, int] = (225, 29, 72),   # Magenta/Rojo neón
    col_secundario: Tuple[int, int, int] = (6, 182, 212), # Cian neón
    progreso_t: float = 0.0
) -> Image.Image:
    """
    Estilo 'ciudad_nocturna' / 'cyber_city':
    Skyline nocturno cyberpunk con siluetas de rascacielos, ventanas titilantes y estelas de tráfico.
    """
    # 1. Cielo de noche profunda
    canvas = _crear_degradado_lineal(ancho, alto, (8, 10, 20), (18, 12, 28))

    # 2. Resplandor de horizonte / smog de neón
    glow = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_g = ImageDraw.Draw(glow)
    y_horizonte = int(alto * 0.72)
    d_g.ellipse([ancho // 2 - 500, y_horizonte - 240, ancho // 2 + 500, y_horizonte + 160], fill=(*col_primario, 80))
    d_g.ellipse([ancho // 2 - 380, y_horizonte - 180, ancho // 2 + 380, y_horizonte + 120], fill=(*col_secundario, 75))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=110))
    canvas = Image.alpha_composite(canvas, glow)

    # 3. Capa de Rascacielos Lejanos (siluetas oscuras + ventanas)
    capa_ciudad_lejos = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_c1 = ImageDraw.Draw(capa_ciudad_lejos)
    edificios_lejos = [
        (40, 240, 110), (170, 310, 130), (320, 260, 95), (435, 360, 140),
        (595, 280, 120), (735, 340, 110), (865, 250, 140)
    ]
    for x_b, h_b, w_b in edificios_lejos:
        y_top = y_horizonte - h_b
        d_c1.rectangle([x_b, y_top, x_b + w_b, y_horizonte + 100], fill=(16, 20, 34, 230))
        # Ventanitas titilantes
        for wx in range(x_b + 12, x_b + w_b - 12, 16):
            for wy in range(y_top + 20, y_horizonte - 20, 24):
                seed = (wx * 13 + wy * 19 + int(progreso_t * 8)) % 10
                if seed > 5:
                    d_c1.rectangle([wx, wy, wx + 6, wy + 8], fill=(*col_secundario, 140))
                elif seed > 3:
                    d_c1.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 230, 150, 130))

    capa_ciudad_lejos = capa_ciudad_lejos.filter(ImageFilter.GaussianBlur(radius=2))
    canvas = Image.alpha_composite(canvas, capa_ciudad_lejos)

    # 4. Capa de Rascacielos Cercanos (siluetas nítidas + bordes de neón)
    capa_ciudad_cerca = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_c2 = ImageDraw.Draw(capa_ciudad_cerca)
    edificios_cerca = [
        (-20, 180, 130), (130, 210, 140), (290, 160, 110),
        (420, 240, 150), (590, 190, 130), (740, 220, 140), (900, 170, 160)
    ]
    for x_b, h_b, w_b in edificios_cerca:
        y_top = y_horizonte - h_b + 30
        d_c2.rectangle([x_b, y_top, x_b + w_b, alto], fill=(10, 12, 20, 255), outline=(30, 36, 54, 255), width=1)
        # Línea de neón en la azotea
        col_neon = col_primario if (x_b % 2 == 0) else col_secundario
        d_c2.line([(x_b, y_top), (x_b + w_b, y_top)], fill=(*col_neon, 210), width=2)
        # Antena con baliza
        x_ant = x_b + w_b // 2
        d_c2.line([(x_ant, y_top), (x_ant, y_top - 25)], fill=(120, 130, 150), width=1)
        d_c2.ellipse([x_ant - 2, y_top - 28, x_ant + 2, y_top - 24], fill=(239, 68, 68, 240))

    canvas = Image.alpha_composite(canvas, capa_ciudad_cerca)

    # 5. Autopista inferior con estelas de luz en movimiento (tráfico rápido)
    trafico = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d_t = ImageDraw.Draw(trafico)
    for i in range(12):
        y_lane = y_horizonte + 60 + i * 22
        vel = (1.2 + (i % 3) * 0.4)
        offset = ((progreso_t * vel * ancho + i * 160) % (ancho * 1.5)) - 200
        largo = 120 + (i % 4) * 80
        col_luz = (244, 63, 94) if i % 2 == 0 else (56, 189, 248)
        d_t.line([(offset, y_lane), (offset + largo, y_lane)], fill=(*col_luz, 220), width=3)
        d_t.line([(offset - 4, y_lane), (offset + largo + 4, y_lane)], fill=(*col_luz, 80), width=6)

    trafico = trafico.filter(ImageFilter.GaussianBlur(radius=3))
    canvas = Image.alpha_composite(canvas, trafico)
    return canvas


CATALOGO_FONDOS = {
    "aurora_ambient": renderizar_fondo_aurora,
    "cyber_spotlight": renderizar_fondo_cyber_spotlight,
    "studio_minimal": renderizar_fondo_studio_minimal,
    "viaje_espacial": renderizar_fondo_viaje_espacial,
    "space_warp": renderizar_fondo_viaje_espacial,
    "ciudad_nocturna": renderizar_fondo_ciudad_nocturna,
    "cyber_city": renderizar_fondo_ciudad_nocturna
}


def renderizar_fondo_estilizado(
    estilo: str,
    ancho: int,
    alto: int,
    col_primario: Tuple[int, int, int],
    col_secundario: Tuple[int, int, int],
    progreso_t: float = 0.0
) -> Image.Image:
    """Despachador para generar fondos estilizados."""
    func = CATALOGO_FONDOS.get(estilo.lower().strip(), renderizar_fondo_aurora)
    return func(ancho, alto, col_primario, col_secundario, progreso_t)

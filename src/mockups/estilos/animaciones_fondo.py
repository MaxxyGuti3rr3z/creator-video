"""
animaciones_fondo.py
--------------------
Motor de Fondos Animados Continuos (Motion Backgrounds) para Byte el Zorrito.
Genera videos de fondo donde NINGÚN elemento es estático:
1. Ciudad Cyberpunk en Vivo:
   - Lluvia diagonal cinemática con gotas veloces y refracción.
   - Tráfico incesante de haces de luz en autopistas a distintas velocidades.
   - Luces de neón y ventanas que titilan orgánicamente.
   - Reflectores de búsqueda (searchlights) barriendo el cielo nocturno.
   - Humo/niebla volumétrica flotando entre los rascacielos.
2. Viaje Espacial Hipervelocidad (Space Warp 3D):
   - Starfield 3D continuo donde cientos de estrellas nacen, viajan hacia la cámara y se estiran en rayos de luz.
   - Nebulosa cósmica que ondula y respira en rotación lenta.
3. Soporte para Video Loops MP4 pre-renderizados o de stock.
"""

from typing import Tuple, List, Dict, Any
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math
import random
import numpy as np


class GeneradorCiudadCyberpunkAnimada:
    """Motor de simulación procedural de una ciudad cyberpunk nocturna viva."""
    def __init__(self, ancho: int = 1080, alto: int = 1920):
        self.ancho = ancho
        self.alto = alto
        self.rng = random.Random(42)

        # 1. Rascacielos estáticos pero con ventanas dinámicas
        self.y_horizonte = int(alto * 0.72)
        self.edificios = [
            (20, 260, 120), (150, 340, 140), (300, 280, 100), (410, 420, 160),
            (580, 310, 130), (720, 380, 120), (850, 270, 150), (1010, 350, 100)
        ]
        # Posición de ventanas fijas para que no salten de lugar
        self.ventanas = []
        for x_b, h_b, w_b in self.edificios:
            y_top = self.y_horizonte - h_b
            for wx in range(x_b + 12, x_b + w_b - 12, 18):
                for wy in range(y_top + 20, self.y_horizonte - 20, 26):
                    tipo_col = self.rng.choice(["cian", "ambar", "blanco", "apagada"])
                    freq = self.rng.uniform(1.5, 4.5)
                    offset = self.rng.uniform(0, 10)
                    self.ventanas.append((wx, wy, tipo_col, freq, offset))

        # 2. Gotas de lluvia (x, y, velocidad, largo)
        self.num_lluvia = 180
        self.lluvia = [
            [self.rng.randint(0, ancho), self.rng.randint(0, alto), self.rng.randint(32, 54), self.rng.randint(25, 45)]
            for _ in range(self.num_lluvia)
        ]

    def render_frame(self, t_sec: float) -> Image.Image:
        # Base de cielo medianoche profundo
        base = Image.new("RGBA", (self.ancho, self.alto), (10, 12, 22, 255))
        draw = ImageDraw.Draw(base)

        # 1. Reflectores de búsqueda (Searchlights) barriendo el cielo nocturno
        searchlights = Image.new("RGBA", (self.ancho, self.alto), (0, 0, 0, 0))
        d_sl = ImageDraw.Draw(searchlights)
        for i, (orig_x, vel_ang, base_ang) in enumerate([(220, 0.4, 0.2), (860, -0.35, -0.3)]):
            ang = base_ang + math.sin(t_sec * vel_ang) * 0.45
            largo = 1400
            x_fin = int(orig_x + math.sin(ang) * largo)
            y_fin = int(self.y_horizonte - math.cos(ang) * largo)
            pts_haz = [
                (orig_x - 15, self.y_horizonte),
                (orig_x + 15, self.y_horizonte),
                (x_fin + 140, y_fin),
                (x_fin - 140, y_fin)
            ]
            col_luz = (6, 182, 212, 45) if i == 0 else (168, 85, 247, 40)
            d_sl.polygon(pts_haz, fill=col_luz)
        searchlights = searchlights.filter(ImageFilter.GaussianBlur(radius=40))
        base = Image.alpha_composite(base, searchlights)

        # 2. Resplandor difuso del horizonte / smog de neón
        glow = Image.new("RGBA", (self.ancho, self.alto), (0, 0, 0, 0))
        d_g = ImageDraw.Draw(glow)
        d_g.ellipse([self.ancho // 2 - 500, self.y_horizonte - 240, self.ancho // 2 + 500, self.y_horizonte + 160], fill=(225, 29, 72, 70))
        d_g.ellipse([self.ancho // 2 - 380, self.y_horizonte - 180, self.ancho // 2 + 380, self.y_horizonte + 120], fill=(6, 182, 212, 85))
        glow = glow.filter(ImageFilter.GaussianBlur(radius=100))
        base = Image.alpha_composite(base, glow)

        # 3. Siluetas de Rascacielos con ventanas titilantes en tiempo real
        edif_layer = Image.new("RGBA", (self.ancho, self.alto), (0, 0, 0, 0))
        d_e = ImageDraw.Draw(edif_layer)
        for x_b, h_b, w_b in self.edificios:
            y_top = self.y_horizonte - h_b
            d_e.rectangle([x_b, y_top, x_b + w_b, self.alto], fill=(12, 15, 24, 255), outline=(28, 34, 48, 255), width=1)
            # Neón en la azotea
            col_borde = (6, 182, 212, 190) if (x_b % 2 == 0) else (244, 63, 94, 190)
            d_e.line([(x_b, y_top), (x_b + w_b, y_top)], fill=col_borde, width=2)
            # Baliza roja de aviación pulsante en la antena
            x_ant = x_b + w_b // 2
            d_e.line([(x_ant, y_top), (x_ant, y_top - 28)], fill=(100, 116, 139), width=1)
            pulso_ant = 0.5 + 0.5 * math.sin(t_sec * 6.0 + x_b)
            d_e.ellipse([x_ant - 3, y_top - 31, x_ant + 3, y_top - 25], fill=(239, 68, 68, int(150 + pulso_ant * 105)))

        # Ventanas que parpadean
        for wx, wy, tipo, freq, off in self.ventanas:
            parpadeo = 0.5 + 0.5 * math.sin(t_sec * freq + off)
            if parpadeo > 0.4:
                alpha = int(120 + parpadeo * 125)
                if tipo == "cian":
                    col = (56, 189, 248, alpha)
                elif tipo == "ambar":
                    col = (251, 191, 36, alpha)
                elif tipo == "blanco":
                    col = (241, 245, 249, alpha)
                else:
                    continue
                d_e.rectangle([wx, wy, wx + 8, wy + 10], fill=col)

        base = Image.alpha_composite(base, edif_layer)

        # 4. Tráfico incesante en autopistas en movimiento continuo
        trafico = Image.new("RGBA", (self.ancho, self.alto), (0, 0, 0, 0))
        d_tr = ImageDraw.Draw(trafico)
        for i in range(14):
            y_carril = self.y_horizonte + 40 + i * 22
            sentido = 1 if (i % 2 == 0) else -1
            vel = 340 + (i % 5) * 90
            largo = 140 + (i % 3) * 80
            # Posición continua
            offset = (t_sec * vel * sentido + i * 230) % (self.ancho + 400) - 200
            col_luz = (244, 63, 94) if sentido == 1 else (56, 189, 248)
            d_tr.line([(offset, y_carril), (offset + largo, y_carril)], fill=(*col_luz, 230), width=3)
            d_tr.line([(offset - 6, y_carril), (offset + largo + 6, y_carril)], fill=(*col_luz, 80), width=6)
        trafico = trafico.filter(ImageFilter.GaussianBlur(radius=2))
        base = Image.alpha_composite(base, trafico)

        # 5. Lluvia cinemática diagonal continua
        capa_lluvia = Image.new("RGBA", (self.ancho, self.alto), (0, 0, 0, 0))
        d_ll = ImageDraw.Draw(capa_lluvia)
        dx_viento = 12
        for g in self.lluvia:
            gx = int((g[0] + t_sec * dx_viento * 28) % self.ancho)
            gy = int((g[1] + t_sec * g[2] * 24) % self.alto)
            largo = g[3]
            d_ll.line([(gx, gy), (gx - dx_viento, gy + largo)], fill=(203, 213, 225, 95), width=1)
        base = Image.alpha_composite(base, capa_lluvia)

        return base


class GeneradorViajeEspacialAnimado:
    """Motor de simulación 3D de Starfield / Salto Hiperespacial continuo con partículas cuánticas vivas."""
    def __init__(self, ancho: int = 1080, alto: int = 1920, num_estrellas: int = 340, num_particulas: int = 70):
        self.ancho = ancho
        self.alto = alto
        self.centro_x = ancho // 2
        self.centro_y = int(alto * 0.45)
        self.rng = random.Random(1337)
        # Cada estrella tiene (angulo_rad, velocidad, semilla_fase, color)
        self.estrellas = [
            (
                self.rng.uniform(0, math.pi * 2),
                self.rng.uniform(1.8, 4.2),
                self.rng.uniform(0, 1.0),
                self.rng.choice([(255, 255, 255), (56, 189, 248), (168, 85, 247), (244, 114, 182), (52, 211, 153)])
            )
            for _ in range(num_estrellas)
        ]
        # Partículas de datos cuánticos flotantes (x0, y0, vel_y, freq_x, amp_x, radio, color)
        self.particulas = [
            (
                self.rng.uniform(20, ancho - 20),
                self.rng.uniform(0, alto),
                self.rng.uniform(60, 160),
                self.rng.uniform(1.2, 3.0),
                self.rng.uniform(15, 45),
                self.rng.choice([2, 3, 4]),
                self.rng.choice([(56, 189, 248), (168, 85, 247), (52, 211, 153), (255, 255, 255)])
            )
            for _ in range(num_particulas)
        ]

    def render_frame(self, t_sec: float) -> Image.Image:
        # Base oscura con nebulosa rotatoria suave
        base = Image.new("RGBA", (self.ancho, self.alto), (10, 10, 22, 255))
        
        # 1. Nebulosa viva que ondea y respira en el centro
        nebulosa = Image.new("RGBA", (self.ancho, self.alto), (0, 0, 0, 0))
        d_neb = ImageDraw.Draw(nebulosa)
        rot_ang = t_sec * 0.35
        cx_neb = self.centro_x + int(math.sin(rot_ang) * 60)
        cy_neb = self.centro_y + int(math.cos(rot_ang * 0.8) * 45)
        d_neb.ellipse([cx_neb - 520, cy_neb - 420, cx_neb + 520, cy_neb + 420], fill=(99, 102, 241, 90))
        d_neb.ellipse([cx_neb - 350, cy_neb - 250, cx_neb + 350, cy_neb + 250], fill=(56, 189, 248, 100))
        d_neb.ellipse([cx_neb - 200, cy_neb - 140, cx_neb + 200, cy_neb + 140], fill=(236, 72, 153, 75))
        nebulosa = nebulosa.filter(ImageFilter.GaussianBlur(radius=120))
        base = Image.alpha_composite(base, nebulosa)

        # 2. Capa de rayos estelares en velocidad continua (Warp Stars)
        warp = Image.new("RGBA", (self.ancho, self.alto), (0, 0, 0, 0))
        d_w = ImageDraw.Draw(warp)

        for ang, vel, semilla, col in self.estrellas:
            # La profundidad z avanza continuamente hacia la cámara a ritmo visible
            fase_z = ((semilla + t_sec * vel * 0.45) % 1.0)
            dist_actual = (fase_z ** 1.6) * (self.ancho * 1.1)
            dist_cola = max(0.0, dist_actual - (fase_z * 130.0 + 15.0))

            x_head = int(self.centro_x + math.cos(ang) * dist_actual)
            y_head = int(self.centro_y + math.sin(ang) * dist_actual * 1.25)
            x_tail = int(self.centro_x + math.cos(ang) * dist_cola)
            y_tail = int(self.centro_y + math.sin(ang) * dist_cola * 1.25)

            if 0 <= x_head < self.ancho and 0 <= y_head < self.alto:
                alpha = int(min(255, (fase_z ** 0.6) * 340))
                grosor = max(1, int(fase_z * 4.5))
                d_w.line([(x_tail, y_tail), (x_head, y_head)], fill=(*col, alpha), width=grosor)
                if fase_z > 0.40:
                    r_h = max(1, int(fase_z * 3.5))
                    d_w.ellipse([x_head - r_h, y_head - r_h, x_head + r_h, y_head + r_h], fill=(255, 255, 255, alpha))

        # 3. Cometas / Estrellas fugaces periódicas de alto impacto
        t_cometa = t_sec % 2.5
        if t_cometa < 0.8:
            prog = t_cometa / 0.8
            cx0, cy0 = -100, int(self.alto * 0.20)
            cx1, cy1 = self.ancho + 100, int(self.alto * 0.70)
            cx_act = int(cx0 + (cx1 - cx0) * prog)
            cy_act = int(cy0 + (cy1 - cy0) * prog)
            cola_len = 220
            dx_c = int(math.cos(0.55) * cola_len)
            dy_c = int(math.sin(0.55) * cola_len)
            d_w.line([(cx_act - dx_c, cy_act - dy_c), (cx_act, cy_act)], fill=(56, 189, 248, int(220 * (1.0 - prog * 0.4))), width=3)
            d_w.ellipse([cx_act - 4, cy_act - 4, cx_act + 4, cy_act + 4], fill=(255, 255, 255, 255))

        # 4. Partículas cuánticas de datos flotando continuamente hacia arriba
        for x0, y0, vel_y, freq_x, amp_x, rad, col in self.particulas:
            y_p = int((y0 - t_sec * vel_y) % self.alto)
            x_p = int((x0 + math.sin(t_sec * freq_x + y0) * amp_x) % self.ancho)
            pulso_p = 0.6 + 0.4 * math.sin(t_sec * 3.5 + x0)
            alpha_p = int(180 * pulso_p)
            d_w.ellipse([x_p - rad, y_p - rad, x_p + rad, y_p + rad], fill=(*col, alpha_p))
            # Halo suave
            d_w.ellipse([x_p - rad - 2, y_p - rad - 2, x_p + rad + 2, y_p + rad + 2], outline=(*col, int(alpha_p * 0.4)), width=1)

        base = Image.alpha_composite(base, warp)
        return base


class GeneradorEstudioCreativoAnimado:
    """Motor de simulación de Estudio Creativo con Mesh de Gradiente en movimiento (Violeta/Magenta) y partículas de diseño."""
    def __init__(self, ancho: int = 1080, alto: int = 1920, num_elementos: int = 50):
        self.ancho = ancho
        self.alto = alto
        self.cx = ancho // 2
        self.cy = int(alto * 0.45)
        self.rng = random.Random(2026)
        # Elementos flotantes de diseño: (x0, y0, vel_y, freq_x, amp_x, tipo, tam, color)
        self.elementos = []
        colores_diseno = [
            (139, 92, 246),  # Violeta neón
            (236, 72, 153),  # Magenta creativo
            (56, 189, 248),  # Cian eléctrico
            (251, 191, 36),  # Ámbar chispa
            (244, 114, 182)  # Rosa suave
        ]
        tipos = ["chispa", "cruz", "rombo", "mote"]
        for _ in range(num_elementos):
            x0 = self.rng.randint(20, ancho - 20)
            y0 = self.rng.randint(0, alto)
            vel_y = self.rng.uniform(35.0, 95.0)
            freq_x = self.rng.uniform(1.2, 2.8)
            amp_x = self.rng.uniform(10.0, 26.0)
            tipo = self.rng.choice(tipos)
            tam = self.rng.randint(3, 7)
            col = self.rng.choice(colores_diseno)
            self.elementos.append((x0, y0, vel_y, freq_x, amp_x, tipo, tam, col))

    def render_frame(self, t_sec: float) -> Image.Image:
        base = Image.new("RGBA", (self.ancho, self.alto), (13, 11, 22, 255))
        mesh_layer = Image.new("RGBA", (self.ancho, self.alto), (0, 0, 0, 0))
        d_m = ImageDraw.Draw(mesh_layer)

        # Orbes de gradiente mesh en órbita suave
        ox1 = self.cx + int(140 * math.cos(t_sec * 0.7))
        oy1 = self.cy + int(120 * math.sin(t_sec * 0.6))
        r1 = int(460 + 30 * math.sin(t_sec * 1.5))
        d_m.ellipse([ox1 - r1, oy1 - r1, ox1 + r1, oy1 + r1], fill=(139, 92, 246, 85))

        ox2 = self.cx + int(160 * math.cos(t_sec * 0.5 + 2.5))
        oy2 = self.cy + int(140 * math.sin(t_sec * 0.7 + 1.8))
        r2 = int(420 + 25 * math.cos(t_sec * 1.2))
        d_m.ellipse([ox2 - r2, oy2 - r2, ox2 + r2, oy2 + r2], fill=(236, 72, 153, 70))

        # Acento cian sutil
        ox3 = self.cx + int(100 * math.sin(t_sec * 0.9))
        oy3 = int(self.alto * 0.65) + int(60 * math.cos(t_sec * 0.8))
        r3 = 340
        d_m.ellipse([ox3 - r3, oy3 - r3, ox3 + r3, oy3 + r3], fill=(6, 182, 212, 45))

        mesh_layer = mesh_layer.filter(ImageFilter.GaussianBlur(110))
        base = Image.alpha_composite(base, mesh_layer)

        # Capa de elementos geométricos y chispas flotantes
        vfx = Image.new("RGBA", (self.ancho, self.alto), (0, 0, 0, 0))
        d_v = ImageDraw.Draw(vfx)
        for x0, y0, vel_y, freq_x, amp_x, tipo, tam, col in self.elementos:
            y_act = int((y0 - t_sec * vel_y) % self.alto)
            x_act = int((x0 + math.sin(t_sec * freq_x + y0) * amp_x) % self.ancho)
            pulso = 0.5 + 0.5 * math.sin(t_sec * 4.0 + x0)
            alpha = int(140 * pulso + 60)

            if tipo == "mote":
                d_v.ellipse([x_act - tam, y_act - tam, x_act + tam, y_act + tam], fill=(*col, alpha))
            elif tipo == "cruz":
                d_v.line([(x_act - tam, y_act), (x_act + tam, y_act)], fill=(*col, alpha), width=1)
                d_v.line([(x_act, y_act - tam), (x_act, y_act + tam)], fill=(*col, alpha), width=1)
            elif tipo == "rombo":
                pts = [(x_act, y_act - tam), (x_act + tam, y_act), (x_act, y_act + tam), (x_act - tam, y_act)]
                d_v.polygon(pts, fill=(*col, int(alpha * 0.8)), outline=(*col, alpha))
            else:  # chispa
                d_v.ellipse([x_act - tam, y_act - tam, x_act + tam, y_act + tam], fill=(*col, alpha))
                d_v.ellipse([x_act - tam - 2, y_act - tam - 2, x_act + tam + 2, y_act + tam + 2], outline=(*col, int(alpha * 0.35)), width=1)

        base = Image.alpha_composite(base, vfx)
        return base


# Instancias singleton cacheadas para rendimiento procedural
_instancia_ciudad = None
_instancia_espacio = None
_instancia_creativo = None


def obtener_lienzo_dinamico_fondo(
    estilo: str = "estudio_tech",
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    velocidad_lenta: float = 0.85,
    atenuacion_oscura: float = 0.28
) -> Image.Image:
    """
    Genera un frame de fondo animado en movimiento continuo y fluido.
    Aplica una sutil atenuación para que los mockups y Byte mantengan contraste
    sin matar la sensación de dinamismo vivo.
    """
    global _instancia_ciudad, _instancia_espacio, _instancia_creativo

    t_lento = t_sec * velocidad_lenta

    if "ciudad" in estilo.lower() or "cyber" in estilo.lower():
        if _instancia_ciudad is None or _instancia_ciudad.ancho != ancho or _instancia_ciudad.alto != alto:
            _instancia_ciudad = GeneradorCiudadCyberpunkAnimada(ancho=ancho, alto=alto)
        frame_base = _instancia_ciudad.render_frame(t_lento)
    elif any(k in estilo.lower() for k in ["espac", "space", "warp", "viaje"]):
        if _instancia_espacio is None or _instancia_espacio.ancho != ancho or _instancia_espacio.alto != alto:
            _instancia_espacio = GeneradorViajeEspacialAnimado(ancho=ancho, alto=alto)
        frame_base = _instancia_espacio.render_frame(t_lento)
    elif any(k in estilo.lower() for k in ["creativo", "diseno", "flyer", "canva", "mesh", "neon"]):
        if _instancia_creativo is None or _instancia_creativo.ancho != ancho or _instancia_creativo.alto != alto:
            _instancia_creativo = GeneradorEstudioCreativoAnimado(ancho=ancho, alto=alto)
        frame_base = _instancia_creativo.render_frame(t_lento)
    else:
        # Estudio Tech Minimalista (Gradiente oscuro con sutil respiración)
        frame_base = Image.new("RGBA", (ancho, alto), (11, 14, 25, 255))
        pulso = math.sin(t_lento * 2.0) * 0.5 + 0.5
        r_glow = int(450 + 40 * pulso)
        glow = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
        d_g = ImageDraw.Draw(glow)
        d_g.ellipse([ancho // 2 - r_glow, int(alto * 0.45) - r_glow, ancho // 2 + r_glow, int(alto * 0.45) + r_glow], fill=(30, 41, 59, 90))
        glow = glow.filter(ImageFilter.GaussianBlur(100))
        frame_base = Image.alpha_composite(frame_base, glow)

    # Capa de atenuación para contraste
    if atenuacion_oscura > 0:
        velo = Image.new("RGBA", (ancho, alto), (10, 13, 22, int(255 * atenuacion_oscura)))
        frame_base = Image.alpha_composite(frame_base, velo)

    return frame_base

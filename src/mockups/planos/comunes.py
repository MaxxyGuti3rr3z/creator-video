"""
src.mockups.planos.comunes
---------------------------------------------------------------------------
Iconos vectoriales compartidos por todos los planos.
Codigo movido desde src/mockups/director_escena.py sin cambios de comportamiento.
"""

from typing import Tuple
from PIL import ImageDraw




def dibujar_icono_alerta(draw: ImageDraw.Draw, cx: int, cy: int, tam: int = 14, color: Tuple[int, ...] = (255, 255, 255)):
    """Dibuja un triángulo de advertencia con signo de exclamación vectorial nítido."""
    pts = [
        (cx, cy - tam),
        (cx + tam, cy + tam),
        (cx - tam, cy + tam)
    ]
    draw.polygon(pts, fill=color)
    draw.line([(cx, cy - int(tam * 0.35)), (cx, cy + int(tam * 0.25))], fill=(15, 23, 42), width=max(2, tam // 5))
    draw.ellipse([cx - max(1, tam // 7), cy + int(tam * 0.55) - max(1, tam // 7), cx + max(1, tam // 7), cy + int(tam * 0.55) + max(1, tam // 7)], fill=(15, 23, 42))


def dibujar_icono_cruz(draw: ImageDraw.Draw, cx: int, cy: int, tam: int = 8, color: Tuple[int, ...] = (244, 63, 94), grosor: int = 2):
    """Dibuja una cruz X vectorial nítida."""
    draw.line([(cx - tam, cy - tam), (cx + tam, cy + tam)], fill=color, width=grosor)
    draw.line([(cx - tam, cy + tam), (cx + tam, cy - tam)], fill=color, width=grosor)


def dibujar_icono_candado(draw: ImageDraw.Draw, cx: int, cy: int, tam: int = 14, color: Tuple[int, ...] = (16, 185, 129)):
    """Dibuja un candado de seguridad vectorial nítido."""
    arco_r = int(tam * 0.7)
    draw.arc([cx - arco_r, cy - tam - arco_r // 2, cx + arco_r, cy], start=180, end=0, fill=color, width=max(2, tam // 4))
    draw.rounded_rectangle([cx - tam, cy - int(tam * 0.2), cx + tam, cy + tam], radius=max(2, tam // 4), fill=color)
    draw.ellipse([cx - max(1, tam // 6), cy + int(tam * 0.1), cx + max(1, tam // 6), cy + int(tam * 0.4)], fill=(15, 23, 42))
    draw.line([(cx, cy + int(tam * 0.3)), (cx, cy + int(tam * 0.65))], fill=(15, 23, 42), width=max(2, tam // 5))


def dibujar_icono_lupa(draw: ImageDraw.Draw, cx: int, cy: int, r: int = 12, color: Tuple[int, ...] = (148, 163, 184)):
    """Dibuja una lupa de búsqueda vectorial nítida."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=max(2, r // 4))
    dx = int(r * 0.65)
    dy = int(r * 0.65)
    largo = int(r * 0.8)
    draw.line([(cx + dx, cy + dy), (cx + dx + largo, cy + dy + largo)], fill=color, width=max(3, r // 3))

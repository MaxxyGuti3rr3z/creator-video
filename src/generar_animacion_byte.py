r"""
generar_animacion_byte.py
-------------------------
Genera las capas de video transparentes animadas de Byte para cada una de las 4 escenas:
- Poses dinámicas multiexpresión sincronizadas con los momentos clave de la narración.
- Micro-saltos (hops) y rebotes orgánicos en las palabras de mayor impacto.
- Micro-reacciones VFX (gotas de estrés, chispas cyan IA, aura zen giratoria, flechas animadas).
- Respiración y balanceo (tilt) sutil para dar vida constante al personaje.
- Exporta en formato QuickTime RLE (RGBA 32-bit) 680x680 a 30fps para overlay nativo en FFmpeg.
"""

import math
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Union
from PIL import Image, ImageDraw, ImageFilter, ImageOps

try:
    from src.rutas import DIR_BYTE_TRANSPARENTES as DIR_TRANS, DIR_VFX, DIR_ANIMACIONES_BYTE
    DIR_OUT = DIR_ANIMACIONES_BYTE
except ImportError:
    from rutas import DIR_BYTE_TRANSPARENTES as DIR_TRANS, DIR_VFX, DIR_ANIMACIONES_BYTE
    DIR_OUT = DIR_ANIMACIONES_BYTE
DIR_OUT.mkdir(parents=True, exist_ok=True)


def _rotar_centrado(img: Image.Image, angulo_grados: float) -> Image.Image:
    """Rota una imagen con transparencia alrededor de su centro sin recortar bordes."""
    if abs(angulo_grados) < 0.1:
        return img
    return img.rotate(angulo_grados, resample=Image.Resampling.BILINEAR, expand=False)


def _escalar_centrado(img: Image.Image, factor: float) -> Tuple[Image.Image, int, int]:
    """Escala una imagen por un factor y retorna (img_escalada, offset_x, offset_y)."""
    if abs(factor - 1.0) < 0.005:
        return img, 0, 0
    w, h = img.size
    nw = max(1, int(w * factor))
    nh = max(1, int(h * factor))
    scaled = img.resize((nw, nh), resample=Image.Resampling.BILINEAR)
    off_x = (w - nw) // 2
    off_y = (h - nh) // 2
    return scaled, off_x, off_y


def generar_video_byte_escena(
    indice_escena: int,
    duracion: float,
    ruta_salida: Optional[Path] = None,
    fps: int = 30,
    sprite_path: Optional[Union[str, Path]] = None
) -> Path:
    """
    Genera un clip de video MOV con canal alfa de Byte animado para la escena indicada.
    Si se provee sprite_path, anima dinámicamente ese sprite con respiración, parpadeo y balanceo.
    """
    if ruta_salida is None:
        ruta_salida = DIR_OUT / f"byte_escena_{indice_escena}_animado.mov"
    ruta_salida = Path(ruta_salida).resolve()
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    ancho, alto = 680, 680
    total_frames = max(1, int(duracion * fps))

    # Cargar sprites de Byte según la escena o parámetro provisto
    if sprite_path and Path(sprite_path).exists():
        sprite_a = Image.open(sprite_path).convert("RGBA")
        sprite_b = sprite_a
        vfx = None
        t_split = 999.0
    elif indice_escena == 0:
        # Hook: estresado inicial -> enojado tecleando
        sprite_a = Image.open(DIR_TRANS / "hook_estresado_transparente.png").convert("RGBA")
        sprite_b = Image.open(DIR_TRANS / "hook_transparente.png").convert("RGBA")
        vfx = Image.open(DIR_VFX / "vfx_estres.png").convert("RGBA") if (DIR_VFX / "vfx_estres.png").exists() else None
        t_split = 2.04
    elif indice_escena == 1:
        # Punto 1 (Shortwave): ojos de estrella asombro -> tecleando feliz en la compu
        sprite_a = Image.open(DIR_TRANS / "punto1_transparente.png").convert("RGBA")
        sprite_b = Image.open(DIR_TRANS / "punto1_feliz_transparente.png").convert("RGBA")
        vfx = Image.open(DIR_VFX / "vfx_chispas_ia.png").convert("RGBA") if (DIR_VFX / "vfx_chispas_ia.png").exists() else None
        t_split = 6.80
    elif indice_escena == 2:
        # Punto 2 (SaneBox): señalando serio analítico -> meditando zen en paz
        sprite_a = Image.open(DIR_TRANS / "cierre_transparente.png").convert("RGBA")
        sprite_b = Image.open(DIR_TRANS / "punto2_transparente.png").convert("RGBA")
        vfx = Image.open(DIR_VFX / "vfx_zen_aura.png").convert("RGBA") if (DIR_VFX / "vfx_zen_aura.png").exists() else None
        t_split = 7.10
    else:
        # Cierre: saltando feliz con confeti
        sprite_a = Image.open(DIR_TRANS / "cierre_saltando_transparente.png").convert("RGBA")
        sprite_b = sprite_a
        vfx = Image.open(DIR_VFX / "vfx_flechas_abajo.png").convert("RGBA") if (DIR_VFX / "vfx_flechas_abajo.png").exists() else None
        t_split = 999.0

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{ancho}x{alto}",
        "-pix_fmt", "rgba",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "qtrle",
        "-t", f"{duracion:.3f}",
        str(ruta_salida)
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        for f_idx in range(total_frames):
            t = f_idx / float(fps)
            canvas = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))

            # 1. Determinación de sprite activo con transición suave
            crossfade_dur = 0.12  # ~4 frames
            if t < (t_split - crossfade_dur / 2):
                active_sprite = sprite_a
                active_alpha = 1.0
                secondary_sprite = None
            elif t < (t_split + crossfade_dur / 2):
                # Crossfade
                p_trans = (t - (t_split - crossfade_dur / 2)) / crossfade_dur
                active_sprite = sprite_b
                active_alpha = p_trans
                secondary_sprite = sprite_a
                sec_alpha = 1.0 - p_trans
            else:
                active_sprite = sprite_b
                active_alpha = 1.0
                secondary_sprite = None

            # 2. Movimiento: Idle Breathing, Tilt y Micro-hops
            y_jump = 0.0
            tilt_deg = 0.0
            breath_scale = 1.0

            if indice_escena == 0:
                # Respiración leve
                breath_scale = 1.0 + 0.015 * math.sin(2 * math.pi * t / 1.5)
                tilt_deg = 1.2 * math.sin(2 * math.pi * t / 1.1)
                # Salto elástico en t=2.04 ("repetitivos")
                if 2.04 <= t < 2.38:
                    p_hop = (t - 2.04) / 0.34
                    y_jump = -28.0 * math.sin(math.pi * p_hop)

            elif indice_escena == 1:
                breath_scale = 1.0 + 0.018 * math.sin(2 * math.pi * t / 1.6)
                tilt_deg = 1.0 * math.sin(2 * math.pi * t / 1.2)
                # Salto de entrada de marca en t=0.40 a 0.75 ("Shortwave")
                if 0.40 <= t < 0.75:
                    p_hop = (t - 0.40) / 0.35
                    y_jump = -30.0 * math.sin(math.pi * p_hop)
                # Pequeño rebote en t=6.80 al cambiar de pose
                elif 6.80 <= t < 7.12:
                    p_hop = (t - 6.80) / 0.32
                    y_jump = -18.0 * math.sin(math.pi * p_hop)

            elif indice_escena == 2:
                # Pose 1 (analítica)
                if t < t_split:
                    breath_scale = 1.0 + 0.015 * math.sin(2 * math.pi * t / 1.5)
                    tilt_deg = 0.8 * math.sin(2 * math.pi * t / 1.2)
                    if 0.40 <= t < 0.75:
                        p_hop = (t - 0.40) / 0.35
                        y_jump = -24.0 * math.sin(math.pi * p_hop)
                else:
                    # Pose zen: flotación más amplia y calmada, sin tilt
                    breath_scale = 1.0 + 0.025 * math.sin(2 * math.pi * t / 2.0)
                    tilt_deg = 0.0
                    y_jump = -8.0 * math.sin(2 * math.pi * (t - t_split) / 1.8)

            else:
                # Cierre: saltos continuos de alegría
                breath_scale = 1.0 + 0.02 * math.sin(2 * math.pi * t / 0.9)
                tilt_deg = 1.8 * math.sin(2 * math.pi * t * 1.5)
                # Rebote rítmico continuo
                y_jump = -26.0 * abs(math.sin(2 * math.pi * t * 1.6))

            # 3. Componer VFX de Fondo si corresponde (ej. Aura Zen en Escena 2)
            if vfx is not None and indice_escena == 2 and t >= t_split:
                ang_zen = (t - t_split) * 45.0  # rota suavemente
                vfx_rot = _rotar_centrado(vfx, ang_zen)
                vfx_sc, vx_off, vy_off = _escalar_centrado(vfx_rot, 1.1 + 0.08 * math.sin(2 * math.pi * t / 1.8))
                canvas.paste(vfx_sc, (100 + vx_off, 110 + vy_off + int(y_jump)), vfx_sc)

            # 4. Renderizar Sprite de Byte (con tilt, respiración, parpadeo procedural y squash/stretch)
            def _preparar_sprite(sp: Image.Image, alpha_mul: float) -> Image.Image:
                sp_mod = sp.copy()
                if abs(tilt_deg) > 0.1:
                    sp_mod = _rotar_centrado(sp_mod, tilt_deg)

                # Micro-parpadeo/squash orgánico cada ~3.0 segundos
                t_blink = t % 3.0
                blink_squash_y = 1.0
                blink_stretch_x = 1.0
                if t_blink < 0.12:
                    p_bl = math.sin(math.pi * (t_blink / 0.12))
                    blink_squash_y = 1.0 - 0.09 * p_bl
                    blink_stretch_x = 1.0 + 0.05 * p_bl

                final_sc_x = breath_scale * blink_stretch_x
                final_sc_y = breath_scale * blink_squash_y

                if abs(final_sc_x - 1.0) > 0.005 or abs(final_sc_y - 1.0) > 0.005:
                    w, h = sp_mod.size
                    nw = max(1, int(w * final_sc_x))
                    nh = max(1, int(h * final_sc_y))
                    sp_mod = sp_mod.resize((nw, nh), resample=Image.Resampling.BILINEAR)

                if alpha_mul < 0.98:
                    r, g, b, a = sp_mod.split()
                    a = a.point(lambda p: int(p * alpha_mul))
                    sp_mod = Image.merge("RGBA", (r, g, b, a))
                return sp_mod

            # Rebote sutil de sorpresa al cambiar de emoción
            if abs(t - t_split) < 0.22:
                p_tr = (t - (t_split - 0.22)) / 0.44
                y_jump += -14.0 * math.sin(math.pi * p_tr)

            if secondary_sprite is not None:
                sec_prepared = _preparar_sprite(secondary_sprite, sec_alpha)
                pos_sec_x = (ancho - sec_prepared.width) // 2
                pos_sec_y = (alto - sec_prepared.height) // 2 + int(y_jump)
                canvas.paste(sec_prepared, (pos_sec_x, pos_sec_y), sec_prepared)

            act_prepared = _preparar_sprite(active_sprite, active_alpha)
            pos_act_x = (ancho - act_prepared.width) // 2
            pos_act_y = (alto - act_prepared.height) // 2 + int(y_jump)
            canvas.paste(act_prepared, (pos_act_x, pos_act_y), act_prepared)

            # 5. Componer VFX Frontales (sobre la cabeza / orejas de Byte)
            if vfx is not None and indice_escena == 0 and t < t_split:
                # Gotas de estrés / alerta sobre la cabeza
                vfx_est_y = 15 + int(6.0 * math.sin(2 * math.pi * t / 0.8)) + int(y_jump)
                vfx_sc = vfx.resize((140, 140), Image.Resampling.BILINEAR)
                canvas.paste(vfx_sc, (380, vfx_est_y), vfx_sc)

            elif vfx is not None and indice_escena == 1 and (0.35 <= t < 2.80):
                # Chispas IA ✨ girando y pulsando en la oreja
                t_ia = t - 0.35
                p_ia = min(1.0, t_ia / 0.3) if t_ia < 0.3 else max(0.0, 1.0 - (t_ia - 2.0) / 0.45) if t_ia > 2.0 else 1.0
                ang_ia = t_ia * 180.0
                vfx_rot = _rotar_centrado(vfx, ang_ia)
                sc_factor = (0.9 + 0.25 * math.sin(2 * math.pi * t / 0.6)) * p_ia
                vfx_sc, vx_off, vy_off = _escalar_centrado(vfx_rot, sc_factor)
                vfx_x = 75 + vx_off
                vfx_y = 25 + vy_off + int(y_jump)
                canvas.paste(vfx_sc, (vfx_x, vfx_y), vfx_sc)

            elif vfx is not None and indice_escena == 3:
                # Flechitas animadas hacia abajo rebotando rítmicamente
                y_arr = 10 + int(12.0 * abs(math.sin(2 * math.pi * t * 2.0)))
                vfx_sc = vfx.resize((180, 140), Image.Resampling.BILINEAR)
                canvas.paste(vfx_sc, (250, y_arr), vfx_sc)

            # Enviar frame RGBA directamente a FFmpeg stdin
            proc.stdin.write(canvas.tobytes())

        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        raise e

    return ruta_salida


if __name__ == "__main__":
    for i in range(4):
        dur = 5.0 if i in (0, 3) else 12.0
        p = DIR_OUT / f"byte_escena_{i}_animado.mov"
        print(f"Generando Byte animado para escena {i} ({dur:.1f}s)...")
        generar_video_byte_escena(i, dur, p)
    print("Todas las animaciones de Byte generadas con éxito!")

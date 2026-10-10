"""
demo_ejecucion.py
-----------------
Ejemplo de extremo a extremo que recrea la estructura exacta solicitada por el usuario:
- 4 imágenes: hook.png, punto1.png, punto2.png, cierre.png
- 1 archivo de audio: narracion.mp3
- 1 JSON de alineación con segmentos y alignment carácter por carácter
- Invocación de las 3 funciones requeridas:
    1. ruta_ass = generar_ass(alignment, segmentos)
    2. ruta_mp4 = ensamblar_video(imagenes, audio, archivo_ass, duracion_total)
    3. es_valido = validar_output(ruta_mp4, duracion_esperada)
"""

import json
import os
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.shorts_assembler import generar_ass, ensamblar_video, validar_output


def crear_imagen(ruta: Path, titulo: str, subtitulo: str, bg_color: tuple, accent: tuple = (0, 229, 255)):
    """Genera una imagen 1080x1920 con estilo visual moderno para Shorts."""
    img = Image.new("RGB", (1080, 1920), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Tarjeta de diseño central
    draw.rounded_rectangle([70, 360, 1010, 1260], radius=40, fill=(18, 22, 32), outline=accent, width=5)
    draw.rectangle([70, 360, 1010, 380], fill=accent)

    # Detalles visuales
    draw.ellipse([880, 410, 950, 480], fill=accent)
    draw.line([120, 1180, 960, 1180], fill=(60, 70, 90), width=2)

    # Textos
    draw.text((120, 430), "BYTE AUTOMATION STUDIO", fill=accent)
    draw.text((120, 560), titulo, fill=(255, 255, 255))
    draw.text((120, 780), subtitulo, fill=(190, 200, 220))
    draw.text((120, 1080), "9:16 Vertical Video (1080x1920) • 30 FPS", fill=(120, 135, 160))

    ruta.parent.mkdir(parents=True, exist_ok=True)
    img.save(ruta)
    print(f" Imagen creada: {ruta.name}")


def generar_audio_silencioso_o_tono(ruta: Path, duracion_seg: float):
    """Genera un archivo MP3 de duración exacta con FFmpeg."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency=523.25:beep_factor=2:sample_rate=44100:duration={duracion_seg}",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        str(ruta)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f" Audio generado: {ruta.name} ({duracion_seg:.1f}s)")


def generar_alignment_completo(segmentos: list) -> dict:
    """Genera caracteres y timestamps carácter por carácter acordes a los rangos de cada segmento."""
    chars = []
    starts = []
    ends = []

    for seg in segmentos:
        texto = seg["texto"]
        t_ini = seg["inicio"]
        t_fin = seg["fin"]
        n = len(texto)
        if n == 0:
            continue
        dt = (t_fin - t_ini) / n

        for i, ch in enumerate(texto):
            s = t_ini + i * dt
            e = s + dt
            chars.append(ch)
            starts.append(round(s, 3))
            ends.append(round(e, 3))

    return {
        "characters": chars,
        "character_start_times_seconds": starts,
        "character_end_times_seconds": ends
    }


def main():
    print("=" * 65)
    print("DEMOSTRACIÓN DE ENSAMBLADO DE VIDEO VERTICAL (SHORTS)")
    print("=" * 65)

    base_dir = DIR_RAIZ / "pruebas" / "demo_assets"
    base_dir.mkdir(parents=True, exist_ok=True)

    # 1. Crear las 4 imágenes requeridas
    img_hook = base_dir / "hook.png"
    img_punto1 = base_dir / "punto1.png"
    img_punto2 = base_dir / "punto2.png"
    img_cierre = base_dir / "cierre.png"

    crear_imagen(img_hook, "¡ESTE TRUCO DE PYTHON\nCAMBIARÁ TUS SHORTS!", "Hook inicial de alto impacto", (15, 23, 42))
    crear_imagen(img_punto1, "SUBTÍTULOS KARAOKE\n100% DINÁMICOS", "Paso 1: Generación precisa con tags \\k", (20, 32, 48))
    crear_imagen(img_punto2, "TRANSICIONES SUAVES\nY KEN BURNS CINEMATOGRÁFICO", "Paso 2: FFmpeg xfade + zoompan sutil", (16, 26, 40))
    crear_imagen(img_cierre, "GUARDA ESTE VIDEO\nY AUTOMATIZA HOY", "Cierre y llamado a la acción", (12, 20, 32))

    imagenes = [img_hook, img_punto1, img_punto2, img_cierre]

    # 2. Configurar JSON de alineación
    # Para la demo rápida usamos 16 segundos totales (4.0s por segmento)
    duracion_total = 16.0
    segmentos = [
        {"texto": "Este truco de Python cambiará tus videos.", "inicio": 0.0, "fin": 4.0, "tipo": "hook"},
        {"texto": "Genera subtítulos karaoke dinámicos en segundos.", "inicio": 4.0, "fin": 8.0, "tipo": "punto_1"},
        {"texto": "Aplica transiciones crossfade con Ken Burns sutil.", "inicio": 8.0, "fin": 12.0, "tipo": "punto_2"},
        {"texto": "Suscríbete y automatiza tu contenido hoy.", "inicio": 12.0, "fin": 16.0, "tipo": "cierre"}
    ]

    alignment = generar_alignment_completo(segmentos)

    json_data = {
        "duracion_total_seg": duracion_total,
        "segmentos": segmentos,
        "alignment": alignment
    }

    json_path = base_dir / "alineacion.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f" JSON de alineación guardado en: {json_path}")

    # 3. Crear audio de narración
    audio_path = base_dir / "narracion.mp3"
    generar_audio_silencioso_o_tono(audio_path, duracion_seg=duracion_total)

    # -------------------------------------------------------------
    # TAREA 1: Generar subtítulos estilo karaoke (.ass)
    # -------------------------------------------------------------
    print("\n[TAREA 1] Generando subtítulos karaoke .ass...")
    ruta_ass = generar_ass(
        alignment=alignment,
        segmentos=segmentos,
        ruta_salida=base_dir / "subtitulos.ass",
        max_words_per_chunk=4
    )
    print(f"-> Archivo ASS generado: {ruta_ass}")

    # -------------------------------------------------------------
    # TAREA 2: Ensamblar video con FFmpeg
    # -------------------------------------------------------------
    print("\n[TAREA 2] Ensamblando video vertical con FFmpeg...")
    ruta_mp4 = ensamblar_video(
        imagenes=imagenes,
        audio=audio_path,
        archivo_ass=ruta_ass,
        duracion_total=duracion_total,
        segmentos=segmentos,
        ruta_salida=base_dir / "short_output.mp4",
        fade_duration=0.3
    )
    print(f"-> Video MP4 final generado: {ruta_mp4}")

    # -------------------------------------------------------------
    # TAREA 3: Validación del output
    # -------------------------------------------------------------
    print("\n[TAREA 3] Validando video final con ffprobe...")
    es_valido = validar_output(ruta_mp4, duracion_esperada=duracion_total, tolerancia=0.1)
    print(f"-> Resultado de validación: {'ÉXITO (Válido)' if es_valido else 'FALLO'}")

    print("\n" + "=" * 65)
    print("RESUMEN DE EJECUCIÓN:")
    print(f"  • Video:      {ruta_mp4}")
    print(f"  • Subtítulos: {ruta_ass}")
    print(f"  • Duración:   {duracion_total}s")
    print(f"  • Válido:     {es_valido}")
    print("=" * 65)


if __name__ == "__main__":
    main()

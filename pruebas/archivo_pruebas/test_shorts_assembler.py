"""
test_shorts_assembler.py
------------------------
Pruebas automatizadas y demostración para shorts_assembler.py.
Crea assets sintéticos de prueba, ejecuta el ensamblado completo y valida las tres tareas.
"""

import json
import os
from pathlib import Path
import subprocess
import unittest
from PIL import Image, ImageDraw, ImageFont

from shorts_assembler import (
    generar_ass,
    ensamblar_video,
    validar_output,
    procesar_short,
    _agrupar_caracteres_en_palabras,
    _dividir_en_chunks
)


def crear_imagen_short(ruta: Path, texto: str, bg_color: tuple, accent_color: tuple = (0, 229, 255)):
    """Crea una imagen de 1080x1920 con diseño moderno para el short."""
    img = Image.new("RGB", (1080, 1920), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Dibujar tarjeta central y acentos de diseño
    draw.rounded_rectangle([80, 400, 1000, 1200], radius=40, fill=(20, 24, 33), outline=accent_color, width=6)
    draw.rectangle([80, 400, 1000, 420], fill=accent_color)

    # Decoración geométrica sutil
    draw.ellipse([880, 440, 960, 520], fill=accent_color)
    draw.line([140, 1140, 940, 1140], fill=(70, 80, 100), width=3)

    # Texto
    draw.text((140, 500), "BYTE CONTENT CREATOR", fill=accent_color)
    draw.text((140, 650), texto, fill=(255, 255, 255))
    draw.text((140, 850), "1080 x 1920 • 9:16 Vertical Video", fill=(180, 190, 205))

    ruta.parent.mkdir(parents=True, exist_ok=True)
    img.save(ruta)


def crear_audio_demo(ruta: Path, duracion_seg: float = 12.0):
    """Crea un archivo MP3 con tono sintetizado de duración exacta usando FFmpeg."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency=440:beep_factor=4:sample_rate=44100:duration={duracion_seg}",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        str(ruta)
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def construir_alignment_sintetico(segmentos: list) -> dict:
    """Construye un alignment de caracteres realista a partir de una lista de segmentos."""
    all_chars = []
    all_starts = []
    all_ends = []

    for seg in segmentos:
        texto = seg["texto"]
        t_ini = seg["inicio"]
        t_fin = seg["fin"]
        total_chars = len(texto)
        if total_chars == 0:
            continue

        char_dur = (t_fin - t_ini) / total_chars

        for i, char in enumerate(texto):
            c_start = t_ini + (i * char_dur)
            c_end = c_start + char_dur
            all_chars.append(char)
            all_starts.append(round(c_start, 3))
            all_ends.append(round(c_end, 3))

    return {
        "characters": all_chars,
        "character_start_times_seconds": all_starts,
        "character_end_times_seconds": all_ends
    }


class TestShortsAssembler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workdir = Path("test_artifacts")
        cls.workdir.mkdir(exist_ok=True)

        # 1. Crear las 4 imágenes requeridas
        cls.img_hook = cls.workdir / "hook.png"
        cls.img_p1 = cls.workdir / "punto1.png"
        cls.img_p2 = cls.workdir / "punto2.png"
        cls.img_cierre = cls.workdir / "cierre.png"

        crear_imagen_short(cls.img_hook, "HOOK: El Secreto De Python", (15, 23, 42))
        crear_imagen_short(cls.img_p1, "PUNTO 1: Automatización Total", (20, 30, 50))
        crear_imagen_short(cls.img_p2, "PUNTO 2: Rendimiento Nativo", (18, 28, 45))
        crear_imagen_short(cls.img_cierre, "CIERRE: Síguenos Para Más Tips", (10, 18, 35))

        cls.imagenes = [cls.img_hook, cls.img_p1, cls.img_p2, cls.img_cierre]

        # 2. Segmentos y duraciones de prueba
        cls.duracion_total = 12.0
        cls.segmentos = [
            {"texto": "Esto cambiará cómo editas videos para siempre.", "inicio": 0.0, "fin": 3.0, "tipo": "hook"},
            {"texto": "Primero ensamblas subtítulos estilo karaoke dinámicos.", "inicio": 3.0, "fin": 6.5, "tipo": "punto_1"},
            {"texto": "Luego aplicas transiciones y efectos con FFmpeg.", "inicio": 6.5, "fin": 9.5, "tipo": "punto_2"},
            {"texto": "Guarda este video y pruébalo hoy.", "inicio": 9.5, "fin": 12.0, "tipo": "cierre"}
        ]

        cls.alignment = construir_alignment_sintetico(cls.segmentos)

        # 3. Audio de prueba
        cls.audio_path = cls.workdir / "narracion.mp3"
        crear_audio_demo(cls.audio_path, duracion_seg=cls.duracion_total)

    def test_01_agrupar_palabras(self):
        """Verifica que el agrupamiento de caracteres en palabras calcule inicio y fin correctos."""
        words = _agrupar_caracteres_en_palabras(self.alignment)
        self.assertGreater(len(words), 10)

        # Todas las palabras deben tener texto no vacío y start < end
        for w in words:
            self.assertTrue(len(w.text) > 0)
            self.assertGreaterEqual(w.end, w.start)

        # Chunks de máximo 4-5 palabras
        chunks = _dividir_en_chunks(words, self.segmentos, max_words_per_chunk=4)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 4)

    def test_02_generar_ass(self):
        """Verifica la generación del archivo .ass de subtítulos estilo karaoke."""
        ass_path = self.workdir / "subtitulos_test.ass"
        resultado_ruta = generar_ass(
            alignment=self.alignment,
            segmentos=self.segmentos,
            ruta_salida=ass_path,
            max_words_per_chunk=4
        )

        self.assertTrue(os.path.exists(resultado_ruta))

        with open(resultado_ruta, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Verificar encabezados y estilo
        self.assertIn("[Script Info]", contenido)
        self.assertIn("PlayResX: 1080", contenido)
        self.assertIn("PlayResY: 1920", contenido)
        self.assertIn("&H00FFE500", contenido)  # Cian Byte #00E5FF
        self.assertIn("&H00FFFFFF", contenido)  # Blanco base
        self.assertIn("Style: KaraokeByte,Arial", contenido)

        # Verificar tags de karaoke \k
        self.assertIn(r"{\k", contenido)
        self.assertIn("Dialogue: 0,", contenido)

    def test_03_ensamblar_y_validar(self):
        """Verifica el ensamblado completo del MP4 y la validación con ffprobe."""
        ass_path = self.workdir / "subtitulos_test.ass"
        out_mp4 = self.workdir / "short_test.mp4"

        # Tarea 2: Ensamblar video
        ruta_mp4 = ensamblar_video(
            imagenes=self.imagenes,
            audio=self.audio_path,
            archivo_ass=ass_path,
            duracion_total=self.duracion_total,
            segmentos=self.segmentos,
            ruta_salida=out_mp4,
            fade_duration=0.3
        )

        self.assertTrue(os.path.exists(ruta_mp4))

        # Tarea 3: Validar video
        valido = validar_output(ruta_mp4, duracion_esperada=self.duracion_total, tolerancia=0.1)
        self.assertTrue(valido)


if __name__ == "__main__":
    unittest.main()

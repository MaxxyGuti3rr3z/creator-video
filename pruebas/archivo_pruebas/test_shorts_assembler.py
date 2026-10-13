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
import sys
import unittest
from PIL import Image, ImageDraw, ImageFont

DIR_RAIZ = Path(__file__).resolve().parent.parent.parent
if str(DIR_RAIZ / "src") not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ / "src"))

from shorts_assembler import (
    generar_ass,
    ensamblar_video,
    validar_output,
    _agrupar_caracteres_en_palabras,
    _dividir_en_chunks,
    TRANSICIONES_XFADE,
    transicion_para_escena,
    _semilla_transiciones,
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

        # Máximo max_words_per_chunk en segmentos de demo; en segmentos de
        # frase completa (hook/problema/cierre) el bloque llega hasta 6 palabras
        # y se parte en 2 líneas con \N (regla de AGENTS.md)
        SEGMENTOS_FRASE_COMPLETA = (
            "cold_open", "hook", "problema", "escena_problema", "panico", "cierre", "pregunta"
        )
        chunks = _dividir_en_chunks(words, self.segmentos, max_words_per_chunk=4)
        self.assertGreater(len(chunks), 0)
        for chunk in chunks:
            inicio = chunk[0].start
            seg = next((s for s in self.segmentos if s["inicio"] <= inicio < s["fin"]), None)
            tipo = str(seg.get("tipo", "")).lower() if seg else ""
            limite = 6 if any(k in tipo for k in SEGMENTOS_FRASE_COMPLETA) else 4
            self.assertLessEqual(len(chunk), limite)

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
        self.assertIn("&H0000F5FF", contenido)  # Amarillo puro #FFF500 (AGENTS.md)
        self.assertIn("&H00FFFFFF", contenido)  # Blanco base
        self.assertIn("Style: KaraokeByte,Arial", contenido)

        # Verificar tags de karaoke \k con duración en centésimas
        self.assertRegex(contenido, r"\\k\d+")
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


class TestTransicionesRotativas(unittest.TestCase):
    def test_catalogo_sin_repeticion_al_envolver(self):
        n = len(TRANSICIONES_XFADE)
        self.assertGreaterEqual(n, 4)
        for idx, nombre in enumerate(TRANSICIONES_XFADE):
            self.assertNotEqual(nombre, TRANSICIONES_XFADE[(idx + 1) % n])

    def test_rotacion_determinista_y_variada(self):
        seq = [transicion_para_escena(i, "", 7) for i in range(12)]
        self.assertEqual(seq, [transicion_para_escena(i, "", 7) for i in range(12)])
        self.assertGreaterEqual(len(set(seq)), 4)
        for a, b in zip(seq, seq[1:]):
            self.assertNotEqual(a, b)

    def test_pin_narrativo_por_tipo(self):
        self.assertEqual(transicion_para_escena(3, "problema", 0), "circleclose")
        self.assertEqual(transicion_para_escena(3, "escena_problema", 0), "circleclose")
        self.assertEqual(transicion_para_escena(3, "panico", 0), "circleclose")
        self.assertEqual(transicion_para_escena(3, "resultado", 0), "circleopen")

    def test_catalogo_sin_fundes_a_negro_o_blanco(self):
        self.assertNotIn("fadeblack", TRANSICIONES_XFADE)
        self.assertNotIn("fadewhite", TRANSICIONES_XFADE)

    def test_anti_repeticion_con_pin_narrativo(self):
        t1 = transicion_para_escena(1, "resultado", 0)
        t2 = transicion_para_escena(2, "resultado", 0, anterior=t1)
        self.assertNotEqual(t1, t2)
        self.assertIn(t2, TRANSICIONES_XFADE)

    def test_semilla_determinista_por_ruta(self):
        self.assertEqual(_semilla_transiciones("video_12_ciberseguridad.mp4"), 12)
        self.assertEqual(_semilla_transiciones("video_14_agua_ia.mp4"), 14)
        self.assertEqual(_semilla_transiciones("short_test.mp4"), 0)


if __name__ == "__main__":
    unittest.main()

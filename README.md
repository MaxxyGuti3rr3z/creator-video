# Pipeline de Video Vertical - Byte el Zorrito (Shorts / Reels / TikTok)

Pipeline automatizado para la creación de videos verticales de alta retención en formato **9:16 (1080x1920)** a **30 FPS** con narración procedural, sincronización karaoke palabra por palabra, mockups dinámicos con paleta emocional y animación del personaje Byte.

---

## 🧰 Requisitos

- **Python 3.13** (probado con 3.13.0).
- **FFmpeg / FFprobe 9.x en el PATH** (binario externo, no se instala por pip): <https://ffmpeg.org/download.html>
- Dependencias de Python:

```bash
python -m pip install -r requirements.txt
```

> `onnxruntime` va explícito en `requirements.txt` porque `rembg` no lo declara como
> dependencia dura: sin él falla `import rembg` y no funciona `shorts_assembler.quitar_fondo()`.

---

## 📁 Estructura del Proyecto

```text
proyecto/
├─ .env                                 # Variables de entorno y API keys (ElevenLabs)
├─ README.md, AGENTS.md, REPORTE_REORGANIZACION.md   # Documentación y normas de desarrollo
├─ requirements.txt                      # Dependencias de Python (ver sección Requisitos)
├─ .agents/                              # Reglas de agentes y prompts del proyecto
│  ├─ rules/puntuacion_guiones.md
│  ├─ rules/arquitectura_visual_variada.md
│  └─ skills/director_visual_byte/
├─ src/                                 # Motor principal del pipeline
│  ├─ rutas.py                          # Gestor centralizado de rutas y directorios
│  ├─ shorts_assembler.py               # Generación ASS karaoke, ensamble FFmpeg y aceleración
│  ├─ generar_animacion_byte.py         # Motor de animación de Byte (clips MOV RGBA)
│  ├─ generar_paisaje_sonoro.py         # Síntesis procedural SFX, BGM Synthwave y masterización
│  ├─ validar_guion.py                  # Validador estricto de guiones (sin puntos, claims)
│  └─ mockups/                          # Motor de interfaces interactivas por temática
│     ├─ motor.py                       # Render unificado, paletas emocionales y pipe FFmpeg
│     ├─ director_escena.py             # Arquetipos visuales y planos por video
│     ├─ estilos/                       # Fondos dinámicos, temas y emociones de Byte
│     └─ plantillas/                    # 16 plantillas de frame (reunión, tareas, correo…)
├─ assets/                              # Recursos gráficos y sonoros estables
│  ├─ byte/
│  │  ├─ transparentes/                 # Sprites PNG con canal alfa
│  │  └─ ilustraciones_originales/      # Arte maestro en alta definición
│  ├─ audio/                            # Efectos de sonido en WAV (whoosh, click, chime, etc.)
│  ├─ fondos/                           # Fondos estáticos pre-renderizados
│  └─ vfx/                              # Efectos visuales de impacto (chispas, estrés, aura zen)
├─ guiones/                             # Catálogo centralizado de guiones maestros
│  ├─ guion_02_reuniones.json
│  └─ guion_03_tareas.json
├─ videos/                              # Espacios de trabajo aislados por proyecto
│  └─ video_XX_nombre/
│     ├─ entrada/                       # Irreemplazable: guion JSON, narracion.mp3, alignment.json
│     ├─ intermedios/                   # Regenerable: fondos, subtitulos.ass, tiempos.txt, audio master
│     └─ final/                         # Entregable: video_guion_XX.mp4 (acelerado 1.12x)
├─ pruebas/                             # Entorno de tests, demos y capturas de staging
│  ├─ prueba_end_to_end.py              # Orquestador del pipeline completo
│  ├─ demo_ejecucion.py                 # Demostración sintética autónoma
│  └─ archivo_pruebas/                  # Tests unitarios
├─ cache/                               # Caché de audio determinista de ElevenLabs
│  └─ cache_audio/                      # *.mp3, *_alignment.json, cache_audio_index.json
```

---

## 🚀 Uso del Módulo de Rutas (`src/rutas.py`)

Para evitar rutas escritas a mano (hardcodeadas) en cualquier script nuevo o refactorizado, importar siempre las constantes y resolutores:

```python
from src.rutas import (
    DIR_RAIZ,
    DIR_SRC,
    DIR_ASSETS,
    DIR_BYTE_TRANSPARENTES,
    DIR_CACHE,
    ruta_video,
    ruta_guion,
    ruta_sprite_byte
)

# Obtener carpetas estructuradas de un video:
v_paths = ruta_video("video_03_tareas")
dir_entrada = v_paths["entrada"]          # videos/video_03_tareas/entrada/
dir_intermedios = v_paths["intermedios"]  # videos/video_03_tareas/intermedios/
dir_final = v_paths["final"]              # videos/video_03_tareas/final/
```

---

## 💻 Ejecución del Pipeline Completo

Para compilar un video completo desde su guion:

> ⚠️ **`prueba_end_to_end.py` no tiene flag `--offline`.** Si el texto no está en la caché de
> `cache/cache_audio/`, consume créditos de ElevenLabs. Ver `REPORTE_REORGANIZACION.md` §3 antes
> de ejecutarlo. Para pruebas sin costo usá `demo_ejecucion.py` o los `test_previews_video_XX.py`.

```bash
# Ejecutar con un guion específico (usa la API de ElevenLabs)
python pruebas/prueba_end_to_end.py guiones/guion_03_tareas.json

# O ejecutando la demo sintética sin costo de API
python pruebas/demo_ejecucion.py
```

---

## 🧪 Pruebas Unitarias

Para correr las pruebas de ensamble:

```bash
python pruebas/archivo_pruebas/test_shorts_assembler.py
```

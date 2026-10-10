# Pipeline de Video Vertical - Byte el Zorrito (Shorts / Reels / TikTok)

Pipeline automatizado para la creación de videos verticales de alta retención en formato **9:16 (1080x1920)** a **30 FPS** con narración procedural, sincronización karaoke palabra por palabra, mockups dinámicos con paleta emocional y animación del personaje Byte.

---

## 📁 Estructura del Proyecto

```text
proyecto/
├─ .env                                 # Variables de entorno y API keys (ElevenLabs)
├─ README.md, AGENTS.md, AUDITORIA.md   # Documentación y normas de desarrollo
├─ .agents/                             # Reglas de agentes y prompts del proyecto
│  └─ rules/puntuacion_guiones.md
├─ src/                                 # Motor principal del pipeline
│  ├─ rutas.py                          # Gestor centralizado de rutas y directorios
│  ├─ shorts_assembler.py               # Generación ASS karaoke, ensamble FFmpeg y aceleración
│  ├─ generar_animacion_byte.py         # Motor de animación de Byte (clips MOV RGBA)
│  ├─ generar_paisaje_sonoro.py         # Síntesis procedural SFX, BGM Synthwave y masterización
│  └─ mockups/                          # Generadores de interfaces interactivas por temática
│     ├─ generar_mockup_tareas.py       # Gestor de tareas / Lista Andes (con paletas emocionales)
│     ├─ generar_mockup_reunion.py      # Videollamadas / Sala Andes
│     └─ generar_animacion_solucion.py  # Bandeja de correo / Shortwave
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
│  ├─ archivo_pruebas/                  # Tests unitarios
│  └─ test_shortwave_frames/            # Frames de prueba de interfaz
├─ cache/                               # Caché de audio determinista de ElevenLabs
│  └─ cache_audio/                      # *.mp3, *_alignment.json, cache_audio_index.json
└─ _archivo/                            # Cuarentena: duplicados, huérfanos y temporales históricos
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

```bash
# Ejecutar con un guion específico
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

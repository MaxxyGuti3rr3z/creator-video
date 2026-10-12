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
│  ├─ rules/reglas_produccion_video.md    # Reglas técnicas COMPLETAS (safe zones, ASS, escenas)
│  ├─ rules/puntuacion_guiones.md
│  ├─ rules/arquitectura_visual_variada.md
│  └─ skills/director_visual_byte/
├─ src/                                 # Motor principal del pipeline
│  ├─ rutas.py                          # Gestor centralizado de rutas y directorios
│  ├─ registro_videos.py                # Catálogo central: carpetas, fondos y sprites por video
│  ├─ chequeos_pipeline.py              # PRE-VUELO / PASO 5 / POST-VUELO (validaciones)
│  ├─ validar_guion.py                  # Validador estricto de guiones (sin puntos, claims)
│  ├─ shorts_assembler.py               # Generación ASS karaoke, ensamble FFmpeg y aceleración
│  ├─ generar_animacion_byte.py         # Motor de animación de Byte (clips MOV RGBA)
│  ├─ generar_paisaje_sonoro.py         # Síntesis procedural SFX, BGM Synthwave y masterización
│  ├─ bloques_narrativos.py             # Bloques narrativos y texto de narración (extraído del orquestador)
│  ├─ audio_elevenlabs.py               # Caché SHA-256, API ElevenLabs y fallback (extraído)
│  ├─ segmentacion.py                   # Segmentos visuales y frames de preview (extraído)
│  └─ mockups/                          # Motor de interfaces interactivas por temática
│     ├─ motor.py                       # Render unificado, paletas emocionales y pipe FFmpeg
│     ├─ director_escena.py             # Orquestador de planos por video
│     ├─ planos/                        # Arquetipos visuales y planos (split de director_escena)
│     ├─ estilos/                       # Fondos dinámicos, temas y emociones de Byte
│     └─ plantillas/                    # Plantillas de frame (reunión, tareas, correo…)
├─ assets/                              # Recursos gráficos y sonoros estables
│  ├─ byte/
│  │  ├─ transparentes/                 # Sprites PNG con canal alfa
│  │  └─ ilustraciones_originales/      # Arte maestro en alta definición
│  ├─ audio/                            # Efectos de sonido en WAV (whoosh, click, chime, etc.)
│  ├─ fondos/                           # Fondos estáticos pre-renderizados
│  └─ vfx/                              # Efectos visuales de impacto (chispas, estrés, aura zen)
├─ guiones/                             # Catálogo centralizado de guiones maestros (13: 02-14)
├─ videos/                              # Espacios de trabajo aislados por proyecto
│  └─ video_XX_nombre/
│     ├─ entrada/                       # Irreemplazable: guion JSON, narracion.mp3, alignment.json
│     ├─ intermedios/                   # Regenerable: fondos, subtitulos.ass, tiempos.txt, audio master
│     └─ final/                         # Entregable: video_guion_XX.mp4 (acelerado 1.12x)
├─ pruebas/                             # Tests, demos y linters de calidad
│  ├─ prueba_end_to_end.py              # Orquestador del pipeline completo
│  ├─ demo_ejecucion.py                 # Demostración sintética autónoma (sin API)
│  ├─ lint_zonas_seguras.py             # Linter: safe zones TikTok/Reels sobre el MP4 final
│  ├─ lint_obsoleto.py                  # Linter: artefactos vencidos (fondos/sprites/final)
│  ├─ lint_subtitulos.py                # Linter: estilo y chunks del .ass karaoke
│  ├─ lint_anti_template.py             # Linter: rotación anti-template entre videos consecutivos
│  ├─ test_lint_*.py, test_chequeos_pipeline.py   # Suites de los linters (99 tests)
│  ├─ test_pipeline_modulos.py           # Módulos extraídos del monolito (19 tests)
│  └─ archivo_pruebas/                  # Tests unitarios del ensamblador
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
python pruebas/prueba_end_to_end.py guiones/guion_14_agua_ia.json

# O ejecutando la demo sintética sin costo de API
python pruebas/demo_ejecucion.py
```

### Flags del pipeline

| Flag | Efecto |
|---|---|
| `--forzar-fondos` | Regenera los MP4 de fondo aunque existan en caché (tras editar planos/configs) |
| `--saltar-validacion` | Salta el PRE-VUELO (validar_guion + lint_obsoleto) y el chequeo ASS del PASO 5 |
| `--sin-chequeo-final` | Salta el POST-VUELO (lint_zonas_seguras sobre el MP4 final) |

---

## 🛡️ Calidad y Validaciones

Cinco chequeos automáticos, todos de solo lectura y calibrados con 0 falsos positivos sobre el catálogo real:

| Etapa | Chequeo | Ejecución | Escape |
|---|---|---|---|
| **PRE-VUELO** (antes de gastar créditos) | `validar_guion` (sin puntos en narración) + `lint_obsoleto` (caché de fondos/sprites vencida) | automático en `prueba_end_to_end.py` | `--saltar-validacion` |
| **PASO 5** (tras `generar_ass`, antes de ensamblar) | `lint_subtitulos` (estilo 46px, amarillo, chunks y `\N` correctos) | automático | `--saltar-validacion` |
| **POST-VUELO** (tras el render) | `lint_zonas_seguras` (contenido en zonas prohibidas del MP4 final) | automático | `--sin-chequeo-final` |
| **Antes de crear un video nuevo** | `lint_anti_template` (estructura, sprite o cierre repetido con el video vecino) | manual | — |
| **Antes de publicar / re-renderizar** | `lint_obsoleto` (catálogo completo) | manual | — |

```bash
# Lint manual de safe zones sobre un video final (acepta la carpeta o el MP4)
python pruebas/lint_zonas_seguras.py videos/video_14_agua_ia/final

# Artefactos obsoletos (fondos, sprites, MP4 final)
python pruebas/lint_obsoleto.py

# Subtítulos ASS (acepta la carpeta, archivos .ass o directorios)
python pruebas/lint_subtitulos.py videos/video_14_agua_ia/intermedios

# Rotación anti-template de un guion nuevo contra sus vecinos
python pruebas/lint_anti_template.py guiones/guion_15_nuevo.json
```

> Los FAIL históricos del catálogo (videos 02-13) son violaciones legítimas previas a las
> reglas: no se "arreglan" re-renderizando videos ya publicados.

---

## 🧪 Pruebas Unitarias

```bash
# Suites de validación (99 tests)
python pruebas/test_lint_zonas.py
python pruebas/test_lint_obsoleto.py
python pruebas/test_lint_subtitulos.py
python pruebas/test_lint_anti_template.py
python pruebas/test_chequeos_pipeline.py

# Catálogo de videos (6 tests)
python pruebas/test_registro_videos.py

# Partición del monolito: módulos src/ + orquestador (19 tests)
python pruebas/test_pipeline_modulos.py

# Ensamble de video (3 tests; ~2.5 min, genera artefactos)
python pruebas/archivo_pruebas/test_shorts_assembler.py
```

**Total: 127 tests en 8 suites**, todos en verde. Además, `python pruebas/test_smoke_planos.py`
es un smoke test visual que renderiza los 49 planos y un clip cinematográfico (RC=0 = OK).

---

## 📈 Estado del Proyecto

- **14 videos** producidos (catálogo de 13 guiones maestros, `guiones/guion_02..14`).
- **127 tests** automatizados en 8 suites (+ 1 smoke test visual), todos en verde.
- **5 linters** de calidad cableados al pipeline; validación previa sin gastar créditos.
- **8.5 / 10** — la nota la bajan dos cosas concretas:

| Pendiente | Impacto |
|---|---|
| CI automático (hoy es repo local sin remoto) | Las suites se corren a mano |
| Unificar las suites de previews (`test_previews_video_XX.py`) bajo un runner único | Experiencia de desarrollo |

---

## 📄 Documentación Relacionada

- **`AGENTS.md`** — normas del proyecto para agentes (safe zones, sprites, emojis PIL, linters obligatorios).
- **`.agents/rules/reglas_produccion_video.md`** — reglas técnicas completas de producción.
- **`REPORTE_REORGANIZACION.md`** — historia y balance de la reorganización del código.

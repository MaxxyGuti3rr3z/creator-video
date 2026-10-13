# Pipeline de Video Vertical - Byte el Zorrito (Shorts / Reels / TikTok)

[![CI](https://github.com/MaxxyGuti3rr3z/creator-video/actions/workflows/ci.yml/badge.svg)](https://github.com/MaxxyGuti3rr3z/creator-video/actions/workflows/ci.yml)

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
├─ .githooks/pre-push, .gitattributes    # CI local: hook pre-push y LF forzado en hooks
├─ .github/workflows/ci.yml             # CI en la nube: ci_local en cada push/PR a main
├─ src/                                 # Motor principal del pipeline
│  ├─ rutas.py                          # Gestor centralizado de rutas y directorios
│  ├─ registro_videos.py                # Catálogo central: carpetas, fondos y sprites por video
│  ├─ chequeos_pipeline.py              # PRE-VUELO / PASO 5 / POST-VUELO (validaciones)
│  ├─ validar_guion.py                  # Validador estricto de guiones (sin puntos, claims)
│  ├─ shorts_assembler.py               # Generación ASS karaoke, ensamble FFmpeg y aceleración
│  ├─ generar_animacion_byte.py         # Motor de animación de Byte (clips MOV RGBA)
│  ├─ generar_paisaje_sonoro.py         # Síntesis procedural SFX, BGM Synthwave y masterización
│  ├─ eventos_voz.py                    # Sync UI ↔ locución (t_ui, t_pildora)
│  ├─ bloques_narrativos.py             # Bloques narrativos y texto de narración
│  ├─ audio_elevenlabs.py               # Caché SHA-256, API ElevenLabs y fallback
│  ├─ segmentacion.py                   # Segmentos visuales y frames de preview
│  └─ mockups/                          # Motor de interfaces interactivas por temática
│     ├─ motor.py                       # Render unificado, paletas emocionales y pipe FFmpeg
│     ├─ director_escena.py             # Orquestador de planos por video (fachada)
│     ├─ motion.py                      # Utilidades de movimiento (ease, pop, typing)
│     ├─ planos/                        # Arquetipos visuales y planos por video
│     │  ├─ router.py                   # MAPA_ARQUETIPOS + renderizar_escena_por_arquetipo
│     │  ├─ arquetipos.py               # Planos base (hero caos, showcase, split, deck, host)
│     │  ├─ wrappers.py                 # CONFIGS_* y wrappers por video
│     │  ├─ comunes.py                  # Iconos vectoriales compartidos
│     │  ├─ video_07_excel.py … video_15_celular.py   # Planos específicos por video
│     │  └─ pestañas_navegador.py
│     ├─ estilos/                       # Fondos dinámicos, temas y emociones de Byte
│     │  ├─ fondos.py                   # Catálogo estático (aurora, spotlight, studio, espacio)
│     │  ├─ animaciones_fondo.py        # Fondos animados (ciudad, espacio, creativo)
│     │  ├─ temas.py                    # Temas de ventana (light, dark, glass, cyber neon)
│     │  └─ byte_emociones.py           # Catálogo de emociones/VFX de Byte
│     └─ plantillas/                    # Plantillas de frame (reunión, tareas, correo…)
├─ assets/                              # Recursos gráficos y sonoros estables
│  ├─ byte/
│  │  ├─ transparentes/                 # Sprites PNG con canal alfa
│  │  └─ ilustraciones_originales/      # Arte maestro en alta definición
│  ├─ audio/                            # Efectos de sonido en WAV (whoosh, click, chime, etc.)
│  ├─ fondos/                           # Fondos estáticos pre-renderizados
│  └─ vfx/                              # Efectos visuales de impacto (chispas, estrés, aura zen)
├─ guiones/                             # Catálogo centralizado de guiones maestros
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
│  ├─ ci_local.py                       # CI local: todas las suites con resumen + hook pre-push
│  ├─ previews.py                       # Runner único de previews (PNG de diagnóstico)
│  └─ archivo_pruebas/                  # Tests unitarios del ensamblador
├─ cache/                               # Caché de audio determinista de ElevenLabs
│  └─ cache_audio/                      # *.mp3, *_alignment.json, cache_audio_index.json
```

---

## 🚀 Uso del Módulo de Rutas (`src/rutas.py`)

Para evitar rutas escritas a mano (hardcodeadas) en cualquier script nuevo o refactorizado, importar siempre las constantes y resolutores:

```python
from src.rutas import (
    DIR_RAIZ, DIR_SRC, DIR_ASSETS, DIR_BYTE_TRANSPARENTES, DIR_CACHE,
    DIR_GUIONES, DIR_VIDEOS, DIR_AUDIO, DIR_FONDOS, DIR_VFX,
    ruta_video, ruta_guion, ruta_sprite_byte, ruta_sfx, ruta_vfx,
    normalizar_id_video,
)

# Carpetas estructuradas de un video:
v_paths = ruta_video("video_15_ia_celular")
dir_entrada = v_paths["entrada"]          # videos/video_15_ia_celular/entrada/
dir_intermedios = v_paths["intermedios"]  # videos/video_15_ia_celular/intermedios/
dir_final = v_paths["final"]              # videos/video_15_ia_celular/final/

# Normalizar identificador: "15" → "video_15"; "video_15_ia_celular" → "video_15"
```

---

## 💻 Ejecución del Pipeline Completo

Para compilar un video completo desde su guion:

> ⚠️ **`prueba_end_to_end.py` no tiene flag `--offline`.** Si el texto no está en la caché de
> `cache/cache_audio/`, consume créditos de ElevenLabs. Ver `REPORTE_REORGANIZACION.md` §3 antes
> de ejecutarlo. Para pruebas sin costo usá `demo_ejecucion.py` o `python pruebas/previews.py 15`.

```bash
# Ejecutar con un guion específico (usa la API de ElevenLabs)
python pruebas/prueba_end_to_end.py guiones/guion_15_ia_celular.json

# O ejecutando la demo sintética sin costo de API
python pruebas/demo_ejecucion.py
```

### Flags del pipeline

| Flag | Efecto |
|---|---|
| `--forzar-fondos` | Regenera los MP4 de fondo aunque existan en caché (tras editar planos/configs) |
| `--saltar-validacion` | Salta el PRE-VUELO (validar_guion + lint_obsoleto) y el chequeo ASS del PASO 5 |
| `--sin-chequeo-final` | Salta el POST-VUELO (lint_zonas_seguras sobre el MP4 final) |
| `--sin-enfasis` | Desactiva el punch-in de énfasis (zoom breve sobre bg+mockup en el arranque de palabra; activo por defecto en videos NO cinemáticos) |
| `--variantes-gancho=N` | Renderiza N variantes VISUALES del gancho (clip 0) con el mismo audio/ASS (0 créditos); la de producción va a `final/`, las demás a `intermedios/variantes/` |

### Pipeline paso a paso (interno)

1. **PRE-VUELO** — `validar_guion` + `lint_obsoleto` (fondos/sprites vencidos bloquean).
2. **PASO 1** — `construir_bloques_narrativos` + `concatenar_texto_completo` → texto único.
3. **PASO 2** — `audio_elevenlabs.generar_audio_con_timestamps_elevenlabs` (caché SHA-256 → API o copia desde disco) → `narracion.mp3` + `alignment.json`.
4. **PASO 3** — `generar_paisaje_sonoro.mezclar_paisaje_sonoro_completo` → `audio_master.wav` (voz + BGM duckeada + SFX).
5. **PASO 4** — `generar_fondos_del_video` (MP4 por escena con eventos de voz) + sprites Byte + ASS karaoke.
6. **PASO 5** — `chequear_ass` (lint_subtitulos) → `ensamblar_video` → `validar_output` → `acelerar_video(1.12x)`.
7. **POST-VUELO** — `lint_zonas_seguras` sobre el MP4 final (55 frames muestreados).

---

## 🎬 Especificaciones de Edición y Animación

### Transiciones xfade (entre escenas)

Catálogo `TRANSICIONES_XFADE` en `src/shorts_assembler.py`. Solo tipos de **revelado/mezcla** (cada píxel de salida toma el valor de A o B en su misma posición — nada sale de las safe zones):

| Tipo | Efecto |
|---|---|
| `fade` | Fundido cruzado lineal (mezcla A↔B). |
| `wiperight` | Barrido de derecha a izquierda (borde de corte recto). |
| `wipeleft` | Barrido de izquierda a derecha. |
| `wipedown` | Barrido de arriba hacia abajo. |
| `circleclose` | Iris que se cierra hacia el centro (enfoque dramático). |
| `circleopen` | Iris que se abre desde el centro (revelado). |

**Prohibidos**: `slide*`, `smooth*`, `zoomin` (desplazan píxeles fuera de safe zones durante el corte) y `fadeblack`/`fadewhite` (fundes a negro/blanco que restan foco al contenido — decisión del editor 2026-10-13).

**Pin narrativo** (`TRANSICIONES_POR_TIPO`) — la escena que llega pinnea la transición:

| Tipo de escena | Transición | Razón narrativa |
|---|---|---|
| `problema` / `escena_problema` / `panico` | `circleclose` | Cierre iris = tensión dramática. |
| `resultado` | `circleopen` | Apertura iris = revelación de la solución. |

**Rotación anti-template**: `transicion_para_escena(i, tipo, semilla, anterior)` elige la transición de cada corte con (1) pin narrativo → (2) rotación sembrada por el número de video (`_semilla_transiciones` extrae los dígitos del nombre de salida) → (3) guardia anti-repetición (nunca dos cortes seguidos iguales). `fade_duration` por defecto: **0.15 s**.

### Grado cinematográfico (post-procesado)

Constantes en `shorts_assembler.py`, aplicadas en el filter graph final ANTES del burn-in de subtítulos:

| Constante | Valor | Efecto |
|---|---|---|
| `GRADO_VIGNETTE` | `PI/6` | Viñeta suave en los bordes (encuadre cinematográfico). |
| `GRADO_EQ` | `contrast=1.06:saturation=1.10` | Contraste y saturación leves. |
| `GRADO_NOISE` | `alls=4:allf=t` | Grano fino temporal (textura de película). |

### Movimiento de cámara y fondos

- **Fondo con paneo/zoom**: cada escena usa `zoompan` sobre un fondo texturado sobredimensionado (1280×2276) con degradado, blobs cyan/coral y patrón de circuito. El hook usa zoom-in; escenas estáticas y cierre usan paneo lento alternado.
- **Fondos dinámicos animados** (`src/mockups/estilos/animaciones_fondo.py`): `obtener_lienzo_dinamico_fondo(estilo, ancho, alto, t_sec, velocidad_lenta, atenuacion_oscura)` genera por frame:
  - `ciudad_cyberpunk` / `ciudad_nocturna` — lluvia diagonal, tráfico de haces, neones titilantes, searchlights, niebla.
  - `viaje_espacial` — starfield 3D con estelas + nebulosa (detectar por `"espac"` o `"viaje"`, NO por `"espacio"`).
  - `estudio_creativo` / `estudio_tech` — mesh gradient violeta/magenta + partículas geométricas (fallback: gradiente oscuro con glow que respira).
  - Velocidad por defecto: **0.85×**; atenuación oscura calibrada para contraste de mockups/Byte.

### Animación de Byte (`src/generar_animacion_byte.py`)

`generar_video_byte_escena(indice_escena, duracion, ruta_salida, fps=30, sprite_path=None)` genera un clip **MOV RGBA 680×680 @30fps** (`qtrle`) por escena. Motion disponible:

| Motion | Descripción | Parámetros |
|---|---|---|
| Respiración | Escala senoidal sutil del sprite completo. | ±1.5–2.5 % |
| Tilt / balanceo | Rotación senoidal alrededor del centro. | 0.8–1.8° |
| Micro-hops | Pequeños saltos senoidales sincronizados a palabras clave del alignment. | — |
| Squash/stretch de parpadeo | Aplanamiento vertical + ensanche horizontal periódico. | Y −9 % / X +5 %, cada ~3 s |
| Crossfade de poses | Transición suave entre sprites de emociones. | 0.12 s |
| Rebote de entrada | Curva elástica BackEaseOut al cambiar de emoción/escena. | 0.35 s, c1=1.70158 |
| VFX por escena | Gotas de estrés, chispas IA rotatorias, aura zen giratoria, flechas. | `byte_emociones.dibujar_micro_vfx` |

Píxeles RGBA → `ffmpeg -f rawvideo -pix_fmt rgba -c:v qtrle` por stdin.

### Emociones de Byte (`src/mockups/estilos/byte_emociones.py`)

`CATALOGO_SPRITES` (estados predefinidos):

| Clave | Sprite / estado |
|---|---|
| `estresado` | Byte agotado con gotas de estrés. |
| `enojado_laptop` | Byte frustrado en la laptop. |
| `ojos_estrella` | Byte maravillado (ojos de estrella). |
| `pacifico_zen` | Byte en calma con aura zen. |
| `saltando_feliz` | Byte celebrando. |
| `serio_analitico` | Byte concentrado / señalando. |

`SECUENCIAS_PREDETERMINADAS` por tipo de escena:

| Escena | Secuencia |
|---|---|
| `escena_problema` | estresado → enojado_laptop |
| `punto_1` | serio_analitico → ojos_estrella |
| `punto_2` | enojado_laptop → ojos_estrella |
| `resultado` | pacifico_zen |
| `cierre` | saltando_feliz |

`resolver_sprite_momento(tipo_escena, tiempo_segundos, secuencia_custom)` devuelve `(img, tipo_vfx, factor_rebote)`; `dibujar_micro_vfx(canvas, tipo_vfx, progreso_t)` pinta `gotas_estres`, `chispas_ia`, `aura_zen` o `confeti`.

### Paletas emocionales de mockups (`src/mockups/motor.py`)

`PALETAS_EMOCIONALES` asocia cada tipo de escena a un esquema de color completo (top, bot, blob, cuadrícula, partícula, chip):

| Escena | Tono | Color dominante |
|---|---|---|
| `escena_problema` | Caos / Tensión | Rojo |
| `punto_1` | Estructura / Orden | Cyan |
| `punto_2` | Automatización IA | Índigo |
| `resultado` | Alivio | Verde |
| `cierre` | Interacción | Ámbar |

### Temas de ventana (`src/mockups/estilos/temas.py`)

`obtener_tema(nombre_o_alias)` → `TemaMockup(ventana, header, sello, cards, accent)`:

| Tema | Estilo |
|---|---|
| `TEMA_LIGHT_SLATE` | Claro, slate gris (default). |
| `TEMA_DARK_OBSIDIAN` | Oscuro, obsidiana. |
| `TEMA_GLASS` | Cristal esmerilado (glassmorphism). |
| `TEMA_CYBER_NEON` | Neón cyberpunk. |

Regla de marca: 3 puntos gris neutro `#94A3B8` en la ventana + sello "Simulación ilustrativa".

### Síntesis de audio procedural (`src/generar_paisaje_sonoro.py`)

**SFX** (100 % generados, sin samples externos; `generar_sfx_*(ruta_wav, sample_rate=44100)`):

| SFX | Duración | Uso |
|---|---|---|
| `whoosh` | 0.35 s | Transiciones entre escenas. |
| `click` | 0.08 s | Clics de UI en demos. |
| `slide` (swish) | 0.45 s | Deslizamientos / cambios de escena. |
| `chime` | 1.2 s | Acorde mayor estilo "Inbox Zero" (resultado). |
| `bounce` | 0.22 s | Entrada de Byte. |
| `riser` | 0.85 s | Anticipación antes del payoff. |
| `impact` | 0.5 s | Payoff (sub + golpe seco). |

**BGM**: `generar_musica_fondo_tech(ruta_wav, duracion_total=35.0)` — Synthwave/Lo-Fi **112 BPM**, progresión Cm9→Abmaj7→Fm7→Bbadd9, pads detune + bajo + batería analógica + arpegio, fade in 0.4 s / out 1.2 s.

**Masterización**: `mezclar_paisaje_sonoro_completo(ruta_voz, salida_wav, duracion_total, segmentos, dir_audio)`:
- Voz normalizada a **0.90** centrada en estéreo.
- BGM con **sidechain ducking** adaptativo (gain 0.085 con voz ≈ −21 dB / 0.22 en pausas).
- SFX inyectados según `_planificar_sfx(segmentos)` (whoosh+bounce por corte, click/slide en demos, riser+impact en payoff).
- **Master limiter** `tanh` a 0.95; WAV estéreo 16-bit 44.1 kHz.

### Sincronización voz ↔ UI (`src/eventos_voz.py`)

Para que los mockups reaccionen al momento exacto de la locución:

- `construir_eventos_escena(seg, alignment, pildora=None, ui_clave=None)` → `{"t_ui", "t_pildora", "t_enfasis"}`.
- `t_ui`: instante del **pop del elemento UI hero** (primer keyword de `ui_clave`, matching difuso contra el alignment carácter a carácter).
- `t_pildora`: inicio del **typing de la píldora clave** de la escena.
- `t_enfasis`: tupla con los tiempos locales de **todas** las ocurrencias de cada keyword de `ui_clave` (puntos candidatos a punch-in; vacía si no hay keywords).
- Fallback: si no hay sync (`None`), se usa `fraccion_fallback=0.30` de la duración del segmento.

### Subtítulos karaoke ASS (`generar_ass` en `shorts_assembler.py`)

- Estilo único `KaraokeByte`: **Arial 46px**, amarillo `#FFF500` (`&H0000F5FF`) con borde negro, `Alignment 2`, `MarginL/R: 80`, `MarginV: 860`.
- Chunks de **4–6 palabras** (clave) o **≤4** (demo) con `\N` obligatorio desde 3 palabras; máximo **2–3 palabras por sublínea**.
- Timing por `\k` (centésimas), suma de `\k` == duración del diálogo, sin solapes.
- Pop `\t` sincronizado por palabra + palabras clave en blanco.
- PlayRes: **1080×1920**.

### Safe zones móviles (TikTok / Reels / Shorts)

Canvas 1080×1920. El linter `lint_zonas_seguras` detecta contenido brillante (media RGB >110) en zonas prohibidas:

| Franja | Y | Regla |
|---|---|---|
| Zona muerta superior | 0..240 | Vacía (batería, hora, LIVE, pestañas, buscador). Mockups arrancan en **y=250**. |
| UI / Mockups | 250..780 | Ancho máx. 880–900px centrado (x:100..980). |
| Píldora flotante | 790..870 | **Una sola** píldora 28–32px. |
| Subtítulos karaoke | 960..1080 | `#FFF500` borde negro, 46px. |
| Zona sagrada de Byte | 1120..1650 | Prohibido banners en y:1200..1850; base de Byte ≤1650. |

Márgenes laterales en franja y=250..900: x≥70 y x≤1011.

### Punch-in de énfasis (`src/enfasis.py`)

Zoom breve (~0.20 s) sobre la capa de **fondo+mockup** en el arranque de una palabra clave, sincronizado con el cambio a blanco del subtítulo. Solo capa bg: **Byte y subtítulos quedan intactos** (se overlay-ean después).

- Curva: `Z(t) = 1 + amplitud·sin(π·u^0.6)` con `u∈[0,1]` (subida rápida con ease-out y retorno suave; exactamente 1.0 en los bordes de la ventana).
- Rango **Z∈[1.0, 1.035]** (siempre ≥1; `crop` exige entrada ≥1080×1920 y `zoompan` con z<1 revela bordes negros). Alternancia: punch fuerte 3.5% / suave 2%.
- Ancla **(540, 250)**: el contenido se aleja del ancla, de modo que el mockup (y≥252) jamás sube fuera de y≥250 ni roza x<70/x>1011 (verificado: x=100→84.6, x=980→995.4, y=252→252.07).
- **Excluido en videos cinemáticos** (Byte horneado en el bg; ningún ancla admite 3–4% sin escalarlo fuera de safe zones). El linter `lint_zonas_seguras` es el árbitro final (el test de integración de `test_enfasis.py` lo valida en PASS a fps completa).
- `zoompan` no admite `t`; la expresión usa `on` (frame de salida) a 30fps.

### Director del gancho (`src/director_gancho.py`)

Variantes **visuales** A/B/C del primer segmento (clip 0) con el **mismo audio y ASS** (0 créditos ElevenLabs). Cada variante cambia solo el tratamiento del clip 0 dentro de `ensamblar_video`:

| Arquetipo | Tratamiento del clip 0 |
|---|---|
| `texto_pantalla` (A, control) | Comportamiento histórico: paneo suave + Byte desde abajo. |
| `byte_reacciona` (B) | Punch de impacto en el fondo (z 1.00→1.04→1.00) + Byte con escala de choque (1.25→1.0). |
| `mockup_inmediato` (C) | Zoom-in lento del fondo (1.00→1.03) que empuja al mockup; Byte entra lateral. |

- Rotación determinista por semilla (número de video), sin `random` de Python. `ConfigVideo.gancho_preferido` fija el arquetipo en A.
- Si el clip 0 tiene variante con zoom, el punch-in de énfasis se omite ahí (evita multiplicar zooms y violar safe zones).
- `--variantes-gancho=N` renderiza N variantes; la de producción va a `final/`, las demás a `intermedios/variantes/`. El linter `lint_gancho.py` audita el gancho del guion (sin puntos, longitud ≤18/20 palabras, sin métricas inventadas, rotación anti-template).

### Registro de experimentos (`src/registro_experimentos.py`)

CSV append-only rastreado por git en `datos/experimentos.csv`. Cada variante renderizada (tras el POST-VUELO) agrega una fila con: `fecha_utc`, `video`, `variante_id`, `arquetipo_gancho`, `punch_enfasis`, `ruta_mp4`, `notas`. Deja trazable qué se produjo y con qué tratamiento, para comparar variantes después.

### Arquetipos visuales anti-template (`.agents/rules/arquitectura_visual_variada.md`)

Prohibido repetir composición en 2 videos consecutivos. Rotar entre:

| # | Arquetipo | Zona | Ejemplo |
|---|---|---|---|
| 1 | Smartphone Native POV | x:140..940, y:250..850 | `video_15_celular.py`, `PLANO_SMARTPHONE_INSTAGRAM_FEED` |
| 2 | Hero Byte Center-Stage | y:400..1200 | `PLANO_HERO_CAOS` |
| 3 | Split Before/After o Batalla VS | pantalla dividida | `renderizar_plano_split_before_after`, `PLANO_BATTLE_VS` |
| 4 | Bento Grid Modular | y:250..820 | `video_10_cotizacion.py`, `video_13_noticias.py` |
| 5 | Panoramic Pro Workspace | y:250..850 | `PLANO_SHOWCASE_PANORAMICO`, `pestanias_navegador.py` |

Rotación obligatoria de sprites (`byte_agotado` nunca 2 veces seguidas). Biblioteca: `Imagen_byte_frente`, `byte_sentado_frente_feliz`, `byte_perfil`, `byte_ojos_estrella`, `byte_señalando_serio`, `byte_saltando_feliz`, `byte_paz`, `cierre_transparente`.

### Aceleración final

`acelerar_video(entrada, factor=1.12)` — `setpts` + `atempo` (pitch preservado), libx264/AAC. Objetivo: 22–30 s finales, ~200–250 PPM (palabras por minuto efectivas).

---

## 🛡️ Calidad y Validaciones

Cinco chequeos automáticos, todos de solo lectura y calibrados con 0 falsos positivos sobre el catálogo real:

| Etapa | Chequeo | Ejecución | Escape |
|---|---|---|---|
| **PRE-VUELO** (antes de gastar créditos) | `validar_guion` (sin puntos en narración) + `lint_obsoleto` (caché de fondos/sprites vencida) | automático en `prueba_end_to_end.py` | `--saltar-validacion` |
| **PASO 5** (tras `generar_ass`, antes de ensamblar) | `lint_subtitulos` (estilo 46px, amarillo, chunks y `\N` correctos) | automático | `--saltar-validacion` |
| **POST-VUELO** (tras el render) | `lint_zonas_seguras` (contenido en zonas prohibidas del MP4 final) | automático | `--sin-chequeo-final` |
| **Antes de crear un video nuevo** | `lint_anti_template` (estructura, sprite o cierre repetido con el video vecino) | manual | — |
| **Antes de crear/editar el gancho** | `lint_gancho` (sin puntos, ≤18/20 palabras, sin métricas inventadas, rotación de arquetipo) | manual | — |
| **Antes de publicar / re-renderizar** | `lint_obsoleto` (catálogo completo) | manual | — |

```bash
# Lint manual de safe zones sobre un video final (acepta la carpeta o el MP4)
python pruebas/lint_zonas_seguras.py videos/video_15_ia_celular/final

# Artefactos obsoletos (fondos, sprites, MP4 final)
python pruebas/lint_obsoleto.py

# Subtítulos ASS (acepta la carpeta, archivos .ass o directorios)
python pruebas/lint_subtitulos.py videos/video_15_ia_celular/intermedios

# Rotación anti-template de un guion nuevo contra sus vecinos
python pruebas/lint_anti_template.py guiones/guion_16_nuevo.json

# Linter del gancho (catálogo completo o un guion concreto)
python pruebas/lint_gancho.py
python pruebas/lint_gancho.py guiones/guion_16_nuevo.json
```

> Los FAIL históricos del catálogo (videos 02-13) son violaciones legítimas previas a las
> reglas: no se "arreglan" re-renderizando videos ya publicados.

### Validación de guiones (`src/validar_guion.py`)

`validar_guion(ruta_guion)` → `{"valido", "errores", "advertencias", "detalles"}`. Valida:

1. Ningún término `no_afirmar` ni lista fija de prohibidos (`gratis`, `free`, `sin costo`, `precio`, `plan`, `usd`, `$`, `reemplaza al humano`…) en la narración.
2. **Cero puntos `.`** en cualquier bloque de narración (evita silencios de 1–2 s en ElevenLabs).
3. Duración estimada (`palabras/180*60`) dentro de ±15 % de `duracion_objetivo_seg` (advertencia).
4. `confianza_dato == "media"` → advertencia, no error.

### Linter del gancho (`pruebas/lint_gancho.py`)

Audita el gancho inicial (`cold_open` + `hook`) de un guion: sin puntos `.` (regla crítica de ElevenLabs), longitud ≤18/20 palabras (calibrada sobre el catálogo real 01–15), sin métricas inventadas ni promesas imposibles (%, "cero", "garantiz", "100%", "siempre funciona"), y rotación anti-template del arquetipo de gancho (`ConfigVideo.gancho_preferido`) entre videos consecutivos. Uso: `python pruebas/lint_gancho.py` (catálogo) o con rutas de guiones (pre-vuelo). Exit 1 si hay FAIL.

### API ElevenLabs con caché (`src/audio_elevenlabs.py`)

- `calcular_hash_audio(texto, voice_id, model_id, voice_settings)` — SHA-256 determinista.
- `generar_audio_con_timestamps_elevenlabs(...)` — **caché primero**: si el hash + archivos existen en `cache/cache_audio/`, copia a rutas destino sin gastar créditos; si no, `POST /v1/text-to-speech/{voice}/with-timestamps`, valida >10 KB, guarda `{hash}.mp3` + `{hash}_alignment.json` + índice.
- `sintetizar_audio_y_alignment_fallback(...)` — sin API key: tono FFmpeg 440 Hz + alignment sintético (advertencia visible).
- Voice settings por defecto: stability 0.45, similarity 0.80, style 0.05, speed 1.15.

### Catálogo de videos (`src/registro_videos.py`)

- `@dataclass ConfigVideo` — una fila por video: `id`, `carpeta`, `generador_fondos`, `sprites`, `claves_sprites`, `cinematico`, `gancho_preferido`, etc.
- `CONFIGS: Tuple[ConfigVideo, ...]` — catálogo central (videos 01–15).
- `resolver_carpeta(stem)` — resuelve `videos/video_XX…` desde el nombre del guion.
- `sprites_para(nombre_base, mockup_sugerido)` — devuelve `Tuple[(bloque, ruta_png), ...]`.
- `generar_fondos_del_video(cfg, segmentos, dir_fondos, forzar, alignment)` — MP4 por escena; reutiliza si >50 KB; inyecta `eventos` de voz si el generador lo acepta.

---

## 🧪 Pruebas Unitarias

```bash
# CI local (recomendado): todas las suites con resumen y exit code (~1 min, requiere ffmpeg)
python pruebas/ci_local.py
python pruebas/ci_local.py --sin-ffmpeg    # solo suites sin ffmpeg (~3 s)
python pruebas/ci_local.py --lista         # qué corre cada modo
python pruebas/ci_local.py --instalar-hook # hook pre-push .githooks (saltar: git push --no-verify)

# Corrida individual de suites
# Suites de validación
python pruebas/test_lint_zonas.py
python pruebas/test_lint_obsoleto.py
python pruebas/test_lint_subtitulos.py
python pruebas/test_lint_anti_template.py
python pruebas/test_chequeos_pipeline.py

# Catálogo de videos
python pruebas/test_registro_videos.py

# Módulos extraídos del monolito
python pruebas/test_pipeline_modulos.py

# Motion, SFX y eventos de voz
python pruebas/test_motion_y_sfx.py
python pruebas/test_eventos_voz.py

# Punch-in de énfasis, director del gancho y registro de experimentos
python pruebas/test_enfasis.py
python pruebas/test_director_gancho.py
python pruebas/test_registro_experimentos.py

# Runner de previews y CI local
python pruebas/test_runner_previews.py
python pruebas/test_ci_local.py

# Ensamble de video (~1 min, genera artefactos)
python pruebas/archivo_pruebas/test_shorts_assembler.py
```

**Total: 248 tests en 15 suites**, todos en verde. Además, `python pruebas/test_smoke_planos.py`
es un smoke test visual que renderiza los ~54 planos y un clip cinematográfico (RC=0 = OK).

El mismo `ci_local.py` corre **en la nube**: GitHub Actions lo ejecuta en cada push/PR a `main`
(`.github/workflows/ci.yml` — ubuntu + ffmpeg + Python 3.13).

### Previews visuales (runner único)

```bash
python pruebas/previews.py            # lista los scripts disponibles
python pruebas/previews.py 15         # previews del video 15
python pruebas/previews.py --todos    # todas
```

Renderiza PNG de diagnóstico en `videos/video_XX/intermedios/previews_director/`
(sin créditos ni pipeline).

---

## 📈 Estado del Proyecto

- **15 videos** producidos (catálogo de guiones maestros `guion_02..15`).
- **248 tests** automatizados en 15 suites (+ 1 smoke test visual), todos en verde.
- **6 linters** de calidad (`validar_guion` + 5 `lint_*`, cableados al pipeline o manuales); validación previa sin gastar créditos.
- **Edición automática**: 6 transiciones xfade rotativas anti-template con pin narrativo
  por tipo de escena + grado cinematográfico (vignette, contraste, saturación, grano fino)
  + aceleración final 1.12x.
- **Audio 100 % procedural**: 7 SFX + BGM Synthwave 112 BPM + masterización con
  sidechain ducking y limiter.
- **Animación de Byte**: respiración, squash/stretch, micro-hops, crossfade de emociones,
  VFX (chispas, gotas, aura, confeti).
- **Fondos dinámicos animados**: ciudad cyberpunk, viaje espacial, estudio creativo.
- **Sync voz ↔ UI**: eventos `t_ui`, `t_pildora` y `t_enfasis` desde el alignment de ElevenLabs.
- **Punch-in de énfasis** (`src/enfasis.py`): zoom breve sobre bg+mockup sincronizado con la
  palabra clave, con ancla y rango verificados contra safe zones (excluido en cinemáticos).
- **Director del gancho** (`src/director_gancho.py`): variantes visuales A/B/C del clip 0 con
  el mismo audio (0 créditos), rotación determinista y lint_gancho.
- **Registro de experimentos** (`src/registro_experimentos.py`): CSV append-only en
  `datos/experimentos.csv` con trazabilidad de cada variante producida.
- **CI doble**: local (`python pruebas/ci_local.py` + hook pre-push opcional) y en la nube
  (GitHub Actions en cada push/PR a `main`).

---

## 📄 Documentación Relacionada

- **`AGENTS.md`** — normas del proyecto para agentes (safe zones, sprites, emojis PIL, linters obligatorios).
- **`.agents/rules/reglas_produccion_video.md`** — reglas técnicas completas de producción.
- **`.agents/rules/arquitectura_visual_variada.md`** — arquetipos visuales y rotación anti-template.
- **`REPORTE_REORGANIZACION.md`** — historia y balance de la reorganización del código.

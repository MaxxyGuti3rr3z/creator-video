# Reglas de Generación de Guiones y Audio (ElevenLabs)

## 1. Puntuación y Fluidez del Guión
- **PROHIBIDO usar puntos (`.`) en el texto de narración**: ElevenLabs interpreta los puntos como silencios dramáticos o descansos largos (1 a 2 segundos de silencio muerto). En videos verticales cortos de alta retención (TikTok, Reels, Shorts), esto destruye la retención del espectador.
- **Alternativa fluida**:
  - Emplear comas (`,`) únicamente cuando se requiera una micro-pausa natural de milisegundos.
  - Usar conectores fluidos directos (ej: "y", "además", "mientras") sin puntuación fuerte.
  - Eliminar puntos finales de las oraciones en los campos `hook`, `explicacion`, `opinion_byte` y `cierre`.

## 2. Estilo y Estructura de Subtítulos
- Mantener siempre texto amarillo puro (`PrimaryColour=&H0000F5FF&` en BGR ASS) con borde negro sólido y tamaño calibrado en **46px** (evitar tamaños gigantes >70px que empequeñecen a Byte; el valor canónico del generador es 46, validado por `pruebas/lint_subtitulos.py`).
- **Premisa, Problema y Preguntas Completas al Inicio**:
  - En los segmentos iniciales de impacto (`cold_open`, `hook`, `problema`) y en preguntas clave de cierre (`cierre`), la frase debe presentarse como un **bloque de sentido completo** (hasta 10-12 palabras) para eliminar la fricción cognitiva en los primeros 3 segundos.
  - Si el bloque supera las 4 palabras, debe dividirse armónicamente en 2 líneas usando el salto de línea `\N` respetando límites gramaticales (comas o dos puntos). Todas las palabras permanecen visibles en pantalla y se iluminan dinámicamente con animación pop-in en sincronía con la locución.
  - En los segmentos intermedios de herramientas y demostraciones técnicas, mantener fragmentos cortos y ágiles de 3 a 4 palabras por pantalla para acompañar la velocidad de la interfaz.

## 3. Aislamiento de Proyectos y Estructura
- Cada nuevo video generado debe residir en su propia carpeta en `videos/video_XX_nombre/` subdividido en:
  - `entrada/`: guion JSON (`guion_XX.json`), narración de voz original (`narracion_XX.mp3`) y alineación carácter por carácter (`alignment_XX.json`). Activos irreemplazables.
  - `intermedios/`: fondos animados (`fondos/`), subtítulos (`subtitulos_XX.ass`), tabla de tiempos (`tiempos_XX.txt`), audio masterizado (`audio_master_*.wav`), SFX y capturas de verificación (`capturas_frames/`). Activos regenerables.
  - `final/`: video final acelerado a 1.12x (`video_XX.mp4`).
- Toda resolución de rutas en el código debe usar el módulo centralizado `src.rutas` (`ruta_video()`, `DIR_ASSETS`, `DIR_CACHE`, etc.).

## 4. Prohibición de Métricas Numéricas Inventadas
- **PROHIBIDO inventar cifras de tiempo, porcentaje o dinero ahorrado** en ningún mockup (ni ahora ni en el futuro).
- Usar siempre términos y conceptos cualitativos (ej: "Más liviano", "Menos caos", "Enfoque claro", "Flujo continuo", "Al día").

## 5. Estilo de Ventanas y Mockups
- En la esquina superior izquierda de las ventanas usar **3 puntos simples en un solo tono gris neutro** (ej: slate claro), evitando colores tipo semáforo (rojo/amarillo/cian) para no parecerse a macOS.

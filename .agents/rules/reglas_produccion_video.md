# Reglas de Producción de Video — Byte el Zorrito
# Versión consolidada desde la conversación (videos 7 al 13)
# ⚠️ ESTAS REGLAS DEBEN APLICARSE EN TODOS LOS VIDEOS SIN EXCEPCIÓN

---

## 1. SAFE ZONE MÓVIL ESTRICTA (TikTok / Reels / Shorts — Canvas 1080x1920)

### Zonas Fijas Obligatorias (4 franjas inamovibles):

| Franja | Coordenadas Y | Contenido permitido |
|--------|--------------|---------------------|
| **Zona Muerta Superior** | y: 0..240 | VACÍA — Reservada para batería, hora 8:00, LIVE, pestañas "Siguiendo / Para ti" y buscador de TikTok. PROHIBIDO colocar NADA aquí. |
| **Zona UI / Mockups** | y: 250..780 | Ventanas de software, mockups, tarjetas VS, navegador, smartphone POV. Ancho máximo: 880px centrado (x: 100..980). |
| **Píldora Flotante / Callout** | y: 790..870 | UNA SOLA píldora de beneficio unificada. Tipografía grande (28-32px negrita). PROHIBIDO apilar múltiples banners. |
| **Subtítulos Karaoke ASS** | y: 960..1080 | Subtítulos amarillo puro #FFF500 con borde negro. Tamaño: 46px. MarginL/R: 80px. |
| **Zona Sagrada de Byte** | y: 1120..1650 | 100% exclusiva para Byte. PROHIBICIÓN ABSOLUTA de banners en y: 1200..1850. |

---

## 2. SUBTÍTULOS KARAOKE ASS — ESPECIFICACIONES EXACTAS

Color: #FFF500 (amarillo puro) con borde negro
Tamaño fuente: 46px
MarginL: 80px
MarginR: 80px
Posición Y: 960..1080 (centrados)

### Regla de corte de chunks:
- En cold open, hook y preguntas de cierre: 4 a 6 palabras por chunk, partidos en 2 líneas cortas con \N a partir de 3 palabras.
- Máximo 2 a 3 palabras por sublínea.
- Ejemplo correcto: "ABRÍS DIEZ PÁGINAS \N Y NINGUNA RESPONDE"
- Ejemplo incorrecto: "ABRÍS DIEZ PÁGINAS DISTINTAS Y NINGUNA TE DA LA RESPUESTA COMPLETA"
- En escenas de demostración: chunks de 3 a 4 palabras para ritmo ágil.

---

## 3. NARRACIÓN — REGLA ANTI-PAUSA ELEVENLABS

PROHIBIDO usar puntos (.) en los textos de narración del JSON.
Los puntos generan silencios de 1 a 2 segundos en ElevenLabs. Usar comas o redacción continua.

MAL: "Necesito encontrar un dato entre 50 archivos. Los voy a abrir uno por uno."
BIEN: "Necesito encontrar un dato clave entre cincuenta facturas,"

---

## 4. ANTI-TEMPLATE — ROTACIÓN OBLIGATORIA DE ARQUETIPOS VISUALES

TERMINANTEMENTE PROHIBIDO repetir la misma estructura en dos videos consecutivos.

### Los 5 Arquetipos a rotar:
1. Smartphone Native POV — Celular vertical centrado, Dynamic Island visible.
2. Hero Byte Center-Stage — Byte gigante en el centro con micro-cards flotantes.
3. Split Before/After o Batalla VS — Pantalla dividida comparativa.
4. Bento Grid Modular — Mosaico asimétrico estilo Apple/Linear.
5. Panoramic Pro Workspace — Escritorio panorámico de software.

### Rotación de sprites de Byte — también obligatoria:
PROHIBIDO usar byte_agotado echado sobre la laptop dos veces consecutivas.
Sprites disponibles: Imagen_byte_frente, byte_sentado_frente_feliz, byte_perfil, byte_ojos_estrella, byte_señalando_serio, byte_saltando_feliz, cierre_transparente, byte_agotado.

---

## 5. COMPOSICIÓN TEMÁTICA 100% NATIVA

| Tema del guion | Mockup correcto |
|---|---|
| Navegador / Pestañas | Navegador oscuro con 10+ pestañas apretadas, spinners, banner cookies, alerta RAM |
| Buscadores IA (Perplexity) | Barra de búsqueda futurista con prompt y citas [1][2][3] |
| Documentos (NotebookLM) | Escáner de archivos con haz láser y notas verificadas |
| WhatsApp / Cotizaciones | Smartphone moderno centrado con Dynamic Island y chat real |
| Ciberseguridad | Lupa revelando dominio falso, badge rojo de phishing |
| Diseño / Flyers | Canva con Magic Design + comparativa Remove.bg Before/After |
| 50 archivos | Mosaico PDFs flotantes + panel RAG + respuesta con citas de origen |

---

## 6. CLARIDAD VISUAL — REGLA DE ASIMILACIÓN EN 1 SEGUNDO

PROHIBIDO:
- Acumular 4+ viñetas densas con texto chico (<20px) y métricas inventadas.
- Apilar 2 o 3 tarjetas oscuras con párrafos en la zona inferior.
- Inventar cifras de tiempo ahorrado, porcentajes o dinero en mockups.
- Afirmar "cero alucinaciones" — Usar: "Menos alucinaciones", "Fuentes verificadas", "Respuestas ancladas a tus notas".

OBLIGATORIO:
- Máximo 2 líneas grandes (24-28px) de síntesis directa en los mockups.
- Una única píldora flotante (28-32px en negrita) en y = 790..870.
- Chips de fuentes: [1] Bloomberg, [2] Reuters — máximo 4 chips.

---

## 7. EMOJIS EN PIL (Python Image Library) — REGLA CRÍTICA

PROHIBIDO insertar emojis Unicode directamente en textos renderizados con PIL/Pillow.
PIL no soporta emojis del plano suplementario. Usar tags ASCII:
- [OK], [!], [X], [CHECK], [>>], [>>>]

MAL (crash en PIL): texto = "⚡ Citas reales"
BIEN: texto = "[!] Citas reales con fuentes verificadas"

Los emojis pueden ir en guiones JSON y copies para redes, pero NO en código PIL.

---

## 8. FONDOS DINÁMICOS — IDs CORRECTOS Y BUG CONOCIDO

Fondos disponibles:
- ciudad_cyberpunk: Estrés, trabajo de noche, urgencias, ciberseguridad.
- viaje_espacial: Automatizaciones, IA/futuro, análisis, saltos de productividad.
- estudio_tech: Presentaciones de diseño, atención al cliente, comparativas sobrias.
- estudio_creativo: Diseño gráfico, flyers, creatividad visual.

Bug corregido en animaciones_fondo.py:
- El detector verificaba "espacio" in estilo.lower() — FALLABA con "viaje_espacial".
- Condición correcta: detectar "espac", "viaje", "warp", "space" o "cyber".
- Velocidad correcta: 0.85x (no 0.30x — era imperceptible en escenas de 2-3s).
- Partículas: 70 unidades con oscilación sinusoidal.

---

## 9. JERARQUÍA DE 7 MICRO-ESCENAS (estructura estándar)

01 Cold Open — Hook visual nativo al tema
02 Hook — Elemento de dolor/urgencia
03 Problema — Contexto del dolor
04 Demo 1 — Herramienta 1 en acción (Byte: Eureka)
05 Demo 2 — Herramienta 2 o resultado parcial (Byte: Zen)
06 Resultado — Transformación o éxito (Byte: Celebrando)
07 Cierre CTA — Encuesta/Debate/Pregunta (Byte: Host mirando al espectador)

Duración promedio por escena: ~2.5s

---

## 10. VALIDACIÓN DE GUIÓN — ESTÁNDAR MÍNIMO

Ejecutar antes de producir:
python src/validar_guion.py guiones/guion_XX_nombre.json

Requisitos:
- "valido": true
- "errores": []
- "advertencias": []
- duracion_estimada_seg: entre 22 y 30 segundos
- 0 puntos finales en textos de narración

---

## 11. ACELERACIÓN Y DURACIÓN FINAL

- Aceleración: 1.12x con FFmpeg
- Duración base objetivo: 25-30 segundos
- Duración final acelerada objetivo: 22-27 segundos
- Ritmo: 200-250 PPM sin silencios por puntos

---

## 12. ESTRUCTURA DE ARCHIVOS POR VIDEO

videos/video_XX_nombre/
  entrada/
    guion.json           (guión original — irreemplazable)
    narracion.mp3        (audio ElevenLabs — irreemplazable)
    alignment.json       (timestamps por palabra — irreemplazable)
  intermedios/
    fondos/              (fondos dinámicos — regenerables)
    subtitulos_*.ass     (subtítulos karaoke ASS — regenerables)
    tiempos_*.txt        (tabla de tiempos \k — regenerables)
    capturas_frames/     (capturas PNG de validación — regenerables)
    previews_director/   (previsualizaciones por plano — regenerables)
  final/
    video_*.mp4          (video final acelerado a 1.12x)

---

## 13. PROTOCOLO DE KICKOFF PARA NUEVO VIDEO

ANTES de generar código, mockups o audio, formular 4 preguntas con opciones contextualizadas:
1. Fondo dinámico — 2 o 3 opciones justificadas según el tema.
2. Representación del dolor (Escena 1) — Variantes del problema concreto.
3. Demostración práctica — Cómo mostrar la solución (evitar "caja negra").
4. Llamado a la acción (CTA) — Palabra clave adaptada al recurso.

Esperar validación del usuario antes de proceder a producción.

---

## 14. REGLA ANTI-REPETICIÓN DE CIERRE

PROHIBIDO repetir el mismo formato de encuesta de cierre en videos consecutivos:
- Si el anterior usó encuesta A/B/C → el siguiente usa Battle Card VS o pregunta abierta.
- Si el anterior usó Battle Card VS → el siguiente usa pregunta de debate directo o encuesta con stickers.
- Si el anterior usó poll interactivo → el siguiente usa pregunta de comunidad o humor.

---

## 15. PROTOCOLO DE REFERENCIA DE SPRITES

Sprites transparentes disponibles en assets/sprites/:
- Imagen_byte_frente.png — Byte mirando al frente neutral
- byte_sentado_frente_feliz.png — Byte sentado sonriendo
- byte_perfil.png — Byte de perfil
- byte_ojos_estrella.png — Byte con ojos de estrella (Eureka/asombro)
- byte_señalando_serio.png — Byte señalando con determinación
- byte_saltando_feliz.png — Byte saltando con alegría (cierre)
- cierre_transparente.png — Byte presentando/apuntando (anchor de noticias)
- byte_agotado.png — Byte exhausto sobre laptop (usar con moderación)

Regla: Nunca el mismo sprite en dos escenas consecutivas del MISMO video.
Regla: Nunca el sprite de apertura repetido entre dos VIDEOS consecutivos.

---

Última actualización: Extraída de conversación 78c3750e (Videos 7-13, octubre 2026)

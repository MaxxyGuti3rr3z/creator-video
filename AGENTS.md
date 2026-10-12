# Normas del Proyecto - Byte el Zorrito

> ⚠️ **REGLAS TÉCNICAS COMPLETAS DE PRODUCCIÓN**: Ver `.agents/rules/reglas_produccion_video.md`
> Este archivo contiene TODAS las mejoras acumuladas (videos 7-13): safe zones exactas, ASS subtítulos, anti-template, emojis PIL, fondos dinámicos, estructura de escenas, validación de guión y protocolo de kickoff. Cualquier IA que genere videos DEBE leerlo antes de producir.

Consulte las reglas específicas en `.agents/rules/`:
  - **No usar puntos (`.`) en los guiones**: Para evitar pausas/silencios largos de 1 a 2 segundos en ElevenLabs. Emplear comas o redacción continua.
  - **Subtítulos (Safe Zone Móvil y Lectura Ágil)**: Amarillo puro `#FFF500` con borde negro (tamaño 46px, `MarginL/R: 80px`). En el inicio (cold open, hook, problema) y preguntas de cierre, mantener chunks de 4 a 6 palabras partiendo en 2 líneas cortas con `\N` a partir de 3 palabras. Máximo 2 a 3 palabras por sublínea para que el texto jamás roce los laterales ni sea tapado por la interfaz de TikTok o Instagram Reels.
  - **Organización de archivos**: Todo el contenido de cada video se guarda aislado en `videos/video_XX_nombre/` subdividido en:
    - `entrada/`: guion JSON, narración MP3 y alignment JSON (irreemplazables).
    - `intermedios/`: fondos, subtítulos ASS, tiempos, capturas y video base (regenerables).
    - `final/`: video final acelerado a 1.12x.
  - **Fondos dinámicos en movimiento lento**: Variar el fondo entre videos usando movimiento sutil a baja velocidad con partículas/haces visibles y atenuación oscura calibrada (`ciudad_cyberpunk`, `viaje_espacial`, o `estudio_tech`) para dar dinamismo vivo sin robar foco a Byte ni a los mockups.
  - **Protocolo de Kickoff al Iniciar un Video ("Armemos un nuevo video")**: ANTES de generar código, mockups o audio de un video nuevo, el agente DEBE pausar y formular una serie de preguntas de dirección creativa con opciones 100% contextualizadas y adaptadas al guion específico (fondo sugerido, arquetipo de dolor, mecánica de la demo y palabra clave de CTA). Prohibido usar opciones predeterminadas o genéricas. Esperar validación del usuario antes de proceder.
  - **Módulo de rutas**: Todas las rutas deben importarse desde `src.rutas` (evitar rutas hardcodeadas).
  - **Claridad Visual en Móviles y Regla de Asimilación en 1 Segundo**:
    - Las interfaces de software deben entenderse en menos de 1 segundo. Prohibido acumular 4 viñetas densas con párrafos explicativos en letra chica. Usar 2 líneas grandes y legibles (25-28px) de síntesis directa.
    - Ancho de ventana recortando márgenes laterales (1020px - 1040px) para máxima nitidez en smartphones.
    - Reemplazar bloques inferiores por una única píldora flotante grande (28-32px) con una sola frase clave de beneficio directo.
  - **Prohibición de Clonación Estructural entre Videos (Rotación Obligatoria Anti-Template)**:
    - Terminantemente prohibido repetir la misma estructura visual en dos videos consecutivos (no repetir la fórmula fija de "caja oscura arriba + subtítulo al medio + Byte con laptop abajo").
    - Cada video DEBE empezar y estructurarse diferente utilizando los 5 arquetipos de `.agents/rules/arquitectura_visual_variada.md`:
      1. *Smartphone Native POV* (celular vertical centrado o notificación para chats/WhatsApp).
      2. *Hero Byte Center-Stage* (Byte gigante al centro con micro-cards flotantes).
      3. *Split Before / After o Batalla VS* (pantalla dividida comparativa).
      4. *Bento Grid Modular* (mosaico moderno de tarjetas asimétricas).
      5. *Panoramic Pro Workspace* (escritorio pro con software detallado).
    - Prohibido repetir el sprite `byte_agotado` echado sobre la laptop dos veces seguidas. Rotar obligatoriamente entre la biblioteca completa de sprites (`Imagen_byte_frente`, `byte_sentado_frente_feliz`, `byte_perfil`, `byte_ojos_estrella`, `byte_señalando_serio`, etc.).
  - **Jerarquía Vertical y Safe Zones Móviles Estrictas (TikTok / Reels / Shorts)**:
    - **Zona Muerta Superior (`y: 0..240`)**: Queda terminantemente PROHIBIDO colocar ventanas, banners, píldoras, títulos o textos en `y < 240` (zona ocupada por batería, hora `8:00`, LIVE, pestañas "Siguiendo / Para ti" y búsqueda). Todo mockup o tarjeta superior DEBE comenzar a partir de `y = 250` o inferior.
    - **Franja UI / Mockups**: `y = 250..780` (ancho máximo 860px - 900px, centrado en `x: 90..990` para no rozar los botones laterales derechos de TikTok).
    - **Píldora flotante / Callout clave**: `y = 790..870` (una sola píldora unificada; prohibido apilar múltiples banners redundantes).
    - **Subtítulos karaoke ASS**: `y = 960..1080` (centrados, safe zone de lectura).
    - **Zona exclusiva de Byte**: `y = 1120..1650` (la base de Byte no debe bajar de `y = 1650` para no ser tapada por el username, caption y audio de TikTok).
    - Queda terminantemente prohibido colocar banners o píldoras flotantes en la mitad inferior de la pantalla (`y: 1200..1850`) tapando el cuerpo, cara o laptop de Byte.
  - **Sin métricas inventadas ni promesas imposibles**: Prohibido inventar cifras de tiempo ahorrado, porcentajes ficticios o dinero en mockups. Prohibido afirmar "cero alucinaciones" (usar conceptos rigurosos: "Menos alucinaciones", "Fuentes verificadas", "Respuestas ancladas a tus notas").
  - **Estilo de ventana**: 3 puntos simples en gris neutro, sin colores tipo semáforo de macOS.
  - **CRÍTICO — Emojis en PIL/Pillow**: Terminantemente PROHIBIDO insertar emojis Unicode en textos renderizados con PIL. PIL no soporta el plano suplementario Unicode y genera crashes silenciosos. Usar tags ASCII: `[OK]`, `[!]`, `[X]`, `[>>]`. Los emojis solo van en los guiones JSON y copies de redes sociales, NUNCA en código de renderizado Python.
  - **CRÍTICO — Detección de fondos dinámicos**: El ID `viaje_espacial` NO contiene la cadena "espacio" — verificar siempre usando `"espac" in estilo or "viaje" in estilo` para no caer en el fallback de fondo plano sin animación.
  - **Biblioteca de sprites de Byte**: `Imagen_byte_frente`, `byte_sentado_frente_feliz`, `byte_perfil`, `byte_ojos_estrella`, `byte_señalando_serio`, `byte_saltando_feliz`, `cierre_transparente`, `byte_agotado`. Nunca el mismo sprite en dos escenas consecutivas del mismo video.
  - **Rotación de formato de cierre**: Prohibido repetir el mismo formato de encuesta de cierre en videos consecutivos. Rotar entre: encuesta A/B/C, Battle Card VS, pregunta de debate directo, medidor de dolor.

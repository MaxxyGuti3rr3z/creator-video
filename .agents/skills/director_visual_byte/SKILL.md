---
name: director-visual-byte
description: >-
  Dirección de arte cinematográfica y narrativa para los videos de Byte el Zorrito.
  Analiza cualquier guion JSON nuevo para definir una estructura visual única, eliminando
  plantillas repetitivas mediante un catálogo de arquetipos visuales (Hero Caos, Showcase
  Panorámico, Split Before/After, Deck 3D y Host Community).
---

# Skill: Director Visual de Escenas - Byte el Zorrito

Esta skill se activa **cada vez que se procesa, analiza o genera un nuevo video o guion** para la serie de Byte.

Su objetivo es **garantizar que ningún video repita la misma estructura rígida**. Cada video debe tener su propia dirección de arte basada en el tema del guion.

---

## 1. Regla de Oro: Prohibido el Molde Único
Queda estrictamente prohibido usar el esquema estático repetitivo:
`[Ventana 940x560 arriba] -> [Subtítulo medio] -> [Byte estático abajo]`
repetido idéntico a lo largo de las 5 escenas de un video.

Cada escena debe cumplir una función narrativa y adoptar un **Arquetipo Visual** diferenciado.

---

## 2. Catálogo de Arquetipos Visuales

Para cada una de las 5 escenas del guion, el director visual debe asignar uno de los siguientes arquetipos:

### 1. `PLANO_HERO_CAOS` (Para Escena 1 - Hook & Problema)
*   **Propósito:** Detener el scroll en los primeros 2 segundos transmitiendo el dolor visceral del usuario.
*   **Composición:**
    *   **Byte Protagonista:** Ocupa el centro-inferior en tamaño grande (600x600px) con expresión de estrés/desesperación.
    *   **Elementos flotantes del caos:** Objetos temáticos desordenados volando/cayendo por la pantalla (ej. hojas rotas con Lorem Ipsum para presentaciones, hilos de correo acumulados para email, relojes en rojo para gestión de tiempo).
    *   **Cero ventanas de software con 3 puntos:** La escena es dramática y limpia.

### 2. `PLANO_SHOWCASE_PANORAMICO` (Para Escena 2 - Herramienta 1 / Revelación)
*   **Propósito:** Demostrar la magia del producto en formato grande y legible.
*   **Composición:**
    *   **Lienzo Showcase:** Ocupa el 85% del ancho de la pantalla (panorámico y espacioso), mostrando el flujo del software o la generación de contenido.
    *   **Byte Comentarista / Streamer:** Pasa a la esquina inferior derecha o izquierda (380x380px) asomándose con ojos de estrella (`byte_ojos_estrella`) o señalando la pantalla.

### 3. `PLANO_SPLIT_BEFORE_AFTER` (Para Escena 3 - Herramienta 2 / Transformación)
*   **Propósito:** Mostrar el "Glow-up" estético o el salto de calidad que produce la IA.
*   **Composición:**
    *   **Pantalla Dividida o Deslizante:** Lado izquierdo muestra el método manual aburrido/lento ("Antes"), y el lado derecho muestra el diseño pulido y profesional ("Después").
    *   **Byte Creador:** Byte con laptop en el centro inferior (`Byte_enojado_computadora` enfocado o sonriendo) validando el resultado.

### 4. `PLANO_DECK_3D` (Para Escena 4 - Resultado / Alivio)
*   **Propósito:** Transmitir control, orden y sensación de victoria sin métricas numéricas inventadas.
*   **Composición:**
    *   **Muro / Abanico 3D:** Un conjunto de 3 o 4 tarjetas/diapositivas completas en perspectiva isométrica o abanico elegante.
    *   **Byte Zen:** Byte levitando o meditando en calma (`byte_pacifico_zen`) con aura suave.
    *   **Badges Cualitativos:** 3 pastillas flotantes con conceptos de alivio (*Presentable, Ordenado, Visual* o *Al Día, Más Liviano, Menos Caos*).

### 5. `PLANO_HOST_COMMUNITY` (Para Escena 5 - Cierre & Call to Action)
*   **Propósito:** Invitar a la comunidad a debatir y comentar en la publicación.
*   **Composición:**
    *   **Byte Host:** Byte centrado mirando directo a cámara en plano medio (`byte_saltando_feliz`).
    *   **Encuesta Interactiva:** 3 tarjetas grandes estilo sticker de TikTok/Instagram con opciones A, B y C.
    *   **Flecha hacia el feed:** Indicador animado apuntando a la caja de comentarios.

---

## 3. Protocolo de Ejecución al Recibir un Guion

1. **Lectura y Clasificación del Tema:**
   Identificar el dominio principal:
   * `presentaciones_diseño` (Diapositivas, Gamma, Canva, pitch decks).
   * `correo_comunicacion` (Bandeja de entrada, Shortwave, Gmail, respuestas automáticas).
   * `tareas_productividad` (Todoist, Notion, calendarios, prioridades).
   * `reuniones_voz` (Videollamadas, Otter, Fireflies, transcripciones).
   * `automatizacion_codigo` (Python, scripts, terminal, APIs).

2. **Generación del Storyboard (`storyboard.json`):**
   Crear el plan de dirección en `videos/video_XX/intermedios/storyboard.json` especificando:
   * Arquetipo visual por cada escena.
   * Expresión de Byte y posición en pantalla (`centro_hero`, `esquina_derecha`, `esquina_izquierda`, `host_centro`).
   * Paleta emocional y fondo en movimiento (Ciudad Cyberpunk, Estudio Minimal, Espacio Warp, etc.).
   * Elementos interactivos (badges, split-screen, stickers de encuesta).

3. **Presentación al Usuario:**
   Presentar el storyboard propuesto en formato de tabla clara antes del renderizado para que el usuario pueda validar o ajustar cualquier plano en 10 segundos.

---

## 4. Dirección Tipográfica y Subtítulos Narrativos (Safe Zone Móvil)
* **Subtítulos con Márgenes de Seguridad Amplios (`MarginL/R: 80px`, fuente 46px)**:
  * El texto debe mantenerse estrictamente dentro de la safe zone de TikTok e Instagram Reels, lejos de los botones de interacción de la derecha y de la barra inferior.
* **Premisas Iniciales y Preguntas de Cierre**:
  * Chunks de 4 a 6 palabras que se parten en 2 líneas cortas con `\N` a partir de 3 palabras.
  * Máximo 2 a 3 palabras por sublínea. Nunca líneas largas que toquen los márgenes.
* **Demostración de Herramientas**:
  * Subtítulos dinámicos de 3 a 4 palabras por chunk para acompasar el ritmo ágil del software sin invadir la interfaz.

---

## 5. Catálogo de Fondos Dinámicos en Movimiento Lento (Motion Backgrounds)
Para evitar que los videos tengan lienzos estáticos o planos, el motor dispone de fondos generados proceduralmente que corren a velocidad calibrada con partículas luminosas y atenuación oscura para dar atmósfera viva sin robar el foco de atención:
1. **`ciudad_cyberpunk`**: Rascacielos nocturnos con lluvia suave en ángulo, reflectores lejanos y autopistas con haces de luz que fluyen con calma. Ideal para ganchos de estrés, trabajo de noche, urgencias de oficina y caos técnico.
2. **`viaje_espacial` (Space Warp)**: Campo estelar 3D infinito con nebulosa cósmica respirando, cometas diagonales y 70 partículas cuánticas flotando hacia arriba. Ideal para automatizaciones, código, futuro, saltos cuánticos de productividad e IA.
3. **`estudio_tech` (Minimal Dark)**: Lienzo oscuro medianoche con gradiente radial y respiración lumínica azulada/morada. Ideal para presentaciones de diseño, atención al cliente o comparativas sobrias.

---

## 6. Protocolo Obligatorio de Kickoff al Iniciar un Nuevo Video
Cuando el usuario diga *"Armemos un nuevo video"* o proporcione un guion/tema nuevo, **QUEDA TERMINANTEMENTE PROHIBIDO generar código, mockups o audio de forma inmediata**.

El agente DEBE detenerse y presentar una **Entrevista de Dirección Creativa** de 4 preguntas estructuradas donde las opciones ofrecidas estén **100% contextualizadas con las herramientas, dolores y situaciones del guion provisto** (prohibidas las opciones genéricas de plantilla):

1. **Pregunta 1: Atmósfera y Fondo Dinámico**:
   * Proponer 2 o 3 opciones justificando cómo cada una acompaña la temática del guion (ej. *"A) Ciudad Cyberpunk nocturna con lluvia lenta (para reforzar la urgencia del informe un viernes)", "B) Estudio Tech Medianoche con resplandor cian (para un look más sobrio y analítico)"*).
2. **Pregunta 2: Representación del Dolor / Conflicto (Escena 1)**:
   * Proponer variantes visuales para el problema basadas en el dolor concreto (ej. *"A) Reloj digital en cuenta regresiva con ventana de crash del software", "B) Hero Caos con fórmulas rotas y celdas volando alrededor de Byte"*).
3. **Pregunta 3: Demostración Práctica (Evitar 'Caja Negra')**:
   * Proponer cómo mostrar la solución (ej. *"A) Micro-animación de prompt tipeado ('Analizá tendencias y armá gráficos') antes del dashboard", "B) Pantalla dividida Antes manual vs Después generado"*).
4. **Pregunta 4: Llamado a la Acción (CTA de Conversión)**:
   * Proponer una palabra clave detonante adaptada al recurso del video (ej. *"A) Comentá 'EXCEL' para enviarte los prompts", "B) Pregunta de debate comunitario"*).

**Esperar la selección o indicaciones del usuario antes de proceder a la fase de producción.**

---

## 7. Claridad Visual y Regla de Asimilación en 1 Segundo (Hero UI & Badge Clave)
Diseñado específicamente para optimizar la legibilidad en pantallas de smartphones (6 pulgadas) y eliminar la fatiga cognitiva del espectador en TikTok, Shorts y Reels:

1. **Regla de Asimilación en 1 Segundo (Prohibidas las Viñetas Densas y Métricas Inventadas)**:
   * La interfaz mostrada debe entenderse en menos de 1 segundo sin necesidad de pausar el video.
   * **Prohibido:** Acumular 4 viñetas de texto chico (<20px) con métricas inventadas (ej. "42% en 0.4s").
   * **Obligatorio:** 2 líneas grandes (24-28px) de síntesis directa (ej. *"Síntesis directa basada en fuentes oficiales"* + *"Cada dato incluye enlace a la cita original"*).
   * **Prohibido prometer "cero alucinaciones":** Usar afirmaciones rigurosas y profesionales ("Menos alucinaciones", "Respuestas ancladas a tus notas", "Fuentes verificadas").

2. **Agrandar la Interfaz de la Herramienta (Recortar Márgenes a 20-30px)**:
   * Las ventanas de software no deben verse encogidas con márgenes excesivos.
   * Usar un ancho de ventana de **1020px a 1040px** (sobre el lienzo de 1080px), aprovechando el 95% del ancho de pantalla.
   * Esto garantiza que el nombre del software (ej. *"PERPLEXITY AI"*), el prompt y los elementos visuales se lean con total nitidez a primera vista.

3. **Simplificar Tarjetas Inferiores a una Sola Frase Clave (Píldora Única)**:
   * **Prohibido:** Acumular 2 o 3 tarjetas oscuras con párrafos explicativos en la zona inferior.
   * **Obligatorio:** Reemplazar todo ese bloque por **una única píldora flotante prominente** (*Floating Pill Badge*) con tipografía grande (**28px a 32px en negrita**) en `y = 710..800` (arriba de subtítulos y de Byte).

---

## 8. Prohibición de Clonación de Plantillas y Diseños Temáticos Nativos
Para mantener a la audiencia enganchada y evitar la fatiga visual de ver siempre el mismo "esqueleto" en la cuenta:

1. **Prohibido el Molde Repetitivo entre Videos**:
   * No repetir la misma fórmula compositiva de un video anterior (ej. si el video anterior usó tarjetas flotantes de alerta roja, el siguiente NO debe usar tarjetas flotantes; si usó una laptop cerrada para el viernes, NO usar la misma laptop para temas que no son de viernes a la tarde; si usó 3 barras verticales de encuesta A/B/C, el siguiente debe usar otro formato de cierre).

2. **Diseño de Escenas 100% Nativas al Tema**:
   * Cada video debe representar la **metáfora visual real** de lo que narra:
     * **Navegador Web / Pestañas**: Renderizar un navegador real saturado de pestañas apretadas con spinners de carga, banners de cookies y avisos 404, no cajas genéricas.
     * **Buscadores de IA (Perplexity)**: Barra de búsqueda futurista con prompt visible y tarjetas de citas enlazadas `[1][2][3]`.
     * **Gestión Documental (NotebookLM)**: Escáner visual de archivos (PDFs/Sheets) con haz láser y notas verificadas.
     * **Resultados**: Metáfora del tema (ej. 1 sola pestaña limpia para navegación, bandeja vacía para email, etc.).
     * **Cierres**: Variar entre **Battle Cards 'VS'**, medidores de dolor, stickers de debate directo o elecciones visuales de dos bandos.




---

## 9. Jerarquía Vertical de 4 Zonas (Prohibido tapar a Byte con Banners)
Para garantizar una estética cinematográfica limpia y que el personaje protagonista de la cuenta (Byte) brille en pantalla sin obstrucciones:

El lienzo vertical de 1080x1920 píxeles se divide obligatoriamente en 4 alturas fijas:
1. **Zona 1 - Interfaz / UI / Cards Temáticas (`y = 60..700`)**:
   * Ocupa la mitad superior. Es donde viven las interfaces de software, tarjetas VS, o ventanas saturadas de pestañas.
2. **Zona 2 - Píldora Flotante de Alto Impacto / Callout (`y = 710..800`)**:
   * Se ubica **inmediatamente debajo de la ventana de software y por encima de los subtítulos**.
   * Aquí se coloca la píldora flotante (`⚡ Citas reales`, `✓ De 10 pestañas a 1 sola`, `¿De qué lado estás? Votá en comentarios`).
   * Al estar en `y = 710..800`, el ojo del espectador lee el beneficio sin desviar la mirada y **NUNCA** colisiona con el personaje.
3. **Zona 3 - Subtítulos Karaoke ASS (`y = 980..1080`)**:
   * Zona de texto amarillo de lectura rápida y comprensión fluida.
4. **Zona 4 - Zona Sagrada de Byte (`y = 1150..1880`)**:
   * La franja inferior pertenece 100% a Byte (sea meditando zen, tecleando en la laptop o interactuando con la audiencia).
   * **PROHIBICIÓN ESTRICTA:** Queda terminantemente prohibido dibujar banners, píldoras flotantes, botones o tarjetas en esta franja inferior (`y: 1200..1850`). Byte debe verse completo, libre de cualquier caja o texto que lo tape.

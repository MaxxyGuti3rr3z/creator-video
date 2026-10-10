# Reglas de Arquitectura Visual Variada y Safe Zones Móviles

## 1. Safe Zones Móviles Estrictas (TikTok / Instagram Reels / YouTube Shorts)
En un lienzo vertical de 1080x1920:

- **ZONA MUERTA SUPERIOR (`y: 0..240`)**:
  - En esta franja habitan:
    - Reloj del sistema (`8:00`), batería, señal (`y: 0..90`).
    - Pestañas de TikTok (`LIVE`, `Siguiendo | Para ti`, Lupa de búsqueda) (`y: 90..230`).
  - **REGLA ABSOLUTA**: Queda terminantemente PROHIBIDO colocar ventanas, banners, píldoras, títulos o textos en `y < 240`. Todo mockup o tarjeta superior DEBE iniciar en `y = 250` o inferior.
  - **PROHIBIDO crear dobles o triples banners superiores**: Nada de "Tag en y=70" + "Badge en y=130" + "Ventana en y=225". Solo una interfaz unificada, elegante y limpia que arranque a partir de `y = 250`.

- **ZONA DE INTERACCIÓN LATERAL DERECHA (`x: 940..1080`)**:
  - En esta franja vertical habitan los botones de acción de TikTok/Reels: avatar, corazón (likes), comentarios, guardados y compartir.
  - **REGLA**: El ancho de los mockups no debe superar los 900px (`x: 90..970` o centrados `x: 100..980`) para evitar que los botones tapen información o botones de las tarjetas.

- **ZONA DE SUBTÍTULOS KARAOKE (`y: 960..1080`)**:
  - Centrados horizontalmente, fuente amarilla pura `#FFF500` con borde negro grueso. Máximo 2 a 3 palabras por línea con saltos `\N`.

- **ZONA DE CAPTION Y AUDIO INFERIOR (`y: 1620..1920`)**:
  - En esta franja habitan el nombre de la cuenta (`@Byte el zorrito`), descripción con hashtags y la barra de sonido.
  - **REGLA**: La base de los personajes o elementos interactivos debe asentarse en `y <= 1650`.

---

## 2. Prohibición de Clonación y Rotación Obligatoria de Estructura (Anti-Template)

Queda estrictamente PROHIBIDO repetir la misma composición visual o el mismo plano de apertura en dos videos consecutivos. El agente DEBE alternar automáticamente entre los siguientes **5 Arquetipos de Apertura y Composición**:

### Arquetipo 1: Smartphone Native POV (Para Mensajes, WhatsApp, Chats, Notificaciones)
- **Centro visual**: Smartphone estilizado vertical (`x: 140..940`, `y: 250..850`) con interfaz móvil real (WhatsApp, Push Notification de iOS/Android).
- **Byte**: De pie al costado o de frente reaccionando al celular (NO con laptop).
- **Uso**: Temas de mensajería, atención al cliente, cotizaciones, llamadas.

### Arquetipo 2: Hero Byte Center-Stage (Para Problemas Emocionales, Bloqueos, Mitos)
- **Centro visual**: Byte protagonista gigante en el centro (`y: 400..1200`), con micro-tarjetas flotantes girando a su alrededor.
- **Uso**: Temas de frustración con herramientas, agotamiento, noticias bomba.

### Arquetipo 3: Split Before / After o Batalla VS (Para Comparativas y Métodos)
- **Centro visual**: Pantalla dividida en dos columnas o dos tarjetas en pugna: "Método Manual (Roto)" vs "Método IA (Limpio)".
- **Byte**: En el centro como juez/árbitro señalando la diferencia.
- **Uso**: Canva vs Photoshop, Excel vs IA, Búsqueda tradicional vs Perplexity.

### Arquetipo 4: Bento Grid Modular (Para Datos, Dashboards, Extracciones)
- **Centro visual**: Mosaico asimétrico moderno de 3 a 4 tarjetas limpias estilo Apple / Linear (`y: 250..820`).
- **Byte**: En la zona inferior con expresiones variadas (ojos de estrella, señalando, zen).
- **Uso**: Organización de pedidos, resúmenes de reuniones, análisis de métricas.

### Arquetipo 5: Panoramic Pro Workspace (Para Herramientas de Escritorio Complejas)
- **Centro visual**: Ventana de software en ultra-definición con sidebar, canvas y toolbar real (`y: 250..850`), cursor simulado interactivo.
- **Byte**: Side-kick en la esquina inferior derecha o inferior izquierda.
- **Uso**: Gamma, NotebookLM, herramientas web de escritorio.

---

## 3. Rotación de Sprites de Byte
- PROHIBIDO usar el sprite `byte_agotado` echado sobre la laptop dos veces seguidas.
- Cada video debe explorar la biblioteca completa:
  - `Imagen_byte_frente` (Byte de pie mirando a cámara)
  - `byte_sentado_frente_feliz` (Byte sentado de frente cercano)
  - `byte_perfil` (Byte mirando a la izquierda/derecha hacia la interfaz)
  - `byte_ojos_estrella` (Asombro, eureka)
  - `byte_señalando_serio` (Autoridad, señalamiento directo)
  - `byte_saltando_feliz` (Celebración, éxito)
  - `byte_paz` (Alivio, tranquilidad)

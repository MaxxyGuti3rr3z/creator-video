# Reporte de Reorganización del Proyecto: Byte el Zorrito

**Fecha:** 29 de septiembre de 2026  
**Copia de seguridad previa:** `../backup_proyecto_2026-09-29.zip` (367.69 MB, 242 archivos, excluyendo estrictamente `.env`).  
**Estado:** Fase 2 completada exitosamente sin pérdida de datos ni cambios en la lógica de negocio.

---

## 1. Resumen de Movimientos Realizados

Todos los archivos fueron reubicados según el plan aprobado. Ningún archivo fue eliminado; los elementos huérfanos, duplicados o regenerables fueron archivados en `_archivo/`.

### A. Motor y Código Fuente (`src/` y `src/mockups/`)
- `shorts_assembler.py` $\to$ `src/shorts_assembler.py`
- `generar_animacion_byte.py` $\to$ `src/generar_animacion_byte.py`
- `generar_paisaje_sonoro.py` $\to$ `src/generar_paisaje_sonoro.py`
- `generar_mockup_tareas.py` $\to$ `src/mockups/generar_mockup_tareas.py`
- `generar_mockup_reunion.py` $\to$ `src/mockups/generar_mockup_reunion.py`
- `generar_animacion_solucion.py` $\to$ `src/mockups/generar_animacion_solucion.py`
- **Nuevos módulos:**
  - `src/rutas.py` (Módulo central de resolución de rutas dinámicas y constantes).
  - `src/__init__.py`, `src/mockups/__init__.py`.

### B. Recursos Estables (`assets/`)
- `assets_transparentes/` $\to$ `assets/byte/transparentes/`
- `imagenes_byte/` $\to$ `assets/byte/ilustraciones_originales/`
- `assets_audio/` $\to$ `assets/audio/`
- `assets_fondos/` $\to$ `assets/fondos/`
- `assets_vfx/` $\to$ `assets/vfx/`

### C. Catálogo de Guiones (`guiones/`)
- `guion_02_reuniones.json` (raíz) $\to$ `guiones/guion_02_reuniones.json`
- `guion_03_tareas.json` (raíz) $\to$ `guiones/guion_03_tareas.json`

### D. Videos Estructurados (`videos/video_02_reuniones/`)
- `entrada/`:
  - `guion_02_reuniones.json`
  - `narracion_guion_02.mp3`
  - `alignment_guion_02.json`
- `intermedios/`:
  - `video_guion_02_base.mp4`
  - `subtitulos_guion_02.ass`
  - `tiempos_guion_02.txt`
  - `audio_master_narracion_guion_02.wav`
  - `musica_fondo.wav`
  - `sfx_*.wav` (5 archivos)
  - `fondos/`
  - `capturas_frames/`
  - `mockups_preview/`
  - `frames_punto1/`
- `final/`:
  - `video_guion_02.mp4`

### E. Videos Estructurados (`videos/video_03_tareas/`)
- `entrada/`:
  - `guion_03_tareas.json`
  - `narracion_guion_03.mp3`
  - `alignment_guion_03.json`
- `intermedios/`:
  - `video_guion_03_base.mp4`
  - `subtitulos_guion_03.ass`
  - `tiempos_guion_03.txt`
  - `audio_master_narracion_guion_03.wav`
  - `musica_fondo.wav`
  - `sfx_*.wav` (5 archivos)
  - `fondos/`
  - `capturas_frames/`
  - `preview_frames/`
- `final/`:
  - `video_guion_03.mp4`

### F. Entorno de Pruebas (`pruebas/`)
- `prueba_end_to_end.py` $\to$ `pruebas/prueba_end_to_end.py`
- `demo_ejecucion.py` $\to$ `pruebas/demo_ejecucion.py`
- `archivo_pruebas/` $\to$ `pruebas/archivo_pruebas/`
- `test_shortwave_frames/` $\to$ `pruebas/test_shortwave_frames/`

### G. Caché de Audio (`cache/`)
- `cache_audio/` $\to$ `cache/cache_audio/` (Preserva intactos los 4 audios cacheados y su índice).

### H. Archivo y Cuarentena (`_archivo/`)
- `_archivo/raiz_legacy/`:
  - `alignment_real.json` (huérfano de Video 01 en raíz)
  - `subtitulos_karaoke_real.ass` (huérfano de Video 01 en raíz)
  - `tiempos_palabras_k.txt` (huérfano de Video 01 en raíz)
  - `capturas_frames/` (capturas de prueba de Video 01 en raíz)
  - `frames_animacion_solucion/` (frames de renderizados de Video 01)
  - `frames_reunion_punto1/` (frames de prueba de Video 02)
- `_archivo/generar_mockups_revision.py` (script legacy de mockups preliminares)
- `_archivo/assets_animaciones_byte/` (clips MOV pre-renderizados antiguos)

---

## 2. Implementación de `src/rutas.py`

Se implementó el módulo [`src/rutas.py`](file:///c:/Users/hgmax/Desktop/bootcamp/Comienzo/src/rutas.py), el cual elimina cualquier ruta hardcodeada y resuelve de forma dinámica y absoluta:
- **Constantes de directorio:** `DIR_RAIZ`, `DIR_SRC`, `DIR_ASSETS`, `DIR_BYTE_TRANSPARENTES`, `DIR_BYTE_ILUSTRACIONES`, `DIR_AUDIO`, `DIR_FONDOS`, `DIR_VFX`, `DIR_GUIONES`, `DIR_VIDEOS`, `DIR_CACHE`, `DIR_PRUEBAS`, `DIR_ARCHIVO`.
- **Funciones de resolución:**
  - `ruta_video(identificador)`: Retorna un diccionario con las rutas `base`, `entrada`, `intermedios` y `final` para cualquier video (ej: `2`, `'video_02_reuniones'`), creándolas si no existieran.
  - `ruta_guion(nombre_o_numero)`: Localiza automáticamente el guion JSON tanto en `guiones/` como en `videos/video_XX/entrada/`.
  - `ruta_sprite_byte(nombre)`, `ruta_sfx(nombre)`, `ruta_vfx(nombre)`: Resuelven assets sin paths relativos frágiles.

Todos los scripts relevantes fueron adaptados para importar sus dependencias desde `src.rutas` sin alterar su lógica matemática, visual o de render.

---

## 3. Aviso sobre `prueba_end_to_end.py` y ElevenLabs

Siguiendo tu instrucción estricta:
> *"Ejecutá prueba_end_to_end.py solo si tiene un modo que no llame a ElevenLabs. Si no lo tiene, no la ejecutes y avisame."*

**No se ejecutó `prueba_end_to_end.py`.**  
**Motivo:** Aunque el script reutiliza los audios y alignments existentes en `cache/cache_audio/` cuando los hashes coinciden, no dispone actualmente de un flag o modo de línea de comandos explícito (ej: `--offline`, `--no-api` o `--dry-run`) que bloquee a nivel de red cualquier llamada a la API si un archivo de caché no se encontrara. Por seguridad absoluta de tus créditos de ElevenLabs, el script quedó listo, compilado y verificado con `py_compile`, pero sin invocar la ejecución de audio/video.

---

## 4. Elementos Pendientes de Borrado o Limpieza Futura

Si en el futuro deseás liberar espacio en disco, los siguientes elementos ubicados en `_archivo/` pueden ser eliminados con seguridad tras verificar que no se requieran:
1. `_archivo/raiz_legacy/`: Contiene residuos de frames y alignments del prototipo de Video 01.
2. `_archivo/assets_animaciones_byte/`: Videos MOV de 680x680 que se regeneran en cualquier momento con `src/generar_animacion_byte.py`.
3. `_archivo/generar_mockups_revision.py`: Reemplazado por los generadores modernos en `src/mockups/`.

---

## 5. Procedimiento para Revertir los Cambios

Si por cualquier razón desearas volver exactamente al estado anterior:

### Método Automático (Recomendado):
El backup comprimido contiene el 100% de los archivos originales (excepto `.env` que se mantuvo intacto en la raíz). Para restaurar:
1. Guardá una copia de tu `.env` actual.
2. Borrá el contenido de la carpeta del proyecto.
3. Descomprimí el archivo `../backup_proyecto_2026-09-29.zip` en la carpeta del proyecto.
4. Restaurá tu `.env`.

### Método Manual:
Si preferís mover los archivos individualmente a su ubicación previa:
```powershell
# Motor a la raíz
Move-Item src/shorts_assembler.py .
Move-Item src/generar_animacion_byte.py .
Move-Item src/generar_paisaje_sonoro.py .
Move-Item src/mockups/generar_mockup_tareas.py .
Move-Item src/mockups/generar_mockup_reunion.py .
Move-Item src/mockups/generar_animacion_solucion.py .

# Assets a la raíz
Move-Item assets/byte/transparentes assets_transparentes
Move-Item assets/byte/ilustraciones_originales imagenes_byte
Move-Item assets/audio assets_audio
Move-Item assets/fondos assets_fondos
Move-Item assets/vfx assets_vfx

# Pruebas y caché a la raíz
Move-Item pruebas/prueba_end_to_end.py .
Move-Item pruebas/demo_ejecucion.py .
Move-Item pruebas/archivo_pruebas .
Move-Item pruebas/test_shortwave_frames .
Move-Item cache/cache_audio .

# Videos: aplanar de nuevo entrada/intermedios/final a la raíz de cada video_XX
```

"""
plantillas/__init__.py
----------------------
Catálogo unificado de plantillas visuales para el motor de mockups.
Cada plantilla expone:
- textos_permitidos: List[str] (para validación de guiones en validar_guion.py)
- renderizar_frame(...) -> Image.Image
"""

from . import tareas_problema
from . import tareas_todoist
from . import tareas_calendario
from . import tareas_resultado
from . import tareas_cierre
from . import reunion_hook
from . import reunion_transcripcion
from . import reunion_asistente
from . import reunion_cierre
from . import correo_hilo_resumen
from . import correo_chat_generico
from . import presentaciones_problema
from . import presentaciones_gamma
from . import presentaciones_canva
from . import presentaciones_resultado
from . import presentaciones_cierre

PLANTILLAS = {
    # Tareas (Video 3)
    "tareas_problema": tareas_problema,
    "tareas_todoist": tareas_todoist,
    "tareas_calendario": tareas_calendario,
    "tareas_resultado": tareas_resultado,
    "tareas_cierre": tareas_cierre,

    # Reuniones (Video 2)
    "reunion_hook": reunion_hook,
    "reunion_transcripcion": reunion_transcripcion,
    "reunion_asistente": reunion_asistente,
    "reunion_cierre": reunion_cierre,

    # Correo (Video 4)
    "correo_hilo_resumen": correo_hilo_resumen,
    "correo_chat_generico": correo_chat_generico,

    # Presentaciones / Informes (Video 5)
    "presentaciones_problema": presentaciones_problema,
    "presentaciones_gamma": presentaciones_gamma,
    "presentaciones_canva": presentaciones_canva,
    "presentaciones_resultado": presentaciones_resultado,
    "presentaciones_cierre": presentaciones_cierre,
}

# Alias genéricos por escena para retrocompatibilidad
ALIAS_ESCENAS = {
    "escena_problema": tareas_problema,
    "punto_1": tareas_todoist,
    "punto_2": tareas_calendario,
    "resultado": tareas_resultado,
    "cierre": tareas_cierre,
}


def obtener_plantilla(nombre: str):
    """Devuelve el módulo de la plantilla según su clave o alias."""
    if nombre in PLANTILLAS:
        return PLANTILLAS[nombre]
    if nombre in ALIAS_ESCENAS:
        return ALIAS_ESCENAS[nombre]
    raise KeyError(f"Plantilla '{nombre}' no encontrada en el catálogo de mockups.")

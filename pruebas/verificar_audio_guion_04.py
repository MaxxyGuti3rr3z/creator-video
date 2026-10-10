"""
pruebas/verificar_audio_guion_04.py
-----------------------------------
Verifica los detalles de audio, caracteres, hash y presencia en caché para Guion 04.
"""

import json
import hashlib
from pathlib import Path

def main():
    with open('guiones/guion_04_correo.json', 'r', encoding='utf-8') as f:
        g = json.load(f)

    hook = g['hook'].strip()
    prob = g['problema'].strip()
    d1 = g['demostracion'][0]['accion'].strip()
    d2 = g['demostracion'][1]['accion'].strip()
    res = g['resultado'].strip()
    cie = g['cierre'].strip()

    if hook.endswith('?') or hook.endswith(',') or hook.endswith('!'):
        p0 = f'{hook} {prob}'
    else:
        p0 = f'{hook}, {prob}'

    bloques = [
        ("Hook", hook),
        ("Problema", prob),
        ("Demostración 1 (Shortwave)", d1),
        ("Demostración 2 (Claude)", d2),
        ("Resultado", res),
        ("Cierre", cie)
    ]

    texto_completo = '\n\n'.join([p0, d1, d2, res, cie])

    print("=== BLOQUES NARRATIVOS (ORDEN CRONOLÓGICO) ===")
    for nombre, txt in bloques:
        print(f"[{nombre}] ({len(txt)} caracteres):\n  \"{txt}\"\n")

    print("=== TEXTO CONCATENADO PARA ELEVENLABS ===")
    print(repr(texto_completo))
    print("\n" + texto_completo)
    print("==========================================")
    print(f"Total caracteres (con saltos): {len(texto_completo)}")
    print(f"Total caracteres (sin saltos): {len(texto_completo.replace('\n', ''))}")
    print(f"Total palabras: {len(texto_completo.split())}")

    # Calcular hash de caché como en prueba_end_to_end.py
    voice_id = 'qd1yh69dLnH0MmK6EJwE'
    model_id = 'eleven_multilingual_v2'
    payload = f'{voice_id}_{model_id}_0.45_0.8_0.05_True_1.15_{texto_completo}'
    h = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    print(f"\nHash SHA-256 esperado: {h}")

    cache_file = Path(f'cache/cache_audio/{h}.mp3')
    print(f"¿Existe en cache/cache_audio?: {cache_file.exists()}")

    # Hook alternativo
    hook_alt = g['hook_alternativo'].strip()
    print(f"\nHook alternativo: \"{hook_alt}\"")
    print(f"Caracteres de hook_alternativo: {len(hook_alt)} caracteres")

    # Guion alternativo completo B
    if hook_alt.endswith('?') or hook_alt.endswith(',') or hook_alt.endswith('!'):
        p0_alt = f'{hook_alt} {prob}'
    else:
        p0_alt = f'{hook_alt}, {prob}'
    texto_completo_alt = '\n\n'.join([p0_alt, d1, d2, res, cie])
    print(f"Guion alternativo completo (Versión B): {len(texto_completo_alt)} caracteres")

if __name__ == "__main__":
    main()

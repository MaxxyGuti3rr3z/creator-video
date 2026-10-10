"""
limpiar_tipografia_v12.py
Reemplaza símbolos no soportados por tipografía limpia y vectorizada en los planos de Video 12.
"""
from pathlib import Path

ruta = Path("src/mockups/director_escena.py")
texto = ruta.read_text(encoding="utf-8")

reemplazos = [
    ('DIR_BYTE_TRANSPARENTES / "cold_open_guion_10_cotizacion_automatica_transparente.png"',
     'DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png"'),
    ('p_byte = DIR_BYTE_TRANSPARENTES / "cold_open_guion_10_cotizacion_automatica_transparente.png"',
     'p_byte = DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png"'),
     
    ("↑ ¡CAMBIARON LA 'O' POR UN CERO!", "^ ¡CAMBIARON LA 'O' POR UN CERO!"),
    
    ("<- SI DICE ESTO EN TU BANCO: ¡FRENA!", "<-- SI DICE ESTO EN TU BANCO: ¡FRENA!"),
    ("❌ Dominio Falso: www.banc0-online.xyz (Usa cero y .xyz)", "[X] Dominio Falso: www.banc0-online.xyz (Usa cero y .xyz)"),
    ("❌ Dominio Trucho: www.banco-soporte-oficial.net", "[X] Dominio Trucho: www.banco-soporte-oficial.net"),
    ("✓ Los bancos usan .com, .com.ar y nombres institucionales limpios", "[OK] Los bancos usan .com, .com.ar y dominios oficiales"),

    ("X ANUNCIO CLON", "[X] ANUNCIO CLON"),
    ("❌ NO TOCAR ESTE ENLACE", "[X] NO TOCAR ESTE ENLACE"),
    ("↓ SCROLLEÁ UN SEGUNDO HACIA ABAJO ↓", "vv SCROLLEÁ UN SEGUNDO HACIA ABAJO vv"),
    ("✓ RESULTADO OFICIAL", "[OK] RESULTADO OFICIAL"),
    ('f"✓ {b_txt}"', 'f"[OK] {b_txt}"'),

    ("✓ GUARDÁ TU BANCO EN FAVORITOS", "[OK] GUARDÁ TU BANCO EN FAVORITOS"),
    ("✓ SCROLLEÁ 2 SEGUNDOS ANTES DE CLIQUEAR", "[OK] SCROLLEÁ 2 SEGUNDOS ANTES DE CLIQUEAR"),
    ("✓ Tus claves y cuentas a salvo con 2 segundos de atención", "[OK] Tus claves y cuentas a salvo con 2 segundos de atención"),
]

cambios = 0
for viejo, nuevo in reemplazos:
    if viejo in texto:
        texto = texto.replace(viejo, nuevo)
        cambios += 1

ruta.write_text(texto, encoding="utf-8")
print(f"Limpieza de tipografia completada! Total reemplazos: {cambios}")

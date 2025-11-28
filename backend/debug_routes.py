"""Script para debuggear rutas académicas"""
import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Crear la aplicación
app = create_app()

print("\n" + "=" * 80)
print("🔍 TODAS LAS RUTAS REGISTRADAS")
print("=" * 80)

academic_routes = []
for rule in app.url_map.iter_rules():
    route_str = f"{rule.methods} {rule.rule}"
    if '/api/academic' in str(rule.rule):
        academic_routes.append(route_str)
        print(f"✅ {route_str}")

print("\n" + "=" * 80)
print(f"📊 Total de rutas académicas: {len(academic_routes)}")
print("=" * 80)

# Buscar específicamente la ruta de escritura
print("\n🔎 Buscando ruta de evaluación de escritura...")
found = False
for rule in app.url_map.iter_rules():
    if 'evaluate-writing' in str(rule.rule):
        print(f"✅ ENCONTRADA: {rule.methods} {rule.rule}")
        found = True
        break

if not found:
    print("❌ NO ENCONTRADA: /api/academic/tools/evaluate-writing")
    print("\n🔍 Rutas que contienen 'tools':")
    for rule in app.url_map.iter_rules():
        if 'tools' in str(rule.rule):
            print(f"   {rule.methods} {rule.rule}")

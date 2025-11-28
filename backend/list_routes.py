"""
Script para listar todas las rutas registradas en Flask
"""
from app import create_app

app = create_app()

print("=" * 80)
print("📋 RUTAS REGISTRADAS EN EL BACKEND")
print("=" * 80)

academic_routes = []
other_routes = []

for rule in app.url_map.iter_rules():
    if '/api/academic' in str(rule):
        academic_routes.append(rule)
    else:
        other_routes.append(rule)

print(f"\n🎓 RUTAS ACADÉMICAS ({len(academic_routes)}):")
print("-" * 80)
for rule in sorted(academic_routes, key=lambda x: str(x)):
    methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
    print(f"  {methods:12} {rule}")

print(f"\n🔧 OTRAS RUTAS ({len(other_routes)}):")
print("-" * 80)
for rule in sorted(other_routes, key=lambda x: str(x))[:20]:  # Solo primeras 20
    methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
    print(f"  {methods:12} {rule}")

# Buscar específicamente la ruta de escritura
print("\n" + "=" * 80)
writing_route = None
for rule in app.url_map.iter_rules():
    if 'evaluate-writing' in str(rule):
        writing_route = rule
        break

if writing_route:
    print("✅ RUTA DE EVALUACIÓN DE ESCRITURA ENCONTRADA:")
    print(f"   Endpoint: {writing_route}")
    print(f"   Métodos: {', '.join(sorted(writing_route.methods - {'HEAD', 'OPTIONS'}))}")
else:
    print("❌ RUTA DE EVALUACIÓN DE ESCRITURA NO ENCONTRADA")
    print("\n🔧 Esto significa que necesitas REINICIAR el backend:")
    print("   1. Ctrl+C en la terminal del backend")
    print("   2. python run.py")

print("=" * 80)

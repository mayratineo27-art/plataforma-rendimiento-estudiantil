from app import create_app

app = create_app()

print("\n🔍 Rutas de Video disponibles:\n")
for rule in app.url_map.iter_rules():
    if 'video' in str(rule) or 'audio' in str(rule):
        print(f"  {rule.methods} {rule}")

print("\n✅ Todas las rutas:\n")
for rule in app.url_map.iter_rules():
    print(f"  {rule.methods} {rule}")

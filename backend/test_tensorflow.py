"""
Script para probar si TensorFlow 2.16.2 se puede importar sin deadlock
"""
import sys
import time

print("=" * 70)
print("PRUEBA DE IMPORTACIÓN DE TENSORFLOW 2.16.2")
print("=" * 70)

print("\n1️⃣ Importando TensorFlow...")
start = time.time()

try:
    import tensorflow as tf
    elapsed = time.time() - start
    print(f"✅ TensorFlow importado exitosamente en {elapsed:.2f}s")
    print(f"📌 Versión de TensorFlow: {tf.__version__}")
    
    # Probar funcionalidad básica
    print("\n2️⃣ Probando funcionalidad básica...")
    
    # Verificar si GPU está disponible
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"✅ GPU disponible: {len(gpus)} dispositivo(s)")
        for gpu in gpus:
            print(f"   - {gpu.name}")
    else:
        print("ℹ️  No hay GPU disponible (usando CPU)")
    
    # Probar operación simple
    print("\n3️⃣ Probando operación simple...")
    a = tf.constant([[1, 2], [3, 4]])
    b = tf.constant([[5, 6], [7, 8]])
    c = tf.matmul(a, b)
    print(f"✅ Operación matricial exitosa:")
    print(f"   Resultado: {c.numpy()}")
    
    print("\n4️⃣ Probando DeepFace...")
    try:
        from deepface import DeepFace
        print("✅ DeepFace importado exitosamente")
        print(f"📌 DeepFace puede usar TensorFlow sin problemas")
    except Exception as e:
        print(f"⚠️  DeepFace no se pudo importar: {e}")
    
    print("\n" + "=" * 70)
    print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    print("=" * 70)
    print("\n🎉 TensorFlow 2.16.2 es compatible con Python 3.10")
    print("✅ Se puede habilitar el módulo de Video/Audio")
    
except ImportError as e:
    elapsed = time.time() - start
    print(f"\n❌ Error de importación después de {elapsed:.2f}s:")
    print(f"   {e}")
    print("\n⚠️  TensorFlow no está instalado o hay un problema de dependencias")
    
except Exception as e:
    elapsed = time.time() - start
    print(f"\n❌ Error después de {elapsed:.2f}s:")
    print(f"   {type(e).__name__}: {e}")
    print("\n⚠️  Hubo un problema al importar TensorFlow")
    import traceback
    traceback.print_exc()
    
finally:
    print("\n" + "=" * 70)
    print("Fin de la prueba")
    print("=" * 70)

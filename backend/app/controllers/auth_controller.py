# backend/app/controllers/auth_controller.py
# CÓDIGO CORREGIDO PARA REGISTRO

from flask import Blueprint, request, jsonify
from app.models.user import User
from app.config.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """
    Endpoint de registro - VERSIÓN CORREGIDA
    """
    try:
        # 1. Obtener datos del request
        data = request.get_json()
        
        # 2. Validar datos requeridos
        if not data:
            return jsonify({
                'success': False,
                'message': 'No se recibieron datos'
            }), 400
        
        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        
        # Validaciones básicas
        if not all([nombre, email, password]):
            return jsonify({
                'success': False,
                'message': 'Faltan campos requeridos: nombre, email, password'
            }), 400
        
        # 3. Verificar si el email ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'El email ya está registrado'
            }), 409
        
        # 4. Hash de la contraseña
        password_hash = generate_password_hash(password)
        
        # 5. Crear nuevo usuario
        nuevo_usuario = User(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            created_at=datetime.now()
        )
        
        # 6. CRÍTICO: Guardar en la base de datos
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()  # ← ESTE ES EL PASO CRÍTICO
            
            # Verificar que se guardó
            db.session.refresh(nuevo_usuario)
            
            print(f"✅ Usuario creado exitosamente: ID={nuevo_usuario.id}, Email={nuevo_usuario.email}")
            
            return jsonify({
                'success': True,
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'id': nuevo_usuario.id,
                    'nombre': nuevo_usuario.nombre,
                    'email': nuevo_usuario.email
                }
            }), 201
            
        except Exception as db_error:
            db.session.rollback()
            print(f"❌ Error al guardar en DB: {str(db_error)}")
            return jsonify({
                'success': False,
                'message': f'Error al guardar en la base de datos: {str(db_error)}'
            }), 500
        
    except Exception as e:
        print(f"❌ Error en registro: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }), 500


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """
    Endpoint de login - VERSIÓN CORREGIDA
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No se recibieron datos'
            }), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({
                'success': False,
                'message': 'Email y contraseña son requeridos'
            }), 400
        
        # CRÍTICO: Buscar usuario por email
        usuario = User.query.filter_by(email=email).first()
        
        if not usuario:
            print(f"⚠️ Usuario no encontrado: {email}")
            return jsonify({
                'success': False,
                'message': 'Credenciales inválidas'
            }), 401
        
        # CRÍTICO: Verificar password
        if not check_password_hash(usuario.password_hash, password):
            print(f"⚠️ Password incorrecto para: {email}")
            return jsonify({
                'success': False,
                'message': 'Credenciales inválidas'
            }), 401
        
        # Login exitoso
        print(f"✅ Login exitoso: {email} (ID: {usuario.id})")
        
        return jsonify({
            'success': True,
            'message': 'Login exitoso',
            'user': {
                'id': usuario.id,  # ← Este debe ser el ID REAL del usuario
                'nombre': usuario.nombre,
                'email': usuario.email
            },
            'token': 'JWT_TOKEN_AQUI'  # Implementar JWT si lo necesitas
        }), 200
        
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }), 500


# ============================================
# CHECKLIST DE PROBLEMAS COMUNES
# ============================================

"""
PROBLEMA 1: Registro dice "exitoso" pero no guarda en DB
✅ SOLUCIÓN: Verificar que db.session.commit() se ejecuta
✅ SOLUCIÓN: Verificar que no hay errores silenciosos en try/except
✅ SOLUCIÓN: Agregar prints para debugging

PROBLEMA 2: Login siempre retorna user_id=1
❌ CAUSA: Estás retornando un usuario hardcodeado
❌ CAUSA: No estás buscando el usuario en la DB
✅ SOLUCIÓN: Usar User.query.filter_by(email=email).first()

PROBLEMA 3: Frontend recibe respuesta pero no es correcta
❌ CAUSA: Backend retorna datos mock en lugar de datos reales
✅ SOLUCIÓN: Eliminar cualquier return hardcodeado

VERIFICACIÓN:
1. Agrega prints en cada paso crítico
2. Revisa los logs del backend al registrar
3. Verifica en MySQL que el usuario se guardó
4. Verifica en MySQL que el login busca al usuario correcto
"""
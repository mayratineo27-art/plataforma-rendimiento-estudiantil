"""
app/routes/auth_routes.py - Rutas de Autenticación
Plataforma Integral de Rendimiento Estudiantil
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app import db
from app.models.user import User
from datetime import datetime

# Crear blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registrar un nuevo usuario
    
    Esperado en el body (JSON):
    {
        "email": "estudiante@universidad.edu",
        "username": "estudiante01",
        "password": "password123",
        "first_name": "Juan",
        "last_name": "Pérez",
        "student_code": "2021-01234",
        "career": "Ingeniería de Sistemas"
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['email', 'username', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': True,
                    'message': f'El campo {field} es requerido'
                }), 400
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'message': 'El correo electrónico ya está registrado'
            }), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'error': True,
                'message': 'El nombre de usuario ya está en uso'
            }), 400
        
        # Crear nuevo usuario
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=generate_password_hash(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name'],
            student_code=data.get('student_code'),
            career=data.get('career'),
            current_cycle=data.get('current_cycle', 1)
        )
        
        # Guardar en la base de datos
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Iniciar sesión
    
    Esperado en el body (JSON):
    {
        "email": "estudiante@universidad.edu",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'error': True,
                'message': 'Email y contraseña son requeridos'
            }), 400
        
        # Buscar usuario
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({
                'error': True,
                'message': 'Credenciales inválidas'
            }), 401
        
        # Verificar si está bloqueado
        if user.is_locked_out():
            return jsonify({
                'error': True,
                'message': f'Cuenta bloqueada. Intenta después de {user.lockout_until}'
            }), 403
        
        # Verificar contraseña
        if not user.check_password(data['password']):
            user.increment_failed_login()
            db.session.commit()
            
            return jsonify({
                'error': True,
                'message': 'Credenciales inválidas',
                'attempts_remaining': max(0, 5 - user.failed_login_attempts)
            }), 401
        
        # Login exitoso
        user.update_last_login()
        db.session.commit()
        
        # TODO: Implementar JWT tokens aquí
        return jsonify({
            'success': True,
            'message': 'Login exitoso',
            'user': user.to_dict()
            # 'token': generate_jwt_token(user)  # A implementar
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al iniciar sesión: {str(e)}'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Cerrar sesión"""
    # TODO: Implementar invalidación de token JWT
    return jsonify({
        'success': True,
        'message': 'Sesión cerrada exitosamente'
    }), 200


@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Obtener perfil del usuario actual
    TODO: Implementar autenticación con JWT
    """
    # TODO: Extraer user_id del token JWT
    # user_id = get_current_user_id_from_token()
    
    return jsonify({
        'message': 'Endpoint protegido - Implementar autenticación JWT'
    }), 501


@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    """
    Actualizar perfil del usuario
    TODO: Implementar autenticación con JWT
    """
    return jsonify({
        'message': 'Endpoint protegido - Implementar autenticación JWT'
    }), 501


@auth_bp.route('/test', methods=['GET'])
def test():
    return {'message': 'Auth routes working'}
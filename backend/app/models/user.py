"""
app/models/user.py - Modelo de Usuario
Plataforma Integral de Rendimiento Estudiantil
"""

from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    Modelo de Usuario/Estudiante
    
    Representa a un estudiante o usuario del sistema con toda su información
    personal, académica y de autenticación.
    """
    
    __tablename__ = 'users'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Información Personal
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    profile_image_url = db.Column(db.String(500))
    
    # Información Académica
    student_code = db.Column(db.String(50), unique=True, index=True)
    career = db.Column(db.String(100))
    current_cycle = db.Column(db.Integer, default=1)
    enrollment_date = db.Column(db.Date)
    
    # Rol y Estado
    role = db.Column(
        db.Enum('student', 'admin', 'instructor', name='user_roles'),
        default='student'
    )
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Seguridad
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    lockout_until = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # Relaciones
    documents = db.relationship(
        'Document', 
        backref='user', 
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    video_sessions = db.relationship(
        'VideoSession',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    audio_sessions = db.relationship(
        'AudioSession',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    profile = db.relationship(
        'StudentProfile',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan'
    )
    
    reports = db.relationship(
        'Report',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __init__(self, email, username, password, first_name, last_name, **kwargs):
        """
        Inicializar usuario
        
        Args:
            email (str): Email del usuario
            username (str): Nombre de usuario
            password (str): Contraseña en texto plano
            first_name (str): Nombre
            last_name (str): Apellido
            **kwargs: Campos opcionales adicionales
        """
        self.email = email
        self.username = username
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def set_password(self, password):
        """
        Hashear y establecer contraseña
        
        Args:
            password (str): Contraseña en texto plano
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verificar contraseña
        
        Args:
            password (str): Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta
        """
        return check_password_hash(self.password_hash, password)
    
    def is_locked_out(self):
        """
        Verificar si la cuenta está bloqueada
        
        Returns:
            bool: True si la cuenta está bloqueada
        """
        if self.lockout_until is None:
            return False
        return datetime.utcnow() < self.lockout_until
    
    def increment_failed_login(self, max_attempts=5, lockout_minutes=15):
        """
        Incrementar contador de intentos fallidos de login
        
        Args:
            max_attempts (int): Máximo de intentos permitidos
            lockout_minutes (int): Minutos de bloqueo
        """
        self.failed_login_attempts += 1
        
        if self.failed_login_attempts >= max_attempts:
            from datetime import timedelta
            self.lockout_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)
    
    def reset_failed_login(self):
        """Resetear contador de intentos fallidos"""
        self.failed_login_attempts = 0
        self.lockout_until = None
    
    def update_last_login(self):
        """Actualizar fecha de último login"""
        self.last_login = datetime.utcnow()
        self.reset_failed_login()
    
    @property
    def full_name(self):
        """Obtener nombre completo"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_student(self):
        """Verificar si es estudiante"""
        return self.role == 'student'
    
    @property
    def is_admin(self):
        """Verificar si es administrador"""
        return self.role == 'admin'
    
    def to_dict(self, include_sensitive=False):
        """
        Convertir usuario a diccionario
        
        Args:
            include_sensitive (bool): Incluir información sensible
            
        Returns:
            dict: Representación del usuario
        """
        data = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'profile_image_url': self.profile_image_url,
            'student_code': self.student_code,
            'career': self.career,
            'current_cycle': self.current_cycle,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'role': self.role,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_sensitive:
            data['failed_login_attempts'] = self.failed_login_attempts
            data['is_locked_out'] = self.is_locked_out()
            data['lockout_until'] = self.lockout_until.isoformat() if self.lockout_until else None
        
        return data
    
    def __repr__(self):
        """Representación string del usuario"""
        return f'<User {self.username} ({self.email})>'
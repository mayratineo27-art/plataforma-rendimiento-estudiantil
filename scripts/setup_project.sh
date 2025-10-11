#!/bin/bash

# ============================================
# Script de Instalación y Configuración
# Plataforma Integral de Rendimiento Estudiantil
# ============================================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Plataforma Integral de Rendimiento Estudiantil             ║"
echo "║  Script de Instalación y Configuración                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con color
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Verificar prerequisitos
echo "══════════════════════════════════════════════════════════════"
echo "1. Verificando prerequisitos..."
echo "══════════════════════════════════════════════════════════════"

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python no está instalado. Por favor instala Python 3.13.8"
    exit 1
fi

# Verificar Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js encontrado: $NODE_VERSION"
else
    print_error "Node.js no está instalado. Por favor instala Node.js 22.20.0"
    exit 1
fi

# Verificar npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_success "npm encontrado: $NPM_VERSION"
else
    print_error "npm no está instalado"
    exit 1
fi

# Verificar Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    print_success "Git encontrado: $GIT_VERSION"
else
    print_error "Git no está instalado"
    exit 1
fi

# Verificar MySQL
if command -v mysql &> /dev/null; then
    MYSQL_VERSION=$(mysql --version)
    print_success "MySQL encontrado"
else
    print_warning "MySQL no detectado. Asegúrate de tenerlo instalado"
fi

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "2. Configurando Backend..."
echo "══════════════════════════════════════════════════════════════"

cd backend

# Crear entorno virtual
print_info "Creando entorno virtual..."
if [ -d "venv" ]; then
    print_warning "El entorno virtual ya existe. Eliminando..."
    rm -rf venv
fi

python3 -m venv venv
print_success "Entorno virtual creado"

# Activar entorno virtual
print_info "Activando entorno virtual..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
print_success "Entorno virtual activado"

# Actualizar pip
print_info "Actualizando pip..."
pip install --upgrade pip
print_success "pip actualizado"

# Instalar dependencias
print_info "Instalando dependencias de Python (esto puede tomar varios minutos)..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Dependencias de Python instaladas correctamente"
else
    print_error "Error al instalar dependencias de Python"
    exit 1
fi

# Descargar modelo de spaCy
print_info "Descargando modelo de spaCy en español..."
python -m spacy download es_core_news_md
print_success "Modelo de spaCy descargado"

# Copiar archivo .env si no existe
if [ ! -f ".env" ]; then
    print_info "Creando archivo .env desde .env.example..."
    cp .env.example .env
    print_success "Archivo .env creado"
    print_warning "¡IMPORTANTE! Edita el archivo .env con tus configuraciones"
else
    print_warning "El archivo .env ya existe. No se sobrescribirá"
fi

# Crear carpetas necesarias
print_info "Creando estructura de carpetas..."
mkdir -p uploads/documents uploads/videos uploads/audio
mkdir -p generated/reports generated/templates
mkdir -p logs
touch uploads/.gitkeep generated/.gitkeep logs/.gitkeep
print_success "Carpetas creadas"

cd ..

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "3. Configurando Frontend..."
echo "══════════════════════════════════════════════════════════════"

cd frontend

# Instalar dependencias
print_info "Instalando dependencias de Node.js (esto puede tomar varios minutos)..."
npm install
if [ $? -eq 0 ]; then
    print_success "Dependencias de Node.js instaladas correctamente"
else
    print_error "Error al instalar dependencias de Node.js"
    exit 1
fi

# Copiar archivo .env si no existe
if [ ! -f ".env" ]; then
    print_info "Creando archivo .env desde .env.example..."
    cp .env.example .env
    print_success "Archivo .env creado"
else
    print_warning "El archivo .env ya existe. No se sobrescribirá"
fi

cd ..

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "4. Configurando Base de Datos..."
echo "══════════════════════════════════════════════════════════════"

print_info "¿Deseas crear la base de datos ahora? (s/n)"
read -r CREATE_DB

if [ "$CREATE_DB" = "s" ] || [ "$CREATE_DB" = "S" ]; then
    print_info "Ingresa la contraseña de MySQL root:"
    read -s MYSQL_PASSWORD
    echo ""
    
    print_info "Creando base de datos..."
    mysql -u root -p"$MYSQL_PASSWORD" < database/schema/01_create_database.sql 2>/dev/null
    
    if [ $? -eq 0 ]; then
        print_success "Base de datos creada correctamente"
        
        print_info "¿Deseas insertar datos de prueba? (s/n)"
        read -r INSERT_SEEDS
        
        if [ "$INSERT_SEEDS" = "s" ] || [ "$INSERT_SEEDS" = "S" ]; then
            mysql -u root -p"$MYSQL_PASSWORD" rendimiento_estudiantil < database/seeds/demo_data.sql 2>/dev/null
            print_success "Datos de prueba insertados"
        fi
    else
        print_warning "No se pudo crear la base de datos automáticamente"
        print_info "Puedes crearla manualmente ejecutando: mysql -u root -p < database/schema/01_create_database.sql"
    fi
else
    print_info "Puedes crear la base de datos más tarde ejecutando:"
    print_info "  mysql -u root -p < database/schema/01_create_database.sql"
fi

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "5. Configuración Completada"
echo "══════════════════════════════════════════════════════════════"
echo ""
print_success "¡Instalación completada exitosamente!"
echo ""
print_info "Próximos pasos:"
echo ""
echo "1. Configura tus variables de entorno:"
echo "   - backend/.env (API keys, configuración de base de datos)"
echo "   - frontend/.env (URL del API)"
echo ""
echo "2. Inicia el backend:"
echo "   cd backend"
echo "   source venv/bin/activate  # o venv\\Scripts\\activate en Windows"
echo "   flask run"
echo ""
echo "3. En otra terminal, inicia el frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "4. Accede a la aplicación:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:5000"
echo ""
print_warning "Recuerda configurar tu API Key de Google Gemini en backend/.env"
echo ""
echo "══════════════════════════════════════════════════════════════"
echo "📚 Documentación completa en: docs/"
echo "🐛 Reportar problemas en: GitHub Issues"
echo "══════════════════════════════════════════════════════════════"
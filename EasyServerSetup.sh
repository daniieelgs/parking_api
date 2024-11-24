#!/bin/bash

# Script de configuración automática del entorno para el proyecto
# Asegúrate de que el archivo tenga permisos de ejecución: chmod +x EasyServerSetup.sh

echo "Bienvenido al asistente de configuración del servidor."

# Función para generar el archivo .env en la raíz
generate_root_env() {
    cat <<EOL > .env
FLASK_DEBUG=1
REDIS_HOST=redis
REDIS_PORT=6379
API_VERSION=preview 1.0
REDIS_URL=redis://redis:6379/0
DB_USER=USERNAME
DB_PASSWORD=PASSWORD
DB_HOST=database
DB_PORT=3306
DB_NAME=parking
GOOGLE_MAPS_API_KEY=<API-KEY-DE-GOOGLE-MAPS>
HMAC_SECRET_KEY=<HMAC-SECRET-KEY>
EOL
    echo "Archivo .env generado en la raíz del proyecto."
}

# Función para generar el archivo .env en la carpeta docker
generate_docker_env() {
    cat <<EOL > docker/.env
PORT=5000
FLASK_ENV=development
HOST=0.0.0.0
FLASK_RUN_WORKERS=5
FLASK_RUN_TIMEOUT=60
REDIS_EXPOSE_PORT=6379
MYSQL_ROOT_PASSWORD=PASSWORD
MYSQL_DATABASE=parking
MYSQL_USER=USERNAME
MYSQL_PASSWORD=PASSWORD
DB_EXPOSE_PORT=3306
PHPMYADMIN_EXPOSE_PORT=80
EOL
    echo "Archivo .env generado en la carpeta docker."
}

# Verificar si los archivos .env ya existen
if [ -f ".env" ]; then
    read -p "El archivo .env en la raíz ya existe. ¿Deseas sobrescribirlo? (y/n): " OVERWRITE_ROOT
    if [ "$OVERWRITE_ROOT" = "y" ]; then
        generate_root_env
    else
        echo "Archivo .env en la raíz no modificado."
    fi
else
    generate_root_env
fi

if [ -f "docker/.env" ]; then
    read -p "El archivo .env en la carpeta docker ya existe. ¿Deseas sobrescribirlo? (y/n): " OVERWRITE_DOCKER
    if [ "$OVERWRITE_DOCKER" = "y" ]; then
        generate_docker_env
    else
        echo "Archivo .env en la carpeta docker no modificado."
    fi
else
    generate_docker_env
fi

# Preguntar al usuario si quiere configuración para desarrollo o producción
read -p "¿Deseas configurar el entorno en modo Desarrollo (dev) o Producción (pro)? (dev/pro): " ENVIRONMENT

if [ "$ENVIRONMENT" = "dev" ]; then
    echo "Configuración para el entorno de desarrollo seleccionada."

    # Verificar si Python está instalado
    if ! command -v python3 &> /dev/null; then
        echo "Python3 no está instalado. Por favor, instálalo antes de continuar."
        exit 1
    fi

    # Verificar si el entorno virtual existe
    if [ ! -d "venv" ]; then
        echo "Creando entorno virtual..."
        python3 -m venv venv
    fi

    echo "Activando entorno virtual..."
    source venv/bin/activate

    echo "Instalando dependencias..."
    pip install --upgrade pip
    pip install -r requirements.txt

    echo "Iniciando la aplicación en modo desarrollo..."
    python3 app.py

elif [ "$ENVIRONMENT" = "pro" ]; then
    echo "Configuración para el entorno de producción seleccionada."

    # Verificar si Docker está instalado
    if ! command -v docker &> /dev/null; then
        echo "Docker no está instalado. Por favor, instálalo antes de continuar."
        exit 1
    fi

    # Verificar si Docker Compose está instalado
    if ! command -v docker-compose &> /dev/null; then
        echo "Docker Compose no está instalado. Por favor, instálalo antes de continuar."
        exit 1
    fi

    echo "Configurando contenedores de Docker..."
    docker-compose -f docker/docker-compose.yml up -d

    echo "Despliegue en producción completado. Los contenedores están corriendo."
else
    echo "Opción inválida. Por favor, elige 'dev' o 'pro'."
    exit 1
fi

echo "Configuración finalizada. Todo listo."

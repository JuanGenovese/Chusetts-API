#!/bin/bash

# Determinar el directorio raíz del backend donde reside este script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "${SCRIPT_DIR}" || exit 1

export PYTHONPATH="${SCRIPT_DIR}"

# Activar el entorno virtual si existe
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Activando entorno virtual (venv)..."
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "Activando entorno virtual (.venv)..."
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    echo "Activando entorno virtual Windows (venv)..."
else
    echo "Advertencia: No se encontró entorno virtual en ${SCRIPT_DIR}"
fi

echo "🚀 Iniciando Chusetts Backend API en http://localhost:8000 (Swagger: http://localhost:8000/docs)..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

FROM python:3.11-slim

# Evitar escritura de bytecode y forzar salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copiar definicion de dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el codigo fuente
COPY . .

# Permisos de ejecucion para el script de inicio
RUN chmod +x start_service.sh

EXPOSE 8000

CMD ["./start_service.sh"]

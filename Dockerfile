FROM python:3.11

WORKDIR /code

# 1. Copiamos los requisitos e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copiamos TODO el contenido del proyecto (necesario para Alembic)
# Esto copiará app/, alembic/, alembic.ini, etc.
COPY . .

# 3. Configuramos el path para que Python encuentre los módulos
ENV PYTHONPATH=/code

# 4. Comando final corregido:
# Ejecutamos las migraciones y luego iniciamos la aplicación.
# Usamos "sh -c" para poder encadenar comandos con "&&"
CMD ["sh", "-c", "python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 10000"]
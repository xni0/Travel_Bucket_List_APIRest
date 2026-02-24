FROM python:3.11

WORKDIR /code

# Copio los requisitos e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copio todo el contenido del proyecto (es necesario para Alembic)
COPY . .

# Configuro el path para que Python encuentre los módulos
ENV PYTHONPATH=/code

# Ejecuto las migraciones y luego inicio la aplicación.
# Uso "sh -c" para poder encadenar comandos con "&&"
CMD ["sh", "-c", "python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 10000"]
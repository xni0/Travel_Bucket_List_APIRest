FROM python:3.11

WORKDIR /code

# Copiamos los requisitos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido de la carpeta app actual al directorio de trabajo
COPY ./app /code/app

# Importante: Para que Python encuentre los módulos dentro de /app
ENV PYTHONPATH=/code

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
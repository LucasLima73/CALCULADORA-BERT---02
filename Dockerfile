# Use uma imagem base do Python
FROM python:3.9-slim

# Instalar dependências do sistema para PySide6, OpenGL e bibliotecas gráficas
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libxkbcommon0 \
    libegl1 \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do seu projeto para o diretório de trabalho no container
COPY . .

# Instalar as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Definir o comando de inicialização do container
CMD ["python3", "calculadora.py"]

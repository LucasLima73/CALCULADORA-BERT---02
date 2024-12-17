# Use uma imagem base do Python
FROM python:3.9-slim

# Instalar dependências do sistema necessárias para PySide6 e bibliotecas gráficas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libegl1 \
    libxkbcommon0 \
    libfontconfig1 \
    libfreetype6 \
    libglib2.0-0 \
    libdbus-1-3 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxi6 \
    libxrender1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho no container
COPY . .

# Instalar as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que será utilizada (substitua 8080 pela porta que sua aplicação usa)
EXPOSE 8080

# Configurar a variável de ambiente para exibir o aplicativo no host
ENV QT_QPA_PLATFORM=offscreen

# Definir o comando de inicialização do container
CMD ["python3", "calculadora.py"]

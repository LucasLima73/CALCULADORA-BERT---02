# Use uma imagem base do Python
FROM python:3.9-slim

# Instalar dependências do sistema necessárias para PySide6 e bibliotecas gráficas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libegl1 \
    libxkbcommon0 \
    libfontconfig1 \
    libglib2.0-0 \
    libdbus-1-3 \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no container
WORKDIR /app

# Instalar as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baixar os arquivos do modelo BERT durante o build
RUN python -c "from transformers import BertTokenizer, BertModel; \
    BertTokenizer.from_pretrained('bert-base-uncased'); \
    BertModel.from_pretrained('bert-base-uncased')"

# Copiar os arquivos do projeto para o diretório de trabalho no container
COPY . .

# Configurar a variável de ambiente para exibir o aplicativo no host (se necessário)
ENV QT_QPA_PLATFORM=offscreen

# Definir o comando de inicialização do container
CMD ["python3", "calculadora.py"]

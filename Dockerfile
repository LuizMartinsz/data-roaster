# Usa uma imagem Python leve e segura
FROM python:3.10-slim

# Define diretório de trabalho no container
WORKDIR /app

# Instala dependências do sistema necessárias para compilar algumas libs (se precisar)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o requirements primeiro (cache layer do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Variáveis de ambiente padrão (podem ser sobrescritas no run)
ENV FLASK_APP=run.py

# Comando para rodar (em prod usaríamos gunicorn, mas pro MVP isso serve)
CMD ["python", "run.py"]
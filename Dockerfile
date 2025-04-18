# Imagem base oficial do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos necessários para o contêiner
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código-fonte
COPY . .

# Criar diretório para arquivos estáticos
RUN mkdir -p /app/staticfiles

# Expor a porta onde a aplicação rodará
EXPOSE 8000

# Comando para iniciar o servidor Gunicorn
CMD ["gunicorn", "auth_api.wsgi:application", "--bind", "0.0.0.0:8000"]
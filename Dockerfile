# Use a imagem base do Python
FROM python:3.8-slim

# Defina o diretório de trabalho
WORKDIR /app

# Instale as dependências do seu aplicativo
RUN pip install streamlit requests folium streamlit-folium

# Copie os arquivos do projeto para o diretório de trabalho
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "clima.py", "--server.port=8501", "--server.address=0.0.0.0"]


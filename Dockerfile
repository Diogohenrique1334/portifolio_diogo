# syntax=docker/dockerfile:1

# ==============================================================
# Portfólio Streamlit — Diogo Oliveira
# Imagem enxuta baseada em Python slim, rodando como usuário
# não-root e com healthcheck no endpoint nativo do Streamlit.
# ==============================================================
FROM python:3.12-slim

# Não gerar .pyc e não bufferizar stdout/stderr (logs em tempo real)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 1) Instala dependências primeiro para aproveitar o cache de camadas:
#    só reinstala quando requirements.txt mudar.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copia o código da aplicação (respeitando o .dockerignore)
COPY . .

# 3) Cria usuário sem privilégios e cede a posse do app a ele
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

# Porta padrão do Streamlit
EXPOSE 8501

# Healthcheck no endpoint interno de saúde do Streamlit
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://localhost:8501/_stcore/health').status==200 else sys.exit(1)"

# Binding explícito para 0.0.0.0 (acessível fora do container).
# Não depende do .streamlit/config.toml para as flags de servidor.
CMD ["streamlit", "run", "Home.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]

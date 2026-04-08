FROM python:3.13-slim
git push origin 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos apenas o motor essencial
RUN pip install --no-cache-dir "fastapi[standard]"

# Porta padrão alinhada ao seu Traefik
EXPOSE 8000

# Comando direto, limpo e rápido
# O '--proxy-headers' é importante porque você está atrás do Traefik (Reverse Proxy)
CMD ["python", "-m", "uvicorn", "fast_zero.app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
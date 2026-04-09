FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# O SEGREDO ESTÁ AQUI: Incluir os módulos que o código precisa
RUN pip install --no-cache-dir \
    "fastapi[standard]" \
    sqlalchemy \
    pydantic-settings \
    requests \
    beautifulsoup4 \
    gspread

# Expõe a porta para o Traefik
EXPOSE 8000

# Comando de inicialização
CMD ["python", "-m", "uvicorn", "fast_zero.app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
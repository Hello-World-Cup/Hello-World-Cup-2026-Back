FROM python:3.11-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    git \
    make \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

FROM base AS production
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "app.adapters.routing.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS local
RUN pip install debugpy
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "app.adapters.routing.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
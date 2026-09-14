# --- Build Stage ---
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# Устанавливаем PyTorch CPU (без тяжелых CUDA зависимостей) и остальные пакеты
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Предзагружаем веса модели эмбеддингов в кэш образа для мгновенного старта офлайн
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('cointegrated/rubert-tiny2')"


# --- Final Stage ---
FROM python:3.11-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    HF_HOME="/home/appuser/.cache/huggingface"

WORKDIR /app

# Копируем виртуальное окружение и кэш HuggingFace моделей
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /root/.cache /home/appuser/.cache

# Копируем исходный код приложения и предзаполненную базу фильмов
COPY config.py main.py ./
COPY bot_features/ ./bot_features/
COPY database/ ./database/
COPY kinopoisk_generated_client/ ./kinopoisk_generated_client/
COPY kp_sdk/ ./kp_sdk/
COPY recommendation/ ./recommendation/
COPY seed_database.db ./seed_database.db
COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x entrypoint.sh && \
    useradd -mr -u 1000 appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app /home/appuser/.cache

USER appuser

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "main.py"]

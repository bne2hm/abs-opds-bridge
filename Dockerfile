FROM alt:sisyphus

WORKDIR /app

# Установка Python и зависимостей для сборки
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-module-pip \
    gcc \
    libxml2-devel \
    libxslt-devel \
    python3-dev \
    && apt-get clean && \
    rm -rf /var/cache/apt

# Копирование requirements.txt и установка зависимостей Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Копирование исходного кода приложения
COPY opds_bridge/ ./opds_bridge/

# Создание непривилегированного пользователя
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Переменные окружения (значения по умолчанию, будут переопределены при запуске)
ENV ABS_BASE="" \
    ABS_TOKEN="" \
    OPDS_BASIC_USER="" \
    OPDS_BASIC_PASS="" \
    CACHE_TTL_DEFAULT=30

# Порт, на котором слушает приложение
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "opds_bridge.main:app", "--host", "0.0.0.0", "--port", "8000"]

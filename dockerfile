FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей, включая git
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Копируем только pyproject.toml (без poetry.lock)
COPY pyproject.toml /app/

# Устанавливаем Poetry и зависимости
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --no-cache

# Копируем остальные файлы проекта
COPY . /app/

# Команда для запуска
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

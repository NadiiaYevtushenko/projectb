# Встановлюємо базовий образ Python
FROM python:3.12-slim

# Встановлюємо залежності для операційної системи
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Встановлюємо залежності для Python
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Копіюємо весь проект до контейнера
COPY . /app

# Встановлюємо робочу директорію
WORKDIR /app

# Задаємо змінну оточення для Django
ENV DJANGO_SETTINGS_MODULE=projectb.settings

# Вказуємо порт, який буде використовуватися
EXPOSE 8000

# Команда для запуску сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

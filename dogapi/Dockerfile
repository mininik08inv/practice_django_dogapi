FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создаем пользователя
RUN adduser --disabled-password dog-user

USER dog-user

# установливаем рабочий каталог
WORKDIR /code

# Копируем и устанавливаем зависимости
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY . /code/

# Открываем потр
EXPOSE 8000

# Команда для запуска проета
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
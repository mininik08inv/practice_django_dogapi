# Dog Breed API

API для управления информацией о собаках и их породах с дополнительной аналитикой.

## Оглавление
1. [Установка и запуск](#установка-и-запуск)
2. [Архитектура проекта](#архитектура-проекта)
3. [Использование API](#использование-api)
4. [Примеры запросов](#примеры-запросов)
5. [Тестирование](#тестирование)

## Установка и запуск

### Требования
- Docker и Docker Compose
- Python 3.9+

### 1. Клонирование репозитория
```bash
git clone https://github.com/mininik08inv/practice_django_dogapi.git
cd dog-api
```

### 2. Настройка окружения
Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

### 3. Запуск с Docker
```bash
docker-compose up --build
```

### 4. Миграции и суперпользователь
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу: `http://localhost:8000/`

## Архитектура проекта

### Основные компоненты
- **Модели**:
  - `Breed` - породы собак с характеристиками
  - `Dog` - собаки с ссылкой на породу

- **API Endpoints**:
  - `/api/dogs/` - управление собаками
  - `/api/breeds/` - управление породами


### Технологии
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL
- Docker

## Использование API

### Аутентификация
API работает без аутентификации (для тестового режима). В production рекомендуется добавить аутентификацию.

### Доступные методы

#### Для собак (`/api/dogs/`)
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/dogs/` | Список всех собак со средним возрастом по породам |
| POST | `/api/dogs/` | Создание новой собаки |
| GET | `/api/dogs/<id>/` | Получение конкретной собаки (с количеством собак той же породы) |
| PUT | `/api/dogs/<id>/` | Обновление собаки |
| DELETE | `/api/dogs/<id>/` | Удаление собаки |

#### Для пород (`/api/breeds/`)
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/breeds/` | Список всех пород с количеством собак |
| POST | `/api/breeds/` | Создание новой породы |
| GET | `/api/breeds/<id>/` | Получение конкретной породы |
| PUT | `/api/breeds/<id>/` | Обновление породы |
| DELETE | `/api/breeds/<id>/` | Удаление породы |

## Примеры запросов

### 1. Создание породы
```bash
POST /api/breeds/
Content-Type: application/json

{
    "name": "Labrador",
    "size": "Large",
    "friendliness": 5,
    "trainability": 4,
    "shedding_amount": 3,
    "exercise_needs": 4
}
```

### 2. Создание собаки
```bash
POST /api/dogs/
Content-Type: application/json

{
    "name": "Rex",
    "age": 3,
    "breed": 1,
    "gender": "Male",
    "color": "Black",
    "favorite_food": "Meat",
    "favorite_toy": "Ball"
}
```

### 3. Получение списка собак
```bash
GET /api/dogs/
```
Ответ будет содержать поле `average_age` с средним возрастом по породе.

### 4. Получение конкретной собаки
```bash
GET /api/dogs/1/
```
Ответ будет содержать поле `same_breed_count` с количеством собак той же породы.

### 5. Получение списка пород
```bash
GET /api/breeds/
```
Ответ будет содержать поле `dogs_count` с количеством собак каждой породы.

## Тестирование

Для запуска тестов:
```bash
docker-compose exec web python manage.py test dogs.tests
```

Тесты проверяют:
- Все эндпоинты API
- Корректность данных

---

Для доступа к административной панели:
1. Перейдите по адресу `http://localhost:8000/admin/`
2. Используйте учетные данные суперпользователя
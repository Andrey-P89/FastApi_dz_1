# FastAPI API для объявлений

REST API сервис для объявлений купли/продажи.

## Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```
## Переменные окружения

Файл `.env` должен содержать:

```env
POSTGRES_USER=postgres          # Имя пользователя БД
POSTGRES_PASSWORD=postgres      # Пароль БД
POSTGRES_DB=advertisement_db    # Название БД
POSTGRES_HOST=db                # для Docker; для локального запуска замените на localhost
POSTGRES_PORT=5432              # Порт БД
```
# Запуск
## Через Docker (рекомендуется)

1. Скопировать настройки окружения
```bash
cp .env.example .env
```

2. Запустить контейнеры
```bash
docker-compose up --build -d
```
3. Проверить работу
```bash
# Открыть в браузере http://localhost:8080/docs
```
## Локальный запуск (с PostgreSQL на хосте)

**Требования:**
- Python 3.11+
- PostgreSQL установлен и запущен

**Шаги:**

```bash
# 1. Скопировать настройки окружения
cp .env.example .env

# 2. Отредактировать .env (указать данные своей БД)
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=твой_пароль
POSTGRES_DB=advertisement_db
POSTGRES_PORT=5432

# 3. Создать базу данных
psql -U postgres -c "CREATE DATABASE advertisement_db;"

# 4. Установить зависимости
pip install -r requirements.txt

# 5. Запустить приложение
uvicorn app.main:app --reload --port 8080
```
## Примеры запросов

```bash
# Создать объявление
curl -X POST http://localhost:8080/v1/ad \
  -H "Content-Type: application/json" \
  -d '{"title":"iPhone 15","description":"Отличное состояние","price":70000,"author":"Алексей"}'

# Получить объявление
curl http://localhost:8080/v1/ad/1

# Обновить объявление
curl -X PATCH http://localhost:8080/v1/ad/1 \
  -H "Content-Type: application/json" \
  -d '{"price":65000}'

# Удалить объявление
curl -X DELETE http://localhost:8080/v1/ad/1

# Поиск по полям
curl "http://localhost:8080/v1/ad?title=iPhone&price_min=60000&price_max=80000"
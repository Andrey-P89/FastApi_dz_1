# FastAPI API для объявлений

## Запуск

```bash
# 1. Запустить БД и приложение
docker-compose up --build -d

# 2. Проверить работу
# Открыть в браузере http://localhost:8080/docs
```
## Остановка

```bash
docker-compose down
```

## Настройки
Переименуйте `.env.example` в `.env` и при необходимости измените параметры.

## Переменные окружения

Файл `.env` должен содержать:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=advertisement_db
POSTGRES_HOST=db      # для Docker; для локального запуска замените на localhost
POSTGRES_PORT=5432
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
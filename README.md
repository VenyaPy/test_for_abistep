# FastAPI User Balance Service

Небольшой REST-сервис на [FastAPI](https://fastapi.tiangolo.com/), управляющий списком пользователей и их балансом. Хранение данных осуществляется в памяти.

## Возможности

- `POST /users` — создание пользователя (параметры: `name`, `email`, `balance`). Email должен быть уникальным.
- `GET /users` — получение списка пользователей.
- `POST /transfer` — перевод между пользователями (параметры: `from_user_id`, `to_user_id`, `amount`). Проверяется наличие средств и запрет перевода самому себе.
- `GET /ping` — проверка доступности сервиса. Все запросы требуют заголовок `x-api-key` со значением, указанным в переменной окружения `API_KEY`.

## Локальный запуск

```bash
docker-compose up --build
```

Сервис будет доступен по адресу http://localhost:8150.

## Запуск в Docker Swarm

Соберите и запушьте образ, затем разверните стек:

```bash
export IMAGE_TAG=registry.example.com/project/app:latest
docker stack deploy --compose-file itat-stack-swarm.yaml itat-stack
```

## Тесты

```bash
pytest
```

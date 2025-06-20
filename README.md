# Сервис-балансировщик

## Описание

Простой сервис-балансировщик пользовательских
запросов, перенаправляющий пользователя с помощью 301-го HTTP
редиректа смотреть фильм либо на корневые сервера, либо отправлять его в CDN по
определённым правилам.

## Используемые технологии

- **FastAPI**
- **asyncpg**
- **redis**
- **dbmate** — миграции
- **dishka** — DI-контейнер
- **locust** — нагрузочный тестировщик, чтобы можно было посмотреть рпс на графике:)

## Запуск

1. **Клон репозитория:**

   ```sh
   git clone https://github.com/fookashi/fastapi_simple_balancer.git
   cd fastapi_simple_balancer
   ```
2. **Запуск приложения:**

   ```sh
   make up
   ```
3. **Применение миграций:**

   ```sh
   make migrate
   ```
4. **Посмотреть логи сервисов:**

   ```sh
   make logs
   ```
5. **Остановка приложения:**

   ```sh
   make down
   ```

## Куда можно зайти:

- localhost:8000 - FastAPI-балансировщик (OpenAPI path - localhost:8000/docs)
- localhost:8089 - Locust для нагрузочного теста

## API

### Балансировка

- **GET /**

  - Параметры: `video: URL`
  - ****Ответ (код 301): `Redirect-ответ с вложенным хэдером location - урлом куда нужно отправить пользователя`

### Управление CDN-конфигом

- **GET /config**
  - Получить текущий CDN-конфиг
  - Парметры: `id: int | null`
  - Ответ (код 200):
    ```json{
    {
      "id": int,
      "cdn_host": string,
      "distribution_rate": int,
      "created_at": datetime,
      "updated_at": datetime
    }
    ```
- **PATCH /config**
  - Изменить конфиг (можно менять только нужные поля)
  - Тело запроса:

    ```
    {
      "id": int,
      "cdn_host": string | null,
      "distribution_rate": int | null
    }
    ```
  - Тело ответа (код 200):

    ```json{
    {
      "id": int,
      "cdn_host": string,
      "distribution_rate": int,
      "created_at": datetime,
      "updated_at": datetime
    }
    ```

## Чего не хватает:

- Нет аутентификации/авторизации
- Нет рейт лимитера
- Нет полноценного логирования и мониторинга
- Нет CI/CD
- Нет версионирования и истории изменений конфига

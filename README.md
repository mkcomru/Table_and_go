# Table & Go - Руководство для фронтенд-разработчика

## Содержание
1. [Установка и запуск](#установка-и-запуск)
2. [Структура API](#структура-api)
3. [API-эндпоинты](#api-эндпоинты)
   - [Заведения](#заведения)
   - [Филиалы](#филиалы)
   - [Бронирование](#бронирование)
   - [Пользователи](#пользователи)

## Установка и запуск

### Предварительные требования
- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/) (обычно включен в Docker Desktop)

### Шаги по установке

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/mkcomru/Table_and_go
   cd web
   ```
    не уверен насчет рабочейпапки, поймешь
    
2. **Запуск с помощью Docker**
   ```bash
   docker-compose up --build
   ```
   
   При первом запуске это займет некоторое время, так как Docker:
   - Скачает необходимые образы
   - Соберет контейнеры
   - Создаст и инициализирует базу данных PostgreSQL
   - Выполнит миграции Django
   - Заполнит базу данных начальными данными (районы, кухни, заведения, филиалы, столики)

3. **Доступ к приложению**  
   После успешного запуска API будет доступно по адресу:
   ```
   http://localhost:8000/api/
   ```

4. **Остановка приложения**  
   Для остановки приложения используйте комбинацию клавиш `Ctrl+C` в терминале, где запущен Docker, затем выполните:
   ```bash
   docker-compose down
   ```

5. **Запуск без перестроения контейнеров**  
   Если вы не вносили изменения в файлы Docker:
   ```bash
   docker-compose up
   ```

## Структура API

### Основные модели данных

1. **Заведение (Establishment)**
   - Имеет тип (ресторан/бар)
   - Содержит основную информацию (название, описание, email)
   - Связано с типами кухни и имеет один или несколько филиалов

2. **Филиал (Branch)**
   - Привязан к конкретному заведению
   - Имеет адрес, телефон, средний чек
   - Содержит часы работы, доступные столики

3. **Столик (Table)**
   - Принадлежит определенному филиалу
   - Имеет номер, вместимость и статус доступности

4. **Бронирование (Booking)**
   - Связывает пользователя, филиал и столик
   - Содержит информацию о дате, времени и продолжительности бронирования
   - Имеет статус (ожидает подтверждения, подтверждено, отменено, завершено)

5. **Пользователь (User)**
   - Содержит личные данные (имя, фамилия, email, телефон)
   - Может иметь роли (обычный пользователь, администратор)

## API-эндпоинты

Базовый URL API: `http://localhost:8000/api/`

### Заведения

#### Получение списка заведений (GET `/api/establishments/`)

**Описание**: Получение списка всех заведений с основной информацией.

**Параметры запроса**:
- `type`: Тип заведения (`restaurant` или `bar`)

**Пример запроса**:
```http
GET /api/establishments/?type=restaurant
```

**Пример ответа**:
```json
[
  {
    "id": 1,
    "name": "Супра",
    "establishment_type": "restaurant",
    "photo": "/static/images/default-restaurant.jpg",
    "cuisine_types": ["Грузинская", "Русская"],
    "average_check": "1500.00",
    "address": "ул. Светланская, 1",
    "average_rating": 0,
    "branches_count": 1
  },
  {
    "id": 2,
    "name": "Миллионка",
    "establishment_type": "restaurant",
    "photo": "/static/images/default-restaurant.jpg",
    "cuisine_types": ["Русская"],
    "average_check": "2000.00",
    "address": "ул. Светланская, 2",
    "average_rating": 0,
    "branches_count": 1
  }
]
```

### Филиалы

#### Получение списка филиалов (GET `/api/branch/`)

**Описание**: Получение списка всех филиалов заведений.

**Параметры фильтрации**:
- `type`: Тип заведения (`restaurant` или `bar`)
- `district`: ID района
- `rating`: Минимальный рейтинг
- `check`: Минимальный средний чек
- `cuisine_id`: ID кухни

**Пример запроса**:
```http
GET /api/branch/?district=1&cuisine_id=4
```

**Пример ответа**:
```json
[
  {
    "id": 1,
    "name": "Филиал 1",
    "address": "ул. Светланская, 1",
    "district": "Центральный",
    "phone": "2340001",
    "average_check": "1500.00",
    "is_main": true,
    "establishment_name": "Супра",
    "establishment_type": "restaurant",
    "photo": "/static/images/default-restaurant.jpg",
    "rating": 0,
    "working_hours": [
      {
        "day_of_week": 0,
        "day_name": "Понедельник",
        "status": "10:00 - 22:00",
        "is_closed": false
      },
      {
        "day_of_week": 1,
        "day_name": "Вторник",
        "status": "10:00 - 22:00",
        "is_closed": false
      },
      {
        "day_of_week": 5,
        "day_name": "Суббота",
        "status": "10:00 - 23:00",
        "is_closed": false
      },
      {
        "day_of_week": 6,
        "day_name": "Воскресенье",
        "status": "10:00 - 23:00",
        "is_closed": false
      }
    ],
    "tables_count": 4,
    "available_tables_count": 4,
    "cuisine_types": ["Грузинская", "Русская"]
  }
]
```

#### Получение доступных столиков (GET `/api/branch/{id}/available_tables/`)

**Описание**: Получение списка доступных столиков в филиале на указанное время.

**Параметры запроса**:
- `datetime`: Дата и время бронирования (формат ISO: YYYY-MM-DDTHH:MM:SS)
- `capacity`: Минимальная вместимость столика

**Пример запроса**:
```http
GET /api/branch/1/available_tables/?datetime=2025-04-10T19:00:00&capacity=4
```

**Пример ответа**:
```json
[
  {
    "id": 1,
    "number": 1,
    "capacity": 4,
    "status": "available"
  },
  {
    "id": 3,
    "number": 3,
    "capacity": 6,
    "status": "available"
  }
]
```

### Бронирование

#### Создание бронирования (POST `/api/bookings/`)

**Описание**: Создание нового бронирования столика.

**Пример запроса**:
```http
POST /api/bookings/
Content-Type: application/json
Authorization: Bearer <ваш_токен>

{
  "branch": 1,
  "table": 3,
  "booking_datetime": "2025-04-10T19:00:00",
  "duration": 2,
  "guests_count": 4,
  "special_requests": "Хотел бы столик у окна, если возможно"
}
```

**Пример ответа**:
```json
{
  "id": 1,
  "branch": {
    "id": 1,
    "name": "Филиал 1",
    "establishment": {
      "id": 1,
      "name": "Супра"
    }
  },
  "table": {
    "id": 3,
    "number": 3,
    "capacity": 6
  },
  "booking_datetime": "2025-04-10T19:00:00",
  "duration": 2,
  "guests_count": 4,
  "special_requests": "Хотел бы столик у окна, если возможно",
  "status": "pending",
  "created_at": "2025-04-09T12:34:56.789Z"
}
```

#### Получение информации о бронировании (GET `/api/bookings/{id}/`)

**Описание**: Получение подробной информации о конкретном бронировании.

**Пример запроса**:
```http
GET /api/bookings/1/
Authorization: Bearer <ваш_токен>
```

**Пример ответа**:
```json
{
  "id": 1,
  "branch": {
    "id": 1,
    "name": "Филиал 1",
    "establishment": {
      "id": 1,
      "name": "Супра"
    }
  },
  "table": {
    "id": 3,
    "number": 3,
    "capacity": 6
  },
  "booking_datetime": "2025-04-10T19:00:00",
  "duration": 2,
  "guests_count": 4,
  "special_requests": "Хотел бы столик у окна, если возможно",
  "status": "pending",
  "created_at": "2025-04-09T12:34:56.789Z",
  "updated_at": "2025-04-09T12:34:56.789Z"
}
```

#### Отмена бронирования (PUT `/api/bookings/{id}/cancel/`)

**Описание**: Отмена существующего бронирования.

**Пример запроса**:
```http
PUT /api/bookings/1/cancel/
Authorization: Bearer <ваш_токен>
```

**Пример ответа**:
```json
{
  "id": 1,
  "status": "cancelled",
  "message": "Бронирование успешно отменено"
}
```

### Пользователи

#### Регистрация пользователя (POST `/api/auth/register/`)

**Описание**: Регистрация нового пользователя.

**Пример запроса**:
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "phone": "9991112233",
  "password": "securePassword123",
  "first_name": "Иван",
  "last_name": "Иванов"
}
```

**Пример ответа**:
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "phone": "9991112233",
    "first_name": "Иван",
    "last_name": "Иванов"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Авторизация пользователя (POST `/api/auth/login/`)

**Описание**: Вход пользователя в систему.

**Пример запроса**:
```http
POST /api/auth/login/
Content-Type: application/json

{
  "phone": "9991112233",
  "password": "securePassword123"
}
```

**Пример ответа**:
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "phone": "9991112233",
    "first_name": "Иван",
    "last_name": "Иванов"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Получение профиля пользователя (GET `/api/auth/profile/`)

**Описание**: Получение информации о профиле текущего пользователя.

**Пример запроса**:
```http
GET /api/auth/profile/
Authorization: Bearer <ваш_токен>
```

**Пример ответа**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "phone": "9991112233", 
  "first_name": "Иван",
  "last_name": "Иванов",
  "photo": null,
  "bookings": [
    {
      "id": 1,
      "branch": {
        "id": 1,
        "name": "Филиал 1",
        "establishment": {
          "id": 1,
          "name": "Супра"
        }
      },
      "booking_datetime": "2025-04-10T19:00:00",
      "status": "pending"
    }
  ]
}
```

## Дополнительная информация

### Коды статусов HTTP

- `200 OK`: Запрос выполнен успешно
- `201 Created`: Ресурс создан успешно
- `400 Bad Request`: Некорректный запрос (проверьте отправляемые данные)
- `401 Unauthorized`: Требуется авторизация
- `403 Forbidden`: Доступ запрещен
- `404 Not Found`: Ресурс не найден
- `500 Internal Server Error`: Внутренняя ошибка сервера

### Аутентификация

Для доступа к защищенным эндпоинтам используйте токен JWT в заголовке:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Пагинация

Для запросов, возвращающих списки объектов, используется пагинация:

```http
GET /api/establishments/?page=2&page_size=10
```

**Параметры**:
- `page`: Номер страницы (по умолчанию 1)
- `page_size`: Количество объектов на странице (по умолчанию 10, максимум 100)

**Пример ответа с пагинацией**:
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/establishments/?page=3&page_size=10",
  "previous": "http://localhost:8000/api/establishments/?page=1&page_size=10",
  "results": [
    // список объектов
  ]
}
```

### Общие параметры фильтрации

Многие эндпоинты поддерживают дополнительные параметры фильтрации:

- `search`: Поиск по текстовым полям
- `ordering`: Сортировка (например, `ordering=name` или `ordering=-created_at` для обратной сортировки)

### Структура данных в базе

При запуске проекта в базе данных создаются следующие начальные данные:

- **Районы**: Центральный, Первореченский, Ленинский, Первомайский, Советский
- **Кухни**: Русская, Итальянская, Японская, Грузинская, Китайская, и другие
- **Заведения**: Несколько ресторанов с разными типами кухни
- **Филиалы**: По 1-2 филиала для каждого заведения с адресами
- **Столики**: Несколько столиков разной вместимости в каждом филиале
- **Часы работы**: График работы для каждого филиала (Пн-Чт: 10:00-22:00, Пт-Вс: 10:00-23:00)

---

При возникновении вопросов или проблем, обращайтесь к бэкенд-разработчику проекта.

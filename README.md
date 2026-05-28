# Foodgram

**Foodgram** — учебный fullstack-проект: онлайн-сервис для публикации рецептов, подписок на авторов, добавления рецептов в избранное и формирования списка покупок.

Проект состоит из backend API на Django REST Framework, frontend-приложения на React и инфраструктуры для запуска через Docker, PostgreSQL и Nginx.

## О проекте

Foodgram позволяет пользователям публиковать рецепты, просматривать рецепты других авторов, добавлять рецепты в избранное, подписываться на пользователей и формировать список покупок на основе выбранных рецептов.

Проект реализован как backend/fullstack-сервис с REST API, базой данных, авторизацией, фильтрацией, загрузкой изображений и контейнеризацией.

## Функциональность

* Регистрация и авторизация пользователей
* Получение и изменение данных текущего пользователя
* Загрузка и удаление аватара пользователя
* Просмотр списка рецептов
* Создание, редактирование и удаление рецептов
* Загрузка изображений рецептов
* Фильтрация рецептов по тегам
* Поиск ингредиентов
* Добавление рецептов в избранное
* Добавление рецептов в список покупок
* Скачивание списка покупок в виде текстового файла
* Подписки на авторов рецептов
* Просмотр подписок пользователя
* Просмотр профилей пользователей
* Получение короткой ссылки на рецепт
* Админ-панель Django
* API-документация

## Технологический стек

### Backend

* Python 3.11
* Django 4.2
* Django REST Framework
* Djoser
* Token Authentication
* django-filter
* drf-extra-fields
* PostgreSQL
* Gunicorn

### Frontend

* React
* React Router
* React Scripts

### Инфраструктура

* Docker
* Docker Compose
* Nginx
* PostgreSQL

## Структура проекта

```text
foodgram-st/
├── backend/              # Backend-приложение Django
│   ├── api/              # API: фильтры, пагинация, permissions, urls
│   ├── foodgram/         # Настройки Django-проекта
│   ├── recipes/          # Приложение рецептов
│   ├── users/            # Пользователи и подписки
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-entrypoint.sh
│
├── frontend/             # Frontend-приложение React
├── infra/                # Docker Compose и конфигурация Nginx
├── docs/                 # OpenAPI-документация
├── data/                 # Данные для импорта ингредиентов
├── postman_collection/   # Postman-коллекция
└── README.md
```

## Модель данных

В проекте используются основные сущности:

### User

Пользователь сервиса.

Основные поля:

* `email`
* `username`
* `first_name`
* `last_name`
* `avatar`

### Subscription

Подписка пользователя на автора рецептов.

Основные поля:

* `user`
* `author`
* `created`

### Ingredient

Ингредиент.

Основные поля:

* `name`
* `measurement_unit`

### Tag

Тег рецепта.

Основные поля:

* `name`
* `color`
* `slug`

### Recipe

Рецепт.

Основные поля:

* `author`
* `name`
* `image`
* `text`
* `ingredients`
* `tags`
* `cooking_time`
* `pub_date`

### RecipeIngredient

Связь рецепта и ингредиента с указанием количества.

Основные поля:

* `recipe`
* `ingredient`
* `amount`

### Favorite

Избранные рецепты пользователя.

Основные поля:

* `user`
* `recipe`
* `date_added`

### ShoppingCart

Список покупок пользователя.

Основные поля:

* `user`
* `recipe`
* `date_added`

## API

Backend предоставляет REST API для работы с пользователями, рецептами, ингредиентами, тегами, избранным, подписками и списком покупок.

Основные группы endpoints:

```text
/api/users/                          # пользователи
/api/users/me/                       # текущий пользователь
/api/users/me/avatar/                # добавление / удаление аватара
/api/users/subscriptions/            # подписки текущего пользователя
/api/users/{id}/subscribe/           # подписка / отписка от автора
/api/users/set_password/             # изменение пароля

/api/auth/token/login/               # получение токена авторизации
/api/auth/token/logout/              # удаление токена авторизации

/api/recipes/                        # рецепты
/api/recipes/{id}/                   # конкретный рецепт
/api/recipes/{id}/get_link/          # короткая ссылка на рецепт
/api/recipes/{id}/favorite/          # добавление / удаление из избранного
/api/recipes/{id}/shopping_cart/     # добавление / удаление из списка покупок
/api/recipes/download_shopping_cart/ # скачивание списка покупок

/api/ingredients/                    # ингредиенты
/api/tags/                           # теги
```

API-документация после запуска доступна по адресу:

```text
http://localhost/api/docs/
```

## Установка и запуск

### Требования

Перед запуском необходимо установить:

* Docker
* Docker Compose

### Локальный запуск через Docker

Клонируйте репозиторий:

```bash
git clone https://github.com/smizereens/foodgram-st.git
cd foodgram-st
```

Создайте файл `.env` в директории `backend/`:

```env
SECRET_KEY=your-django-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend
```

Перейдите в директорию `infra/`:

```bash
cd infra
```

Запустите контейнеры:

```bash
docker-compose up -d
```

При запуске backend-контейнера автоматически выполняются:

* применение миграций;
* сбор статических файлов;
* импорт ингредиентов из `ingredients.json`.

После запуска будут доступны:

```text
http://localhost/           # frontend
http://localhost/api/       # API
http://localhost/api/docs/  # API-документация
http://localhost/admin/     # Django admin
```

## Полезные команды

Выполнить миграции вручную:

```bash
docker-compose exec backend python manage.py migrate
```

Собрать статику:

```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

Импортировать ингредиенты:

```bash
docker-compose exec backend python manage.py import_ingredients
```

Создать суперпользователя:

```bash
docker-compose exec backend python manage.py createsuperuser
```

Посмотреть логи backend-контейнера:

```bash
docker-compose logs -f backend
```

Остановить контейнеры:

```bash
docker-compose down
```

Остановить контейнеры и удалить volumes:

```bash
docker-compose down -v
```

## Что реализовано

* Спроектированы модели пользователей, подписок, рецептов, ингредиентов, тегов, избранного и списка покупок
* Реализовано REST API на Django REST Framework
* Настроена авторизация пользователей через token-based authentication
* Реализованы permissions для ограничения действий пользователей
* Добавлена фильтрация рецептов
* Реализован поиск ингредиентов
* Добавлена загрузка изображений рецептов в формате base64
* Реализовано добавление рецептов в избранное
* Реализовано добавление рецептов в список покупок
* Добавлено скачивание списка покупок в виде текстового файла
* Реализованы подписки на авторов рецептов
* Добавлена загрузка и удаление аватара пользователя
* Реализовано получение короткой ссылки на рецепт
* Настроена админ-панель Django
* Подключена OpenAPI-документация
* Проект контейнеризирован с помощью Docker и Docker Compose
* Настроена раздача frontend, static/media и API через Nginx

## Возможные доработки

* Добавить тесты для API
* Улучшить обработку ошибок
* Добавить CI-проверки не только для flake8, но и для тестов
* Добавить отдельные настройки для production/development
* Улучшить документацию по локальному запуску без Docker
* Добавить скриншоты интерфейса
* Настроить автоматическое наполнение тестовыми данными
* Добавить Docker healthcheck для backend и PostgreSQL

## Автор

Максим Жикин
Студент направления «Программная инженерия» / «Информатика и вычислительная техника»

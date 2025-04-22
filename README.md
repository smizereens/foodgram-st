# Foodgram - Продуктовый помощник

## Описание проекта

Foodgram - это онлайн-сервис и API для публикации рецептов. 
Авторизованные пользователи могут публиковать рецепты, добавлять понравившиеся рецепты в избранное, 
подписываться на публикации других авторов и формировать список покупок для выбранных рецептов.

### Функциональность

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление рецептов
- Фильтрация рецептов по тегам
- Добавление рецептов в избранное
- Подписки на авторов рецептов
- Формирование списка покупок и выгрузка в виде файла
- Поиск ингредиентов

## Технологии

- Python 3.11
- Django 4.2
- Django REST Framework
- PostgreSQL
- Docker
- NGINX
- React (фронтенд)

## Как запустить проект

### Предварительные требования
* Docker
* Docker Compose

### Шаги по запуску

1. Клонировать репозиторий:
```bash
git clone https://github.com/smizereens/foodgram-st.git
```

2. Создать .env файл в директории /backend/ с следующим содержимым:
```
SECRET_KEY='django-insecure-(!e&g)n2bo@w1ot!x^v3f$zfu2qwc9qn!pw=2s$*ck&vi4b7i('
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend
```

3. Запустить Docker Compose:
```bash
cd infra
docker-compose up -d
```

4. После успешного запуска выполнить миграции и загрузить данные:
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py import_ingredients
```

5. Создать суперпользователя (при необходимости):
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Доступ к проекту

- Веб-интерфейс будет доступен по адресу: http://localhost/
- API документация: http://localhost/api/docs/
- Админ-панель: http://localhost/admin/
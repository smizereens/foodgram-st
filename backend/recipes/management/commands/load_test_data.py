import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.files.base import ContentFile
import base64

from users.models import User, Subscription
from recipes.models import (
    Ingredient, Tag, Recipe, RecipeIngredient, Favorite, ShoppingCart
)


class Command(BaseCommand):
    """Команда для загрузки тестовых данных."""
    help = 'Загружает тестовые данные в БД'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                if Ingredient.objects.count() == 0:
                    self.stdout.write(
                        self.style.WARNING(
                            'Ингредиенты отсутствуют. '
                            'Сначала выполните команду import_ingredients'
                        )
                    )
                    return
                # Создаем тестовые теги, если их еще нет
                tags = self._create_tags()
                # Создаем тестовых пользователей, если их еще нет
                users = self._create_users()
                # Создаем тестовые рецепты (если их меньше 10)
                if Recipe.objects.count() < 10:
                    self._create_recipes(users, tags)
                # Создаем тестовые подписки, избранное и списки покупок
                self._create_subscriptions(users)
                self._create_favorites_and_shopping_carts(users)
                self.stdout.write(
                    self.style.SUCCESS('Тестовые данные успешно загружены')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Произошла ошибка: {e}')
            )

    def _create_tags(self):
        """Создание тегов."""
        tags_data = [
            {'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#49B64E', 'slug': 'dinner'},
            {'name': 'Ужин', 'color': '#8775D2', 'slug': 'supper'},
            {'name': 'Десерт', 'color': '#FFA500', 'slug': 'dessert'},
            {'name': 'Напиток', 'color': '#1E90FF', 'slug': 'drink'},
        ]
        tags = []
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                slug=tag_data['slug'],
                defaults={
                    'name': tag_data['name'],
                    'color': tag_data['color']
                }
            )
            tags.append(tag)
            if created:
                self.stdout.write(f'Создан тег: {tag.name}')
        return tags

    def _create_users(self):
        """Создание пользователей."""
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'first_name': 'Админ',
                'last_name': 'Сайта',
                'is_staff': True,
                'is_superuser': True,
                'password': 'admin'
            },
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'password': 'user1pass'
            },
            {
                'username': 'user2',
                'email': 'user2@example.com',
                'first_name': 'Мария',
                'last_name': 'Петрова',
                'password': 'user2pass'
            },
            {
                'username': 'user3',
                'email': 'user3@example.com',
                'first_name': 'Алексей',
                'last_name': 'Сидоров',
                'password': 'user3pass'
            },
        ]
        users = []
        for user_data in users_data:
            password = user_data.pop('password')
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'Создан пользователь: {user.username}')
            users.append(user)
        return users

    def _create_recipes(self, users, tags):
        """Создание рецептов."""
        ingredients = list(Ingredient.objects.all())
        # Базовое изображение для всех рецептов (простой пиксель)
        base64_image = (
            'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAA'
            'ABAAEAAAIBRAA7'
        )
        image_format, imgstr = base64_image.split(';base64,')
        image_data = base64.b64decode(imgstr)
        recipes_data = [
            {
                'name': 'Омлет с помидорами',
                'text': 'Классический омлет с сочными помидорами и зеленью.',
                'cooking_time': 15,
                'author': users[1]  # user1
            },
            {
                'name': 'Картофель по-деревенски',
                'text': 'Ароматный картофель с чесноком и специями.',
                'cooking_time': 40,
                'author': users[1]  # user1
            },
            {
                'name': 'Паста карбонара',
                'text': 'Итальянская паста с яичным соусом, беконом и сыром.',
                'cooking_time': 30,
                'author': users[2]  # user2
            },
            {
                'name': 'Греческий салат',
                'text': 'Свежий салат с огурцами, помидорами и сыром фета.',
                'cooking_time': 20,
                'author': users[2]  # user2
            },
            {
                'name': 'Куриные котлеты',
                'text': 'Сочные котлеты из куриного фарша с луком и чесноком.',
                'cooking_time': 35,
                'author': users[3]  # user3
            },
            {
                'name': 'Овощной суп',
                'text': 'Легкий и полезный овощной суп на курином бульоне.',
                'cooking_time': 60,
                'author': users[3]  # user3
            },
            {
                'name': 'Шоколадный маффин',
                'text': 'Нежный шоколадный маффин с жидкой начинкой внутри.',
                'cooking_time': 25,
                'author': users[0]  # admin
            },
            {
                'name': 'Глинтвейн',
                'text': 'Согревающий напиток с вином и пряностями.',
                'cooking_time': 20,
                'author': users[0]  # admin
            },
        ]
        for recipe_data in recipes_data:
            recipe, created = Recipe.objects.get_or_create(
                name=recipe_data['name'],
                author=recipe_data['author'],
                defaults={
                    'text': recipe_data['text'],
                    'cooking_time': recipe_data['cooking_time'],
                }
            )
            if created:
                # Добавляем изображение
                recipe.image.save(
                    f'recipe_{recipe.id}.png',
                    ContentFile(image_data),
                    save=True
                )
                # Добавляем теги к рецепту
                recipe_tags = random.sample(tags, k=random.randint(1, 3))
                recipe.tags.set(recipe_tags)
                # Добавляем ингредиенты к рецепту
                recipe_ingredients = []
                for _ in range(random.randint(3, 8)):
                    ingredient = random.choice(ingredients)
                    amount = random.randint(1, 500)
                    recipe_ingredient = RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=amount
                    )
                    recipe_ingredients.append(recipe_ingredient)
                RecipeIngredient.objects.bulk_create(recipe_ingredients)
                self.stdout.write(f'Создан рецепт: {recipe.name}')

    def _create_subscriptions(self, users):
        """Создание подписок между пользователями."""
        for user in users:
            for author in users:
                if user != author:  # Пользователь не может подписаться на себя
                    subscription, created = Subscription.objects.get_or_create(
                        user=user,
                        author=author
                    )
                    if created:
                        self.stdout.write(
                            f'Создана подписка: {user.username} -> '
                            f'{author.username}'
                        )

    def _create_favorites_and_shopping_carts(self, users):
        """Создание избранных рецептов и списков покупок."""
        recipes = list(Recipe.objects.all())
        if not recipes:
            return
        for user in users:
            # Добавляем случайные рецепты в избранное
            for _ in range(random.randint(1, min(5, len(recipes)))):
                recipe = random.choice(recipes)
                favorite, created = Favorite.objects.get_or_create(
                    user=user,
                    recipe=recipe
                )
                if created:
                    self.stdout.write(
                        f'Рецепт {recipe.name} добавлен в избранное '
                        f'пользователя {user.username}'
                    )
            # Добавляем случайные рецепты в список покупок
            for _ in range(random.randint(1, min(3, len(recipes)))):
                recipe = random.choice(recipes)
                cart, created = ShoppingCart.objects.get_or_create(
                    user=user,
                    recipe=recipe
                )
                if created:
                    self.stdout.write(
                        f'Рецепт {recipe.name} добавлен в список покупок '
                        f'пользователя {user.username}'
                    )

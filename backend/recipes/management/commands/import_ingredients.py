import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда для импорта ингредиентов из JSON-файла."""
    help = 'Импорт ингредиентов из JSON-файла'
    def handle(self, *args, **options):
        """Основной метод команды."""
        data_path = self._find_ingredients_file()
        if not data_path:
            return
        try:
            ingredients_data = self._load_json_file(data_path)
            if ingredients_data is None:
                return
            self._import_ingredients(ingredients_data)
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Произошла ошибка: {e}')
            )

    def _find_ingredients_file(self):
        """Поиск файла с ингредиентами среди возможных путей."""
        possible_paths = [
            os.path.join(settings.BASE_DIR, '..', 'data', 'ingredients.json'),
            os.path.join(settings.BASE_DIR, 'data', 'ingredients.json'),
            '/app/data/ingredients.json',
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        self.stdout.write(
            self.style.ERROR(
                f'Файл ingredients.json не найден. Проверенные пути: {possible_paths}'
            )
        )
        return None

    def _load_json_file(self, file_path):
        """Загрузка данных из JSON-файла."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {file_path}')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Ошибка декодирования JSON в файле: {file_path}')
            )
        return None

    def _import_ingredients(self, ingredients_data):
        """Импорт ингредиентов из данных JSON."""
        ingredients_to_create = []
        existing_ingredients = self._get_existing_ingredients()
        # Подготавливаем список ингредиентов для создания
        for item in ingredients_data:
            name = item.get('name')
            measurement_unit = item.get('measurement_unit')
            if not name or not measurement_unit:
                continue
            key = f"{name}_{measurement_unit}"
            if key in existing_ingredients:
                continue
            ingredients_to_create.append(
                Ingredient(name=name, measurement_unit=measurement_unit)
            )
            existing_ingredients[key] = True
        
        self._create_ingredients(ingredients_to_create)

    def _get_existing_ingredients(self):
        """Получение словаря существующих ингредиентов для проверки дубликатов."""
        existing_ingredients = {}
        for ingredient in Ingredient.objects.all():
            key = f"{ingredient.name}_{ingredient.measurement_unit}"
            existing_ingredients[key] = True
        return existing_ingredients

    def _create_ingredients(self, ingredients_to_create):
        """Сохранение новых ингредиентов в базу данных."""
        if ingredients_to_create:
            Ingredient.objects.bulk_create(ingredients_to_create)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно импортировано {len(ingredients_to_create)} ингредиентов'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('Нет новых ингредиентов для импорта')
            )

import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда для импорта ингредиентов из JSON-файла."""
    help = 'Импорт ингредиентов из JSON-файла'

    def handle(self, *args, **options):
        # Список возможных путей к файлу
        possible_paths = [
            os.path.join(settings.BASE_DIR, '..', 'data', 'ingredients.json'),
            os.path.join(settings.BASE_DIR, 'data', 'ingredients.json'),
            '/app/data/ingredients.json',
        ]
        
        data_path = None
        for path in possible_paths:
            if os.path.exists(path):
                data_path = path
                break
        
        if not data_path:
            self.stdout.write(
                self.style.ERROR(f'Файл ingredients.json не найден. Проверенные пути: {possible_paths}')
            )
            return
        
        try:
            with open(data_path, 'r', encoding='utf-8') as file:
                ingredients_data = json.load(file)
            
            ingredients_to_create = []
            existing_ingredients = {}
            
            # Получаем существующие ингредиенты для проверки дубликатов
            for ingredient in Ingredient.objects.all():
                key = f"{ingredient.name}_{ingredient.measurement_unit}"
                existing_ingredients[key] = True
            
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
            
            # Используем bulk_create для более эффективного добавления
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
        
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {data_path}')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Ошибка декодирования JSON в файле: {data_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Произошла ошибка: {e}')
            )
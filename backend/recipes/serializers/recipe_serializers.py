from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (
    Ingredient, Recipe, RecipeIngredient, Tag, Favorite, ShoppingCart
)
from users.serializers.user_serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для представления ингредиентов в рецепте."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipe_ingredients', read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
            'tags',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиента при создании рецепта."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления рецептов."""
    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, value):
        """Валидация ингредиентов."""
        if not value:
            raise serializers.ValidationError(
                'Необходимо добавить хотя бы один ингредиент!'
            )
        
        ingredients_list = []
        for item in value:
            ingredient = get_object_or_404(Ingredient, id=item['id'])
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться!'
                )
            if int(item['amount']) < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше нуля!'
                )
            ingredients_list.append(ingredient)
        
        return value

    def validate_tags(self, value):
        """Валидация тегов."""
        if value and len(value) != len(set(value)):
            raise serializers.ValidationError(
                'Теги не должны повторяться!'
            )
        return value

    def create_update_ingredients(self, ingredients, recipe):
        """Создание или обновление ингредиентов рецепта."""
        ingredient_list = []
        for item in ingredients:
            ingredient_list.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient_id=item['id'],
                    amount=item['amount']
                )
            )
        RecipeIngredient.objects.bulk_create(ingredient_list)

    @transaction.atomic
    def create(self, validated_data):
        """Создание рецепта."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags', [])
        author = self.context.get('request').user
        
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.create_update_ingredients(ingredients, recipe)
        
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """Обновление рецепта."""
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_update_ingredients(ingredients, instance)
        
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)
        
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Представление для возврата после создания/обновления."""
        return RecipeListSerializer(
            instance, context=self.context
        ).data


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого представления рецепта."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class ShortLinkSerializer(serializers.ModelSerializer):
    """Сериализатор для коротких ссылок на рецепты."""
    short_link = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('short_link',)

    def get_short_link(self, obj):
        request = self.context.get('request')
        if request:
            domain = request.build_absolute_uri('/').strip('/')
            return f"{domain}/s/{obj.id}"
        return f"/s/{obj.id}"

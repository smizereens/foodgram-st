from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views.user_views import CustomUserViewSet
from recipes.views.recipe_views import (
    IngredientViewSet, RecipeViewSet, TagViewSet
)

me_avatar_view = CustomUserViewSet.as_view({'put': 'me_avatar', 'delete': 'me_avatar'})

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('users/me/avatar/', me_avatar_view, name='user-me-avatar'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
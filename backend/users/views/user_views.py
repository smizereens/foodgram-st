from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet

from users.models import Subscription
from users.serializers.user_serializers import (
    CustomUserSerializer, UserWithRecipesSerializer,
    SetAvatarSerializer, PasswordChangeSerializer
)
from api.pagination import CustomPagination

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        """Получение списка подписок."""
        queryset = User.objects.filter(
            subscribers__user=request.user
        )
        page = self.paginate_queryset(queryset)
        serializer = UserWithRecipesSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        """Подписка и отписка от пользователя."""
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if request.user == author:
                return Response(
                    {'detail': 'Нельзя подписаться на самого себя!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Subscription.objects.filter(
                user=request.user, author=author
            ).exists():
                return Response(
                    {'detail': 'Вы уже подписаны на этого автора!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscription.objects.create(user=request.user, author=author)
            serializer = UserWithRecipesSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = Subscription.objects.filter(
            user=request.user, author=author
        )
        if not subscription.exists():
            return Response(
                {'detail': 'Вы не подписаны на этого автора!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['put', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me_avatar(self, request):
        """Добавление или удаление аватара пользователя."""
        if request.method == 'PUT':
            serializer = SetAvatarSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            is_valid = serializer.is_valid()
            if is_valid:
                try:
                    serializer.save()
                    user_serializer = CustomUserSerializer(
                        request.user, context={'request': request}
                    )
                    return Response(user_serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(
                        {'detail': 'Error saving avatar.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        if request.user.avatar:
            try:
                request.user.avatar.delete(save=True)
            except Exception as e:
                return Response(
                    {'detail': 'Error deleting avatar.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def set_password(self, request):
        """Изменение пароля пользователя."""
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(
                serializer.validated_data['current_password']
            ):
                return Response(
                    {'current_password': ['Неверный пароль.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

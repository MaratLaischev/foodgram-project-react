from api.pogination import RecipePogination
from api.serializers import SubscriptionSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from user.models import Follow, User


class UserViewSet(DjoserUserViewSet):
    pagination_class = RecipePogination

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return Response(
                {"detail": "Учетные данные не были предоставлены."},
                status=HTTP_401_UNAUTHORIZED
            )
        context = {'request': request}
        serializer = UserSerializer(user, context=context)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['GET'],
        pagination_class=RecipePogination,
        permission_classes=[IsAuthenticated, ]
    )
    def subscriptions(self, request):
        users = Follow.objects.filter(following=request.user)
        context = {'request': request}
        obj_users = [(user.user)for user in users]
        page = self.paginate_queryset(obj_users)
        serializer = SubscriptionSerializer(
            page, many=True, context=context
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated, ]
    )
    def subscribe(self, request, id):
        user = get_object_or_404(User, id=id)
        if Follow.objects.filter(user=user, following=request.user).exists():
            return Response(
                {'error': 'Вы уже подписаны!'},
                status=HTTP_400_BAD_REQUEST
            )
        Follow.objects.create(user=user, following=request.user)
        context = {'request': request}
        serializer = SubscriptionSerializer(user, context=context)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        user = get_object_or_404(User, id=id)
        obj = Follow.objects.filter(user=user, following=request.user)
        if obj.exists():
            obj.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны!'},
            status=HTTP_400_BAD_REQUEST
        )

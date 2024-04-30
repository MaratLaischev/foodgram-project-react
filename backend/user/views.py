from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from api.pogination import RecipePogination
from user.models import Follow, User
from user.serializers import (FollowSerializer, SubscriptionSerializer,
                              UserSerializer)


class UserViewSet(DjoserUserViewSet):
    pagination_class = RecipePogination

    @action(['get'], detail=False, permission_classes=[IsAuthenticated, ])
    def me(self, request, *args, **kwargs):
        user = request.user
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
        context = {'request': request, 'pk': id}
        data = {'user': id, 'following': request.user.id}
        serializer = FollowSerializer(
            data=data, context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
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

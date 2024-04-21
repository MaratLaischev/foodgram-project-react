from io import BytesIO

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnlyPermission
from api.pogination import RecipePogination
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             RecipeSerializerRead, RecipeSerializerRecord,
                             TagSerializer)
from ingredient.models import Ingredient, IngredientRecipe
from recipe.models import Cart, Favorite, Recipe, Tag


class RecipeView(ModelViewSet):
    queryset = Recipe.objects.prefetch_related('tags', 'author')
    pagination_class = RecipePogination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorOrReadOnlyPermission, ]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializerRead
        return RecipeSerializerRecord

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def adding_method(self, model, user, pk):
        if model.objects.filter(author=user, recipe__id=pk).exists():
            return Response(
                {'error': 'Рецепт уже добавлен!'},
                status=HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(author=user, recipe=recipe)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete_method(self, model, user, pk):
        obj = model.objects.filter(author=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Рецепта нету в списке'},
            status=HTTP_400_BAD_REQUEST
        )

    def encode_cart(self, data):
        output = ''
        number = 0
        for ordered_dict in data:
            name = ordered_dict['ingredient__name']
            amount = ordered_dict['amount']
            measurement_unit = ordered_dict['ingredient__measurement_unit']
            number += 1
            output += f'{number}. {name} {amount} {measurement_unit}\n'
        return output

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        shopping_list = IngredientRecipe.objects.filter(
            recipe__cart__author=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        if not shopping_list.exists():
            return Response(
                {'error': 'В карзине нет рецептов!'},
                status=HTTP_400_BAD_REQUEST
            )
        output = self.encode_cart(shopping_list)
        buffer = BytesIO(output.encode('utf8'))
        return FileResponse(
            buffer, filename='shopping_list.txt', as_attachment=True
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        user = request.user
        if request.method == 'POST':
            return self.adding_method(Favorite, user, pk)
        return self.delete_method(Favorite, user, pk)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk):
        user = request.user
        if request.method == 'POST':
            return self.adding_method(Cart, user, pk)
        return self.delete_method(Cart, user, pk)


class TagView(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientView(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter

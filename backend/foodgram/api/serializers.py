import base64
import io

from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from PIL import Image
from rest_framework import serializers

from ingredient.models import Ingredient
from recipe.models import Cart, Favorite, IngredientRecipe, Recipe, Tag
from user.serializers import UserRecipeSerializer, UserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializerRead(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(
        source='ingredient_recipes', many=True
    )
    tags = TagSerializer(many=True)
    author = UserSerializer()
    cooking_time = serializers.IntegerField(min_value=1)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'name',
            'author',
            'text',
            'cooking_time',
            'tags',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and user.favorites.filter(
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and user.carts.filter(recipe=obj).exists()


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'recipe', 'amount')


class RecipeSerializerRecord(serializers.ModelSerializer):
    ingredients = AddIngredientRecipeSerializer(many=True, required=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=True
    )
    image = Base64ImageField(max_length=None, required=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'name',
            'text',
            'cooking_time',
            'tags',
            'ingredients'
        )

    def validate(self, data):
        ingredients = data.get('ingredients')
        tags = data.get('tags')
        image = data.get('image')
        if not image:
            raise serializers.ValidationError(
                'Вы не выбрали картинку'
            )
        if not tags:
            raise serializers.ValidationError(
                'Вы не выбрали теги'
            )
        tags_list = []
        for tag in tags:
            tags_list.append(tag.id)
        if len(tags_list) != len(set(tags_list)):
            raise serializers.ValidationError(
                'Проверьте, какой-то тег был выбран более 1 раза'
            )
        if not ingredients:
            raise serializers.ValidationError(
                'Вы не выбрали ингредиенты'
            )
        ingredients_list = []
        for ingredient in ingredients:
            if not IngredientRecipeSerializer(data=ingredient).is_valid():
                raise serializers.ValidationError(
                    'Игредиент пуст'
                )
            ingredients_list.append(ingredient['ingredient'].id)
        if len(ingredients_list) != len(set(ingredients_list)):
            raise serializers.ValidationError(
                'Проверьте, какой-то ингредиент был выбран более 1 раза'
            )
        return data

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        serializers = RecipeSerializerRead(instance, context=context)
        return serializers.data

    def create_ingredients(self, recipe, ingredients):
        all_ingredients = [
            IngredientRecipe(
                ingredient=ingredient['ingredient'],
                recipe=recipe,
                amount=ingredient['amount']
            )for ingredient in ingredients]
        IngredientRecipe.objects.bulk_create(all_ingredients)

    def decode_design_image(self, data):
        try:
            data = base64.b64decode(data.encode('UTF-8'))
            buf = io.BytesIO(data)
            img = Image.open(buf)
            return img
        except Exception:
            return None

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        validated_data['author'] = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe=recipe, ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.set(tags)
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredients(recipe=instance, ingredients=ingredients)
        return super().update(instance, validated_data)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'id',
        )

    def to_representation(self, cart):
        recipe = cart.recipe
        serializers = UserRecipeSerializer(recipe)
        return serializers.data

    def validate(self, data):
        user = self.context['request'].user
        pk = self.context['pk']
        if user.carts.filter(recipe__id=pk).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен!'
            )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        pk = self.context['pk']
        recipe = get_object_or_404(Recipe, id=pk)
        return user.carts.create(recipe=recipe)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'id',
        )

    def to_representation(self, favorite):
        recipe = favorite.recipe
        serializers = UserRecipeSerializer(recipe)
        return serializers.data

    def validate(self, data):
        user = self.context['request'].user
        pk = self.context['pk']
        if user.favorites.filter(recipe__id=pk).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен!'
            )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        pk = self.context['pk']
        recipe = get_object_or_404(Recipe, id=pk)
        return user.favorites.create(recipe=recipe)

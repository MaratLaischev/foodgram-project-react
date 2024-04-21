import base64
import io

from drf_extra_fields.fields import Base64ImageField
from PIL import Image
from rest_framework import serializers

from foodgram.settings import RECIPES_LIMIT_DEFOLT
from ingredient.models import Ingredient, IngredientRecipe
from recipe.models import Cart, Favorite, Recipe, Tag, User
from user.models import Follow


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if obj.id == user.id:
            return False
        return Follow.objects.filter(user=obj.id, following=user.id).exists()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')

    def to_representation(self, instance):
        serializers = super(
            IngredientRecipeSerializer, self
        ).to_representation(instance)
        serializers['name'] = instance.ingredient.name
        serializers['measurement_unit'] = instance.ingredient.measurement_unit
        return serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializerRead(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
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

    def get_ingredients(self, obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj.id)
        return IngredientRecipeSerializer(list(queryset), many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(author=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Cart.objects.filter(author=user, recipe=obj).exists()


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeSerializerRecord(serializers.ModelSerializer):
    ingredients = AddIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(max_length=None, required=False)

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

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        serializers = RecipeSerializerRead(instance, context=context)
        return serializers.data

    def create_ingredients(self, recipe, ingredients):
        all_ingredients = [
            IngredientRecipe(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
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


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'name',
            'cooking_time'
        )


class SubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is None:
            recipes_limit = RECIPES_LIMIT_DEFOLT
        recipe = Recipe.objects.filter(author=obj)[:int(recipes_limit)]
        serializers = RecipeSerializer(list(recipe), many=True)
        return serializers.data

from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipe.models import Recipe
from user.models import Follow, User


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Не используйте me в username'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.following.filter(
            following=user.id
        ).exists()


class UserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'name',
            'cooking_time'
        )


class SubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit and recipes_limit.isdigit():
            return UserRecipeSerializer(
                recipes[:int(recipes_limit)], many=True
            ).data
        return UserRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            'user',
            'following'
        )

    def to_representation(self, follow):
        serializer = SubscriptionSerializer(follow.user, context=self.context)
        return serializer.data

    def validate(self, data):
        follower = data['following']
        pk = self.context['pk']
        user = data['user']
        if not user:
            raise serializers.ValidationError(
                f'Пользователя с id {pk} не существует!'
            )
        if follower.followers.filter(user=user).exists():
            raise serializers.ValidationError(
                f'Вы уже подписаны на {user.username}'
            )
        if user == follower:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя'
            )
        return data

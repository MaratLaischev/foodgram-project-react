from django.urls import include, path
from rest_framework import routers

from api.views import IngredientView, RecipeView, TagView
from user.views import UserViewSet

router = routers.DefaultRouter()
router.register('recipes', RecipeView, basename='recipes')
router.register('tags', TagView, basename='tags')
router.register('ingredients', IngredientView, basename='ingredients')
router.register("users", UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

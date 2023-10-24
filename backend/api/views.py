from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import RecipeFilter
from .pagination import CustomPageNumberPagination
from .serializers import (
    CUDRecipeSerializer,
    IngredientSerializer,
    ReadRecipeSerializer,
    ShortRecipeSerializer,
    TagSerializer,
)

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)  # new

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadRecipeSerializer
        return CUDRecipeSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            IngredientInRecipe.objects.filter(recipe__cart__user=user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .order_by("ingredient__name")
            .annotate(amount=Sum("amount"))
        )
        file_name = f"{user.username}_shopping_cart.txt"
        shopping_cart = f"{user.first_name} хочет купить:\n\n"
        shopping_cart += "\n".join(
            [
                f'{ingredient["ingredient__name"]} — '
                f'{ingredient["amount"]}'
                f'{ingredient["ingredient__measurement_unit"]}'
                for ingredient in ingredients
            ]
        )
        response = HttpResponse(shopping_cart, content_type="text.txt; charset=utf-8")
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response

    @action(
        methods=["post", "delete"], detail=True, permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        if request.method == "POST":
            return self.add_recipe(ShoppingCart, request.user, pk)
        if request.method == "DELETE":
            return self.delete_recipe(ShoppingCart, request.user, pk)

    @action(
        methods=["post", "delete"], detail=True, permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        if request.method == "POST":
            return self.add_recipe(Favorite, request.user, pk)
        if request.method == "DELETE":
            return self.delete_recipe(Favorite, request.user, pk)

    def add_recipe(self, model, user, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        instance = model.objects.filter(user=user, recipe=recipe)
        if instance.exists():
            return Response(
                {"errors": "Рецепт уже добавлен."}, status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, user, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        instance = model.objects.filter(user=user, recipe=recipe)
        if not instance.exists():
            return Response(
                {"errors": "Рецепт уже удален."}, status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

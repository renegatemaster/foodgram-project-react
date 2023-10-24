from api.pagination import CustomPageNumberPagination
from api.serializers import CustomUserSerializer, SubscribeSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe
from .permissions import UserPermission

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (UserPermission,)

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get("id")
        author = get_object_or_404(User, id=author_id)
        # Подписка
        if request.method == "POST":
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Отписка
        sub = get_object_or_404(Subscribe, user=user, author=author)
        sub.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=[
            "get",
        ],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def subscriptions(self, request):
        user = request.user
        subs = User.objects.filter(subscriber__user=user)
        pages = self.paginate_queryset(subs)
        serializer = SubscribeSerializer(pages, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        return User.objects.all()

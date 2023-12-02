from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, UserLoginSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action
from .permissions import IsOwnerOrIsStaff
from django.contrib.auth import authenticate, login, logout


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrIsStaff]
    http_method_names = ["get", "post", "update"]

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer
        return super().get_serializer_class()

    @action(methods=["post"], detail=False)
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=200)

    @action(methods=["post"], detail=False)
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user:
            login(request, user)
            return Response(status=200)

        return Response(status=400)

    @action(methods=["get"], detail=False)
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response(status=204)

        return Response(status=401)

    @action(methods=["get"], detail=False)
    def me(self, request):
        user = UserSerializer(instance=request.user, many=False)

        return Response({"user": user.data})

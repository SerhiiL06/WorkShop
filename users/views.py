from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, UserLoginSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from rest_framework.decorators import action, permission_classes as perm
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

    @action(methods=["post"], detail=False, serializer_class=UserRegisterSerializer)
    def register(self, request):
        if not request.user.is_authenticated:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if (
                serializer.validated_data["password1"]
                != serializer.validated_data["password2"]
            ):
                return Response(status=400)

            serializer.save()

            return Response(status=200)

        return Response(status=400)

    @action(
        methods=["post"],
        detail=False,
        serializer_class=UserLoginSerializer,
        permission_classes=[permissions.AllowAny],
    )
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

    @action(
        methods=["get"], detail=False, permission_classes=[permissions.IsAuthenticated]
    )
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response(status=204)

        return Response(status=401)

    @action(
        methods=["get"], detail=False, permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = UserSerializer(instance=request.user, many=False)

        return Response({"user": user.data})

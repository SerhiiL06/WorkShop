from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, permission_classes as permiss
from .models import Order
from rest_framework import permissions
from .serializers import CreateOrderSerializer, AssignedMasterSerializer
from .permissions import OrderPermission
from users.models import User


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [OrderPermission]
    serializer_class = CreateOrderSerializer
    lookup_field = "id"

    def get_permissions_class(self):
        if self.action == "create":
            return permissions.IsAuthenticated
        return super().get_permissions()

    @permiss(permissions.IsAuthenticated)
    def create(self, request, *args, **kwargs):
        serilizer = CreateOrderSerializer(data=request.data)

        serilizer.is_valid(raise_exception=True)

        serilizer.save(customer=request.user, category_id=request.data["category"])

        return Response(status=200)

    @action(
        methods=["put"],
        detail=True,
        url_path="consider-order",
        serializer_class=AssignedMasterSerializer,
    )
    def assigned_master(self, request, *args, **kwargs):
        if request.user.is_staff:
            order = get_object_or_404(Order, pk=self.kwargs["id"])
            user = get_object_or_404(User, username=request.data["master"])

            if request.data["result"] == "accept":
                order.master = user
                order.status = "assigned"

                order.save()
                return Response(status=200)

            else:
                order.status = "rejected"
                order.save()

                return Response(status=200)

        return Response(status=403)


class MasterOrder:
    pass

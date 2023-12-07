from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .models import Order
from rest_framework import permissions
from .serializers import (
    CreateOrderSerializer,
    AssignedMasterSerializer,
    MasterOrderSerializer,
)

from users.models import User
from django.utils import timezone
from datetime import timedelta
from .tasks import send_email_about_assigned_master, send_email_about_canceled_order


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CreateOrderSerializer
    lookup_field = "id"

    def get_permissions_class(self):
        if self.action == "create":
            return permissions.IsAuthenticated

        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        if request.user.is_master:
            return Response({"wrong": "master cannot create order"}, status=400)
        serilizer = CreateOrderSerializer(data=request.data)

        serilizer.is_valid(raise_exception=True)

        serilizer.save(customer=request.user, category_id=request.data["category"])

        return Response(status=200)

    @action(
        methods=["put"],
        detail=True,
        url_path="consider-order",
        serializer_class=AssignedMasterSerializer,
        permission_classes=[permissions.IsAdminUser],
    )
    def assigned_master(self, request, *args, **kwargs):
        if request.user.is_staff:
            order = get_object_or_404(Order, pk=self.kwargs["id"])

            if request.data["result"] == "accept":
                user = get_object_or_404(User, id=request.data["master"])
                order.master = user
                order.status = "assigned"
                order.meeting_time = timezone.now() + timedelta(days=1)

                send_email_about_assigned_master.delay(
                    order.meeting_time, order.customer.email
                )

                order.save()
                return Response(status=200)

            else:
                order.status = "rej"
                order.save()

                send_email_about_canceled_order.delay(order.customer.email)

                return Response(status=200)

        return Response(status=403)


class MasterOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = MasterOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(master=self.request.user)

    @action(methods=["get"], detail=True, url_path="complete-order")
    def complete_order(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs["pk"])

        order.status = "complete"

        order.save()

        return Response(status=200)

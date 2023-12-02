from rest_framework import viewsets
from rest_framework.response import Response
from .models import Order
from rest_framework import permissions
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serilizer = OrderSerializer(data=request.data)

        serilizer.is_valid(raise_exception=True)

        serilizer.save(customer=request.user)

        return Response(status=200)

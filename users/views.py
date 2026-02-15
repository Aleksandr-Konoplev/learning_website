from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Платежи
class PaymentCreateAPIView(CreateAPIView):
    pass


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = {
        'content_type__model': ['exact'],  # 'course' или 'lesson'
        'object_id': ['exact'], # id курса или урока
        'payment_method': ['exact'], # Фильтрация по способу оплаты
    }
    ordering_fields = ('payment_date',)


class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(UpdateAPIView):
    pass


class PaymentDestroyAPIView(DestroyAPIView):
    pass
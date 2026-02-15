from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
# from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


# Пользователи
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UsersListAPIView(ListAPIView):
    pass


class UserRetrieveAPIView(RetrieveAPIView):
    pass


class UserUpdateAPIView(UpdateAPIView):
    pass


class UserDestroyAPIView(DestroyAPIView):
    pass


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
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.models import User, Payment, Subscription
from users.serializers import UserSerializer, PaymentSerializer
from users.paginators import UsersPaginator


#-----------------------------------------
#------------- Пользователи --------------
#-----------------------------------------
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UsersListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = UsersPaginator


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


#-----------------------------------------
#---------------- Платежи ----------------
#-----------------------------------------
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

#-----------------------------------------
#---------------- Подписки ---------------
#-----------------------------------------
class CourseSubscriptionAPIView(APIView):
    """API для подписки/отписки курса"""
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')  # ищем id курса

        # проверяем нашелся id, или нет
        if not course_id:
            return Response(
                {"error": "Не указан ID курса"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Логика подписки/отписки
        if subs_item.exists():
            # Если подписка уже есть - удаляем её
            subs_item.delete()
            message = 'подписка удалена'
        else:
            # Если подписки нет - создаём
            Subscription.objects.create(
                user=user,
                course=course_item
            )
            message = 'подписка добавлена'
        return Response({"message": message})
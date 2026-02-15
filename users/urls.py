from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter
from users.views import (
    UserCreateAPIView,
    # Платежи
    PaymentListAPIView)
from users.apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Платежи
    path('payments/', PaymentListAPIView.as_view(), name='payments_list'),
] + router.urls

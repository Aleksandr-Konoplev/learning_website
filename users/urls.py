from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import UsersViewSet
from users.apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UsersViewSet)

urlpatterns = [

] + router.urls

from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'









# from rest_framework.viewsets import ModelViewSet
# from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
#
# from materials.models import Course, Lesson
# from materials.serializers import CourseSerializer, LessonSerializer
#
# # CRUD через ModelViewSet для курсов
# class CourseViewSet(ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
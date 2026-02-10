from rest_framework.serializers import ModelSerializer

from materials.models import Course


class CourseSerializer(ModelSerializer):
    model = Course
    fields = '__all__'
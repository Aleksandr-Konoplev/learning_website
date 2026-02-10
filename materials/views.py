from rest_framework.viewsets import ViewSet

from materials.models import Course
from materials.serializers import CourseSerializer


class CourseViewSet(ViewSet):
    queryset = Course.objects.all()
    serializers_class = CourseSerializer
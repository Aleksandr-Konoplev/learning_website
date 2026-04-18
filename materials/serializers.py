from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import WebLinkValidator

from users.models import Subscription


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [WebLinkValidator(field="video_url")]
        read_only_fields = ("owner",)


class CourseSerializer(ModelSerializer):
    """Сериалайзер курсов"""

    count_lesson_in_course = SerializerMethodField(label="Количество уроков в курсе")
    lessons_info = SerializerMethodField(label="Общая информация по уроку")
    is_subscribed = SerializerMethodField()

    @staticmethod
    def get_count_lesson_in_course(course):
        return Lesson.objects.filter(course=course.pk).count()

    @staticmethod
    def get_lessons_info(course):
        lessons = Lesson.objects.filter(course=course.pk)
        return LessonSerializer(lessons, many=True).data

    def get_is_subscribed(self, course):
        request = self.context.get("request")

        # если пользователь не авторизован
        if not request or not request.user.is_authenticated:
            return False

        return Subscription.objects.filter(user=request.user, course=course).exists()

    class Meta:
        model = Course
        fields = (
            "name",
            "count_lesson_in_course",
            "lessons_info",
            "description",
            "is_subscribed",
            "owner",
            "id",
        )

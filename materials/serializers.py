from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    """Сериалайзер курсов"""
    count_lesson_in_course = SerializerMethodField()
    lessons_info = SerializerMethodField()

    @staticmethod
    def get_count_lesson_in_course(course):
        return Lesson.objects.filter(course=course.pk).count()

    @staticmethod
    def get_lessons_info(course):
        lessons = Lesson.objects.filter(course=course.pk)
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = ('name', 'count_lesson_in_course', 'lessons_info', 'description')

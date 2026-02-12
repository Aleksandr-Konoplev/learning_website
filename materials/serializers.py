from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):

    count_lesson_in_course = SerializerMethodField()

    @staticmethod
    def get_count_lesson_in_course(course):
        return Lesson.objects.filter(course=course.pk).count()

    class Meta:
        model = Course
        fields = ('name', 'count_lesson_in_course', 'description')


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

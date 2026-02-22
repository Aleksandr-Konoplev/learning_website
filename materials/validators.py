from rest_framework.serializers import ValidationError


class WebLinkValidator:

    def __init__(self, field):
        self.field = field
        self.allowed_domains = ['youtube.com']

    def __call__(self, attrs):
        url = attrs.get(self.field)

        # Проверка на пустой домен
        if not url:
            return attrs

        for domain in self.allowed_domains:
            if domain in url.lower():
                return attrs
        raise ValidationError('Запрещено использовать этот ресурс')
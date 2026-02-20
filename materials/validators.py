from rest_framework.serializers import ValidationError


class WebLinkValidator:

    def __init__(self, field):
        self.field = field
        self.allowed_domains = ['youtube.com']

    def __call__(self, attrs):
        url = attrs.get(self.field)

        for domain in self.allowed_domains:
            if url and domain in url.lower():
                return attrs
        raise ValidationError('Запрещено использовать этот ресурс')
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class GhibliApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('ghiblikey')
        if api_key != settings.GHIBLI_API_KEY:
            raise AuthenticationFailed('No or incorrect API key provided')

        # Normally, you would return a user, but since this is system-to-system,
        # you can return `None`. This will allow the request to be processed,
        # but `request.user` will be set to `AnonymousUser`.
        return None, None
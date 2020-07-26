from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now


class CheckActiveMiddleware(MiddlewareMixin):
    """
    Check last active user
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user.userprofile.last_active = now()
            request.user.userprofile.save()
        return None



from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from django.shortcuts import redirect


class CheckActiveMiddleware(MiddlewareMixin):
    """
    Check last active user
    """
    def process_request(self, request):

        if request.user.is_authenticated:
            request.user.userprofile.last_active = now()
            request.user.userprofile.save()
        return None


class CheckUserPhotoMiddleware(MiddlewareMixin):
    """
    Check user to having avatar if not, redirect to add photo page
    """

    def process_request(self, request):
        if request.user.is_authenticated:

            if not request.user.userprofile.photo and 'addphoto' not in request.path:
                if not request.user.is_staff:
                    return redirect('/profile/addphoto/')
        return redirect('/profile/reg/1')


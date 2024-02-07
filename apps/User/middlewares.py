from django.http import HttpResponseRedirect
from django.urls import reverse


class VerifyEmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/user/signup/':
            if not request.session.get('is_email_verified', False):
                return HttpResponseRedirect(reverse('verify_email_view'))

        response = self.get_response(request)
        return response

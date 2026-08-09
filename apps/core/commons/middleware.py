
from django.utils.timezone import now

class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            request.user.profile.last_activity = now()
            request.user.profile.save(update_fields=['last_activity'])
        return response
    
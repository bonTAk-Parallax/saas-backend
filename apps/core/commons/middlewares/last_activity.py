
from django.utils.timezone import now
from django.core.cache import cache
from apps.user.models.user_profile import UserProfile

class LastActivityMiddleware:
    THROTTLE_SECONDS = 300  

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            self._touch(user)
        return response

    def _touch(self, user):
        cache_key = f"last_activity:{user.id}"
        if cache.get(cache_key):
            return
        UserProfile.objects.filter(user_id=user.id).update(last_activity=now())
        cache.set(cache_key, True, self.THROTTLE_SECONDS)


import hashlib, json
from django.core.cache import cache
from django.http import JsonResponse

class IdempotencyMiddleware:
    TTL = 300

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != 'POST':
            return self.get_response(request)

        key = request.headers.get('Idempotency-Key')
        if not key:
            return self.get_response(request)

        fingerprint = hashlib.sha256(request.body or b'').hexdigest()
        cache_key = f"idempotency:{key}"
        cached = cache.get(cache_key)

        if cached:
            if cached['fingerprint'] != fingerprint:
                return JsonResponse(
                    {"status": "error", "code": 422,
                     "message": "Idempotency-Key reused with a different payload", "data": {}},
                    status=422,
                )
            return JsonResponse(cached['body'], status=cached['status'])

        response = self.get_response(request)

        if response.status_code == 201:
            try:
                body = json.loads(response.content)
                cache.set(cache_key, {'fingerprint': fingerprint, 'body': body, 'status': response.status_code}, self.TTL)
            except (ValueError, TypeError):
                pass

        return response
    
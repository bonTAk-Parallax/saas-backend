
import logging
import uuid, threading

_local = threading.local()

def get_request_id():
    return getattr(_local, 'request_id', '-')

class RequestIDMiddleware:
    HEADER = 'X-Request-ID'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.META.get('HTTP_X_REQUEST_ID') or str(uuid.uuid4())
        request.request_id = request_id
        _local.request_id = request_id
        try:
            response = self.get_response(request)
        finally:
            _local.request_id = None
        response[self.HEADER] = request_id
        return response


class RequestIDLogFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id()
        return True
    
import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Log all HTTP requests and responses.
    """
    
    def process_request(self, request):
        request.start_time = __import__('time').time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = __import__('time').time() - request.start_time
            logger.info(
                f'{request.method} {request.path} - Status: {response.status_code} - Duration: {duration:.2f}s'
            )
        return response

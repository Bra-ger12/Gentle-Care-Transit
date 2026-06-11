import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(MiddlewareMixin):
    """
    Handle uncaught exceptions and return proper error responses.
    """
    
    def process_exception(self, request, exception):
        logger.error(f'Exception: {str(exception)}', exc_info=True)
        
        return JsonResponse(
            {
                'error': 'Internal Server Error',
                'message': str(exception) if __import__('django.conf').settings.DEBUG else 'An error occurred'
            },
            status=500
        )

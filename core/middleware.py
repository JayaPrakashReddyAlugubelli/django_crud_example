import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin

# Get general logger
logger = logging.getLogger('django')

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            log_data = {
                'path': request.path,
                'method': request.method,
                'status_code': response.status_code,
                'duration': f'{duration:.2f}s',
                'user': str(request.user),
            }

            # Add request parameters for non-GET requests
            if request.method != 'GET':
                log_data['post_params'] = dict(request.POST)
                # Remove sensitive information
                if 'password' in log_data['post_params']:
                    log_data['post_params']['password'] = '[FILTERED]'

            logger.info(f'Request processed: {json.dumps(log_data)}')

        return response

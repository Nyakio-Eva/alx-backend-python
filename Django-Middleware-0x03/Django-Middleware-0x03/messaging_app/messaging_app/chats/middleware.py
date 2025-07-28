from datetime import datetime,time
import logging
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Set up logger
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s',
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response
    
    class RestrictAccessByTimeMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            # Define restricted hours: 9PM (21:00) to 6AM (06:00)
            current_time = datetime.now().time()
            start_restriction = time(21, 0)  # 9 PM
            end_restriction = time(6, 0)     # 6 AM

            # If time is between 9PM and midnight or between midnight and 6AM
            if current_time >= start_restriction or current_time < end_restriction:
                return HttpResponseForbidden("Access to the chat is restricted between 9PM and 6AM.")

            return self.get_response(request)
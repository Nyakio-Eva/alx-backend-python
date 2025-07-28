from datetime import datetime,time, timedelta
import logging
from django.http import HttpResponseForbidden
from collections import defaultdict



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
        
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track IPs and their timestamps of messages
        self.ip_message_log = defaultdict(list)

    def __call__(self, request):
        # Only monitor POST requests to message/chat endpoints
        if request.method == 'POST' and '/chat' in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Clean up old entries
            self.ip_message_log[ip] = [
                timestamp for timestamp in self.ip_message_log[ip]
                if now - timestamp < timedelta(minutes=1)
            ]

            # If over the limit
            if len(self.ip_message_log[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: You can only send 5 messages per minute.")

            # Log current message timestamp
            self.ip_message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Handle proxies or direct connections
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')        
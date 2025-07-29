from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

# Simple in-memory store (resets on server restart)
request_log = {}

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 5  # Max messages
        self.time_window = timedelta(minutes=1)  # Per minute

    def __call__(self, request):
        # Apply only to POST requests (messages)
        if request.method == 'POST' and request.path.startswith('/api/conversations/'):
            ip = self.get_client_ip(request)
            now = datetime.now()

            if ip not in request_log:
                request_log[ip] = []

            # Remove timestamps older than 1 minute
            request_log[ip] = [ts for ts in request_log[ip] if now - ts < self.time_window]

            if len(request_log[ip]) >= self.rate_limit:
                return HttpResponseForbidden("Rate limit exceeded. Try again in a minute.")

            request_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get IP address from request (handles proxies)."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check role for authenticated users
        if request.user.is_authenticated:
            # Allow only admin or moderator
            if request.user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("🚫 You do not have permission to perform this action.")
        return self.get_response(request)
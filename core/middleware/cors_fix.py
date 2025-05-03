# core/middleware/cors_fix.py

from corsheaders.middleware import CorsMiddleware
from django.utils.deprecation import MiddlewareMixin

class CustomCorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response = CorsMiddleware().process_response(request, response)
        return response

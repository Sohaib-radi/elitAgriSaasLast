# core/middleware/cors_fix.py

from corsheaders.middleware import CorsMiddleware

class CustomCorsMiddleware(CorsMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request):
        response = self.get_response(request)
        return super().process_response(request, response)

from django import http
from django.utils.deprecation import MiddlewareMixin

XS_SHARING_ALLOWED_ORIGINS = '*'
XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE', 'PATCH']
XS_SHARING_ALLOWED_HEADERS = ['Origin', 'X-Requested-With', 'Content-Type', 'Accept', 'Key', 'Token']


class ExtendedCorsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
            response['Access-Control-Allow-Headers'] = ",".join(XS_SHARING_ALLOWED_HEADERS)
            return response
        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if not response.has_header('Access-Control-Allow-Origin'):
            response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
            response['Access-Control-Allow-Headers'] = ",".join(XS_SHARING_ALLOWED_HEADERS)
        return response

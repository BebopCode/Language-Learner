# decorators.py

from django.http import JsonResponse
from functools import wraps
from .utils import validate_google_token

def google_auth_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]  # Remove 'Bearer ' prefix
            user_info = validate_google_token(token)
            if user_info:
                request.user_info = user_info
                return f(request, *args, **kwargs)
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    return wrap

import traceback
import jwt
from middleware.response import unauthorized
from authentication.models import Session
from banodoco.settings import SECRET_KEY, STATIC_AUTH_TOKEN

def auth_required(*users):
    def authenticator(func):
        def wrap(context, request):
            if 'HTTP_AUTHORIZATION' not in request.META:
                return unauthorized({})

            token = request.META['HTTP_AUTHORIZATION']
            token = token.replace('Bearer ', '')

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            except:
                return unauthorized({})
            
            if data['role_type'] in users:
                request.role_type = data['role_type']
                request.role_id = data['role_id']
                return func(context, request)
            else:
                return unauthorized({})
            
        wrap.__name__ = func.__name__
        return wrap
    return authenticator

def static_auth_required():
    def authenticator(func):
        def wrap(context, request):
            if 'HTTP_AUTHORIZATION' not in request.META:
                return unauthorized({})

            token = request.META['HTTP_AUTHORIZATION']
            if token != STATIC_AUTH_TOKEN:
                return unauthorized({})
            
            return func(context, request)
            
        wrap.__name__ = func.__name__
        return wrap
    
    return authenticator

def refresh_token():
    def authenticator(func):
        def wrap(context, request):
            if 'HTTP_AUTHORIZATION' not in request.META:
                return unauthorized({})

            token = request.META['HTTP_AUTHORIZATION']
            token = token.replace('Bearer ', '')
            
            if not Session.objects.filter(refresh_token=token).exists():
                return unauthorized({})
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            except:
                return unauthorized({})
                
            request.role_type = data['role_type']
            request.role_id = data['role_id']
            return func(context, request)
            
        wrap.__name__ = func.__name__
        return wrap
    return authenticator
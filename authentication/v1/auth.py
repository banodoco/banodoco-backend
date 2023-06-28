from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from authentication.models import Session
from authentication.service import get_model_instance
from authentication.v1.serializers.dto import UserDto
from middleware.response import bad_request, success, error, unauthorized
from middleware.authentication import auth_required, refresh_token
from user.models import User
from authentication.v1.serializers.dao import UserLoginDao
from util.token import generate_tokens

class UserLoginView(APIView):
    def post(self, request):
        attributes = UserLoginDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        user = User.objects.filter(email=attributes.data['email'], is_disabled=False).first()
        if not user or not check_password(attributes.data['password'], user.password):
            return success({}, 'invalid credentials', False)
        
        token, refresh_token = generate_tokens(user.uuid, user.type)
        Session.objects.create(role_id=user.id, role_type=user.type, token=token, refresh_token=refresh_token)

        payload = {
            'token' : token,
            'refresh_token' : refresh_token,
            'user' : UserDto(user).data
        }
        
        return success(payload, "login successfully", True)
    

class RefreshTokenView(APIView):
    @refresh_token()
    def get(self, request):
        user = get_model_instance(
            model_id=request.role_id, model_type=request.role_type
        )
        if not user:
            return success({}, "no user found", False)

        token, refresh_token = generate_tokens(user.uuid, request.role_type)
        Session.objects.create(
            role_id=user.id,
            role_type=request.role_type,
            token=token,
            refresh_token=refresh_token,
        )

        payload = {"token": token, "refresh_token": refresh_token}

        return success(payload, "token refreshed successfully", True)
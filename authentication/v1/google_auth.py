import json
import traceback
from ai_data.models import TrainingData
from authentication.models import Session
from authentication.v1.serializers.dao import GoogleIDTokenDao
from rest_framework.views import APIView
from authentication.v1.serializers.dto import BasicUserDto

from middleware.response import bad_request, success
from user.models import User
from util.google_auth.auth import GoogleAuth
from util.sentry import log_sentry_exception
from util.slack.channels import SLACK_APP_SIGNUP_CHANNEL, SLACK_DATA_UPLOAD_CHANNEL
from util.slack.slack import SlackClient
from util.token import generate_tokens


class UserGoogleLoginView(APIView):
    # @auth_required("user")
    def post(self, request):
        attributes = GoogleIDTokenDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        google_auth = GoogleAuth()
        user_data = google_auth.authenticate_user(attributes.data["id_token"])
        if not user_data:
            return success({}, "invalid auth token", False)
        
        invite_data = TrainingData.objects.filter(video_url='invite_list', is_disabled=False).first()
        if invite_data:
            invite_list = json.loads(invite_data.user_data) if invite_data.user_data else []
            if user_data["email"] not in invite_list:
                return success({}, "user not in the invite list", False)
        else:
            return success({}, "user not in the invite list", False)

        user = User.objects.filter(email=user_data["email"], is_disabled=False).first()
        if not user:
            # user_data['credits'] = 20
            user = User.objects.create(**user_data)

        token, refresh_token = generate_tokens(user.uuid, user.type)
        Session.objects.create(
            role_id=user.id, role_type="user", token=token, refresh_token=refresh_token
        )

        payload = {
            "token": token,
            "refresh_token": refresh_token,
            "user": BasicUserDto(user).data
        }

        return success(payload, "token verified successfully", True)
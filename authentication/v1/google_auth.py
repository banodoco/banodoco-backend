import traceback
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
        
        user = User.objects.filter(email=user_data["email"], is_disabled=False).first()
        if not user:
            user_data['credits'] = 20
            user = User.objects.create(**user_data)
            try:
                slack_client = SlackClient()
                res = slack_client.send_message_to_channel(
                    channel=SLACK_APP_SIGNUP_CHANNEL,
                    text=f"Data upload update",
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "New user signup"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": user.email
                            },
                        },
                    ]
                )
            except Exception as e:
                log_sentry_exception("Banodoco user sign in error" + str(e), {}, traceback)

        token, refresh_token = generate_tokens(user.uuid, "user")
        Session.objects.create(
            role_id=user.id, role_type="user", token=token, refresh_token=refresh_token
        )

        payload = {
            "token": token,
            "refresh_token": refresh_token,
            "user": BasicUserDto(user).data
        }

        return success(payload, "token verified successfully", True)
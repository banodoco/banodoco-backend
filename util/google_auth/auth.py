from google.oauth2 import id_token
from google.auth.transport import requests

from neuralblade.settings import GOOGLE_AUTH_CLIENT_ID
from util.google_auth.serializers import GoogleUserDetailsDao


class GoogleAuth:
    def __init__(self):
        self.client_id = GOOGLE_AUTH_CLIENT_ID
    
    def authenticate_user(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), self.client_id)

            print("user_data found out: ", idinfo)
            user_data = GoogleUserDetailsDao(data=idinfo)
            if not user_data.is_valid():
                print("invalid user token: ", user_data.errors)
                return None

            res = {}
            res["email"] = user_data.data["email"]
            first_name = user_data.data["given_name"] if "given_name" in user_data.data else user_data.data["email"].split('@')[0].replace('.', '')
            last_name = user_data.data["family_name"] if "family_name" in user_data.data else ""
            res["name"] = first_name + (last_name if last_name else "")
            res["profile_pic_url"] = user_data.data["picture"] if "picture" in user_data.data else ""
            res["third_party_id"] = user_data.data["sub"]
            
            return res
        except Exception as e:
            print("invalid user token: ", e)
            return None
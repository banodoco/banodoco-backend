import asyncio
import httpx
from httpx_oauth.clients.google import GoogleOAuth2
import json

from banodoco.settings import GOOGLE_AUTH_CLIENT_ID, GOOGLE_AUTH_REDIRECT_URI, GOOGLE_CLIENT_SECRET
from util.google_auth.serializers import GoogleUserDetailsDao


class GoogleAuth:
    def __init__(self):
        self.client_id = GOOGLE_AUTH_CLIENT_ID
        self.client_secret = GOOGLE_CLIENT_SECRET
        self.redirect_uri = GOOGLE_AUTH_REDIRECT_URI

    async def get_access_token(self, client: GoogleOAuth2, redirect_uri: str, code: str):
        token = await client.get_access_token(code, redirect_uri)
        return token
    
    async def get_user_details(self, token):
        async with httpx.AsyncClient() as client:
            request_headers = {
                "Accept": "application/json",
            }
            url = "https://people.googleapis.com/v1/people/me"
            params = {"personFields": "emailAddresses,names,photos"}
            headers = {**request_headers, "Authorization": f"Bearer {token}"}

            response = await client.get(url, params=params, headers=headers)

            return response

    def authenticate_user(self, code):
        try:
            client: GoogleOAuth2 = GoogleOAuth2(self.client_id, self.client_secret)
            token = asyncio.run(self.get_access_token(client, self.redirect_uri, code))
            res = asyncio.run(self.get_user_details(token['access_token']))

            # TODO: remove repeated serialization
            res = json.loads(res.content)
            user_info = {}
            user_info['email'] = res['emailAddresses'][0]['value']
            user_info['given_name'] = res['names'][0]['givenName']
            user_info['family_name'] = res['names'][0]['familyName']
            user_info['picture'] = res['photos'][0]['url']
            user_info['sub'] = res['emailAddresses'][0]['metadata']['source']['id']

            user_data = GoogleUserDetailsDao(data=user_info)
            if not user_data.is_valid():
                print("invalid user token: ", user_data.errors)
                return None
            print("user_data found out: ", {user_data.data['sub']}, " email: ", {user_data.data['email']})

            res = {}
            res["email"] = user_data.data["email"]
            first_name = user_data.data["given_name"] if "given_name" in user_data.data else user_data.data["email"].split('@')[0].replace('.', '')
            last_name = user_data.data["family_name"] if "family_name" in user_data.data else ""
            res["name"] = first_name + (last_name if last_name else "")
            # res["profile_pic_url"] = user_data.data["picture"] if "picture" in user_data.data else ""
            res["third_party_id"] = user_data.data["sub"]
            
            return res
        except Exception as e:
            print("invalid user token: ", e)
            return None
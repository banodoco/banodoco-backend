from django.conf.urls import url
from authentication.v1.auth import RefreshTokenView, UserLoginView
from authentication.v1.google_auth import UserGoogleLoginView


urlpatterns = [
    url(r'^op$', UserLoginView.as_view()),
    url(r'^refresh$', RefreshTokenView.as_view()),
    url(r'^google$', UserGoogleLoginView.as_view()),
]
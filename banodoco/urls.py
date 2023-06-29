from django.contrib import admin
from django.conf.urls import url
from django.urls import include


urlpatterns = [
    url(r'^v1/user/', include('user.v1.urls')),
    url(r'^v1/authentication/', include('authentication.v1.urls')),
    url(r'^v1/data/', include('ai_model.v1.urls')),
]

from django.contrib import admin
from django.conf.urls import url
from django.urls import include

from banodoco.health_check import HealthCheckView


urlpatterns = [
    url(r'^v1/user/', include('user.v1.urls')),
    url(r'^v1/authentication/', include('authentication.v1.urls')),
    url(r'^v1/data/', include('ai_project.v1.urls')),
    url(r'^v1/payment/', include('payment.v1.urls')),
    url(r'^v1/training-data/', include('ai_data.v1.urls')),
    url(r'^health-check$', HealthCheckView.as_view())
]

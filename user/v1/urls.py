from django.conf.urls import url

from user.v1.crud import UserView

urlpatterns = [
    url(r'^user$', UserView.as_view()),
]
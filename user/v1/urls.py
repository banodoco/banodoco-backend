from django.conf.urls import url

from user.v1.crud import UserListView, UserView

urlpatterns = [
    url(r'^op$', UserView.as_view()),
    url(r'^list$', UserListView.as_view()),
]
from django.conf.urls import url

from ai_data.v1.data import TrainingDataCRUDView, TrainingDataListView


urlpatterns = [
    url(r'^op$', TrainingDataCRUDView.as_view()),
    url(r'^list$', TrainingDataListView.as_view()),
]
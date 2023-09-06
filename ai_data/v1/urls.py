from django.conf.urls import url

from ai_data.v1.data import TrainingDataCRUDView, TrainingDataListView


urlpatterns = [
    url(r'^training-data$', TrainingDataCRUDView.as_view()),
    url(r'^training-data/list$', TrainingDataListView.as_view()),
]
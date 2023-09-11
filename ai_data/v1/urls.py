from django.conf.urls import url

from ai_data.v1.data import TrainingDataCRUDView, TrainingDataListView
from ai_data.v1.image_caption import ImageCaptionCRUDView, ImageCaptionListView


urlpatterns = [
    url(r'^op$', TrainingDataCRUDView.as_view()),
    url(r'^list$', TrainingDataListView.as_view()),
    url(r'^img-op$', ImageCaptionCRUDView.as_view()),
    url(r'^img-list$', ImageCaptionListView.as_view()),

]
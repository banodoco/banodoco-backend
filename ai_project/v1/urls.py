from django.conf.urls import url
from ai_project.v1.ai_model import AIModelListView, AIModelView
from ai_project.v1.app_setting import AppSecretView, AppSettingView
from ai_project.v1.file import FileListView, FileUUIDListView, FileView, TempGalleryFileView, UploadFileView
from ai_project.v1.inference_log import InferenceLogListView, InferenceLogView
from ai_project.v1.project import ProjectListView, ProjectStatsView, ProjectView
from ai_project.v1.project_setting import LockAPIView, ProjectSettingView
from ai_project.v1.shot import ShotCRUDView, ShotClipView, ShotDuplicateView, ShotListView

from ai_project.v1.timing import FrameTimingView, ProjectTimingView, ShiftTimingView, TimingListView, TimingNumberView

urlpatterns = [
    # timing
    url(r'^timing$', FrameTimingView.as_view()),
    url(r'^timing/project$', ProjectTimingView.as_view()),
    url(r'^timing/number$', TimingNumberView.as_view()),
    url(r'^timing/shift$', ShiftTimingView.as_view()),
    url(r'^timing/list$', TimingListView.as_view()),
    # project
    url(r'^project$', ProjectView.as_view()),
    url(r'^project/list$', ProjectListView.as_view()),
    url(r'^project/stats$', ProjectStatsView.as_view()),
    # project setting
    url(r'^project-setting$', ProjectSettingView.as_view()),
    # inference log
    url(r'^log$', InferenceLogView.as_view()),
    url(r'^log/list$', InferenceLogListView.as_view()),
    # file
    url(r'^file$', FileView.as_view()),
    url(r'^file/upload$', UploadFileView.as_view()),
    url(r'^file/uuid-list$', FileUUIDListView.as_view()),
    url(r'^file/list$', FileListView.as_view()),
    url(r'^file/extra$', TempGalleryFileView.as_view()),
    # app setting
    url(r'^app-setting$', AppSettingView.as_view()),
    url(r'^app-secret$', AppSecretView.as_view()),
    # ai model
    url(r'^model$', AIModelView.as_view()),
    url(r'^model/list$', AIModelListView.as_view()),
    # lock
    url(r'^lock$', LockAPIView.as_view()),
    # shot
    url(r'^shot$', ShotCRUDView.as_view()),
    url(r'^shot/list$', ShotListView.as_view()),
    url(r'^shot/interpolated-clip$', ShotClipView.as_view()),
    url(r'^shot/duplicate$', ShotDuplicateView.as_view()),
]
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from uploader.views import *

urlpatterns = [
    path('', UploadCreateView.as_view(), name='uploader-upload'),
    path('view/<int:pk>', UploadDetailView.as_view(), name='uploader-view'),
    path('list', UploadListView.as_view(), name='uploader-list')
]

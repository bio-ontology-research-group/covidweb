from django.urls import include, path
from django.contrib.auth.decorators import login_required
from uploader.api_views import *

urlpatterns = [
    path('metadata/<col_id>', SyncMetadataRDF.as_view()),
]

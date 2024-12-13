from django.urls import path
from .views import WorkspaceDetailView, BlockListView

urlpatterns = [
    path('workspace/', WorkspaceDetailView.as_view(), name='workspace-detail'),
    path('blocks/', BlockListView.as_view(), name='block-list'),
]

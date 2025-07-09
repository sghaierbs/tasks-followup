from django.urls import path
from .views import *

urlpatterns = [
    path('', SnippetListView.as_view(), name='snippet-list'),
    path('create/', SnippetCreateView.as_view(), name='snippet-create'),
    path('<int:pk>/', SnippetDetailView.as_view(), name='snippet-detail'),
    path('<int:pk>/edit/', SnippetUpdateView.as_view(), name='snippet-edit'),
    path('<int:pk>/delete/', SnippetDeleteView.as_view(), name='snippet-delete'),
]
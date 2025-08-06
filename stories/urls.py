from django.urls import path
from .views import *

urlpatterns = [
    path('', UserStoryListView.as_view(), name='userstory-list'),
    path('<int:pk>/', UserStoryDetailView.as_view(), name='userstory-detail'),
    path('create/', UserStoryCreateView.as_view(), name='userstory-create'),
    path('<int:pk>/edit/', UserStoryUpdateView.as_view(), name='userstory-update'),
    path('<int:pk>/delete/', UserStoryDeleteView.as_view(), name='userstory-delete'),
]
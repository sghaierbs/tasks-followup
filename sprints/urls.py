from django.urls import path
from .views import SprintDeleteView, SprintDetailView, SprintListView, SprintManageView, SprintUpdateView, SprintUserStoriesView, SprintCreateView

urlpatterns = [
    path('', SprintListView.as_view(), name='manage-sprints'),
    path('current/', SprintUserStoriesView.as_view(), name='current-sprint'),
    path('<int:pk>/', SprintDetailView.as_view(), name='sprint-detail'),
    path('create/', SprintCreateView.as_view(), name='sprint-create'),
    path('<int:pk>/edit/', SprintUpdateView.as_view(), name='sprint-update'),
    path('<int:pk>/delete/', SprintDeleteView.as_view(), name='sprint-delete'),
]
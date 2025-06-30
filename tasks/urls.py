from django.urls import path
from .views import TaskListView, TaskDetailView, TaskUpdateView, TaskCreateView, UserTaskListView, UserPrivateTaskListView, TaskDeleteView, TaskSearchView, ResolveTaskView, ArchiveTaskView, ArchivedTaskListView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('archived/', ArchivedTaskListView.as_view(), name='archived-task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task-edit'),
    path('new/', TaskCreateView.as_view(), name='task-create'),
    path('<str:username>/', UserTaskListView.as_view(), name='user_tasks'),
    path('<str:username>/private', UserPrivateTaskListView.as_view(), name='private_tasks'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/search/', TaskSearchView.as_view(), name='task-search'),
    path('tasks/<int:pk>/resolve/', ResolveTaskView.as_view(), name='task-resolve'),
    path('tasks/<int:pk>/archive/', ArchiveTaskView.as_view(), name='task-archive'),
]
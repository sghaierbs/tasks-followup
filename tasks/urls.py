from django.urls import path
from .views import TaskCreateAjaxView, TaskListView, TaskDetailView, TaskUpdateView, TaskCreateView, TaskDeleteView, \
                   TaskSearchView, ResolveTaskView, ArchiveTaskView, TaskProgressView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('progress/', TaskProgressView.as_view(), name='progress-view'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task-edit'),
    path('new/', TaskCreateView.as_view(), name='task-create'),
    path('create/', TaskCreateAjaxView.as_view(), name='task-create-ajax'),
    #path('<str:username>/', UserTaskListView.as_view(), name='user_tasks'),
    #path('<str:username>/private', UserPrivateTaskListView.as_view(), name='private_tasks'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/search/', TaskSearchView.as_view(), name='task-search'),
    path('tasks/<int:pk>/resolve/', ResolveTaskView.as_view(), name='task-resolve'),
    path('tasks/<int:pk>/archive/', ArchiveTaskView.as_view(), name='task-archive'),
]
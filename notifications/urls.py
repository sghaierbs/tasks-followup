# notifications/urls.py
from django.urls import path
from . import views
from .views import NotificationsListView

urlpatterns = [
    path('', NotificationsListView.as_view(), name='notification-list'),
    path('read/<int:pk>/', views.mark_notification_read, name='notification-read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_as_read, name='notification-mark-all-read'),
]

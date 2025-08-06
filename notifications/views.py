from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.db.models import Q
from tasks.models import Task

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()

    related_object = notification.related_object

    # Mapping model class to reverse URL name
    model_url_map = {
        'Task': 'task-detail',
        'Assignment': 'assignment-detail',
        'UserStory': 'userstory-detail',
        # Add more mappings as needed
    }

    model_name = related_object.__class__.__name__
    url_name = model_url_map.get(model_name)

    if url_name:
        url = reverse(url_name, args=[related_object.id])
    else:
        url = '/'  # fallback URL

    return redirect(url)

@login_required
def mark_all_notifications_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notification-list')


class NotificationsListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notifications_list.html'
    paginate_by = 15


    def get_queryset(self):
        user = self.request.user
        filter_option = self.request.GET.get('filter', 'all')
        base_queryset = Notification.objects.filter(Q(user=user))
        # if filter_option != 'all':
        #     return base_queryset.filter(status__name=filter_option).order_by('-created_at')
        return base_queryset.order_by('-created_at')
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from stories.models import UserStory
from .models import Task
from .forms import TaskForm
from .mixins import EventLoggingMixin
from django.db.models import Q
from core.models import EventActions, TrackableStatus
from core.mixins import CommentableObjectMixin
from django.views.generic.edit import FormMixin
from core.forms import CommentForm
from django.urls import reverse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.utils import create_and_send_notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def task_create_ajax(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        story_id = request.GET.get('story_id')
        story = UserStory.objects.get(id=story_id)

        task = Task.objects.create(title=title, description=description, story=story)
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'description': task.description
        })

class TaskCreateAjaxView(CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        story_id = self.request.POST.get('story_id')
        form.instance.user_story_id = story_id
        print("---------------------- ", form)
        form.instance.created_by = self.request.user
        task = form.save()
        print("---------------------- created tak ", task)
        
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'status': task.status.id,
        })

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)



class TaskProgressView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/progress_view.html'


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    paginate_by = 15


    def get_queryset(self):
        user = self.request.user
        filter_option = self.request.GET.get('filter', 'all')
        base_queryset = Task.objects.filter(Q(visibility='public') | Q(created_by=user))
        if filter_option != 'all':
            return base_queryset.filter(status__name=filter_option).order_by('-created_at')
        return base_queryset.order_by('-created_at')
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_set'] = TrackableStatus.objects.all()
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context


class TaskDetailView(LoginRequiredMixin, FormMixin, DetailView, CommentableObjectMixin):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_comments(self.object)
        context['form'] = self.get_comment_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.save_comment(request, self.object)
        return super().form_valid(self.get_form())




class TaskUpdateView(LoginRequiredMixin, EventLoggingMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'  # Shared form for edit

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Log event after the object is successfully saved
        self.log_event(
            actor=self.request.user,
            action=EventActions.UPDATED,
            instance=self.object,
            notes="User updated the task"
        )
        for assignee in self.object.assignees.all():
            create_and_send_notification(
                user=assignee,
                created_by=self.request.user,
                notif_type="task",
                title="Task updated",
                message=f"{self.request.user.get_full_name()} updated the following task: #{self.object.id}",
                related_object=self.object
            )
        return response

    
class TaskCreateView(LoginRequiredMixin, EventLoggingMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'


    def get_success_url(self):
        for assignee in self.object.assignees.all():
            print(f"------ get_success_url ")
            create_and_send_notification(
                user=assignee,
                created_by=self.request.user,
                notif_type="task",
                title="You have been assigned a new task",
                message=f"{self.request.user.get_full_name()} assigned you the task: #{self.object.id}",
                related_object=self.object
            )
        return reverse_lazy('task-detail', kwargs={'pk': self.object.pk})


    def form_valid(self, form):
        print(f"------ form_valid ")
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        self.log_event(
            actor=self.request.user,
            action=EventActions.CREATED,
            instance=self.object,
            notes="User created a new task"
        )
        return response
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # this will be used by the task forms.py in order to set the default value of assignee to the current logged in user
        kwargs['user'] = self.request.user
        print(f"------ get_form_kwargs ")
        return kwargs
    

class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.created_by == request.user:
            task.delete()
        return redirect('task-list')
    
    

class TaskSearchView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get("q")
        if query:
            return Task.objects.filter(
                (Q(title__icontains=query) | Q(description__icontains=query)) & (Q(visibility='public') | Q(created_by=user))
            )
        return Task.objects.filter(Q(visibility='public') | Q(created_by=user))  # or all() to return everything on empty query
    



class ResolveTaskView(LoginRequiredMixin, EventLoggingMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user == task.created_by:
            task.is_completed = True
            task.save()
            self.log_event(
                actor=self.request.user,
                action=EventActions.UPDATED,
                instance=task,
                notes="Task marked as completed."
            )
        return redirect(request.META.get('HTTP_REFERER', 'task-list'))

class ArchiveTaskView(LoginRequiredMixin, EventLoggingMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user == task.created_by:
            task.is_archived = True
            task.save()
            self.log_event(
                actor=self.request.user,
                action=EventActions.UPDATED,
                instance=task,
                notes="Task marked as archived."
            )
        print("calling redurection to task list")
        return redirect(request.META.get('HTTP_REFERER', 'task-list'))
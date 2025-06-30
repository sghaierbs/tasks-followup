from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from .mixins import EventLoggingMixin
from django.db.models import Q
from core.models import EventActions, TrackableStatus
from core.mixins import CommentableObjectMixin
from django.views.generic.edit import FormMixin
from core.forms import CommentForm
from django.urls import reverse


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
    
class ArchivedTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/archived_task_list.html'
    paginate_by = 15


    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter((Q(visibility='public') | Q(created_by=user)) & Q(is_archived=True)).order_by('-created_at')


class TaskDetailView(FormMixin, DetailView, CommentableObjectMixin):
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
        return response
    
class TaskCreateView(LoginRequiredMixin, EventLoggingMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'


    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.pk})


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        self.log_event(
            actor=self.request.user,
            action=EventActions.CREATED,
            instance=self.object,
            notes="User created a new task"
        )
        return response
    

class UserTaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs['username']
        return Task.objects.filter(assignee__username=username)
    

class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.created_by == request.user:
            task.delete()
        return redirect('task-list')
    


class UserPrivateTaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 5

    
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(visibility='private') & Q(created_by=user))
    

class TaskSearchView(ListView):
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
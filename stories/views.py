from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from assignments.forms import AssignmentForm
from notifications.utils import create_and_send_notification
from .models import UserStory
from .forms import UserStoryForm, UserStoryUpdateForm  # created below
from sprints.models import Sprint
from django.urls import reverse

class UserStoryListView(ListView):
    model = UserStory
    template_name = "stories/userstory_list.html"
    context_object_name = "stories"

class UserStoryDetailView(DetailView):
    model = UserStory
    template_name = "stories/userstory_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment_form'] = AssignmentForm()
        context['assignments'] = self.object.assignments.all()
        return context

class UserStoryCreateView(CreateView):
    model = UserStory
    form_class = UserStoryForm
    template_name = "stories/userstory_form.html"
    success_url = reverse_lazy("userstory-list")

    def get_initial(self):
        initial = super().get_initial()
        sprint_id = self.request.GET.get('sprint')
        if sprint_id:
            initial['sprint'] = sprint_id
        return initial
    
    def form_valid(self, form):
        # Ensure sprint is set manually in case someone removes it from the form
        form.instance.created_by = self.request.user
        sprint_id = self.request.GET.get('sprint')
        if sprint_id:
            form.instance.sprint = Sprint.objects.get(id=sprint_id)
        return super().form_valid(form)


    def get_success_url(self):
        if self.object.assignee:    
            create_and_send_notification(
                user=self.object.assignee,
                created_by=self.request.user,
                notif_type="User Story",
                title="User Story Created",
                message=f"{self.request.user.get_full_name()} created a new user story: #{self.object.id}",
                related_object=self.object
            )
        return reverse('userstory-detail', kwargs={'pk': self.object.pk})

class UserStoryUpdateView(UpdateView):
    model = UserStory
    form_class = UserStoryUpdateForm
    template_name = "stories/userstory_update_form.html"
    #success_url = reverse_lazy("userstory-list")


    def get_success_url(self):
        # redirect user to user story details view 
        return reverse('userstory-detail', kwargs={'pk': self.object.pk})

class UserStoryDeleteView(DeleteView):
    model = UserStory
    template_name = 'userstories/userstory_confirm_delete.html'

    def get_success_url(self):
        sprint = self.object.sprint
        return f"{reverse('current-sprint')}?sprint_id={sprint.pk}"

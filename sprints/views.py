from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from sprints.forms import SprintForm
from .models import Sprint
from stories.models import UserStory
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin



from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin




class SprintUserStoriesView(LoginRequiredMixin, TemplateView):
    template_name = "sprints/current_sprint.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_sprint_id = self.request.GET.get("sprint")
        sprints = Sprint.objects.all()
        context["sprints"] = sprints

        if selected_sprint_id:
            selected_sprint = get_object_or_404(Sprint, id=selected_sprint_id)
        else:
            selected_sprint = Sprint.objects.filter(is_current=True).first()

        context["selected_sprint"] = selected_sprint

        if selected_sprint:
            stories = UserStory.objects.filter(sprint=selected_sprint)
            context["stories"] = stories
        else:
            context["stories"] = []

        return context
    

def is_sprint_manager(user):
    return user.groups.filter(name='sprint_manager').exists()


@method_decorator(user_passes_test(is_sprint_manager), name='dispatch')
class SprintManageView(LoginRequiredMixin, ListView):
    pass




class SprintListView(LoginRequiredMixin, ListView):
    model = Sprint
    template_name = 'sprints/sprint_list.html'
    context_object_name = 'sprints'


class SprintDetailView(LoginRequiredMixin, DetailView):
    model = Sprint
    template_name = 'sprints/sprint_details.html'
    context_object_name = 'sprint'


class SprintCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Sprint
    form_class = SprintForm
    template_name = 'sprints/sprint_form.html'
    success_url = reverse_lazy('manage-sprints')
    permission_required = 'sprints.add_sprint'

    def get_context_data(self, **kwargs):
        '''
        This is used to set the title of the form dynamically using context
        in order to be able to use the same form for create edit
        '''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Sprint'
        return context


class SprintUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Sprint
    form_class = SprintForm
    template_name = 'sprints/sprint_form.html'
    success_url = reverse_lazy('manage-sprints')
    permission_required = 'sprints.change_sprint'

    def get_context_data(self, **kwargs):
        '''
        This is used to set the title of the form dynamically using context
        in order to be able to use the same form for create edit
        '''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Sprint'
        return context


class SprintDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Sprint
    template_name = 'sprints/sprint_confirm_delete.html'
    success_url = reverse_lazy('manage-sprints')
    context_object_name = 'sprint'
    permission_required = 'sprints.delete_sprint'
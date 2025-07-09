from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Snippet
from .forms import SnippetForm
from django.urls import reverse

class SnippetListView(LoginRequiredMixin, ListView):
    model = Snippet
    template_name = 'snippets/snippet_list.html'
    context_object_name = 'snippets'
    paginate_by = 15

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return Snippet.objects.filter(
            Q(title__icontains=q) |
            Q(tags__icontains=q) |
            Q(code__icontains=q),
            created_by=self.request.user
        ).order_by('-created_at')

class SnippetDetailView(LoginRequiredMixin, DetailView):
    model = Snippet
    template_name = 'snippets/snippet_detail.html'

class SnippetCreateView(LoginRequiredMixin, CreateView):
    model = Snippet
    form_class = SnippetForm
    template_name = 'snippets/snippet_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('snippet-detail', kwargs={'pk': self.object.pk})

class SnippetUpdateView(LoginRequiredMixin, UpdateView):
    model = Snippet
    form_class = SnippetForm
    template_name = 'snippets/snippet_form.html'

    def get_success_url(self):
        return reverse('snippet-detail', kwargs={'pk': self.object.pk})

class SnippetDeleteView(LoginRequiredMixin, DeleteView):
    model = Snippet
    template_name = 'snippets/snippet_confirm_delete.html'
    success_url = reverse_lazy('snippet-list')
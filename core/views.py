from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from assignments.forms import AssignmentForm
from assignments.models import Assignment
from sprints.models import Sprint
from stories.models import UserStory
from django.db.models import Prefetch, Count
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sprints'] = Sprint.objects.all()
        context['sprint_id'] = Sprint.objects.filter(is_current=True)
        context['assignment_form'] = AssignmentForm()

        users = User.objects.annotate(assignment_count=Count('assignments')
        ).prefetch_related(
            Prefetch('assignments', queryset=Assignment.objects.all())
        )

        context['users'] = users
        return context
    
    
class GanttDataView(LoginRequiredMixin, View):

    TASK_STATUS_TO_CLASS = {
        'pending': 'gtaskyellow',
        'started': 'gtaskred',
        'done': 'gtaskgreen',
    }


    def get(self, request, *args, **kwargs):
        data = []
        task_id = 1
        sprint_id_filter = request.GET.get("sprint_id")

        sprint_qs = Sprint.objects.all().prefetch_related(
            Prefetch('user_stories', queryset=UserStory.objects.prefetch_related(
                Prefetch('assignments', queryset=Assignment.objects.prefetch_related('assignee'))
            ))
        )
        

        if sprint_id_filter and sprint_id_filter != 'all':
            sprint_qs = sprint_qs.filter(id=sprint_id_filter)
        else:
            active = Sprint.objects.filter(is_current=True).first()
            if active:
                sprint_qs = sprint_qs.filter(id=active.id)

        for sprint in sprint_qs:
            sprint_id = task_id
            data.append({
                "pID": sprint_id,
                "pName": sprint.name,
                "pStart": sprint.start_date.strftime('%Y-%m-%d') if sprint.start_date else '',
                #Adding the hours to stretch the taskbar in jsgantt to cover a whole day task
                "pEnd": sprint.end_date.strftime('%Y-%m-%d')+' 23:59' if sprint.end_date else '',
                "pClass": "ggroupblack",
                "pGroup": 1,
                "pOpen": 1,
                "pParent": 0
            })
            task_id += 1

            for story in sprint.user_stories.all():
                story_id = task_id
                data.append({
                    "pID": story_id,
                    "pName": story.title,
                    "pStart": story.planned_start_date.strftime('%Y-%m-%d') if story.planned_start_date else '',
                    #Adding the hours to stretch the taskbar in jsgantt to cover a whole day task
                    "pEnd": story.planned_end_date.strftime('%Y-%m-%d')+' 23:59' if story.planned_end_date else '',
                    "pClass": "gtaskblue",
                    "pGroup": 1,
                    "pOpen": 1,
                    "pParent": sprint_id
                })
                task_id += 1
                first = True
                for assignment in story.assignments.all():
                    data.append({
                        "pID": task_id,
                        "pName": f"{assignment.get_assignment_type_display()} ({assignment.assignee.get_full_name()})",
                        "pStart": assignment.planned_start_date.strftime('%Y-%m-%d') if assignment.planned_start_date else '',
                        #Adding the hours to stretch the taskbar in jsgantt to cover a whole day task
                        "pEnd": assignment.planned_end_date.strftime('%Y-%m-%d')+' 23:59' if assignment.planned_end_date else '',
                        "pClass": GanttDataView.TASK_STATUS_TO_CLASS.get(assignment.status, ''),
                        "pGroup": 0,
                        "pDepend": task_id-1 if not first else "",
                        "pParent": story_id,
                        "pBarText": assignment.get_assignment_type_display(),
                        "pComp": assignment.completion if assignment.completion else "",
                        "pCaption": assignment.get_assignment_type_display(),
                        "pRes": assignment.assignee.get_full_name(),
                        "pPlanStart": assignment.start_date.strftime('%Y-%m-%d') if assignment.start_date else '',
                        #Adding the hours to expand the taskbar in jsgantt to cover a whole day task
                        "pPlanEnd": assignment.end_date.strftime('%Y-%m-%d')+' 23:59' if assignment.end_date else '',
                        "team": assignment.get_assignment_type_display(),
                        "sprint": sprint.name,
                        "current": "🔥" if assignment.status == 'started' else '',
                        "userStoryID": story_id
                    })
                    first = False
                    task_id += 1

        return JsonResponse(data, safe=False)


class AssignmentsDataView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        sprint_id = request.GET.get('sprint_id')

        if not sprint_id:
            return JsonResponse({'error': 'No sprint ID provided'}, status=400)

        users = User.objects.prefetch_related(
            Prefetch(
                'assignments',
                queryset=Assignment.objects.filter(
                    user_story__sprint_id=sprint_id
                ).select_related('user_story')
            )
        )

        data = []
        for user in users:
            assignments = [
                {
                    'title': assignment.user_story.title,
                    'id': assignment.id,
                    'status': assignment.status,
                } for assignment in user.assignments.all()
            ]
            data.append({
                'user': {
                    'id':user.id,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'full_name':user.get_full_name(),
                 },
                'assignments': assignments,
            })

        return JsonResponse({'data': data})
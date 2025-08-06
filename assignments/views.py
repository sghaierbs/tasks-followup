# assignments/views.py
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.http import JsonResponse

from notifications.utils import create_and_send_notification
from stories.models import UserStory
from .models import Assignment
from .forms import AssignmentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.utils.timezone import now

        
@method_decorator(csrf_exempt, name='dispatch')
class AssignmentReorderView(View):
    '''
    This used by by the drag and drop reorder assignments under user story details view 
    it will be overridden by the event of creating a new assignment
    because everytime a new assignment is created the sort_order will be re-computed again based on planned_start_date property.
    '''
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            for item in data.get('order', []):
                Assignment.objects.filter(id=item['id']).update(sort_order=item['sort_order'])
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        

class AssignmentCreateAjaxView(CreateView):
    model = Assignment
    form_class = AssignmentForm

    def form_valid(self, form):
        '''
        Assignments will be sorted based on planned_start_date using the sort_order property whenever a new assignment is created
        and linked to the same user story
        '''
        user_story_id = self.request.POST.get('user_story_id')
        form.instance.user_story_id = user_story_id
        form.instance.created_by = self.request.user  # Set creator
        assignment = form.save()
        assignee_data = None
        if assignment.assignee:
            create_and_send_notification(
                user=assignment.assignee,
                created_by=self.request.user,
                notif_type="User Story",
                title="You have been assigned to a user story",
                message=f"{self.request.user.get_full_name()} Assigned you the user story: #{user_story_id}",
                related_object=get_object_or_404(UserStory, id=user_story_id)
            )
            assignee_data = {
                "id": assignment.assignee.id,
                "username": assignment.assignee.username,
                "first_name": assignment.assignee.first_name,
                "last_name": assignment.assignee.last_name
            }
        return JsonResponse({
            'id': assignment.id,
            'type': assignment.get_assignment_type_display(),
            "completion": assignment.completion if assignment.completion else "",
            'status': assignment.status,
            'planned_start_date': assignment.planned_start_date,
            'planned_end_date': assignment.planned_end_date,
            "start_date": assignment.start_date.strftime('%Y-%m-%d') if assignment.start_date else "",
            "end_date": assignment.end_date.strftime('%Y-%m-%d') if assignment.end_date else "",
            'assignee': assignee_data,
        })

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)


class AssignmentUpdateAjaxView(UpdateView):
    model = Assignment
    form_class = AssignmentForm

    def form_valid(self, form):
        assignment = form.save()
        assignee_data = None
        if assignment.assignee:
            assignee_data = {
                "id": assignment.assignee.id,
                "username": assignment.assignee.username,
                "first_name": assignment.assignee.first_name,
                "last_name": assignment.assignee.last_name
            }
        return JsonResponse({
            'id': assignment.id,
            'type': assignment.get_assignment_type_display(),
            "completion": assignment.completion if assignment.completion else "",
            'status': assignment.status,
            'planned_start_date': assignment.planned_start_date,
            'planned_end_date': assignment.planned_end_date,
            "start_date": assignment.start_date.strftime('%Y-%m-%d') if assignment.start_date else "",
            "end_date": assignment.end_date.strftime('%Y-%m-%d') if assignment.end_date else "",
            "assignee": assignee_data
        })

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)
    
class AssignmentDetailJsonView(View):
    
    def get(self, request, pk):
        assignment = Assignment.objects.get(pk=pk)
        return JsonResponse({
            "id": assignment.id,
            "assignment_type": assignment.assignment_type,
            "completion": assignment.completion if assignment.completion else "",
            "status": assignment.status,
            "planned_start_date": assignment.planned_start_date.strftime('%Y-%m-%d') if assignment.planned_start_date else "",
            "planned_end_date": assignment.planned_end_date.strftime('%Y-%m-%d') if assignment.planned_end_date else "",
            "start_date": assignment.start_date.strftime('%Y-%m-%d') if assignment.start_date else "",
            "end_date": assignment.end_date.strftime('%Y-%m-%d') if assignment.end_date else "",
            "assignee": assignment.assignee.id if assignment.assignee else None,
        })
    

class AssignmentDeleteAjaxView(View):
    def post(self, request, pk):
        Assignment.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True})
    

class StartAssignmentView(LoginRequiredMixin, View):
    '''
    This function is used in Javascript code to update the status of an assignment from within a user story details view.
    '''
    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        if assignment.assignee != request.user:
            return HttpResponseForbidden("You can only start your own assignments.")
        if assignment.status != 'pending':
            return JsonResponse({'success': False,"error": "Assignment not in pending status."}, status=400)
        
        if not assignment.can_be_started():
            # Check if all previous assignment are done or not in order to start the current.
            return JsonResponse({'success': False, 'error': 'Previous assignments must be done'}, status=400)

        assignment.status = 'started'
        assignment.start_date = now()
        assignment.save()
        return JsonResponse({"success": True, "assignment":{
            "id": assignment.id,
            "assignment_type": assignment.assignment_type,
            "completion": assignment.completion if assignment.completion else "",
            "status": assignment.status,
            "planned_start_date": assignment.planned_start_date.strftime('%Y-%m-%d') if assignment.planned_start_date else "",
            "planned_end_date": assignment.planned_end_date.strftime('%Y-%m-%d') if assignment.planned_end_date else "",
            "start_date": assignment.start_date.strftime('%Y-%m-%d') if assignment.start_date else "",
            "end_date": assignment.end_date.strftime('%Y-%m-%d') if assignment.end_date else "",
            "assignee": assignment.assignee.id if assignment.assignee else None,
        }})


class MarkAssignmentDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        if assignment.assignee != request.user:
            return HttpResponseForbidden("You can only update your own assignments.")
        if assignment.status != 'started':
            return JsonResponse({'success': False,"error": "Assignment not in started status."}, status=400)
        
        if not assignment.can_be_started():
            return JsonResponse({'success': False, 'error': 'Previous assignments must be done'}, status=400)

        assignment.status = 'done'
        assignment.end_date = now()
        assignment.save()
        return JsonResponse({"success": True, "assignment":{
            "id": assignment.id,
            "assignment_type": assignment.assignment_type,
            "completion": assignment.completion if assignment.completion else "",
            "status": assignment.status,
            "planned_start_date": assignment.planned_start_date.strftime('%Y-%m-%d') if assignment.planned_start_date else "",
            "planned_end_date": assignment.planned_end_date.strftime('%Y-%m-%d') if assignment.planned_end_date else "",
            "start_date": assignment.start_date.strftime('%Y-%m-%d') if assignment.start_date else "",
            "end_date": assignment.end_date.strftime('%Y-%m-%d') if assignment.end_date else "",
            "assignee": assignment.assignee.id if assignment.assignee else None,
        }})
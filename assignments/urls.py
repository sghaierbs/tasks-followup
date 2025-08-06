# assignments/urls.py
from django.urls import path
from .views import AssignmentCreateAjaxView, AssignmentDetailJsonView, AssignmentReorderView, AssignmentUpdateAjaxView, AssignmentDeleteAjaxView, MarkAssignmentDoneView, StartAssignmentView

urlpatterns = [
    path('create/', AssignmentCreateAjaxView.as_view(), name='assignment-create-ajax'),
    path('update/<int:pk>/', AssignmentUpdateAjaxView.as_view(), name='assignment-update-ajax'),
    path('delete/<int:pk>/', AssignmentDeleteAjaxView.as_view(), name='assignment-delete-ajax'),
    path('<int:pk>/json/', AssignmentDetailJsonView.as_view(), name='assignment-json'),
    path('reorder/', AssignmentReorderView.as_view(), name='update_assignment_order'),

    path('<int:pk>/start/', StartAssignmentView.as_view(), name='assignment-start'),
    path('<int:pk>/done/', MarkAssignmentDoneView.as_view(), name='assignment-done'),
]
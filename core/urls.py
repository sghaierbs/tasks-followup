from django.urls import path
from .views import AssignmentsDataView, GanttDataView, HomePageView


urlpatterns = [
    # path("", views.index, name="index"),
    path('', HomePageView.as_view(), name='home'),
    path('api/sprints/json/', GanttDataView.as_view(), name='sprints-data-json'),
    path('api/sprint/assignments/json/', AssignmentsDataView.as_view(), name='assignments-by-sprint-json'),
]

from django.urls import path
from .views import HomePageView


urlpatterns = [
    # path("", views.index, name="index"),
    path('', HomePageView.as_view(), name='home'),
]

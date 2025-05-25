from django.urls import path

from . import views


urlpatterns = [
    path('<int:id>/location/', views.UserLastLocationView.as_view()),
]

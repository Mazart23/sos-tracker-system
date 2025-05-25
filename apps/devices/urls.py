from django.urls import path

from . import views


urlpatterns = [
    path('<str:id>/assign/', views.AssignDeviceView.as_view()),
    path('<str:id>/location/', views.PingLocationView.as_view()),
    path('<str:id>/unassign/', views.UnassignDeviceView.as_view()),
    path('', views.ListDevicesView.as_view()),
]

from django.urls import path
from .views import trigger_worker_view

urlpatterns = [
    path('start/', trigger_worker_view, name='run-generator')
]
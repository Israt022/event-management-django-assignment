from django.urls import path
from tasks.views import view_task


urlpatterns = [
    path('views/', view_task),
]
from django.urls import path
from tasks.views import main,category_form,event_form,participant_form,dashboard,category_list,event_list,participant_list,category_update,category_delete,event_update,event_delete,participant_update,participant_delete,event_detail


urlpatterns = [
    path('main/', main ,name='main'),
    path('dashboard/', dashboard , name = 'dashboard'),
    path('category_list/', category_list , name = 'category_list'),
    path('event_list/', event_list , name = 'event_list'),
    path('participant_list/', participant_list , name = 'participant_list'),
    path('category_form/', category_form ,name = 'category_form'),
    path('event_form/', event_form , name = 'event_form'),
    path('participant_form/', participant_form,name = 'participant_form'),
    
    path('category_update/<int:id>/', category_update,name = 'category_update'),
    path('category_delete/<int:id>/', category_delete,name = 'category_delete'),
    path('event_update/<int:id>/', event_update,name = 'event_update'),
    path('event_delete/<int:id>/', event_delete,name = 'event_delete'),
    path('event_detail/<int:id>/', event_detail,name = 'event_detail'),
    path('participant_update/<int:id>/', participant_update,name = 'participant_update'),
    path('participant_delete/<int:id>/', participant_delete,name = 'participant_delete'),

    
]
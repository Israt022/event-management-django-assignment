from django.urls import path
from tasks.views import main,category_form,event_form,dashboard,category_list,event_list,participant_list,category_update,category_delete,event_update,event_delete,participant_delete,event_detail,rsvp_event,rsvp_view,CategoryFormView,CategoryListView,CategoryUpdateView,CategoryDeleteView,dashboardMain,about_view,contact_view


urlpatterns = [
    path('main/', main ,name='main'),
    path('about_us/', about_view ,name='about_us'),
    path('contact_us/', contact_view ,name='contact_us'),
    path('dashboard/', dashboard , name = 'dashboard'),
    path('dashboardMain/', dashboardMain , name = 'dashboardMain'),
    # path('category_list/', category_list , name = 'category_list'),
    path('category_list/', CategoryListView.as_view() , name = 'category_list'),
    path('event_list/', event_list , name = 'event_list'),
    path('participant_list/', participant_list , name = 'participant_list'),
    # path('category_form/', category_form ,name = 'category_form'),
    path('category_form/', CategoryFormView.as_view() ,name = 'category_form'),
    path('event_form/', event_form , name = 'event_form'),
    # path('participant_form/', participant_form,name = 'participant_form'),
    
    # path('category_update/<int:id>/', category_update,name = 'category_update'),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(),name = 'category_update'),
    # path('category_delete/<int:id>/', category_delete,name = 'category_delete'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(),name = 'category_delete'),
    path('event_update/<int:id>/', event_update,name = 'event_update'),
    path('event_delete/<int:id>/', event_delete,name = 'event_delete'),
    path('event_detail/<int:id>/', event_detail,name = 'event_detail'),
    # path('participant_update/<int:id>/', participant_update,name = 'participant_update'),
    path('participant_delete/<int:id>/', participant_delete,name = 'participant_delete'),
    path('rsvp-event/<int:event_id>/',rsvp_event, name="rsvp-event"),
    # path('rsvp-list/<int:event_id>/',rsvp_list, name="rsvp_list"),
    path('rsvp-view/<int:event_id>/',rsvp_view, name="rsvp_view"),
    
]
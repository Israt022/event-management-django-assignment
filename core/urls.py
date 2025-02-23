from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path,include
from core.views import home,no_permission
from django.conf.urls.static import static
from django.conf import settings
from core.views import home

urlpatterns = [
    path('',home,name='home'),

]

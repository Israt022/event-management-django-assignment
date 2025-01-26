from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def view_task(request):
    return HttpResponse('This is event management')
from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import CategoryForm,EventForm,ParticipantForm
from tasks.models import Category,Event,Participant
from django.contrib import messages
from django.db.models import Q,Count,Max,Min
from django.utils import timezone
# Create your views here.
def main(request):
    events = Event.objects.all()
    category = Category.objects.all()
    
    search_query = request.GET.get('search')
    if search_query:
        events = events.filter(
            name__icontains = search_query
        ) | events.filter(
            location__icontains = search_query
        )
    
    select_category = request.GET.get('category')
   
    
    if select_category and select_category != 'all':
        events = events.filter(category__id = select_category)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        events = events.filter(date__range = [start_date,end_date])
    context = {
        'events':events,
        'category':category,
        'search_query':search_query
        }
    return render(request,'dashboard/main.html',context)
def dashboard(request):
    total_category = Category.objects.all().count()
    total_event =Event.objects.all().count()
    total_participant = Participant.objects.aggregate(count = Count('id'))['count']
    upcoming_events = Event.objects.filter(date__gte = timezone.now()).count()
    past_events = Event.objects.filter(date__lt = timezone.now()).count()
    
    today = timezone.now().date()
    # today_events = Event.objects.filter(date=today)
    event_filter = request.GET.get('filter','all')
    
    if event_filter == 'upcoming':
        today_events = Event.objects.filter(date__gte = today)
    elif event_filter == 'past':
        today_events = Event.objects.filter(date__lt = today)
    elif event_filter == 'all':
        today_events = Event.objects.all()
    else:
        today_events = Event.objects.filter(date = today)
    context = {
        'total_category':total_category,
        'total_event':total_event,
        'total_participant':total_participant,
        'upcoming_events':upcoming_events,
        'past_events':past_events,
        'today_events':today_events,
        'event_filter':event_filter,
    }
    return render(request,'dashboard/dashboard.html',context)
'''Create catagory Form'''
def category_form(request):
    # form_category = CategoryForm()
    
    if request.method == 'POST':
        form_category = CategoryForm(request.POST)
        if form_category.is_valid():
            form_category.save()
            messages.success(request,'Category Created Successfully')
            return redirect('category_form')
    else:
        form_category = CategoryForm()
        
    context ={
        'form_category' : form_category
    }
    return render(request,'category_form.html',context)
'''Read Category'''
def category_list(request):
    category = Category.objects.all()
    return render(request,'category_list.html',{'category':category})

'''Update Category'''
def category_update(request,id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form_category =  CategoryForm(request.POST,instance = category)
        if form_category.is_valid():
            form_category.save()
            messages.success(request,'Category Updated Successfully')
            return redirect('category_list')
    else:
        form_category = CategoryForm(instance=category)
    return render(request,'category_form.html',{'form_category':form_category})

'''Delete Category'''
def category_delete(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id = id)
        category.delete()
        messages.success(request,'Category Deleted Successfully')
        return redirect('category_list')
    else:
        messages.error(request,'Something went wrong')
        return redirect('category_list')


def event_form(request):
    category = Category.objects.all()
    events = Event.objects.all()
    form_event = EventForm(category = category)
    
    if request.method == 'POST':
        form_event = EventForm(request.POST,category = category)
        if form_event.is_valid():
            form_event.save()
            messages.success(request, 'Event Created Successfully')
            return redirect('event_form')
    else:
        form_event = EventForm(category = category)
    context ={
        'form_event' : form_event,
        'events' : events
    }
    return render(request,'event_form.html',context)
'''Read Event'''
def event_list(request):
    category_f = request.GET.get('category',None)
    start_date = request.GET.get('start_date',None)
    ende_date = request.GET.get('end_date',None)
    
    events = Event.objects.select_related('category').prefetch_related('event')
    
    if category_f:
        events = events.filter(category__id = category_f)
        
    if start_date:
        events = events.filter(date__range = [start_date,ende_date])
    
    total_participant = Participant.objects.count()
    
    context = {
        'events' : events,
        'total_participant' : total_participant,
    }        
    return render(request,'event_list.html',context)
'''Update Event'''
def event_update(request,id):
    event = Event.objects.get(id=id)
    categories = Category.objects.all()
    if request.method == 'POST':
        form_event=  EventForm(request.POST,category = categories,instance = event)
        if form_event.is_valid():
            form_event.save()
            messages.success(request,'Event Updated Successfully')
            return redirect('event_list')
    else:
        form_event = EventForm(category = categories,instance=event)
    return render(request,'event_form.html',{'form_event':form_event})

'''Delete Category'''
def event_delete(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request,'Event Deleted Successfully')
        return redirect('event_list')
    else:
        messages.error(request,'Something went wrong')
        return redirect('event_list')

def event_detail(request,id):
    event = Event.objects.filter(id=id).first()
    if not event:
        return redirect('main')
    context = {
        'event' : event
    }
    return render(request,'event_detail.html',context)

def participant_form(request):
    events = Event.objects.all()
    form_participant = ParticipantForm(events = events)
    
    if request.method == 'POST':
        form_participant = ParticipantForm(request.POST,events = events)
        if form_participant.is_valid():
            form_participant.save()
            messages.success(request,'Participant added Succeccfully!')
            return redirect('participant_form')
    else:
        form_participant = ParticipantForm(events=events)
        
    context = {
        'form_participant' : form_participant
    }
    return render(request,'participant_form.html',context)

'''Read Participant'''
def participant_list(request):
    participant = Participant.objects.all()
    return render(request,'participant_list.html',{'participant':participant})
'''Update Participant'''
def participant_update(request,id):
    participant = Participant.objects.get(id=id)
    events = Event.objects.all()
    if request.method == 'POST':
        form_participant=  ParticipantForm(request.POST,events = events,instance = participant)
        if form_participant.is_valid():
            form_participant.save()
            messages.success(request,'Participant Updated Successfully')
            return redirect('participant_list')
    else:
        form_participant = ParticipantForm(events = events,instance=participant)
    return render(request,'participant_form.html',{'form_participant':form_participant})

'''Delete Participant'''
def participant_delete(request,id):
    if request.method == 'POST':
        participant = Participant.objects.get(id = id)
        participant.delete()
        messages.success(request,'Participant Deleted Successfully')
        return redirect('participant_list')
    else:
        messages.error(request,'Something went wrong')
        return redirect('participant_list')
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from tasks.forms import CategoryForm,EventForm,CustomPasswordResetConfirmForm,CustomPasswordResetForm
from tasks.models import Category,Event
from django.contrib import messages
from django.db.models import Q,Count,Max,Min
from django.utils import timezone
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import send_mail
# from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import UpdateView,DeleteView
# Create your views here.
from django.contrib.auth import get_user_model


User = get_user_model()

def is_admin(user):
    return user.groups.filter(name = 'Admin').exists()
 
def is_organizer(user):
    return user.groups.filter(name = 'Organizer').exists()
def is_user(user):
    return user.groups.filter(name = 'User').exists()
 
def is_admin_or_organizer(user):
    return user.groups.filter(name__in = ['Admin','Organizer']).exists()
def is_admin_or_user(user):
    return user.groups.filter(name__in = ['Admin','User']).exists()
 
@login_required
@user_passes_test(is_admin_or_user,login_url='no-permission')
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

@login_required
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def dashboard(request):
    total_category = Category.objects.all().count()
    total_event =Event.objects.all().count()
    total_participant = User.objects.aggregate(count = Count('id'))['count']
    upcoming_events = Event.objects.filter(date__gte = timezone.now()).count()
    past_events = Event.objects.filter(date__lt = timezone.now()).count()
    
    today = timezone.now().date()
    # today_events = Event.objects.filter(date=today)
    event_filter = request.GET.get('filter','all')
    
    if event_filter == 'upcoming':
        today_events = Event.objects.filter(date__gte = today)
        title = 'Upcoming Events'
    elif event_filter == 'past':
        today_events = Event.objects.filter(date__lt = today)
        title = 'Past Events'
    elif event_filter == 'all':
        today_events = Event.objects.all()
        title = 'Total Events'
    else:
        today_events = Event.objects.filter(date = today)
        title = "Today' Events"
    context = {
        'total_category':total_category,
        'total_event':total_event,
        'total_participant':total_participant,
        'upcoming_events':upcoming_events,
        'past_events':past_events,
        'today_events':today_events,
        'event_filter':event_filter,
        'title':title
    }
    return render(request,'dashboard/dashboard.html',context)
'''Create catagory Form'''
@login_required
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
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

# @method_decorator(login_required, name="dispatch")
class CategoryFormView(LoginRequiredMixin,PermissionRequiredMixin,View):
    form_class = CategoryForm
    template_name = 'category_form.html'
    login_url = 'sign-in'
    permission_required = 'tasks.add_category'
    def get(self,request,*args, **kwargs):
        form_category = self.form_class()
        return render(request, self.template_name, {"form_category": form_category})
    def post(self,request,*args, **kwargs):
        form_category = self.form_class(request.POST)
        if form_category.is_valid():
            form_category.save()
            messages.success(request,'Category Created Successfully')
            return redirect('category_form')
        return render(request, self.template_name, {"form_category": form_category})

'''Read Category'''
@login_required
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def category_list(request):
    category = Category.objects.all()
    return render(request,'category_list.html',{'category':category})

class CategoryListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Category
    template_name = 'category_list.html'
    login_url = 'sign-in'
    permission_required = 'tasks.view_category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_queryset() 
        return context
    

    
'''Update Category'''
@login_required
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
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

class CategoryUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Category
    template_name  = 'category_form.html'
    context_object_name = 'category'
    login_url = 'sign-in'
    permission_required = 'tasks.view_category'
    fields = ['name','description']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_category = self.get_form()
        context["form_category"] = form_category
        return context
        # return render(request,'category_form.html',{'form_category':form_category})
    def post(self,request,*args, **kwargs):
        self.object = self.get_object()
        form_category =  self.get_form()
        if form_category.is_valid():
            form_category.save()
            messages.success(request,'Category Updated Successfully')
            return redirect('category_list')
        return render(request, self.template_name, {"form_category": form_category})

'''Delete Category'''
@login_required
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def category_delete(request,id):
    if request.method == 'POST':
        category = Category.objects.get(id = id)
        category.delete()
        messages.success(request,'Category Deleted Successfully')
        return redirect('category_list')
    else:
        messages.error(request,'Something went wrong')
        return redirect('category_list')

class CategoryDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Category
    login_url = 'sign-in'
    permission_required = 'tasks.delete_category'
    success_url = reverse_lazy("category_list")
    def form_valid(self, form):
    
        messages.success(self.request,'Category Deleted Successfully')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,'Something went wrong')
        return redirect('category_list')

@login_required
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def event_form(request):
    category = Category.objects.all()
    events = Event.objects.all()
    form_event = EventForm(category = category)
    
    if request.method == 'POST':
        form_event = EventForm(request.POST,request.FILES,category = category )
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
@login_required
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def event_list(request):
    category_f = request.GET.get('category',None)
    start_date = request.GET.get('start_date',None)
    ende_date = request.GET.get('end_date',None)
    
    events = Event.objects.select_related('category').prefetch_related('participant')
    
    if category_f:
        events = events.filter(category__id = category_f)
        
    if start_date:
        events = events.filter(date__range = [start_date,ende_date])
    
    total_participant = User.objects.count()
    
    context = {
        'events' : events,
        'total_participant' : total_participant,
    }  
    # print(events,total_participant)      
    return render(request,'event_list.html',context)

'''Update Event'''
@login_required
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
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
@login_required
@user_passes_test(is_admin_or_organizer,login_url='no-permission')
def event_delete(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request,'Event Deleted Successfully')
        return redirect('event_list')
    else:
        messages.error(request,'Something went wrong')
        return redirect('event_list')
@login_required
def event_detail(request,id):
    event = Event.objects.filter(id=id).first()
    if not event:
        return redirect('main')
    context = {
        'event' : event
    }
    return render(request,'event_detail.html',context)

# @user_passes_test(is_admin,login_url='no-permission')
# def participant_form(request):
#     events = Event.objects.all()
#     form_participant = ParticipantForm(events = events)
    
#     if request.method == 'POST':
#         form_participant = ParticipantForm(request.POST,events = events)
#         if form_participant.is_valid():
#             form_participant.save()
#             messages.success(request,'Participant added Succeccfully!')
#             return redirect('participant_form')
#     else:
#         form_participant = ParticipantForm(events=events)
        
#     context = {
#         'form_participant' : form_participant
#     }
#     return render(request,'participant_form.html',context)

'''Read Participant'''
@user_passes_test(is_admin,login_url='no-permission')
def participant_list(request):
    participant = User.objects.all()
    return render(request,'participant_list.html',{'participant':participant})
'''Update Participant'''
# @user_passes_test(is_admin,login_url='no-permission')
# def participant_update(request,id):
#     participant = User.objects.get(id=id)
#     events = Event.objects.all()
#     if request.method == 'POST':
#         form_participant=  ParticipantForm(request.POST,events = events,instance = participant)
#         if form_participant.is_valid():
#             form_participant.save()
#             messages.success(request,'Participant Updated Successfully')
#             return redirect('participant_list')
#     else:
#         form_participant = ParticipantForm(events = events,instance=participant)
#     return render(request,'participant_form.html',{'form_participant':form_participant})

'''Delete Participant'''
@user_passes_test(is_admin,login_url='no-permission')
def participant_delete(request,id):
    if request.method == 'POST':
        participant = User.objects.get(id = id)
        participant.delete()
        messages.success(request,'Participant Deleted Successfully')
        return redirect('participant_list')
    else:
        messages.error(request,'Something went wrong')
        return redirect('participant_list')
    
@login_required
@user_passes_test(is_user, login_url='no-permission')
def rsvp_event(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user not in event.participant.all():
        event.participant.add(request.user)
        return redirect('main')
    return messages.error(request,"Already RSVP'd")


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)
    
@login_required
@user_passes_test(is_admin_or_user, login_url='no-permission')
def rsvp_list(request):
    print('rsvp')
    events = Event.objects.filter(participant=request.user)
    # events = Event.objects.all()
    print("RSVCP Cheack",events)
    return render(request, 'dashboard/rsvp_list.html',{'events':events})
@login_required
@user_passes_test(is_admin_or_user, login_url='no-permission')
def rsvp_view(request,event_id):
    event = get_object_or_404(Event,id=event_id)

    user_rsvp = event.participant.filter(id=request.user.id).first()

    return render(request, 'dashboard/rsvp_view.html', {
        'event': event,
        'user_rsvp': user_rsvp      
    })

@login_required
def dashboardMain(request):
    if is_organizer(request.user):
        return redirect('dashboard')
    elif is_user(request.user):
        return redirect('main')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')
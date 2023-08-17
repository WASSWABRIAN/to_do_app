from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.conf import settings 
from .forms import TaskForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .email_utils import send_custom_email
from django.core.mail import EmailMessage

from .models import Task
import datetime
from django.core.mail import send_mail
# Create your views here.

class CustomLoginView(LoginView):
    template_name= 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

'''class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, *kwargs)'''
        
# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'base/register.html'
    email_template = 'base/account_activation_email.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            email = request.POST.get('email')
            subject = 'Activate Your TODO_LIST Account'
            message = render_to_string(self.email_template, {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)
            

            emailSend2 = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )
            
            emailSend2.send()

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')
        
        return render(request, self.template_name, {'form': form})


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name= 'tasks'
    template_name = 'base/task_list.html'
    queryset = Task.objects.order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        tasks = Task.objects.filter(user=user)
        
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(complete=True).count()
        context['tasks'] = tasks
        context['count'] = total_tasks - completed_tasks
        context['completed_count'] = completed_tasks
     #   context['completed_count'] = tasks.filter(completion_status=100).count()
        context['today'] = timezone.now().date()
        
         # Initialize the progress variable with a default value of 0
        progress = 0
        if total_tasks > 0:
            progress = (completed_tasks / total_tasks) * 100
        #context['progress'] = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        context['progress'] = round(progress, 1)
        
        self.send_warning_emails(tasks)
        return context
   
    def send_warning_emails(self, tasks):
        incomplete_tasks = tasks.filter(complete=False)
        for task in incomplete_tasks:
            if task.deadline and task.deadline_time:
                # Combine date and time to create a timezone-aware datetime
                full_deadline = datetime.datetime.combine(
                    task.deadline,
                    task.deadline_time,
                    tzinfo=timezone.get_current_timezone()
                )
                
                # Calculate the time difference
                time_until_deadline = full_deadline - timezone.now()
                
                # Check if the remaining time is less than or equal to 24 hours
                if time_until_deadline <= datetime.timedelta(days=2):
                    self.send_warning_email(task)
        
    
    def send_warning_email(self, task):
        subject = f'Warning: Deadline approaching for "{task.title}"'
        message = f'Dear {task.user.username},\n\n' \
                  f'This is a reminder that the deadline for your task "{task.title}" is approaching. ' \
                  f'Please complete it before the deadline.\n\n' \
                  f'Best regards,\nYour Brians_ToDo App Team'
        from_email = 'elishahbryans168@gmail.com'  # Update with your email
        print(task.user.email)
        recipient_list = [task.user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
       # send_custom_email(subject, message, recipient_list)
    
    
       # search_input = self.request.GET.get('search-area') or ''
       # if search_input:
       #     context['tasks'] = context['tasks'].filter(title__icontains = search_input)
        #    context['search_input'] = search_input
       # return context
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
   # fields = ['title', 'description', 'complete']
    #fields = '__all__'
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    form_class = TaskForm
    context_object_name = 'task'
    #fields = ['title', 'description', 'complete', 'deadline']
    #fields = '__all__'
    success_url = reverse_lazy('tasks')
    #def form_valid(self, form):
       # task = form.save(commit=False)
       # if task.deadline and task.deadline < timezone.now().date():
         #   task.complete = False
       # return super().form_valid(form)
    
class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account has been confirmed.'))
            return redirect('tasks')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('tasks')
    

    
    
#@csrf_exempt
#def update_task_completion(request, task_id):
   # if request.method == 'POST':
    #    try:
     #       task = Task.objects.get(pk=task_id)
      #      task.complete = request.POST.get('complete') == 'true'
       #     task.save()
        #    return JsonResponse({'status': 'success'})
        #except Task.DoesNotExist:
         #   return JsonResponse({'status': 'error', 'message': 'Task not found'})
    #return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
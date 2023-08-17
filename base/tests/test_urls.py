from django.test import TestCase
from django.urls import reverse, resolve
from base.views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, SignUpView, ActivateAccount
from django.contrib.auth.views import LogoutView

class TestUrls(TestCase):
    
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, CustomLoginView)
    
    def test_list_url_resolves(self):
        url = reverse('tasks')
        self.assertEquals(resolve(url).func.view_class, TaskList)
        
    def test_detail_url_resolves(self):
        url = reverse('task', args=[1])  # Use a valid task ID here
        self.assertEquals(resolve(url).func.view_class, TaskDetail)
        
    def test_create_url_resolves(self):
        url = reverse('task-create')
        self.assertEquals(resolve(url).func.view_class, TaskCreate)
        
    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView) 
        
    def test_update_url_resolves(self):
        url = reverse('task-update', args=[1])  # Use a valid task ID here
        self.assertEquals(resolve(url).func.view_class, TaskUpdate) 
        
    def test_delete_url_resolves(self):
        url = reverse('task-delete', args=[1])  # Use a valid task ID here
        self.assertEquals(resolve(url).func.view_class, DeleteView)   
    
    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignUpView) 
        
    def test_activate_url_resolves(self):
        # Replace 'uidb64' and 'token' with actual values
        url = reverse('activate', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func.view_class, ActivateAccount)
        
        
        
        
        
        
        
        
        
        
'''from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from base.models import Task

class TestEndpoints(TestCase):

    def setUp(self):
        # Set up any necessary data for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(title='Test Task', user=self.user)

    def test_task_list(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/task_list.html')
        # Add more assertions to check the response content, context, etc.

    def test_task_detail(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/task.html')
        # Add more assertions to check the response content, context, etc.

    # Define similar test methods for other endpoints

    def test_signup(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/register.html')
        # Add more assertions to check the response content, context, etc.'''
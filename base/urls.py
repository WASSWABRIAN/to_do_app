from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView #RegisterPage
from django.contrib.auth.views import LogoutView
from .views import SignUpView, ActivateAccount

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('', TaskList.as_view(), name= 'tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name= 'task'),
    path('task-create/', TaskCreate.as_view(), name= 'task-create'),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    #path('register/', RegisterPage.as_view(), name="register"),
    #path('task/<int:pk>/', TaskDetail.as_view(), name= 'task'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name= 'task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name= 'task-delete'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
   # path('update-task/<int:task_id>/', views.update_task_completion, name='update_task_completion'),
]
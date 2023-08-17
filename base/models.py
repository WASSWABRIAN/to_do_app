from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)  # Add the deadline field
    deadline_time = models.TimeField(null=True, blank=True)
    percentage_completion = models.IntegerField(default=0)
    completion_status = models.PositiveIntegerField(default=0)
#def is_overdue(self):
#return self.deadline < timezone.now().date() and self.percentage_completion < 100


#def overall_progress():
 #       total_tasks = Task.objects.count()
  #      completed_tasks = Task.objects.filter(complete=True).count()
   #     return round((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

#def progress_percentage(self):
 ##      completed_steps = 1 if self.complete else 1 if self.deadline and self.deadline >= timezone.now().date() else 0
   #     return round((completed_steps / total_steps) * 100)
def __str__(self):
       return self.title
class Meta:
        ordering = ['complete']

#def progress_percentage(self):
      #  total_steps = 1 if self.complete else 2
       # completed_steps = 1 if self.complete else 1 if self.deadline and self.deadline >= timezone.now().date() else 0
        #return round((completed_steps / total_steps) * 100) 
    
#def __str__(self):
 #      return self.title
  #     class Meta:
   #     ordering = ['complete']
   
   
   
   
   
  # def save(self, *args, **kwargs):
   #     if self.complete:
    #        self.percentage_completion = 100
     #   elif self.deadline and self.deadline >= timezone.now().date():
      #      self.percentage_completion = 50
       # else:
        #    self.percentage_completion = 0
    #super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
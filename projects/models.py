from django.db import models
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True)
    status = models.CharField(choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ],
    default='pending'
    )
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='task')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_task')
    due_date = models.DateField()

    def __str__(self):
        return f"{self.project.title}'s task: {self.title}"
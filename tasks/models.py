from django.db import models
# import the custom user
from django.contrib.auth import get_user_model
from django.utils import timezone
#import timezone



User = get_user_model()



class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(blank=True, null=True)
    priority = models.PositiveIntegerField(default=1)  # 1: Low, 2: Medium, 3: High
    # is_completed: BooleanField to indicate if the task is completed
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # <-- Add this line

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['due_date', 'priority']
    def __str__(self):
        return self.title
    
    # handle any future issues with completed at field
    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed and self.completed_at:
            self.completed_at = None
        super().save(*args, **kwargs)
    

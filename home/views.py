from django.shortcuts import render, get_object_or_404
from tasks.models import Task
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.
def home(request):
    # get total counts for all users
    users_count = User.objects.count()
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100, 0)
    else:
        completion_rate = 0
        
    # personal statistics per each user
    user = User()
    if user.is_authenticated:
        tasks = Task.objects.filter(user=request.user.id)
        user_tasks_total = tasks.count()
        user_completed = tasks.filter(is_completed=True).count()
        user_pending = tasks.filter(is_completed=False).count()
        
        recent_activities = tasks.filter(is_completed=True).order_by('-created_at')[:5]
        
    context = {
        # total counts for all users
        'users_count':users_count,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': completion_rate,
        # personal statistics per each user

        'user_tasks_total': user_tasks_total,
        'user_completed': user_completed,
        'user_pending': user_pending,
        'recent_activities': recent_activities,
        
    }
    return render(request, 'main/main.html', context=context)

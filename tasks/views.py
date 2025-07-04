from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.shortcuts import redirect
from django.contrib import messages
from .models import Task
from django.utils import timezone
from datetime import timedelta


# Create your views here.

@login_required
def dashboard(request):
    # get all teasks
    tasks = Task.objects.filter(user=request.user)
    # get done tasks
    completed_tasks = tasks.filter(is_completed=True)
    pending_tasks = tasks.filter(is_completed=False)
    # completion_rate
    if tasks.count() > 0:
        completion_rate = (completed_tasks.count() / tasks.count()) * 100
        
    # recent_tasks
    recent_tasks = tasks.order_by('-created_at')[:4]
    return render(request, 'tasks/dashboard.html', context={'tasks':tasks, 'completed_tasks': completed_tasks, 'pending_tasks': pending_tasks, 'completion_rate': completion_rate, 'recent_tasks': recent_tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # save the form and asign it to the user
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'تم إنشاء المهمة بنجاح!')
            return redirect('create_task')  # Redirect to the task list or any other page
        else:
            messages.error(request, 'حدث خطأ أثناء إنشاء المهمة. يرجى التحقق من البيانات المدخلة.')
    else:
        form = TaskForm()
        return render(request, 'tasks/create_task.html', context={'form': form})



@login_required
def all_tasks(request):
    # get all tasks
    tasks = Task.objects.filter(user=request.user)

    completed = request.GET.get('completed')
    pending = request.GET.get('pending')

    # Only show tasks if a filter is selected
    if completed and not pending:
        tasks = tasks.filter(is_completed=True)
    elif pending and not completed:
        tasks = tasks.filter(is_completed=False)
    # if user selected both
    elif pending and completed:
        pass
    
    # if didn't pick anything then show nothign
    else:
        tasks = None

    # check if user selected somethig, and proceed with the filtering
    if tasks is not None:
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(is_completed=True)
        completion_rate = (completed_tasks.count() / total_tasks) * 100 if total_tasks > 0 else 0

        now = timezone.now()
        month_ago = now - timedelta(days=30)
        tasks_last_month = tasks.filter(created_at__gte=month_ago)
        completed_last_month = tasks_last_month.filter(is_completed=True).count()
        complete_month_rate = (completed_last_month / tasks_last_month.count()) * 100 if tasks_last_month.count() > 0 else 0

        today = timezone.now().date()
        today_tasks = tasks.filter(due_date=today)
        upcoming_tasks = tasks.filter(due_date__gt=today)
        overdue_tasks = tasks.filter(due_date__lt=today)

        context = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completion_rate,
            'tasks_last_month': tasks_last_month,
            'complete_month_rate': complete_month_rate,
            'completed_last_month': completed_last_month,
            'today_tasks': today_tasks,
            'upcoming_tasks': upcoming_tasks,
            'overdue_tasks': overdue_tasks,
        }
    # if selected nothing, return empty context
    else:
        context = {}

    return render(request, 'tasks/all_tasks.html', context=context)
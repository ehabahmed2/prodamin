from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.shortcuts import redirect
from django.contrib import messages
from .models import Task

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
    return render(request, 'tasks/all_tasks.html', context={})  
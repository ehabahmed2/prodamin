from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.shortcuts import redirect
from django.contrib import messages
from .models import Task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


# Create your views here.

@login_required
def dashboard(request):
    # get all teasks
    tasks = Task.objects.filter(user=request.user)
    # get done tasks
    

    # completion_rate
    if tasks.count() > 0:
        completed_tasks = tasks.filter(is_completed=True)
        pending_tasks = tasks.filter(is_completed=False)
        completion_rate = (completed_tasks.count() / tasks.count()) * 100
        
    # recent_tasks
        recent_tasks = tasks.order_by('-created_at')[:4]
        context={'tasks':tasks, 
                'completed_tasks': completed_tasks, 
                'pending_tasks': pending_tasks, 
                'completion_rate': completion_rate, 
                'recent_tasks': recent_tasks}
    else:
        context = {}
    return render(request, 'tasks/dashboard.html', context=context)

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
            messages.warning(request, 'حدث خطأ أثناء إنشاء المهمة. يرجى التحقق من البيانات المدخلة.')
            return redirect('create_task')
    else:
        form = TaskForm()
        return render(request, 'tasks/create_task.html', context={'form': form})



@login_required
def all_tasks(request):
     # get all tasks
    tasks = Task.objects.filter(user=request.user)
    
    # get the search tasks
    search = request.GET.get('search')
    if search:
        tasks = Task.objects.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )


    if not request.GET:
        completed = pending = high = medium = low = today_filter = upcoming = no_date = late = True
    else:
        completed = request.GET.get('completed')
        pending = request.GET.get('pending')
        late = request.GET.get('late')
        high = request.GET.get('high')
        medium = request.GET.get('medium')
        low = request.GET.get('low')
        today_filter = request.GET.get('today')
        upcoming = request.GET.get('upcoming')
        no_date = request.GET.get('no_date')

    # Only show tasks if a filter is selected
    if completed and not pending:
        tasks = tasks.filter(is_completed=True)
    elif pending and not completed:
        tasks = tasks.filter(is_completed=False)

        
    # Priority filtering (priority: 1=Low, 2=Medium, 3=High)
    priority_filters =[]
    if high:
        priority_filters.append(3) 
    if medium:
        priority_filters.append(2)
    if low:
        priority_filters.append(1)
    
    if priority_filters:
        tasks = tasks.filter(priority__in=priority_filters)
    
    
    # handle due dates filtering
    due_q = Q()
    today = timezone.now().date()
    if today_filter:
        due_q |= Q(due_date=today)
    if upcoming:
        due_q |= Q(due_date__gt=today)
    if no_date:
        due_q |= Q(due_date__isnull=True)
    if late:
        due_q |= Q(due_date__lt=today)
    if today_filter or upcoming or no_date or late:
        tasks = tasks.filter(due_q)
    
        
    # if didn't pick anything then show nothign
    else:
        tasks = None

    # check if user selected somethig, and proceed with the filtering
    if tasks is not None:
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(is_completed=True)
        completion_rate = round((completed_tasks.count() / total_tasks) * 100,2) if total_tasks > 0 else 0

        now = timezone.now()
        month_ago = now - timedelta(days=30)
        tasks_last_month = tasks.filter(created_at__gte=month_ago)
        completed_last_month = tasks_last_month.filter(is_completed=True).count()
        complete_month_rate = round((completed_last_month / tasks_last_month.count()) * 100, 2) if tasks_last_month.count() > 0 else 0

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


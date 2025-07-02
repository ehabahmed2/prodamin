from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, ProfileUpdate
from django.contrib.auth import authenticate, login, logout
# import messages 
from django.contrib import messages
# import the login required decorator
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        # handle user login logic
        form = LoginForm(request.POST)
        if form.is_valid():
            # authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'تم تسجيل الدخول بنجاح!')
                return redirect('main')  # Redirect to the main page or dashboard
                # Redirect to a success page or dashboard
            else:
                # Return an 'invalid login' error message
                form.add_error(None, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    else:
        form = LoginForm()
    return render(request, 'users/login_form.html', context={'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


def register_view(request):
    if request.method == 'POST':
        # check if form is valid
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            # save the user data
            user = form.save()
            messages.success(request, 'تم تسجيل حسابك بنجاح!')
            # Optionally, you can log the user in after registration
            login(request, user)
            return redirect('main')  # Redirect to a success page or dashboard
        else:
            messages.error(request, 'حدث خطأ أثناء تسجيل الحساب. يرجى التحقق من البيانات المدخلة.')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})



@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdate(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'users/profile.html', {'form': form, 'success': True})
    else:
        form = ProfileUpdate(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
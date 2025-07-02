from django import forms
# import user creation form
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

# create the log in form
class LoginForm(forms.Form):
    username = forms.CharField(
        label='اسم المستخدم',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'أدخل اسم المستخدم', 'id': 'username', 'name': 'username'})
    )
    password = forms.CharField(
        label='كلمة المرور',
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'أدخل كلمة المرور', 'id': 'password', 'name': 'password'})
    )
    # add remember me checkbox
    remember_me = forms.BooleanField(
        label='تذكرني',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'rememberMe', 'name': 'remember_me'})
    )
    

# create the user registration form
class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='كلمة المرور',
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'أدخل كلمة المرور', 'id': 'password1', 'name': 'password1'})
    )
    password2 = forms.CharField(
        label='تأكيد كلمة المرور',
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'أعد إدخال كلمة المرور', 'id': 'password2', 'name': 'password2'})
    )
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل الاسم الأول', 'id': 'first_name', 'name': 'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل الاسم الأخير', 'id': 'last_name', 'name': 'last_name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم المستخدم', 'id': 'username', 'name': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com', 'id': 'email', 'name': 'email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'أدخل كلمة المرور', 'id': 'password1', 'name': 'password1'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'أعد إدخال كلمة المرور', 'id': 'password2', 'name': 'password2'}),
        }
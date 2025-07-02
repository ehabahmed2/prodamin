from django import forms
from tasks.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'is_completed']
        
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': "id_title",
                'name': 'title',
                'placeholder': 'ماذا تريد أن تنجز اليوم؟'
            }),
            'due_date': forms.DateInput(attrs={'type': 'date',
                                               'class': 'form-control',
                                               'id': "id_due_date",
                                               'name': 'due_date',
                                               'placeholder': 'اختر تاريخ الانتهاء',}),
            
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'id': "id_description", 
                'name': 'description',
                'rows': 4,
                'placeholder': 'صف مهمتك بالتفصيل...'
            }),
            'priority': forms.Select(choices=[
                (1, 'منخفض'),
                (2, 'متوسط'),
                (3, 'مرتفع'),
                
            ], attrs={'class': 'form-select',
                      'id': "id_priority",
                      'name': 'priority',
                      'placeholder': 'اختر أولوية المهمة',
                      }),
            'is_completed':forms.CheckboxInput(attrs={
                    'class': 'form-check-input',
                    'id': "id_is_completed",
                    'name': 'is_completed',
                    'role': 'switch',
                    'type': 'checkbox'
                })
        }
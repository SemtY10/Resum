from django import forms
from .models import Resume, PersonalInfo, Education, Experience, Skill, ResumeTemplate

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наприклад: Резюме Python розробника'
            })
        }
        labels = {
            'title': 'Назва резюме'
        }
        
class ResumeFormWithTemplate(forms.ModelForm):
    template = forms.ModelChoiceField(
        queryset=ResumeTemplate.objects.filter(is_active=True),
        required=False,
        empty_label="Без шаблону (стандартний)",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Шаблон резюме"
    )

    class Meta:
        model = Resume
        fields = ['title', 'template']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наприклад: Резюме Python розробника'
            })
        }

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['full_name', 'job_title', 'email', 'phone', 'address', 'summary', 'photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': "Повне ім'я",
            'job_title': "Посада",
            'email': "Електронна пошта",
            'phone': "Телефон",
            'address': "Адреса",
            'summary': "Про себе",
            'photo': "Фотографія",
        }
        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'degree_type', 'field_of_study', 
                 'start_date', 'end_date', 'currently_studying', 'description']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'degree_type': forms.Select(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'start_date', 'end_date', 
                 'currently_working', 'description']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }
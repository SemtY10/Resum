from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resume
from .forms import ResumeForm

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/dashboard.html', {'resumes': resumes})

@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('dashboard')
    else:
        form = ResumeForm()
    
    return render(request, 'resumes/create_resume.html', {'form': form})

def home(request):
    return render(request, 'resumes/home.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume, PersonalInfo, Education, Experience, Skill
from .forms import ResumeForm, PersonalInfoForm, EducationForm, ExperienceForm, SkillForm

def home(request):
    return render(request, 'resumes/home.html')

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

@login_required
def edit_personal_info(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    try:
        personal_info = PersonalInfo.objects.get(resume=resume)
    except PersonalInfo.DoesNotExist:
        personal_info = None
    
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, instance=personal_info)
        if form.is_valid():
            personal_info = form.save(commit=False)
            personal_info.resume = resume
            personal_info.save()
            return redirect('dashboard')
    else:
        form = PersonalInfoForm(instance=personal_info)
    
    return render(request, 'resumes/edit_personal_info.html', {
        'form': form,
        'resume': resume
    })
    
@login_required
def add_education(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume
            education.save()
            return redirect('dashboard')
    else:
        form = EducationForm()
    
    return render(request, 'resumes/add_education.html', {
        'form': form,
        'resume': resume
    })

@login_required
def add_experience(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.resume = resume
            experience.save()
            return redirect('dashboard')
    else:
        form = ExperienceForm()
    
    return render(request, 'resumes/add_experience.html', {
        'form': form,
        'resume': resume
    })

@login_required
def add_skill(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            return redirect('dashboard')
    else:
        form = SkillForm()
    
    return render(request, 'resumes/add_skill.html', {
        'form': form,
        'resume': resume
    })
    
@login_required
def view_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    personal_info = getattr(resume, 'personal_info', None)
    education = resume.education.all()
    experiences = resume.experiences.all()
    skills = resume.skills.all()
    
    return render(request, 'resumes/view_resume.html', {
        'resume': resume,
        'personal_info': personal_info,
        'education': education,
        'experiences': experiences,
        'skills': skills
    })
    
@login_required
def edit_education(request, education_id):
    education = get_object_or_404(Education, id=education_id, resume__user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EducationForm(instance=education)
    
    return render(request, 'resumes/edit_education.html', {'form': form, 'education': education})

@login_required
def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id, resume__user=request.user)
    
    if request.method == 'POST':
        education.delete()
        return redirect('dashboard')
    
    return render(request, 'resumes/delete_education.html', {'education': education})

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    
    search_query = request.GET.get('search', '')
    if search_query:
        resumes = resumes.filter(title__icontains=search_query)
    
    return render(request, 'resumes/dashboard.html', {
        'resumes': resumes,
        'search_query': search_query
    })
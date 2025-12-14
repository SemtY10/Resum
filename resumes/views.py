from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
from django.conf import settings
from .models import Resume, PersonalInfo, Education, Experience, Skill, ResumeTemplate
from .forms import ResumeForm, PersonalInfoForm, EducationForm, ExperienceForm, SkillForm, ResumeFormWithTemplate

@login_required
def export_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    personal_info = getattr(resume, 'personal_info', None)
    
    if not personal_info:
        messages.error(request, 'Спочатку заповніть персональну інформацію!')
        return redirect('edit_personal_info', resume_id=resume.id)
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    y = 800  # Початок зверху
    
    # Заголовок - англійською
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, y, "RESUME")
    y -= 40
    
    # Контактна інформація
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "CONTACT INFORMATION")
    y -= 20
    
    p.setFont("Helvetica", 10)
    p.drawString(100, y, f"Name: {personal_info.full_name}")
    y -= 15
    p.drawString(100, y, f"Position: {personal_info.job_title}")
    y -= 15
    p.drawString(100, y, f"Email: {personal_info.email}")
    y -= 15
    p.drawString(100, y, f"Phone: {personal_info.phone}")
    y -= 15
    p.drawString(100, y, f"Address: {personal_info.address}")
    y -= 30
    
    # Про себе
    if personal_info.summary:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "SUMMARY")
        y -= 20
        
        p.setFont("Helvetica", 10)
        # Обрізаємо довгий текст
        summary_short = personal_info.summary[:150] + "..." if len(personal_info.summary) > 150 else personal_info.summary
        p.drawString(100, y, summary_short)
        y -= 30
    
    # Освіта
    education = resume.education.all()
    if education:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "EDUCATION")
        y -= 20
        
        p.setFont("Helvetica", 10)
        for edu in education:
            p.drawString(100, y, f"• {edu.institution}")
            y -= 12
            p.drawString(120, y, f"{edu.degree} in {edu.field_of_study}")
            y -= 12
            period = f"{edu.start_date.year} - {edu.end_date.year if edu.end_date else 'Present'}"
            p.drawString(120, y, period)
            y -= 20
            
            # Перевірка чи вистачає місця на сторінці
            if y < 100:
                p.showPage()
                y = 800
                p.setFont("Helvetica", 10)
    
    # Досвід роботи
    experiences = resume.experiences.all()
    if experiences:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "WORK EXPERIENCE")
        y -= 20
        
        p.setFont("Helvetica", 10)
        for exp in experiences:
            p.drawString(100, y, f"• {exp.company}")
            y -= 12
            p.drawString(120, y, f"Position: {exp.position}")
            y -= 12
            period = f"{exp.start_date.year} - {exp.end_date.year if exp.end_date else 'Present'}"
            p.drawString(120, y, period)
            y -= 20
            
            if y < 100:
                p.showPage()
                y = 800
                p.setFont("Helvetica", 10)
    
    # Навички
    skills = resume.skills.all()
    if skills:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "SKILLS")
        y -= 20
        
        p.setFont("Helvetica", 10)
        skills_list = []
        for skill in skills:
            skills_list.append(f"{skill.name} ({skill.level})")
        
        skills_text = ", ".join(skills_list)
        p.drawString(100, y, skills_text)
    
    p.save()
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'
    return response

def home(request):
    return render(request, 'resumes/home.html')

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/dashboard.html', {'resumes': resumes})

@login_required
def create_resume(request):
    template_id = request.GET.get('template')
    initial_data = {}
    
    if template_id:
        try:
            template = ResumeTemplate.objects.get(id=template_id, is_active=True)
            initial_data['template'] = template
        except ResumeTemplate.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = ResumeFormWithTemplate(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, f'Резюме "{resume.title}" створено!')
            return redirect('edit_personal_info', resume_id=resume.id)
    else:
        form = ResumeFormWithTemplate(initial=initial_data)
    
    return render(request, 'resumes/create_resume.html', {'form': form})
@login_required
def edit_personal_info(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    try:
        personal_info = PersonalInfo.objects.get(resume=resume)
    except PersonalInfo.DoesNotExist:
        personal_info = None
    
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=personal_info)
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
def edit_education(request, education_id):
    education = get_object_or_404(Education, id=education_id, resume__user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, 'Освіту оновлено!')
            return redirect('dashboard')
    else:
        form = EducationForm(instance=education)
    
    return render(request, 'resumes/edit_education.html', {
        'form': form,
        'education': education
    })

@login_required
def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id, resume__user=request.user)
    
    if request.method == 'POST':
        education.delete()
        messages.success(request, 'Освіту видалено!')
        return redirect('dashboard')
    
    return render(request, 'resumes/delete_education.html', {'education': education})

@login_required
def edit_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id, resume__user=request.user)
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, 'Досвід роботи оновлено!')
            return redirect('dashboard')
    else:
        form = ExperienceForm(instance=experience)
    
    return render(request, 'resumes/edit_experience.html', {
        'form': form,
        'experience': experience
    })

@login_required
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id, resume__user=request.user)
    
    if request.method == 'POST':
        experience.delete()
        messages.success(request, 'Досвід роботи видалено!')
        return redirect('dashboard')
    
    return render(request, 'resumes/delete_experience.html', {'experience': experience})

@login_required
def edit_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, resume__user=request.user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Навичку оновлено!')
            return redirect('dashboard')
    else:
        form = SkillForm(instance=skill)
    
    return render(request, 'resumes/edit_skill.html', {
        'form': form,
        'skill': skill
    })

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, resume__user=request.user)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Навичку видалено!')
        return redirect('dashboard')
    
    return render(request, 'resumes/delete_skill.html', {'skill': skill})

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
    
def template_catalog(request):
    templates = ResumeTemplate.objects.filter(is_active=True)
    return render(request, 'resumes/template_catalog.html', {'templates': templates})

def template_preview(request, template_id):
    template = get_object_or_404(ResumeTemplate, id=template_id, is_active=True)
    return render(request, 'resumes/template_preview.html', {'template': template})

def home(request):
    try:
        from news.models import News
        latest_news = News.objects.filter(is_active=True).order_by('-created_at')[:2]
    except:
        latest_news = []
    
    return render(request, 'resumes/home.html', {'latest_news': latest_news})

@login_required
def clone_resume(request, resume_id):
    original = get_object_or_404(Resume, id=resume_id, user=request.user)
    cloned = Resume.objects.create(
        user=request.user,
        title=f"Копія {original.title}",
        template=original.template
    )
    return redirect('edit_personal_info', resume_id=cloned.id)

@login_required
def clone_resume(request, resume_id):
    original = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Створюємо копію резюме
    cloned_resume = Resume.objects.create(
        user=request.user,
        title=f"Копія {original.title}",
        template=original.template
    )
    
    # Копіюємо персональну інформацію (якщо є)
    try:
        original_personal = PersonalInfo.objects.get(resume=original)
        PersonalInfo.objects.create(
            resume=cloned_resume,
            full_name=original_personal.full_name,
            job_title=original_personal.job_title,
            email=original_personal.email,
            phone=original_personal.phone,
            address=original_personal.address,
            summary=original_personal.summary,
            photo=original_personal.photo  # Копіюємо фото
        )
    except PersonalInfo.DoesNotExist:
        pass
    
    # Копіюємо освіту
    for edu in original.education.all():
        Education.objects.create(
            resume=cloned_resume,
            institution=edu.institution,
            degree=edu.degree,
            degree_type=edu.degree_type,
            field_of_study=edu.field_of_study,
            start_date=edu.start_date,
            end_date=edu.end_date,
            currently_studying=edu.currently_studying,
            description=edu.description
        )
    
    # Копіюємо досвід роботи
    for exp in original.experiences.all():
        Experience.objects.create(
            resume=cloned_resume,
            company=exp.company,
            position=exp.position,
            start_date=exp.start_date,
            end_date=exp.end_date,
            currently_working=exp.currently_working,
            description=exp.description
        )
    
    # Копіюємо навички
    for skill in original.skills.all():
        Skill.objects.create(
            resume=cloned_resume,
            name=skill.name,
            level=skill.level,
            category=skill.category
        )
    
    messages.success(request, f'Резюме "{original.title}" успішно клоновано!')
    return redirect('dashboard')

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        title = resume.title
        resume.delete()
        messages.success(request, f'Резюме "{title}" видалено!')
        return redirect('dashboard')
    
    return render(request, 'resumes/delete_resume.html', {'resume': resume})
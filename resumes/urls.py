from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_resume, name='create_resume'),
    path('resume/<int:resume_id>/personal-info/', views.edit_personal_info, name='edit_personal_info'),
    path('resume/<int:resume_id>/education/', views.add_education, name='add_education'),
    path('resume/<int:resume_id>/experience/', views.add_experience, name='add_experience'),
    path('resume/<int:resume_id>/skill/', views.add_skill, name='add_skill'),
    path('resume/<int:resume_id>/view/', views.view_resume, name='view_resume'),
    path('education/<int:education_id>/edit/', views.edit_education, name='edit_education'),
    path('education/<int:education_id>/delete/', views.delete_education, name='delete_education'),
    path('templates/', views.template_catalog, name='template_catalog'),
    path('templates/<int:template_id>/preview/', views.template_preview, name='template_preview'),
    path('resume/<int:resume_id>/pdf/', views.export_pdf, name='export_pdf'),
    path('education/<int:education_id>/edit/', views.edit_education, name='edit_education'),
    path('education/<int:education_id>/delete/', views.delete_education, name='delete_education'),
    path('experience/<int:experience_id>/edit/', views.edit_experience, name='edit_experience'),
    path('experience/<int:experience_id>/delete/', views.delete_experience, name='delete_experience'),
    path('skill/<int:skill_id>/edit/', views.edit_skill, name='edit_skill'),
    path('skill/<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),
]
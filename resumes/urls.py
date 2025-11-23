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
]
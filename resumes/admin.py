from django.contrib import admin
from .models import Resume, PersonalInfo, Education, Experience, Skill, ResumeTemplate

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active', 'is_premium', 'price']
    list_filter = ['template_type', 'is_active', 'is_premium']
    search_fields = ['name', 'description']

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'user__username']
    date_hierarchy = 'created_at'

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job_title', 'email', 'phone']
    search_fields = ['full_name', 'email', 'job_title']
    list_filter = ['job_title']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'degree', 'degree_type', 'start_date']
    list_filter = ['degree_type', 'start_date']
    search_fields = ['institution', 'degree', 'field_of_study']
    date_hierarchy = 'start_date'

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'position', 'start_date', 'currently_working']
    list_filter = ['currently_working', 'start_date']
    search_fields = ['company', 'position']
    date_hierarchy = 'start_date'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'category', 'resume']
    list_filter = ['level', 'category']
    search_fields = ['name', 'category']
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResumeTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('modern', 'Сучасний'),
        ('classic', 'Класичний'), 
        ('creative', 'Креативний'),
        ('minimal', 'Мінімалістичний'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Назва шаблону")
    description = models.TextField(verbose_name="Опис")
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES, default='modern', verbose_name="Тип шаблону")
    preview_image = models.ImageField(upload_to='template_previews/', blank=True, null=True, verbose_name="Зображення перегляду")
    html_template = models.TextField(verbose_name="HTML шаблон")
    css_styles = models.TextField(verbose_name="CSS стилі")
    is_active = models.BooleanField(default=True, verbose_name="Активний")
    is_premium = models.BooleanField(default=False, verbose_name="Преміум")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Ціна")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Шаблон резюме"
        verbose_name_plural = "Шаблони резюме"

    def __str__(self):
        return self.name

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    title = models.CharField(max_length=200, verbose_name="Назва резюме")
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Шаблон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Резюме"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
class PersonalInfo(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='personal_info', verbose_name="Резюме")
    full_name = models.CharField(max_length=100, verbose_name="Повне ім'я")
    job_title = models.CharField(max_length=100, verbose_name="Посада")
    email = models.EmailField(verbose_name="Електронна адреса")
    phone = models.CharField(max_length = 20,  verbose_name="Номер телефону")
    address = models.TextField(verbose_name="Адреса")
    summary = models.TextField(verbose_name="Про себе")

    def __str__(self):
            return self.full_name
    
class Education(models.Model):
    DEGREE_TYPES = [
        ('high_school', 'Середня школа'),
        ('bachelor', 'Бакалавр'),
        ('master', 'Магістр'),
        ('phd', 'Доктор наук'),
        ('certificate', 'Сертифікат'),
        ('other', 'Інше'),
    ]
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='education',
        verbose_name="Резюме"
    )
    institution = models.CharField(
        max_length=200,
        verbose_name="Навчальний заклад"
    )
    degree = models.CharField(
        max_length=100,
        verbose_name="Ступінь"
    )
    degree_type = models.CharField(
        max_length=20,
        choices=DEGREE_TYPES,
        default='bachelor',
        verbose_name="Тип ступеня"
    )
    field_of_study = models.CharField(
        max_length=100,
        verbose_name="Спеціальність"
    )
    start_date = models.DateField(
        verbose_name="Дата початку"
    )
    end_date = models.DateField(
        null=True,        
        blank=True,      
        verbose_name="Дата закінчення"
    )
    currently_studying = models.BooleanField(
        default=False,
        verbose_name="Навчаюсь зараз"
    )
    
    description = models.TextField(
        blank=True,   
        verbose_name="Опис"
    )

    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
class Experience(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='experiences',
        verbose_name="Резюме"
    )
    
    company = models.CharField(
        max_length=100,
        verbose_name="Компанія"
    )
    
    position = models.CharField(
        max_length=100,
        verbose_name="Посада"
    )
    
    start_date = models.DateField(
        verbose_name="Дата початку"
    )
    
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата закінчення"
    )
    
    currently_working = models.BooleanField(
        default=False,
        verbose_name="Працюю зараз"
    )
    
    description = models.TextField(
        verbose_name="Опис обов'язків"
    )
   
    def __str__(self):
        return f"{self.position} в {self.company}"

class Skill(models.Model):
    SKILL_LEVELS = [
        ('beginner', 'Початківець'),
        ('intermediate', 'Середній'),
        ('advanced', 'Просунутий'),
        ('expert', 'Експерт'),
    ]
    
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name="Резюме"
    )
    
    name = models.CharField(
        max_length=50,
        verbose_name="Назва навички"
    )
    
    level = models.CharField(
        max_length=20,
        choices=SKILL_LEVELS,
        verbose_name="Рівень"
    )
    
    category = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Категорія"
    )
    
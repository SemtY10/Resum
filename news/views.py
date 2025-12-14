from django.shortcuts import render
from .models import News

def news_list(request):
    news = News.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'news/news_list.html', {'news': news})
from django.shortcuts import render
from django.http.response import JsonResponse
from .util.chart import get_content_chart
from .util.synthesis_content_title import get_synthesized_content_title
from .models import Book

# Create your views here.

def index(request):
    return render(request, 'index.html')

def books(request):
    if request.method == 'GET':
        books = list(Book.objects.all().values())
        return JsonResponse({'books': books})

def synthesized_content_title(request):
    if request.method == 'POST':
        content, title = get_synthesized_content_title(request.data['urls'], request.data['titles'])
        data = {
            'content': content,
            'title': title
        }
        return JsonResponse(data)

def content_chart(request):
    if request.method == 'POST':
        content, chart = get_content_chart(request.data['url'])
        data = {
            'content': content,
            'chart': chart
        }
        return JsonResponse(data)
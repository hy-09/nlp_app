from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from .util.chart import get_content_chart
from .util.synthesis_content_title import get_synthesized_content_title
from .models import Book

# Create your views here.

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def books(request):
    books = list(Book.objects.all().values())
    return JsonResponse({'books': books})


@api_view(['POST'])
def synthesized_content_title(request):
    content, title = get_synthesized_content_title(request.data['books'])
    data = {
        'content': content,
        'title': title
    }
    return JsonResponse(data)

@api_view(['POST'])
def content_chart(request):
    content, chart = get_content_chart(request.data['id'], request.data['url'])
    data = {
        'content': content,
        'chart': chart
    }
    return JsonResponse(data)
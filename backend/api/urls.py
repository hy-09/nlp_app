from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/books/', views.books),
    path('api/synthesize_content_title/', views.synthesized_content_title),
    path('api/content_chart/', views.content_chart),
]
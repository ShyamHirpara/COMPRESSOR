from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_temp_image_view, name='upload_temp'),
    path('compress/', views.compress_view, name='compress_image'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('contact/', views.contact_view, name='contact'),
    path('projects/', views.all_projects_view, name='all_projects'),
    path('projects/<slug:slug>/', views.project_detail_view, name='project_detail'),
    path('about/', views.about_view, name='about'),
]
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.dashboard_login, name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),
    path('', views.dashboard_home, name='dashboard_home'),
    
    # Projects CRUD 
    path('projects/', views.dashboard_projects, name='dashboard_projects'),
    path('projects/add/', views.dashboard_project_add, name='dashboard_project_add'),
    path('projects/edit/<int:project_id>/', views.dashboard_project_edit, name='dashboard_project_edit'),
    path('projects/delete/<int:project_id>/', views.dashboard_project_delete, name='dashboard_project_delete'),
    path('projects/image/delete/<int:image_id>/', views.dashboard_project_image_delete, name='dashboard_project_image_delete'),
    
    # Site Settings
    path('settings/', views.dashboard_settings, name='dashboard_settings'),
    
    # cv upload
    path('cv/', views.dashboard_cv_upload, name='dashboard_cv_upload'),
    
    # About Me
    path('settings/about/', views.dashboard_about_edit, name='dashboard_about_edit'),
    
    # edit goals
    path('settings/goals/', views.dashboard_goals_edit, name='dashboard_goals_edit'),
    
    # edit theme settings
    path('settings/theme/', views.dashboard_theme_settings, name='dashboard_theme_settings'),
    

]
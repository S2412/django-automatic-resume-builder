from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views  # Import views


urlpatterns = [
    path('', views.home, name='home'),  # ✅ Define homepage route
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),  # Include core app's URLs

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Employee & Resume Routes
    path('search/', views.search_employee, name='search_employee'),
    path('download-resume/', views.download_resume, name='download_resume'),

    # Logout Confirmation
    path('logout-confirm/', views.logout_confirm, name='logout_confirm'),



    # Employee URLs
    path('employees/', views.manage_employees, name='manage_employees'),
    path('employees/add/', views.add_employee, name='add_employee'),

    path('employees/edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:pk>/', views.delete_employee, name='delete_employee'),


    

   


   path('technical-skills/', views.manage_technical_skills, name='manage_technical_skills'),
   path('technical-skills/add/<int:employee_id>/', views.add_technical_skill, name='add_technical_skill'),
   path('technical-skills/edit/<int:pk>/', views.edit_technical_skill, name='edit_technical_skill'),
   path('technical-skills/delete/<int:pk>/', views.delete_technical_skill, name='delete_technical_skill'),


    path('projects/', views.manage_projects, name='manage_projects'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('projects/delete/<int:pk>/', views.delete_project, name='delete_project'),


    path('mappings/', views.manage_mappings, name='manage_mappings'),
    path('mappings/add/', views.add_mapping, name='add_mapping'),
    path('mappings/edit/<int:pk>/', views.edit_mapping, name='edit_mapping'),
    path('mappings/delete/<int:pk>/', views.delete_mapping, name='delete_mapping'),


    path('forgot-password/', views.forgot_password_request, name='forgot_password_request'),
    path('reset-password/', views.reset_password_form, name='reset_password_form'),


    path('settings/', views.user_settings, name='user_settings'),
    path('settings/change-password/', views.change_password, name='change_password'),
    path('settings/delete-account/', views.delete_account, name='delete_account'),
   




]
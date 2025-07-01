from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
   


    path('signup/', views.sign, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),  # Optional: home page after login







    path('employees/', views.manage_employees, name='manage_employees'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('autocomplete/', views.employee_autocomplete, name='employee_autocomplete'),


   
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



       path('resume/edit/', views.edit_resume, name='edit_resume'),
    path('resume/preview/', views.resume_preview, name='resume_preview'),
    path('resume/download/', views.download_resume_pdf, name='download_resume_pdf'),
    # Optional: manage project assignments
   


    path('create-resume/', views.create_resume, name='create_resume'),
    path('generate-resume/', views.generate_resume, name='generate_resume'),  # This view handles the PDF generation
    path('download-resume/', views.download_resume, name='download_resume'),
    path('resumes/download/<int:employee_id>/', views.download_resume, name='download_resume'),
    
    

    
    path('forgot-password/', views.forgot_password_request, name='forgot_password_request'),
    path('reset-password/', views.reset_password_form, name='reset_password_form'),

    path('search/', views.search_employee, name='search_employee'),              # renders search page
    path('api/search_employees/', views.search_employee_api, name='search_api'),  # JSON API for search
    # Include Django's authentication URLs within core
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', views. dashboard_view, name='dashboard_overview'),



   path('settings/', views.user_settings, name='user_settings'),
    path('settings/change-password/', views.change_password, name='change_password'),
    path('settings/delete-account/', views.delete_account, name='delete_account'),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
   

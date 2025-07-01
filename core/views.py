from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Employee
from django.contrib.auth.decorators import login_required, permission_required
import logging
from django.http import JsonResponse
from io import BytesIO
import os
from django.conf import settings
from django.templatetags.static import static
from django.template.loader import render_to_string 
from django.contrib import messages
from django.db import IntegrityError













def home(request):
    return render(request,'core/home.html')



@login_required
def search_employee(request):
    return render(request, 'core/search.html')



@login_required
def search_employee_api(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        employees = Employee.objects.filter(full_name__icontains=query)[:10]
        results = [
            {'id': emp.id, 'full_name': emp.full_name, 'employee_id': emp.employee_id}
            for emp in employees
        ]
    return JsonResponse(results, safe=False)




def download_resume(request):
    template_path = 'core/resume_template.html'

    query = request.GET.get('query', '').strip()
    if not query:
        return HttpResponse("Query is empty", status=400)

    try:
        # Retrieve employee object based on the query
        if query.isdigit():
            employee = get_object_or_404(Employee, employee_id=query)
        else:
            employee = get_object_or_404(Employee, full_name__icontains=query)

        # Debugging: Check if employee is retrieved
        print("Employee Name:", employee.full_name)

        # ✅ Convert Logo Image to Base64 (Fix)
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'images/img.png')
        logo_uri = None

        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

            logo_uri = f"data:images/png;base64,{encoded_string}"
        else:
            print("⚠️ Warning: Logo file not found!")  # Debugging
            logo_uri = None  # Handle missing image gracefully

        # Prepare context
        context = {
            'title': 'Full Stack Developer',
            'logo_uri': logo_uri,  # Embedded Base64 image (Ensures visibility)
            'employee': employee,
            
        }

        # Load template
        template = get_template(template_path)
        html_content = template.render(context)

        # Generate PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{employee.full_name}_Resume.pdf"'

        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)

        return response

    except Employee.DoesNotExist:
        return HttpResponse("Employee not found", status=404)

def create_resume(request):
    employees = Employee.objects.all()

    for emp in employees:
     print(f"Employee: {emp.full_name}, Skills: {emp.technical_skill.all()}")  # Check if skills exist

    return render(request, 'resume_template.html', {'employees': employees})


import os
import base64
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

 # Make sure pdfkit is installed and wkhtmltopdf is configured

def generate_resume(request):
    if request.method == 'POST':
        emp_id = request.POST.get('employee_id')
        employee = get_object_or_404(Employee, id=emp_id)

        # Fetch related projects (adjust based on your models)
        projects = employee.project_set.all()

        # Embed logo image as base64
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'img.png')
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            logo_uri = f"data:image/png;base64,{encoded_string}"
        else:
            logo_uri = None  # Handle missing image gracefully

        context = {
            'employee': employee,
            'projects': projects,
            'logo_uri': logo_uri,
        }

        # Render HTML with embedded base64 image
        html_content = render_to_string('resume_template.xhtml', context)

        pdf_options = {
            'disable-smart-shrinking': '',
            'no-outline': '',
            'page-size': 'A4',
            'encoding': 'UTF-8',
        }

        # Generate PDF from HTML string
        pdf_file = pdfkit.from_string(html_content, False, options=pdf_options)

        # Return PDF response with attachment header
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{employee.full_name}_Resume.pdf"'

        return response

    return HttpResponse("Invalid request", status=400)




from django.contrib.auth import logout
from django.shortcuts import render, redirect

def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'core/logout_confirm.html')



from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegisterForm  # Your custom user registration form

def sign(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login the newly registered user
            messages.success(request, f'Welcome {user.username}, your account was created successfully!')
            return redirect('home')  # Redirect to a home/dashboard page after login
    else:
        form = UserRegisterForm()

    return render(request, 'core/signup.html', {'form': form})


import logging
logger = logging.getLogger(__name__)





from .forms import ProfileForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'settings/edit_profile.html', {'form': form})



from .models import Employee
from .forms import EmployeeForm
from django.core.paginator import Paginator

from django.http import JsonResponse

def employee_autocomplete(request):
    query = request.GET.get('term', '')
    results = Employee.objects.filter(full_name__icontains=query)[:10]
    suggestions = [emp.full_name for emp in results]
    return JsonResponse(suggestions, safe=False)

def manage_employees(request):
    query = request.GET.get('q')
    employees = Employee.objects.order_by('id')  # or another field like 'name'
    paginator = Paginator(employees, 10)

    page_obj = paginator.get_page(request.GET.get('page'))
    form = EmployeeForm()
    return render(request, 'core/manage_employees.html', {
        'page_obj': page_obj,
        'form': form,
        'query': query,
    })


# Make sure this is imported
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from django.db import IntegrityError
@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('manage_employees')  # Redirect to employee management page
            except IntegrityError:
                form.add_error(None, "An employee with this ID already exists.")  # Handle duplicate entry
        else:
            print(form.errors)  # Debugging: Show errors
    else:
        form = EmployeeForm()

    return render(request, 'core/employee_form.html', {'form': form, 'action': 'Add'})







def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('manage_employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'core/employee_form.html', {'form': form, 'action': 'Edit'})

def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('manage_employees')
    return render(request, 'core/confirm_delete.html', {'employee': employee})




from .models import Employee, Project, ResumeDownload
@login_required
def dashboard_view(request):
    employee_count = Employee.objects.count()
    project_count = Project.objects.count()
    recent_resumes = ResumeDownload.objects.select_related('employee').order_by('-timestamp')[:5]

    return render(request, 'core/dashboard_overview.html', {
        'employee_count': employee_count,
        'project_count': project_count,
        'recent_resumes': recent_resumes,
    })

  
from django.core.paginator import Paginator
from .models import Project
from .forms import ProjectForm

def manage_projects(request):
    query = request.GET.get('q', '')
    projects = Project.objects.filter(title__icontains=query).order_by('-id')

    paginator = Paginator(projects, 5)  # 5 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = ProjectForm()
    context = {
        'page_obj': page_obj,
        'query': query,
        'form': form,
    }
    return render(request, 'core/manage_projects.html', context)


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('manage_projects')


def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('manage_projects')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/edit_project.html', {'form': form, 'project': project})


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('core/manage_projects')




from .models import EmployeeProjectMapping
from .forms import EmployeeProjectMappingForm
from django.core.paginator import Paginator

def manage_mappings(request):
    query = request.GET.get('q', '')
    mappings = EmployeeProjectMapping.objects.filter(role__icontains=query).order_by('-id')
    paginator = Paginator(mappings, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = EmployeeProjectMappingForm()
    return render(request, 'core/manage_mappings.html', {'page_obj': page_obj, 'form': form, 'query': query})

def add_mapping(request):
    if request.method == 'POST':
        form = EmployeeProjectMappingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_mappings')  # Redirect only after saving
    else:
        form = EmployeeProjectMappingForm()  # Show empty form on GET request
    
    return render(request, 'mappings/add_mapping.html', {'form': form})

def edit_mapping(request, pk):
    mapping = get_object_or_404(EmployeeProjectMapping, pk=pk)
    if request.method == 'POST':
        form = EmployeeProjectMappingForm(request.POST, instance=mapping)
        if form.is_valid():
            form.save()
            return redirect('manage_mappings')
    else:
        form = EmployeeProjectMappingForm(instance=mapping)
    return render(request, 'core/edit_mapping.html', {'form': form, 'mapping': mapping})

def delete_mapping(request, pk):
    mapping = get_object_or_404(EmployeeProjectMapping, pk=pk)
    mapping.delete()
    return redirect('manage_mappings')


# views.py

from .models import Employee, TechnicalSkill
from .forms import TechnicalSkillForm
from django.core.paginator import Paginator

def manage_technical_skills(request):
    query = request.GET.get('q', '')
    # Search employees by name or filter by skill field
    employees = Employee.objects.filter(full_name__icontains=query).order_by('full_name')
    paginator = Paginator(employees, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'technical_skills/manage_technical_skills.html', {
        'page_obj': page_obj,
        'query': query,
    })

def add_technical_skill(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if employee.technical_skill.exists():  # Check if there are related skills
     return redirect('edit_technical_skill', pk=employee.technical_skill.first().id)  # Use `.first()`
    if request.method == 'POST':
        form = TechnicalSkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.employee = employee
            skill.save()
            return redirect('manage_technical_skills')
    else:
        form = TechnicalSkillForm()
    return render(request, 'technical_skills/form.html', {'form': form, 'employee': employee})

def edit_technical_skill(request, pk):
    skill = get_object_or_404(TechnicalSkill, pk=pk)
    if request.method == 'POST':
        form = TechnicalSkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('manage_technical_skills')
    else:
        form = TechnicalSkillForm(instance=skill)
    return render(request, 'technical_skills/form.html', {'form': form, 'employee': skill.employee})

def delete_technical_skill(request, pk):
    skill = get_object_or_404(TechnicalSkill, pk=pk)
    employee_id = skill.employee.id
    if request.method == 'POST':
        skill.delete()
        return redirect('manage_technical_skills')
    return render(request, 'technical_skills/confirm_delete.html', {'skill': skill, 'employee': skill.employee})




















import base64, os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Employee, TechnicalSkill, EmployeeProjectMapping
from .forms import ResumeEditForm, TechnicalSkillFormSet, ProjectMappingFormSet
from django.contrib.auth.decorators import login_required

# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee
from .forms import ResumeEditForm

# core/views.py

# core/views.py

import os
import base64

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
import pdfkit



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Employee, TechnicalSkill, EmployeeProjectMapping
from .forms import ResumeEditForm, TechnicalSkillForm, EmployeeProjectMappingForm

@login_required
def edit_resume(request):
    employee, created = Employee.objects.get_or_create(
        user=request.user,
        defaults={
            'email': request.user.email,
            'full_name': request.user.get_full_name() or request.user.username,
            'experience_years': 0,
        }
    )

    skill_instance = TechnicalSkill.objects.filter(employee=employee).first()
    mapping_instance = EmployeeProjectMapping.objects.filter(employee=employee).first()

    if request.method == 'POST':
        form = ResumeEditForm(request.POST, instance=employee)
        skill_form = TechnicalSkillForm(request.POST, instance=skill_instance)
        mapping_form = EmployeeProjectMappingForm(request.POST, instance=mapping_instance)

        if form.is_valid() and skill_form.is_valid() and mapping_form.is_valid():
            form.save()

            skill = skill_form.save(commit=False)
            skill.employee = employee
            skill.save()

            mapping = mapping_form.save(commit=False)
            mapping.employee = employee
            mapping.save()

            return redirect('resume_preview')
    else:
        form = ResumeEditForm(instance=employee)
        skill_form = TechnicalSkillForm(instance=skill_instance)
        mapping_form = EmployeeProjectMappingForm(instance=mapping_instance)

    return render(request, 'resume/edit_resume.html', {
        'form': form,
        'skill_form': skill_form,
        'mapping_form': mapping_form,
    })


@login_required
def resume_preview(request):
    # Fetch the employee record for the logged in user or return 404 if not found.
    employee = get_object_or_404(Employee, user=request.user)
    
    # Fetch related skills and project mappings (ensure these relationships are defined in your models)
    skills = TechnicalSkill.objects.filter(employee=employee)
    projects = EmployeeProjectMapping.objects.filter(employee=employee)
    
    # Build the logo URI by reading the static image and encoding it
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/img.png')
    logo_uri = None
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            logo_uri = f"data:image/png;base64,{encoded_string}"
    
    context = {
        'employee': employee,
        'skills': skills,
        'projects': projects,
        'logo_uri': logo_uri,
    }
    
    # The template 'resume/resume_preview.html' must exist in a directory that Django can find.
    return render(request, 'resume/resume_preview.html', context)

import os
import base64
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from weasyprint import HTML

from .models import Employee, TechnicalSkill, EmployeeProjectMapping

@login_required
def download_resume_pdf(request):
    employee = get_object_or_404(Employee, user=request.user)
    skills = TechnicalSkill.objects.filter(employee=employee)
    projects = EmployeeProjectMapping.objects.filter(employee=employee)

    # Read and encode the logo image as base64
    logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'images/img.png')
    logo_uri = None
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            logo_uri = f"data:image/png;base64,{encoded_string}"

    context = {
        'employee': employee,
        'skills': skills,
        'projects': projects,
        'logo_uri': logo_uri,
    }

    # Render HTML from template
    html_string = render_to_string('resume/resume_template.html', context)

    # Generate PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    # Serve PDF as response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{employee.full_name}_Resume.pdf"'
    return response







from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django import forms

# Step 1: Enter username
def forgot_password_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['reset_username'] = user.username  # Save in session
            return redirect('reset_password_form')
        except User.DoesNotExist:
            messages.error(request, 'No user found with that username.')
    return render(request, 'custom/forgot_password.html')




from .forms import ResetPasswordForm
def reset_password_form(request):
    username = request.session.get('reset_username')
    if not username:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('forgot_password_request')
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user.')
        return redirect('forgot_password_request')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password successfully reset. You can now log in.')
            return redirect('login')
    else:
        form = ResetPasswordForm()
    
    return render(request, 'custom/reset_password_form.html', {'form': form, 'username': username})






from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import ProfileForm

@login_required
def user_settings(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_settings')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'settings/user_settings.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('user_settings')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'settings/change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('home')
    return render(request, 'settings/delete_account.html')
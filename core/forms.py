from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Employee
from django.forms import modelformset_factory
from django.forms import modelformset_factory

from .models import Employee, TechnicalSkill, Project, EmployeeProjectMapping


class UserRegisterForm(UserCreationForm):
   class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']




from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'designation', 'employee_id', 'email', 'phone', 'address', 'summary', 'experience_years']


from django import forms
from .models import TechnicalSkill

class TechnicalSkillForm(forms.ModelForm):
    class Meta:
        model = TechnicalSkill
        fields = [
            'programming_and_scripting',
            'frameworks',
            'development_tools',
            'web_api_tools',
            'operating_system_and_version',
            'tools',
        ]
        widgets = {
            'programming_and_scripting': forms.Textarea(attrs={'rows': 3}),
            'frameworks': forms.Textarea(attrs={'rows': 3}),
            'development_tools': forms.Textarea(attrs={'rows': 3}),
            'web_api_tools': forms.Textarea(attrs={'rows': 3}),
            'operating_system_and_version': forms.Textarea(attrs={'rows': 2}),
            'tools': forms.Textarea(attrs={'rows': 2}),
        }
        
TechnicalSkillFormSet = modelformset_factory(
    TechnicalSkill, form=TechnicalSkillForm, extra=1, can_delete=True
)




from django import forms
from .models import Project  # Ensure Project model exists in core/models.py

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'technology_used', 'duration_months']


from .models import EmployeeProjectMapping

class EmployeeProjectMappingForm(forms.ModelForm):
    class Meta:
        model = EmployeeProjectMapping
        fields = ['employee', 'project', 'role', 'responsibilities']
ProjectMappingFormSet = modelformset_factory(
    EmployeeProjectMapping,
    form=EmployeeProjectMappingForm,
    extra=0,
    can_delete=False
        )


from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }




    from django import forms
from .models import Employee

from django import forms
from .models import Employee

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'email', 'phone', 'address', 'summary', 'experience_years']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),

           
        }



from django import forms
from .models import Employee

# core/forms.py

from django import forms
from .models import Employee

class ResumeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'employee_id', 'email', 'phone', 'address', 'summary', 'experience_years']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
        }



from django import forms

class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password1")
        p2 = cleaned_data.get("new_password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
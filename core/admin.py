from django.contrib import admin
from .models import Employee, Project, EmployeeProjectMapping

admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(EmployeeProjectMapping)


from .models import TechnicalSkill

@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ('employee',)
    search_fields = ('employee__full_name',)




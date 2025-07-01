from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=255, default="Employee")
    employee_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    summary = models.TextField()
    experience_years = models.DecimalField(max_digits=4, decimal_places=1)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee_profile",
        null=True,      # Allow null values for now
        blank=True
    )

    
    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"


from django.db import models

class TechnicalSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='technical_skill')
    programming_and_scripting = models.TextField()
    frameworks = models.TextField()
    development_tools = models.TextField()
    web_api_tools = models.TextField()
    operating_system_and_version = models.TextField()
    tools = models.TextField()

    def __str__(self):
     return f"Technical Skills of {self.employee.full_name}"





class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technology_used = models.CharField(max_length=200)
    duration_months = models.IntegerField()
    def duration_years(self):
        return round(self.duration_months / 12, 1)


    def __str__(self):
        return self.title
    
class EmployeeProjectMapping(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    responsibilities = models.TextField()



from django.utils import timezone

class ResumeDownload(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def str(self):
        return f"Resume generated for {self.employee.full_name} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    

# In your models.py or a dedicated signals.py

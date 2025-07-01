# core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee

@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(
            user=instance,
            email=instance.email,
            full_name=instance.get_full_name() or instance.username,
            experience_years=0,  # Default value
        )
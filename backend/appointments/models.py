# appointments/models.py
from django.db import models

class Appointment(models.Model):
    ghl_id = models.CharField(max_length=100, unique=True)
    location_id = models.CharField(max_length=100)
    calendar_id = models.CharField(max_length=100)
    contact_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200, default="Cita")
    appointment_status = models.CharField(max_length=50, default="confirmed")
    assigned_user_id = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    source = models.CharField(max_length=50, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.ghl_id})"

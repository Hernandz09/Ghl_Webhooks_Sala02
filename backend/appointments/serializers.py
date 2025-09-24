# appointments/serializers.py
# Serializador para el modelo Appointment - GHL Sala 02
from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Appointment.
    Maneja la serialización/deserialización de datos de citas.
    """
    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ['date_added', 'date_updated']

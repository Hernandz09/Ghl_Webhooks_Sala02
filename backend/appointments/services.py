# appointments/services.py
# Servicios para la gestión de citas - GHL Sala 02

"""
Módulo de servicios para la gestión de citas.
Contiene lógica de negocio y funciones auxiliares.
"""

def validate_appointment_data(data):
    """
    Valida los datos de una cita antes de guardarla.
    
    Args:
        data (dict): Datos de la cita a validar
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['ghl_id', 'location_id', 'calendar_id', 'contact_id']
    
    for field in required_fields:
        if not data.get(field):
            return False, f"El campo '{field}' es requerido"
    
    return True, None


def format_appointment_for_ghl(appointment):
    """
    Formatea una cita para envío a GoHighLevel API.
    
    Args:
        appointment (Appointment): Instancia del modelo Appointment
        
    Returns:
        dict: Datos formateados para GHL
    """
    return {
        'id': appointment.ghl_id,
        'locationId': appointment.location_id,
        'calendarId': appointment.calendar_id,
        'contactId': appointment.contact_id,
        'title': appointment.title,
        'appointmentStatus': appointment.appointment_status,
        'assignedUserId': appointment.assigned_user_id,
        'notes': appointment.notes,
        'startTime': appointment.start_time.isoformat(),
        'endTime': appointment.end_time.isoformat(),
        'source': appointment.source
    }

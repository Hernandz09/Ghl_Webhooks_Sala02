from django.contrib import admin
from django.utils import timezone
from django.conf import settings
from .models import Appointment
import requests, os, uuid
from django.utils.dateparse import parse_datetime


# === Constantes GHL ===
GHL_BASE_URL = "https://services.leadconnectorhq.com"
GHL_API_VERSION = os.getenv("GHL_API_VERSION", "2021-04-15")
ACCESS_TOKEN = os.getenv("GHL_ACCESS_TOKEN")
GHL_LOCATION_ID = os.getenv("GHL_LOCATION_ID")


def _to_datetime(iso_str):
    if not iso_str:
        return None
    dt = parse_datetime(iso_str)
    if dt and settings.USE_TZ and timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "ghl_id", "calendar_id", "contact_id", "title",
        "appointment_status", "assigned_user_id", "start_time", "end_time",
        "date_added", "date_updated"
    )
    search_fields = ("ghl_id", "title", "contact_id")
    list_filter = ("appointment_status", "calendar_id")

    # Campos que el admin puede editar
    fields = (
        "calendar_id",
        "contact_id",
        "start_time",
        "end_time",
        "title",
        "appointment_status",
        "assigned_user_id",
    )

    readonly_fields = ("ghl_id", "location_id", "source", "date_added", "date_updated")

    def save_model(self, request, obj, form, change):
        """Sobrescribe save para sincronizar con GHL."""
        location_id = obj.location_id or GHL_LOCATION_ID
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Version": GHL_API_VERSION,
            "Content-Type": "application/json",
            "LocationId": location_id
        }

        payload = {
            "calendarId": obj.calendar_id,
            "locationId": location_id,
            "contactId": obj.contact_id,
            "startTime": obj.start_time.isoformat(),
            "endTime": obj.end_time.isoformat(),
            "title": obj.title or "Cita creada desde Admin",
            "appointmentStatus": obj.appointment_status or "confirmed",
            "assignedUserId": obj.assigned_user_id,
            "ignoreFreeSlotValidation": True,
            "toNotify": True
        }

        try:
            if not change or not obj.ghl_id:
                # === Crear cita en GHL ===
                resp = requests.post(f"{GHL_BASE_URL}/calendars/events/appointments", json=payload, headers=headers, timeout=15)
                resp.raise_for_status()
                ghl_data = resp.json()
            else:
                # === Actualizar cita en GHL ===
                url = f"{GHL_BASE_URL}/calendars/events/appointments/{obj.ghl_id}"
                resp = requests.put(url, json=payload, headers=headers, timeout=15)
                resp.raise_for_status()
                ghl_data = resp.json()

            # Actualizamos con lo que devuelve GHL
            obj.ghl_id = ghl_data.get("id") or obj.ghl_id or uuid.uuid4().hex[:20]
            obj.location_id = ghl_data.get("locationId") or location_id
            obj.calendar_id = ghl_data.get("calendarId") or obj.calendar_id
            obj.contact_id = ghl_data.get("contactId") or obj.contact_id
            obj.title = ghl_data.get("title") or obj.title
            obj.appointment_status = ghl_data.get("appointmentStatus") or obj.appointment_status
            obj.assigned_user_id = ghl_data.get("assignedUserId") or obj.assigned_user_id
            obj.notes = ghl_data.get("notes") or None
            obj.start_time = _to_datetime(ghl_data.get("startTime")) or obj.start_time
            obj.end_time = _to_datetime(ghl_data.get("endTime")) or obj.end_time
            obj.source = ghl_data.get("source") or "calendar_page"
            obj.date_added = _to_datetime(ghl_data.get("dateAdded")) or obj.date_added or timezone.now()
            obj.date_updated = _to_datetime(ghl_data.get("dateUpdated")) or timezone.now()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error sincronizando con GHL: {str(e)}")

        super().save_model(request, obj, form, change)

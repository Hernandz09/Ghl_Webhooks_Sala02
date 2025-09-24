# appointments/views.py
# Vistas para la gestión de citas - GHL Sala 02
import os
import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from .models import Appointment
from .serializers import AppointmentSerializer
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.conf import settings
from rest_framework.generics import ListAPIView


# Cargar variables de entorno
load_dotenv()

# Constantes GHL
GHL_BASE_URL = "https://services.leadconnectorhq.com"
GHL_API_VERSION = os.getenv("GHL_API_VERSION", "2021-04-15")
ACCESS_TOKEN = os.getenv("GHL_ACCESS_TOKEN")
GHL_LOCATION_ID = os.getenv("GHL_LOCATION_ID")  # fallback si viene vacío en el webhook
GHL_DEFAULT_ASSIGNED_USER_ID = os.getenv("GHL_ASSIGNED_USER_ID")

# Nota: No lanzar excepción en import. Validar token solo en endpoints que lo requieran.

def _to_datetime(iso_str):
    """Convierte ISO8601 string a datetime aware o devuelve None."""
    if not iso_str:
        return None
    dt = parse_datetime(iso_str)
    if dt is None:
        return None
    if settings.USE_TZ and timezone.is_naive(dt):
        tz = timezone.get_current_timezone()
        dt = timezone.make_aware(dt, tz)
    return dt

class AppointmentCreateView(APIView):
    """Crear una cita en GHL y guardarla en MySQL (ya lo tenías)."""
    def post(self, request, *args, **kwargs):
        if not ACCESS_TOKEN:
            return Response({"error": "Falta GHL_ACCESS_TOKEN en servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = request.data or {}
        required_fields = ["calendarId", "contactId", "startTime", "endTime"]
        for field in required_fields:
            if field not in data:
                return Response({"error": f"Falta el campo: {field}"}, status=status.HTTP_400_BAD_REQUEST)

        location_id = data.get("locationId") or GHL_LOCATION_ID
        if not location_id:
            return Response({"error": "No se encontró locationId (poner GHL_LOCATION_ID en .env o enviarlo en el payload)"},
                            status=status.HTTP_400_BAD_REQUEST)

        # assignedUserId es requerido por algunas cuentas/configuraciones de GHL
        assigned_user_id = data.get("assignedUserId") or GHL_DEFAULT_ASSIGNED_USER_ID
        if not assigned_user_id:
            return Response(
                {"error": "Falta assignedUserId",
                 "details": "Incluye assignedUserId en el payload o configura GHL_ASSIGNED_USER_ID en el .env"},
                status=status.HTTP_400_BAD_REQUEST
            )

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Version": GHL_API_VERSION,
            "Content-Type": "application/json",
            "LocationId": location_id
        }

        api_payload = {
            "calendarId": data["calendarId"],
            "locationId": location_id,
            "contactId": data["contactId"],
            "startTime": data["startTime"],
            "endTime": data["endTime"],
            "title": data.get("title", "Cita creada desde API"),
            "appointmentStatus": data.get("appointmentStatus", "confirmed"),
            "assignedUserId": assigned_user_id,
            "ignoreFreeSlotValidation": True,
            "toNotify": True
        }

        try:
            resp = requests.post(f"{GHL_BASE_URL}/calendars/events/appointments", json=api_payload, headers=headers, timeout=15)
            resp.raise_for_status()
            ghl_data = resp.json()

            start_dt = _to_datetime(ghl_data.get("startTime") or api_payload["startTime"])
            end_dt = _to_datetime(ghl_data.get("endTime") or api_payload["endTime"])

            appointment, created = Appointment.objects.update_or_create(
                ghl_id=ghl_data.get("id"),
                defaults={
                    "location_id": ghl_data.get("locationId") or location_id,
                    "calendar_id": ghl_data.get("calendarId") or api_payload["calendarId"],
                    "contact_id": ghl_data.get("contactId") or api_payload["contactId"],
                    "title": ghl_data.get("title") or api_payload.get("title", "Cita"),
                    "appointment_status": ghl_data.get("appointmentStatus") or api_payload.get("appointmentStatus", "confirmed"),
                    "assigned_user_id": ghl_data.get("assignedUserId") or api_payload.get("assignedUserId"),
                    "notes": ghl_data.get("notes") or None,
                    "start_time": start_dt,
                    "end_time": end_dt,
                    "source": ghl_data.get("source")
                }
            )

            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except requests.exceptions.HTTPError as http_err:
            resp = http_err.response
            details = resp.text if resp is not None else str(http_err)
            code = resp.status_code if resp is not None else 500
            return Response({"error": "Error HTTP al crear cita en GHL", "details": details}, status=code)
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error conexión GHL", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response({"error": "Error interno", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def ghl_webhook(request):
    """
    Endpoint público que recibe los webhooks de GHL.
    Maneja AppointmentCreate, AppointmentUpdate y AppointmentDelete.
    """
    event = request.data or {}
    print("=== Webhook recibido de GHL ===")
    print(json.dumps(event, indent=2, ensure_ascii=False))

    # Payload típico: { "type": "...", "locationId": "...", "appointment": { ... } }
    appointment_data = event.get("appointment") if "appointment" in event else event
    event_type = event.get("type") or request.headers.get("X-GHL-Event")
    ghl_id = appointment_data.get("id") if isinstance(appointment_data, dict) else None

    # location puede venir en la raíz o dentro de appointment
    location_id = event.get("locationId") or (appointment_data.get("locationId") if isinstance(appointment_data, dict) else None) or GHL_LOCATION_ID

    # Validaciones básicas
    if not isinstance(appointment_data, dict) or not ghl_id:
        return Response({"error": "Payload inválido: no se encontró appointment.id"}, status=status.HTTP_400_BAD_REQUEST)

    # convertir fechas si vienen
    start_dt = _to_datetime(appointment_data.get("startTime"))
    end_dt = _to_datetime(appointment_data.get("endTime"))
    date_added_dt = _to_datetime(appointment_data.get("dateAdded"))
    date_updated_dt = _to_datetime(appointment_data.get("dateUpdated"))

    try:
        # === DELETE / CANCEL ===
        if event_type == "AppointmentDelete" or appointment_data.get("appointmentStatus") == "cancelled":
            # Opción 1: marcar como cancelada
            Appointment.objects.filter(ghl_id=ghl_id).update(appointment_status="cancelled")
            print("🟡 Marcada como cancelled en BD:", ghl_id)

            # Opción 2 (si prefieres borrarla de la tabla)
            # Appointment.objects.filter(ghl_id=ghl_id).delete()
            # print("❌ Eliminada de la BD:", ghl_id)

            return Response({"status": "cancelled", "ghl_id": ghl_id}, status=status.HTTP_200_OK)

        # === CREATE / UPDATE ===
        if event_type in ["AppointmentCreate", "AppointmentUpdate"] or appointment_data.get("id"):
            appointment, created = Appointment.objects.update_or_create(
                ghl_id=ghl_id,
                defaults={
                    "location_id": location_id,
                    "calendar_id": appointment_data.get("calendarId"),
                    "contact_id": appointment_data.get("contactId"),
                    "title": appointment_data.get("title"),
                    "appointment_status": appointment_data.get("appointmentStatus"),
                    "assigned_user_id": appointment_data.get("assignedUserId"),
                    "notes": appointment_data.get("notes") or None,
                    "start_time": start_dt,
                    "end_time": end_dt,
                    "source": appointment_data.get("source"),
                    "date_added": date_added_dt,
                    "date_updated": date_updated_dt,
                }
            )
            print("✅ Guardada/actualizada en MySQL:", appointment.ghl_id)
            return Response({"status": "ok", "ghl_id": ghl_id}, status=status.HTTP_200_OK)

        # === Evento no esperado ===
        print("⚠️ Evento no manejado:", event_type)
        return Response({"status": "ignored", "event_type": event_type}, status=status.HTTP_200_OK)

    except Exception as e:
        print("❌ Error al procesar webhook:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentUpdateView(APIView):
    """Actualizar cita en GHL y sincronizar BD local."""
    def put(self, request, appointment_id):
        if not ACCESS_TOKEN:
            return Response({"error": "Falta GHL_ACCESS_TOKEN en servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        appointment = Appointment.objects.filter(ghl_id=appointment_id).first()
        location_id = appointment.location_id if appointment else GHL_LOCATION_ID

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Version": GHL_API_VERSION,
            "Content-Type": "application/json",
            "LocationId": location_id
        }
        url = f"{GHL_BASE_URL}/calendars/events/appointments/{appointment_id}"

        try:
            resp = requests.put(url, headers=headers, json=request.data, timeout=15)
            resp.raise_for_status()

            # Algunas respuestas PUT de GHL pueden devolver 204 o cuerpo vacío.
            response_has_body = bool(resp.content and resp.content.strip())
            if response_has_body:
                try:
                    data = resp.json()
                except ValueError:
                    # Cuerpo no JSON; usar payload enviado como fuente de verdad
                    data = {}
            else:
                data = {}

            # Fallback a los valores enviados si el body viene vacío
            merged = {
                "title": data.get("title", request.data.get("title")),
                "appointmentStatus": data.get("appointmentStatus", request.data.get("appointmentStatus")),
                "assignedUserId": data.get("assignedUserId", request.data.get("assignedUserId")),
                "notes": data.get("notes", request.data.get("notes")),
                "startTime": data.get("startTime", request.data.get("startTime")),
                "endTime": data.get("endTime", request.data.get("endTime")),
            }

            start_dt = _to_datetime(merged.get("startTime"))
            end_dt = _to_datetime(merged.get("endTime"))

            Appointment.objects.filter(ghl_id=appointment_id).update(
                title=merged.get("title"),
                appointment_status=merged.get("appointmentStatus"),
                assigned_user_id=merged.get("assignedUserId"),
                notes=(merged.get("notes") or None),
                start_time=start_dt,
                end_time=end_dt,
            )

            # Devolver lo mejor posible: si no hay body, devolver merged y 200
            return Response(data if response_has_body else merged, status=resp.status_code if response_has_body else status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error al actualizar cita en GHL", "details": str(e)}, status=500)
        except Exception as e:
            # Capturar errores no previstos (por ejemplo, JSON decode) para evitar 500 no controlados
            return Response({"error": "Error interno al procesar actualización", "details": str(e)}, status=500)


class AppointmentDeleteView(APIView):
    """Cancelar cita en GHL (PUT appointmentStatus=cancelled)."""
    def delete(self, request, appointment_id):
        if not ACCESS_TOKEN:
            return Response({"error": "Falta GHL_ACCESS_TOKEN en servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        appointment = Appointment.objects.filter(ghl_id=appointment_id).first()
        location_id = appointment.location_id if appointment else GHL_LOCATION_ID

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Version": GHL_API_VERSION,
            "Content-Type": "application/json",
            "LocationId": location_id
        }
        url = f"{GHL_BASE_URL}/calendars/events/appointments/{appointment_id}"

        payload = {"appointmentStatus": "cancelled"}

        try:
            resp = requests.put(url, headers=headers, json=payload, timeout=15)
            print("PUT GHL status:", resp.status_code)
            print("PUT GHL body:", resp.text)
            resp.raise_for_status()
            # Actualizar BD local
            Appointment.objects.filter(ghl_id=appointment_id).update(appointment_status="cancelled")
            return Response({"message": "Cita cancelada correctamente"}, status=resp.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error al cancelar cita en GHL", "details": str(e)}, status=500)

class AppointmentListView(ListAPIView):
    queryset = Appointment.objects.all().order_by('-start_time')
    serializer_class = AppointmentSerializer
from django.urls import path
from .views import AppointmentListView

from .views import (
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    ghl_webhook
)

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name="create_appointment"),
    path('update/<str:appointment_id>/', AppointmentUpdateView.as_view(), name="update_appointment"),
    path('delete/<str:appointment_id>/', AppointmentDeleteView.as_view(), name="delete_appointment"),
    # 🔥 Ahora coincide con lo que configuraste en GHL
    path('webhooks/ghl/appointments/', ghl_webhook, name="ghl_webhook"),
        path('appointments/', AppointmentListView.as_view(), name="list_appointments"),

]

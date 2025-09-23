import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

export const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,
})

// Appointments
export interface Appointment {
  id: number
  ghl_id: string
  location_id: string
  calendar_id: string
  contact_id: string
  title: string
  appointment_status: string
  assigned_user_id?: string | null
  notes?: string | null
  start_time: string
  end_time: string
  source?: string | null
  date_added: string
  date_updated: string
}

export async function fetchAppointments(): Promise<Appointment[]> {
  const res = await api.get('/api/appointments/appointments/')
  return res.data
}

export interface CreateAppointmentPayload {
  calendarId: string
  contactId: string
  startTime: string
  endTime: string
  locationId?: string
  title?: string
  appointmentStatus?: string
  assignedUserId?: string
}

export async function createAppointment(payload: CreateAppointmentPayload) {
  const res = await api.post('/api/appointments/create/', payload)
  return res.data as Appointment
}

export async function updateAppointment(appointmentId: string, data: Partial<CreateAppointmentPayload>) {
  const res = await api.put(`/api/appointments/update/${appointmentId}/`, data)
  return res.data
}

export async function cancelAppointment(appointmentId: string) {
  const res = await api.delete(`/api/appointments/delete/${appointmentId}/`)
  return res.data
}



import { FormEvent, useState } from 'react'
import { createAppointment } from '../api/client'
import { useNavigate } from 'react-router-dom'

export default function NewAppointmentPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    calendarId: '',
    contactId: '',
    // Mantener en estado en formato "YYYY-MM-DDTHH:mm" (datetime-local)
    startTimeLocal: '',
    endTimeLocal: '',
    locationId: '',
    title: 'Cita creada desde Frontend',
    assignedUserId: '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  function toIsoUtc(localValue: string) {
    // localValue: "YYYY-MM-DDTHH:mm" interpretado en zona local
    if (!localValue) return ''
    return new Date(localValue).toISOString()
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      const payload = {
        calendarId: form.calendarId,
        contactId: form.contactId,
        startTime: toIsoUtc(form.startTimeLocal),
        endTime: toIsoUtc(form.endTimeLocal),
        locationId: form.locationId || undefined,
        title: form.title,
        assignedUserId: form.assignedUserId || undefined,
      }
      await createAppointment(payload)
      navigate('/appointments')
    } catch (e: any) {
      const data = e?.response?.data
      const base = data?.error || e?.message || 'Error al crear cita'
      const details = typeof data?.details === 'string' ? `: ${data.details}` : ''
      setError(base + details)
    } finally {
      setSubmitting(false)
    }
  }

  function set<K extends keyof typeof form>(key: K, value: string) {
    setForm(prev => ({ ...prev, [key]: value }))
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2 className="panel-title">Nueva cita</h2>
      </div>
      <div className="panel-body">
        {error && <p style={{ color: 'crimson' }}>{error}</p>}
        <form onSubmit={onSubmit} className="form">
          <div className="field">
            <label className="label">Calendar ID</label>
            <input className="input" value={form.calendarId} onChange={e => set('calendarId', e.target.value)} required />
          </div>
          <div className="field">
            <label className="label">Contact ID</label>
            <input className="input" value={form.contactId} onChange={e => set('contactId', e.target.value)} required />
          </div>
          <div className="field">
            <label className="label">Location ID (opcional si ya está en backend)</label>
            <input className="input" value={form.locationId} onChange={e => set('locationId', e.target.value)} />
          </div>
          <div className="field">
            <label className="label">assignedUserId (requerido por GHL en tu cuenta)</label>
            <input className="input" value={form.assignedUserId} onChange={e => set('assignedUserId', e.target.value)} placeholder="uuid del usuario" />
          </div>
          <div className="field">
            <label className="label">Inicio</label>
            <input type="datetime-local" className="input" value={form.startTimeLocal} onChange={e => set('startTimeLocal', e.target.value)} required />
          </div>
          <div className="field">
            <label className="label">Fin</label>
            <input type="datetime-local" className="input" value={form.endTimeLocal} onChange={e => set('endTimeLocal', e.target.value)} required />
          </div>
          <div className="field">
            <label className="label">Título</label>
            <input className="input" value={form.title} onChange={e => set('title', e.target.value)} />
          </div>
          <div className="form-actions">
            <button className="btn btn-primary" type="submit" disabled={submitting}>{submitting ? 'Creando...' : 'Crear'}</button>
          </div>
        </form>
      </div>
    </div>
  )
}



import { FormEvent, useEffect, useState } from 'react'
import { updateAppointment, fetchAppointments } from '../api/client'
import { useNavigate, useParams } from 'react-router-dom'

export default function EditAppointmentPage() {
  const navigate = useNavigate()
  const { id } = useParams()
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({
    title: '',
    appointmentStatus: 'confirmed',
    // Guardar en estado como "YYYY-MM-DDTHH:mm" para inputs datetime-local
    startTimeLocal: '',
    endTimeLocal: '',
    notes: '',
    assignedUserId: '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  function fromIsoToLocalInput(iso: string) {
    if (!iso) return ''
    const dt = new Date(iso)
    const yyyy = dt.getFullYear()
    const mm = String(dt.getMonth() + 1).padStart(2, '0')
    const dd = String(dt.getDate()).padStart(2, '0')
    const hh = String(dt.getHours()).padStart(2, '0')
    const min = String(dt.getMinutes()).padStart(2, '0')
    return `${yyyy}-${mm}-${dd}T${hh}:${min}`
  }

  function toIsoUtc(localValue: string) {
    if (!localValue) return ''
    return new Date(localValue).toISOString()
  }

  useEffect(() => {
    (async () => {
      if (!id) return
      try {
        const all = await fetchAppointments()
        const found = all.find(a => a.ghl_id === id)
        if (found) {
          setForm({
            title: found.title || '',
            appointmentStatus: found.appointment_status || 'confirmed',
            startTimeLocal: fromIsoToLocalInput(found.start_time),
            endTimeLocal: fromIsoToLocalInput(found.end_time),
            notes: found.notes || '',
            assignedUserId: found.assigned_user_id || '',
          })
        }
      } finally {
        setLoading(false)
      }
    })()
  }, [id])

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    if (!id) return
    setSubmitting(true)
    setError(null)
    try {
      const payload = {
        title: form.title,
        appointmentStatus: form.appointmentStatus,
        startTime: toIsoUtc(form.startTimeLocal),
        endTime: toIsoUtc(form.endTimeLocal),
        notes: form.notes || undefined,
        assignedUserId: form.assignedUserId || undefined,
      }
      await updateAppointment(id, payload)
      navigate('/appointments')
    } catch (e: any) {
      const data = e?.response?.data
      const base = data?.error || e?.message || 'Error al actualizar cita'
      const details = typeof data?.details === 'string' ? `: ${data.details}` : ''
      setError(base + details)
    } finally {
      setSubmitting(false)
    }
  }

  function set<K extends keyof typeof form>(key: K, value: string) {
    setForm(prev => ({ ...prev, [key]: value }))
  }

  if (loading) return <div className="panel"><div className="panel-body"><p>Cargando...</p></div></div>

  return (
    <div className="panel">
      <div className="panel-header">
        <h2 className="panel-title">Editar cita</h2>
      </div>
      <div className="panel-body">
        {error && <p style={{ color: 'crimson' }}>{error}</p>}
        <form onSubmit={onSubmit} className="form">
          <div className="field">
            <label className="label">Título</label>
            <input className="input" value={form.title} onChange={e => set('title', e.target.value)} />
          </div>
          <div className="field">
            <label className="label">Estado</label>
            <select className="select" value={form.appointmentStatus} onChange={e => set('appointmentStatus', e.target.value)}>
              <option value="confirmed">confirmed</option>
              <option value="cancelled">cancelled</option>
              <option value="rescheduled">rescheduled</option>
            </select>
          </div>
          <div className="field">
            <label className="label">assignedUserId</label>
            <input className="input" value={form.assignedUserId} onChange={e => set('assignedUserId', e.target.value)} />
          </div>
          <div className="field">
            <label className="label">Inicio</label>
            <input type="datetime-local" className="input" value={form.startTimeLocal} onChange={e => set('startTimeLocal', e.target.value)} />
          </div>
          <div className="field">
            <label className="label">Fin</label>
            <input type="datetime-local" className="input" value={form.endTimeLocal} onChange={e => set('endTimeLocal', e.target.value)} />
          </div>
          <div className="field">
            <label className="label">Notas</label>
            <textarea className="textarea" value={form.notes} onChange={e => set('notes', e.target.value)} />
          </div>
          <div className="form-actions">
            <button className="btn btn-primary" type="submit" disabled={submitting}>{submitting ? 'Guardando...' : 'Guardar'}</button>
          </div>
        </form>
      </div>
    </div>
  )
}



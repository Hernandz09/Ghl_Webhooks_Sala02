import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Appointment, cancelAppointment, fetchAppointments } from '../api/client'
import StatusBadge from '../components/StatusBadge'

export default function AppointmentsPage() {
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function load() {
    try {
      setLoading(true)
      setError(null)
      const data = await fetchAppointments()
      setAppointments(data)
    } catch (e: any) {
      setError(e?.message || 'Error cargando citas')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function handleCancel(ghlId: string) {
    if (!confirm('¿Cancelar esta cita?')) return
    await cancelAppointment(ghlId)
    await load()
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2 className="panel-title">Citas</h2>
        <Link to="/appointments/new" className="btn btn-primary">Nueva cita</Link>
      </div>
      <div className="panel-body">
        {loading && <p>Cargando...</p>}
        {error && <p style={{ color: 'crimson' }}>{error}</p>}
        {!loading && appointments.length === 0 && <div className="empty">No hay citas.</div>}
        {!loading && appointments.length > 0 && (
          <table className="table">
            <thead>
              <tr>
                <th>Título</th>
                <th>Estado</th>
                <th>Inicio</th>
                <th>Fin</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map(a => (
                <tr key={a.ghl_id}>
                  <td>{a.title}</td>
                  <td>
                    <StatusBadge status={a.appointment_status} />
                  </td>
                  <td>{new Date(a.start_time).toLocaleString()}</td>
                  <td>{new Date(a.end_time).toLocaleString()}</td>
                  <td>
                    <div className="grid-actions">
                      <Link to={`/appointments/${a.ghl_id}/edit`} className="btn">Editar</Link>
                      {a.appointment_status !== 'cancelled' && (
                        <button className="btn btn-danger" onClick={() => handleCancel(a.ghl_id)}>Cancelar</button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}



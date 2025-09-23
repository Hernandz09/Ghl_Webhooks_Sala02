import { Link, Route, Routes, Navigate } from 'react-router-dom'
import AppointmentsPage from './pages/AppointmentsPage'
import EditAppointmentPage from './pages/EditAppointmentPage'
import NewAppointmentPage from './pages/NewAppointmentPage'

export default function App() {
  return (
    <div>
      <header className="app-header">
        <div className="app-header-inner">
          <div className="brand">
            <div className="brand-badge" />
            <div className="brand-title">Reflexo</div>
          </div>
          <nav className="nav">
            <Link to="/appointments">Citas</Link>
            <Link to="/appointments/new" className="btn btn-primary">Nueva cita</Link>
          </nav>
        </div>
      </header>
      <div className="container page">
        <Routes>
          <Route path="/" element={<Navigate to="/appointments" replace />} />
          <Route path="/appointments" element={<AppointmentsPage />} />
          <Route path="/appointments/new" element={<NewAppointmentPage />} />
          <Route path="/appointments/:id/edit" element={<EditAppointmentPage />} />
        </Routes>
      </div>
    </div>
  )
}



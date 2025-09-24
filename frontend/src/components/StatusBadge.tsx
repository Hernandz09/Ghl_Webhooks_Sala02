interface StatusBadgeProps {
  status: string
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  const getStatusConfig = (status: string) => {
    switch (status.toLowerCase()) {
      case 'confirmed':
        return {
          label: 'Confirmada',
          icon: '✓',
          className: 'confirmed'
        }
      case 'cancelled':
        return {
          label: 'Cancelada',
          icon: '✕',
          className: 'cancelled'
        }
      default:
        return {
          label: status,
          icon: '?',
          className: 'confirmed'
        }
    }
  }

  const config = getStatusConfig(status)

  return (
    <span className={`status-badge ${config.className}`}>
      <span>{config.icon}</span>
      <span>{config.label}</span>
    </span>
  )
}

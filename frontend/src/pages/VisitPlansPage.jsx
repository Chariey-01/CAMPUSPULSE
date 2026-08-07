import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { CalendarCheck, CheckCircle2, XCircle } from 'lucide-react'
import { api } from '../api/client'

export default function VisitPlansPage() {
  const [plans, setPlans] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/api/visit-plans')
      .then(setPlans)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleMarkVisited(planId) {
    const updated = await api.put(`/api/visit-plans/${planId}`, { status: 'Visited' })
    setPlans((prev) => prev.map((p) => (p.id === planId ? updated : p)))
  }

  async function handleCancel(planId) {
    await api.delete(`/api/visit-plans/${planId}`)
    setPlans((prev) => prev.filter((p) => p.id !== planId))
  }

  if (loading) return <p className="loading-state">Loading...</p>

  return (
    <div className="visit-plans-page">
      <div className="page-header">
        <h1>My Visit Plans</h1>
        <p>Places you're planning to check out.</p>
      </div>
      {error && <p className="error">{error}</p>}
      {plans.length === 0 && (
        <div className="empty-state">
          <CalendarCheck size={26} strokeWidth={1.5} />
          <p>No visit plans yet — plan a visit from any place's page.</p>
        </div>
      )}

      <ul className="simple-list">
        {plans.map((plan) => (
          <li key={plan.id}>
            <div className="item-info">
              <Link to={`/places/${plan.place_id}`}>{plan.place?.name}</Link>
              {plan.notes && <p>{plan.notes}</p>}
            </div>
            <span className={`status status-${plan.status.toLowerCase()}`}>{plan.status}</span>
            {plan.status === 'Planned' && (
              <button type="button" onClick={() => handleMarkVisited(plan.id)} className="icon-btn btn-sm">
                <CheckCircle2 size={14} /> Mark as Visited
              </button>
            )}
            <button type="button" onClick={() => handleCancel(plan.id)} className="btn-danger-text icon-btn btn-sm">
              <XCircle size={14} /> Cancel
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

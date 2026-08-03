import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
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

  if (loading) return <p>Loading...</p>

  return (
    <div className="visit-plans-page">
      <h1>My Visit Plans</h1>
      {error && <p className="error">{error}</p>}
      {plans.length === 0 && <p>No visit plans yet.</p>}

      <ul className="simple-list">
        {plans.map((plan) => (
          <li key={plan.id}>
            <Link to={`/places/${plan.place_id}`}>{plan.place?.name}</Link>
            <span className={`status status-${plan.status.toLowerCase()}`}>{plan.status}</span>
            {plan.notes && <p>{plan.notes}</p>}
            {plan.status === 'Planned' && (
              <button onClick={() => handleMarkVisited(plan.id)}>Mark as Visited</button>
            )}
            <button onClick={() => handleCancel(plan.id)}>Cancel</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

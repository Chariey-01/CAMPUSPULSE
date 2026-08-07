import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Building2, Trash2 } from 'lucide-react'
import { api } from '../api/client'

export default function MyPlacesPage() {
  const [places, setPlaces] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/api/places/mine')
      .then((data) => setPlaces(data.items))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleDelete(placeId) {
    if (!window.confirm('Delete this place?')) return

    try {
      await api.delete(`/api/places/${placeId}`)
      setPlaces((prev) => prev.filter((p) => p.id !== placeId))
    } catch (err) {
      setError(err.message)
    }
  }

  if (loading) return <p className="loading-state">Loading...</p>

  return (
    <div className="my-places-page">
      <div className="page-header">
        <h1>My Submitted Places</h1>
        <p>Places you've added to CampusPulse.</p>
      </div>
      {error && <p className="error">{error}</p>}
      {places.length === 0 && (
        <div className="empty-state">
          <Building2 size={26} strokeWidth={1.5} />
          <p>You haven't submitted any places yet.</p>
        </div>
      )}

      <ul className="simple-list">
        {places.map((place) => (
          <li key={place.id}>
            <div className="item-info">
              <Link to={`/places/${place.id}`}>{place.name}</Link>
            </div>
            <span className={`status status-${place.status.toLowerCase()}`}>{place.status}</span>
            <button type="button" onClick={() => handleDelete(place.id)} className="btn-danger-text icon-btn btn-sm">
              <Trash2 size={14} /> Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

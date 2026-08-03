import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
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

  if (loading) return <p>Loading...</p>

  return (
    <div className="my-places-page">
      <h1>My Submitted Places</h1>
      {error && <p className="error">{error}</p>}
      {places.length === 0 && <p>You haven't submitted any places yet.</p>}

      <ul className="simple-list">
        {places.map((place) => (
          <li key={place.id}>
            <Link to={`/places/${place.id}`}>{place.name}</Link>
            <span className={`status status-${place.status.toLowerCase()}`}>{place.status}</span>
            <button onClick={() => handleDelete(place.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

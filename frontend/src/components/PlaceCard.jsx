import { useState } from 'react'
import { Link } from 'react-router-dom'
import { openGoogleMaps } from '../services/googleMaps'

export default function PlaceCard({ place }) {
  const [mapError, setMapError] = useState('')

  function handleVisitClick() {
    setMapError('')
    try {
      openGoogleMaps(place.google_maps_link)
    } catch (err) {
      setMapError(err.message)
    }
  }

  return (
    <div className="place-card">
      <Link to={`/places/${place.id}`} className="place-card-link">
        {place.image_url && <img src={place.image_url} alt={place.name} />}
        <h3>{place.name}</h3>
        <p className="category">{place.category?.name}</p>
        <p>{place.description}</p>
        <div className="place-meta">
          <span>{place.average_rating ? `★ ${place.average_rating}` : 'No ratings yet'}</span>
          <span>{place.review_count ?? 0} review{place.review_count === 1 ? '' : 's'}</span>
        </div>
      </Link>

      <button type="button" onClick={handleVisitClick} className="visit-button">
         Visit
      </button>
      {mapError && <p className="error">{mapError}</p>}
    </div>
  )
}

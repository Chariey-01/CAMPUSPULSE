import { useState, createElement } from 'react'
import { Link } from 'react-router-dom'
import { Star, Clock, MapPin, Navigation2, Bookmark } from 'lucide-react'
import { openGoogleMaps } from '../services/googleMaps'
import PlaceImage from './PlaceImage'
import { getCategoryIcon, getCategoryStyle } from '../lib/categoryVisuals'

export default function PlaceCard({ place, isBookmarked = false, onToggleBookmark, showBookmark = true }) {
  const [mapError, setMapError] = useState('')
  const CategoryIcon = getCategoryIcon(place.category?.icon)
  const catStyle = getCategoryStyle(place.category)

  function handleVisitClick() {
    setMapError('')
    try {
      openGoogleMaps(place.google_maps_link)
    } catch (err) {
      setMapError(err.message)
    }
  }

  function handleBookmarkClick(event) {
    event.preventDefault()
    event.stopPropagation()
    onToggleBookmark?.(place)
  }

  return (
    <div className="place-card">
      <Link to={`/places/${place.id}`} className="place-card-link">
        <PlaceImage place={place} className="place-card-media" iconSize={30} />
      </Link>

      {showBookmark && onToggleBookmark && (
        <button
          type="button"
          className={`bookmark-toggle ${isBookmarked ? 'active' : ''}`}
          onClick={handleBookmarkClick}
          aria-label={isBookmarked ? 'Remove bookmark' : 'Bookmark this place'}
          aria-pressed={isBookmarked}
        >
          <Bookmark size={15} fill={isBookmarked ? 'currentColor' : 'none'} />
        </button>
      )}

      <Link to={`/places/${place.id}`} className="place-card-link">
        <div className="place-card-body">
          {place.category?.name && (
            <span className="category-pill" style={catStyle}>
              {createElement(CategoryIcon, { size: 12, strokeWidth: 2 })}
              {place.category.name}
            </span>
          )}
          <h3>{place.name}</h3>
          {place.description && <p className="description">{place.description}</p>}

          <div className="place-meta">
            <div className="meta-row split">
              <span className={`rating ${place.average_rating ? '' : 'unrated'}`}>
                <Star size={13} fill={place.average_rating ? 'currentColor' : 'none'} />
                {place.average_rating ? place.average_rating : 'No ratings yet'}
              </span>
              <span>{place.review_count ?? 0} review{place.review_count === 1 ? '' : 's'}</span>
            </div>
            {place.opening_hours && (
              <div className="meta-row">
                <Clock size={13} />
                {place.opening_hours}
              </div>
            )}
            {place.address && (
              <div className="meta-row">
                <MapPin size={13} />
                {place.address}
              </div>
            )}
          </div>
        </div>
      </Link>

      <div className="place-card-footer">
        <button type="button" onClick={handleVisitClick} className="visit-button btn-primary">
          <Navigation2 size={14} /> Visit
        </button>
      </div>
      {mapError && <p className="error">{mapError}</p>}
    </div>
  )
}

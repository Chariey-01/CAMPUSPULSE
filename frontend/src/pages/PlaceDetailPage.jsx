import { useState, useEffect, useCallback, createElement } from 'react'
import { useParams } from 'react-router-dom'
import { Star, Clock, MapPin, Phone, Navigation2, Bookmark, CalendarPlus } from 'lucide-react'
import { api } from '../api/client'
import { useAuth } from '../hooks/useAuth'
import { openGoogleMaps } from '../services/googleMaps'
import PlaceImage from '../components/PlaceImage'
import { getCategoryIcon, getCategoryStyle } from '../lib/categoryVisuals'
import ReviewList from '../components/ReviewList'
import ReviewForm from '../components/ReviewForm'

export default function PlaceDetailPage() {
  const { id } = useParams()
  const { user } = useAuth()

  const [place, setPlace] = useState(null)
  const [reviews, setReviews] = useState([])
  const [bookmark, setBookmark] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [visitNotes, setVisitNotes] = useState('')
  const [visitMessage, setVisitMessage] = useState('')
  const [mapError, setMapError] = useState('')

  const loadReviews = useCallback(() => {
    return api.get(`/api/places/${id}/reviews`).then(setReviews)
  }, [id])

  useEffect(() => {
    setLoading(true)
    setError('')

    Promise.all([api.get(`/api/places/${id}`), loadReviews()])
      .then(([placeData]) => setPlace(placeData))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [id, loadReviews])

  useEffect(() => {
    if (!user) return

    // there's no "is this place bookmarked" endpoint, so we fetch the user's full
    // bookmark list and find the match client-side; `id` is a route param (string),
    // hence Number(id) to compare against the numeric place_id from the API
    api
      .get('/api/bookmarks')
      .then((bookmarks) => {
        const match = bookmarks.find((b) => b.place_id === Number(id))
        setBookmark(match || null)
      })
      .catch(() => {})
  }, [id, user])

  async function handleReviewSubmit(reviewData) {
    await api.post(`/api/places/${id}/reviews`, reviewData)
    await loadReviews()
  }

  function handleVisitClick() {
    setMapError('')
    try {
      openGoogleMaps(place.google_maps_link)
    } catch (err) {
      setMapError(err.message)
    }
  }

  async function handleBookmarkToggle() {
    if (bookmark) {
      await api.delete(`/api/bookmarks/${bookmark.id}`)
      setBookmark(null)
    } else {
      const created = await api.post('/api/bookmarks', { place_id: Number(id) })
      setBookmark(created)
    }
  }

  async function handleVisitPlanSubmit(event) {
    event.preventDefault()
    setVisitMessage('')

    try {
      await api.post('/api/visit-plans', { place_id: Number(id), notes: visitNotes })
      setVisitMessage('Visit plan saved!')
      setVisitNotes('')
    } catch (err) {
      setVisitMessage(err.message)
    }
  }

  if (loading) return <p className="loading-state">Loading...</p>
  if (error) return <p className="error">{error}</p>
  if (!place) return null

  const CategoryIcon = getCategoryIcon(place.category?.icon)
  const catStyle = getCategoryStyle(place.category)

  return (
    <div className="place-detail">
      <PlaceImage place={place} className="place-detail-hero" iconSize={56} />

      <div className="place-detail-header">
        <div>
          {place.category?.name && (
            <span className="category-pill" style={catStyle}>
              {createElement(CategoryIcon, { size: 12, strokeWidth: 2 })}
              {place.category.name}
            </span>
          )}
          <h1 style={{ marginTop: 8 }}>{place.name}</h1>
        </div>
        <span className={`rating ${place.average_rating ? '' : 'unrated'}`}>
          <Star size={15} fill={place.average_rating ? 'currentColor' : 'none'} />
          {place.average_rating ? place.average_rating : 'No ratings yet'}
          <span style={{ color: 'var(--text-faint)', fontWeight: 400 }}>
            ({place.review_count ?? 0})
          </span>
        </span>
      </div>

      {place.description && <p className="description">{place.description}</p>}

      <div className="fact-grid">
        {place.opening_hours && (
          <div className="fact">
            <Clock size={17} />
            <div>
              <span className="fact-label">Opening hours</span>
              <span className="fact-value">{place.opening_hours}</span>
            </div>
          </div>
        )}
        {place.address && (
          <div className="fact">
            <MapPin size={17} />
            <div>
              <span className="fact-label">Location</span>
              <span className="fact-value">{place.address}</span>
            </div>
          </div>
        )}
        {place.phone && (
          <div className="fact">
            <Phone size={17} />
            <div>
              <span className="fact-label">Phone</span>
              <span className="fact-value">{place.phone}</span>
            </div>
          </div>
        )}
      </div>

      <button type="button" onClick={handleVisitClick} className="visit-button btn-primary">
        <Navigation2 size={15} /> Get Directions
      </button>
      {mapError && <p className="error">{mapError}</p>}

      {user && (
        <div className="place-actions">
          <div className="action-row">
            <button type="button" onClick={handleBookmarkToggle} className={bookmark ? '' : 'btn-primary'}>
              <Bookmark size={15} fill={bookmark ? 'currentColor' : 'none'} />
              {bookmark ? 'Remove Bookmark' : 'Bookmark this place'}
            </button>
          </div>

          <form onSubmit={handleVisitPlanSubmit} className="visit-plan-form">
            <input
              type="text"
              placeholder="Notes (optional)"
              value={visitNotes}
              onChange={(e) => setVisitNotes(e.target.value)}
            />
            <button type="submit" className="icon-btn">
              <CalendarPlus size={15} /> Plan a visit
            </button>
          </form>
          {visitMessage && <p className="hint">{visitMessage}</p>}
        </div>
      )}

      <h2>Reviews</h2>
      {user ? <ReviewForm onSubmit={handleReviewSubmit} /> : <p className="hint">Log in to write a review.</p>}
      <ReviewList reviews={reviews} />
    </div>
  )
}

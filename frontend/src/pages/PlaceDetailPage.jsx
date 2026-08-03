import { useState, useEffect, useCallback } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api/client'
import { useAuth } from '../hooks/useAuth'
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

  if (loading) return <p>Loading...</p>
  if (error) return <p className="error">{error}</p>
  if (!place) return null

  return (
    <div className="place-detail">
      <h1>{place.name}</h1>
      <p className="category">{place.category?.name}</p>
      {place.image_url && <img src={place.image_url} alt={place.name} />}
      <p>{place.description}</p>
      <p>{place.address}</p>
      <p>{place.opening_hours}</p>
      {place.google_maps_link && (
        <a href={place.google_maps_link} target="_blank" rel="noreferrer">
          View on Google Maps
        </a>
      )}
      <p>
        {place.average_rating ? `★ ${place.average_rating}` : 'No ratings yet'} ({place.review_count} reviews)
      </p>

      {user && (
        <div className="place-actions">
          <button onClick={handleBookmarkToggle}>
            {bookmark ? 'Remove Bookmark' : 'Bookmark this place'}
          </button>

          <form onSubmit={handleVisitPlanSubmit} className="visit-plan-form">
            <input
              type="text"
              placeholder="Notes (optional)"
              value={visitNotes}
              onChange={(e) => setVisitNotes(e.target.value)}
            />
            <button type="submit">Plan a visit</button>
          </form>
          {visitMessage && <p>{visitMessage}</p>}
        </div>
      )}

      <h2>Reviews</h2>
      {user ? <ReviewForm onSubmit={handleReviewSubmit} /> : <p>Log in to write a review.</p>}
      <ReviewList reviews={reviews} />
    </div>
  )
}

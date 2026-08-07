import { useState } from 'react'
import { Star } from 'lucide-react'

export default function ReviewForm({ onSubmit }) {
  const [rating, setRating] = useState(5)
  const [comment, setComment] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      await onSubmit({ rating: Number(rating), comment })
      setComment('')
      setRating(5)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="review-form">
      {error && <p className="error">{error}</p>}

      <label>
        Rating
        <span className="star-picker">
          {[1, 2, 3, 4, 5].map((value) => (
            <button
              key={value}
              type="button"
              className={value <= rating ? 'filled' : ''}
              onClick={() => setRating(value)}
              aria-label={`${value} star${value === 1 ? '' : 's'}`}
            >
              <Star size={20} fill={value <= rating ? 'currentColor' : 'none'} />
            </button>
          ))}
        </span>
      </label>

      <label>
        Comment
        <textarea value={comment} onChange={(e) => setComment(e.target.value)} rows={3} />
      </label>

      <button type="submit" disabled={submitting} className="btn-primary">
        {submitting ? 'Posting...' : 'Post Review'}
      </button>
    </form>
  )
}

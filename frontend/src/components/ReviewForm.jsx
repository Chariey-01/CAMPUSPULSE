import { useState } from 'react'

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
        <select value={rating} onChange={(e) => setRating(e.target.value)}>
          {[5, 4, 3, 2, 1].map((value) => (
            <option key={value} value={value}>{value} star{value === 1 ? '' : 's'}</option>
          ))}
        </select>
      </label>

      <label>
        Comment
        <textarea value={comment} onChange={(e) => setComment(e.target.value)} rows={3} />
      </label>

      <button type="submit" disabled={submitting}>
        {submitting ? 'Posting...' : 'Post Review'}
      </button>
    </form>
  )
}

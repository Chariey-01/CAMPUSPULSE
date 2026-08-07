import { Star, MessageSquareOff } from 'lucide-react'

export default function ReviewList({ reviews }) {
  if (reviews.length === 0) {
    return (
      <div className="empty-state">
        <MessageSquareOff size={24} strokeWidth={1.5} />
        <p>No reviews yet. Be the first to write one.</p>
      </div>
    )
  }

  return (
    <ul className="review-list">
      {reviews.map((review) => (
        <li key={review.id}>
          <div className="review-head">
            <span className="reviewer">{review.user?.username}</span>
            <span className="review-stars">
              {Array.from({ length: 5 }, (_, i) => (
                <Star key={i} size={13} fill={i < review.rating ? 'currentColor' : 'none'} />
              ))}
            </span>
          </div>
          {review.comment && <p>{review.comment}</p>}
        </li>
      ))}
    </ul>
  )
}

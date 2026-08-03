export default function ReviewList({ reviews }) {
  if (reviews.length === 0) {
    return <p>No reviews yet. Be the first to write one.</p>
  }

  return (
    <ul className="review-list">
      {reviews.map((review) => (
        <li key={review.id}>
          <strong>{review.user?.username}</strong> — {'★'.repeat(review.rating)}
          <p>{review.comment}</p>
        </li>
      ))}
    </ul>
  )
}

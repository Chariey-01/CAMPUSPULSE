import { Link } from 'react-router-dom'

export default function PlaceCard({ place }) {
  return (
    <Link to={`/places/${place.id}`} className="place-card">
      {place.image_url && <img src={place.image_url} alt={place.name} />}
      <h3>{place.name}</h3>
      <p className="category">{place.category?.name}</p>
      <p>{place.description}</p>
      <div className="place-meta">
        <span>{place.average_rating ? `★ ${place.average_rating}` : 'No ratings yet'}</span>
        <span>{place.review_count ?? 0} review{place.review_count === 1 ? '' : 's'}</span>
      </div>
    </Link>
  )
}

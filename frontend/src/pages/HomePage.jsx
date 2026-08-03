import { useState, useEffect } from 'react'
import { api } from '../api/client'
import PlaceCard from '../components/PlaceCard'
import CategoryFilter from '../components/CategoryFilter'
import Pagination from '../components/Pagination'

export default function HomePage() {
  const [places, setPlaces] = useState([])
  const [categories, setCategories] = useState([])
  const [categoryId, setCategoryId] = useState('')
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [pagination, setPagination] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/api/categories').then(setCategories).catch(() => {})
  }, [])

  useEffect(() => {
    setLoading(true)
    setError('')

    const params = new URLSearchParams()
    params.set('page', page)
    if (categoryId) params.set('category_id', categoryId)
    if (search) params.set('search', search)

    api
      .get(`/api/places?${params.toString()}`)
      .then((data) => {
        setPlaces(data.items)
        setPagination(data)
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [page, categoryId, search])

  function handleSearchSubmit(event) {
    event.preventDefault()
    setPage(1)
  }

  return (
    <div className="home-page">
      <h1>Discover places around campus</h1>

      <form onSubmit={handleSearchSubmit} className="search-bar">
        <input
          type="text"
          placeholder="Search places..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      <CategoryFilter
        categories={categories}
        selected={categoryId}
        onChange={(id) => {
          setCategoryId(id)
          setPage(1)
        }}
      />

      {error && <p className="error">{error}</p>}
      {loading && <p>Loading places...</p>}
      {!loading && places.length === 0 && <p>No places found.</p>}

      <div className="place-grid">
        {places.map((place) => (
          <PlaceCard key={place.id} place={place} />
        ))}
      </div>

      {pagination && (
        <Pagination page={pagination.page} totalPages={pagination.total_pages} onPageChange={setPage} />
      )}
    </div>
  )
}

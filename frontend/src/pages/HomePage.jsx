import { useState, useEffect, useCallback } from 'react'
import { Search, MapPinOff } from 'lucide-react'
import { api } from '../api/client'
import { useAuth } from '../hooks/useAuth'
import { getBackgroundPhotoUrl } from '../lib/categoryPhotos'
import PlaceCard from '../components/PlaceCard'
import CategoryFilter from '../components/CategoryFilter'
import CategoryBanner from '../components/CategoryBanner'
import PageBackground from '../components/PageBackground'
import Pagination from '../components/Pagination'

export default function HomePage() {
  const { user } = useAuth()

  const [places, setPlaces] = useState([])
  const [categories, setCategories] = useState([])
  const [categoryId, setCategoryId] = useState('')
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [pagination, setPagination] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // place_id -> bookmark object, so PlaceCard can show bookmarked state and
  // toggle it without a dedicated "is this bookmarked" endpoint.
  const [bookmarksByPlace, setBookmarksByPlace] = useState({})

  useEffect(() => {
    api.get('/api/categories').then(setCategories).catch(() => {})
  }, [])

  useEffect(() => {
    // bookmark toggles are hidden on cards whenever `user` is null (see
    // onToggleBookmark below), so stale entries left here after logout are
    // never surfaced — no reset needed.
    if (!user) return

    api
      .get('/api/bookmarks')
      .then((bookmarks) => {
        setBookmarksByPlace(Object.fromEntries(bookmarks.map((b) => [b.place_id, b])))
      })
      .catch(() => {})
  }, [user])

  // NOTE: `search` is in the dependency list below and is updated on every keystroke,
  // so this effect (and the API request it makes) fires on every keystroke, not just
  // on form submit. handleSearchSubmit below only resets the page back to 1.
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

  const handleToggleBookmark = useCallback(
    async (place) => {
      const existing = bookmarksByPlace[place.id]
      try {
        if (existing) {
          await api.delete(`/api/bookmarks/${existing.id}`)
          setBookmarksByPlace((prev) => {
            const next = { ...prev }
            delete next[place.id]
            return next
          })
        } else {
          const created = await api.post('/api/bookmarks', { place_id: place.id })
          setBookmarksByPlace((prev) => ({ ...prev, [place.id]: created }))
        }
      } catch {
        // bookmarking is a convenience action — a failed toggle just leaves state unchanged
      }
    },
    [bookmarksByPlace]
  )

  function handleSearchSubmit(event) {
    event.preventDefault()
    setPage(1)
  }

  const activeCategory = categories.find((c) => String(c.id) === categoryId)

  return (
    <div className="home-page">
      <PageBackground photoUrl={getBackgroundPhotoUrl(activeCategory, { width: 1600 })} />

      <section className="hero">
        <span className="hero-eyebrow">
          {activeCategory ? activeCategory.name : 'Campus discovery'}
        </span>
        <h1>
          {activeCategory
            ? `Explore ${activeCategory.name} around campus`
            : 'Discover everything around your campus, from one place.'}
        </h1>
        {!activeCategory && (
          <p className="hero-dek">
            Find cafeterias, libraries, gyms, hostels, clinics and more — with real student
            ratings, opening hours, and directions, all in one search.
          </p>
        )}

        <form onSubmit={handleSearchSubmit} className="search-bar">
          <Search size={17} />
          <input
            type="text"
            placeholder="Search for a place, e.g. 'library' or 'gym'..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button type="submit" className="btn-primary btn-sm">Search</button>
        </form>
      </section>

      <div className="content-panel">
        <CategoryFilter
          categories={categories}
          selected={categoryId}
          onChange={(id) => {
            setCategoryId(id)
            setPage(1)
          }}
        />

        <CategoryBanner category={activeCategory} />

        {error && <p className="error">{error}</p>}

        {loading && <p className="loading-state">Loading places...</p>}

        {!loading && places.length === 0 && (
          <div className="empty-state">
            <MapPinOff size={28} strokeWidth={1.5} />
            <p>No places found. Try a different search or category.</p>
          </div>
        )}

        {!loading && places.length > 0 && (
          <>
            <p className="results-meta">
              {pagination?.total ?? places.length} place{(pagination?.total ?? places.length) === 1 ? '' : 's'} found
            </p>
            <div className="place-grid">
              {places.map((place) => (
                <PlaceCard
                  key={place.id}
                  place={place}
                  isBookmarked={Boolean(bookmarksByPlace[place.id])}
                  onToggleBookmark={user ? handleToggleBookmark : undefined}
                />
              ))}
            </div>
          </>
        )}

        {pagination && (
          <Pagination page={pagination.page} totalPages={pagination.total_pages} onPageChange={setPage} />
        )}
      </div>
    </div>
  )
}

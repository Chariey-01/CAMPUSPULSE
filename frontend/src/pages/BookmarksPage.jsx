import { useState, useEffect } from 'react'
import PlaceCard from '../components/PlaceCard'
import { api } from '../api/client'

export default function BookmarksPage() {
  const [bookmarks, setBookmarks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/api/bookmarks')
      .then(setBookmarks)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleRemove(bookmarkId) {
    await api.delete(`/api/bookmarks/${bookmarkId}`)
    setBookmarks((prev) => prev.filter((b) => b.id !== bookmarkId))
  }

  if (loading) return <p>Loading...</p>

  return (
    <div className="bookmarks-page">
      <h1>My Bookmarks</h1>
      {error && <p className="error">{error}</p>}
      {bookmarks.length === 0 && <p>No bookmarks yet.</p>}

      <div className="place-grid">
        {bookmarks.map((bookmark) => (
          <div key={bookmark.id} className="bookmark-item">
            <PlaceCard place={bookmark.place} />
            <button onClick={() => handleRemove(bookmark.id)}>Remove</button>
          </div>
        ))}
      </div>
    </div>
  )
}

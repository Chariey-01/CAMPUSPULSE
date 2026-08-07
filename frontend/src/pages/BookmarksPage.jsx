import { useState, useEffect } from 'react'
import { BookmarkX } from 'lucide-react'
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

  if (loading) return <p className="loading-state">Loading...</p>

  return (
    <div className="bookmarks-page">
      <div className="page-header">
        <h1>My Bookmarks</h1>
        <p>Places you've saved for later.</p>
      </div>
      {error && <p className="error">{error}</p>}
      {bookmarks.length === 0 && (
        <div className="empty-state">
          <BookmarkX size={26} strokeWidth={1.5} />
          <p>No bookmarks yet — save a place from its page to see it here.</p>
        </div>
      )}

      <div className="place-grid">
        {bookmarks.map((bookmark) => (
          <div key={bookmark.id} className="bookmark-item">
            <PlaceCard place={bookmark.place} showBookmark={false} />
            <button type="button" onClick={() => handleRemove(bookmark.id)} className="btn-danger-text btn-sm">
              Remove bookmark
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

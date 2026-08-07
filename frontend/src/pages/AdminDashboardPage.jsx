import { useState, useEffect } from 'react'
import { CheckCircle2, XCircle, Trash2, ShieldCheck, Inbox } from 'lucide-react'
import { api } from '../api/client'

export default function AdminDashboardPage() {
  const [pendingPlaces, setPendingPlaces] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [newCategoryName, setNewCategoryName] = useState('')
  const [newCategoryIcon, setNewCategoryIcon] = useState('')
  const [newCategoryHeroImage, setNewCategoryHeroImage] = useState('')

  function loadPendingPlaces() {
    return api.get('/api/places/pending').then((data) => setPendingPlaces(data.items))
  }

  function loadCategories() {
    return api.get('/api/categories').then(setCategories)
  }

  useEffect(() => {
    setLoading(true)
    Promise.all([loadPendingPlaces(), loadCategories()])
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleApprove(placeId) {
    await api.post(`/api/places/${placeId}/approve`)
    setPendingPlaces((prev) => prev.filter((p) => p.id !== placeId))
  }

  async function handleReject(placeId) {
    await api.post(`/api/places/${placeId}/reject`)
    setPendingPlaces((prev) => prev.filter((p) => p.id !== placeId))
  }

  async function handleCreateCategory(event) {
    event.preventDefault()
    setError('')

    try {
      const created = await api.post('/api/categories', {
        name: newCategoryName,
        icon: newCategoryIcon,
        hero_image: newCategoryHeroImage,
      })
      setCategories((prev) => [...prev, created])
      setNewCategoryName('')
      setNewCategoryIcon('')
      setNewCategoryHeroImage('')
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDeleteCategory(categoryId) {
    if (!window.confirm('Delete this category?')) return

    try {
      await api.delete(`/api/categories/${categoryId}`)
      setCategories((prev) => prev.filter((c) => c.id !== categoryId))
    } catch (err) {
      setError(err.message)
    }
  }

  if (loading) return <p className="loading-state">Loading...</p>

  return (
    <div className="admin-dashboard">
      <div className="page-header">
        <h1><ShieldCheck size={22} style={{ verticalAlign: -3, marginRight: 8, color: 'var(--accent)' }} />Admin Dashboard</h1>
      </div>
      {error && <p className="error">{error}</p>}

      <section>
        <h2>Pending Place Submissions</h2>
        {pendingPlaces.length === 0 && (
          <div className="empty-state">
            <Inbox size={24} strokeWidth={1.5} />
            <p>No pending submissions.</p>
          </div>
        )}
        <ul className="simple-list">
          {pendingPlaces.map((place) => (
            <li key={place.id}>
              <div>
                <strong>{place.name}</strong> — {place.category?.name}
                <p>{place.description}</p>
              </div>
              <button type="button" onClick={() => handleApprove(place.id)} className="icon-btn btn-sm">
                <CheckCircle2 size={14} /> Approve
              </button>
              <button type="button" onClick={() => handleReject(place.id)} className="btn-danger-text icon-btn btn-sm">
                <XCircle size={14} /> Reject
              </button>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Manage Categories</h2>

        <form onSubmit={handleCreateCategory} className="inline-form">
          <input
            type="text"
            placeholder="Category name"
            value={newCategoryName}
            onChange={(e) => setNewCategoryName(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Icon (optional)"
            value={newCategoryIcon}
            onChange={(e) => setNewCategoryIcon(e.target.value)}
          />
          <input
            type="text"
            placeholder="Hero image URL (optional)"
            value={newCategoryHeroImage}
            onChange={(e) => setNewCategoryHeroImage(e.target.value)}
          />
          <button type="submit" className="btn-primary btn-sm">Add Category</button>
        </form>
        <p className="hint" style={{ marginTop: -8, marginBottom: 16 }}>
          Hero image is a URL for now — swapping this for a file upload (Cloudinary, Supabase Storage, etc.)
          later won't require any change here, since the backend only ever stores the resulting URL.
        </p>

        <ul className="simple-list">
          {categories.map((category) => (
            <li key={category.id}>
              {category.hero_image && (
                <img
                  src={category.hero_image}
                  alt=""
                  style={{ width: 44, height: 32, objectFit: 'cover', borderRadius: 6, flex: 'none' }}
                />
              )}
              <span style={{ flex: 1 }}>{category.name}</span>
              <button type="button" onClick={() => handleDeleteCategory(category.id)} className="btn-danger-text icon-btn btn-sm">
                <Trash2 size={14} /> Delete
              </button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}

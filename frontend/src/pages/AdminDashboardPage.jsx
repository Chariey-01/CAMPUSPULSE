import { useState, useEffect } from 'react'
import { api } from '../api/client'

export default function AdminDashboardPage() {
  const [pendingPlaces, setPendingPlaces] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [newCategoryName, setNewCategoryName] = useState('')
  const [newCategoryIcon, setNewCategoryIcon] = useState('')

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
      const created = await api.post('/api/categories', { name: newCategoryName, icon: newCategoryIcon })
      setCategories((prev) => [...prev, created])
      setNewCategoryName('')
      setNewCategoryIcon('')
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

  if (loading) return <p>Loading...</p>

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      {error && <p className="error">{error}</p>}

      <section>
        <h2>Pending Place Submissions</h2>
        {pendingPlaces.length === 0 && <p>No pending submissions.</p>}
        <ul className="simple-list">
          {pendingPlaces.map((place) => (
            <li key={place.id}>
              <div>
                <strong>{place.name}</strong> — {place.category?.name}
                <p>{place.description}</p>
              </div>
              <button onClick={() => handleApprove(place.id)}>Approve</button>
              <button onClick={() => handleReject(place.id)}>Reject</button>
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
          <button type="submit">Add Category</button>
        </form>

        <ul className="simple-list">
          {categories.map((category) => (
            <li key={category.id}>
              {category.name}
              <button onClick={() => handleDeleteCategory(category.id)}>Delete</button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}

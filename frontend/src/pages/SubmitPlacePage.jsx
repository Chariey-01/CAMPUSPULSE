import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'

export default function SubmitPlacePage() {
  const [categories, setCategories] = useState([])
  const [form, setForm] = useState({
    name: '',
    description: '',
    address: '',
    phone: '',
    opening_hours: '',
    image_url: '',
    google_maps_link: '',
    category_id: '',
  })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const navigate = useNavigate()

  useEffect(() => {
    api.get('/api/categories').then(setCategories).catch(() => {})
  }, [])

  function handleChange(field) {
    return (event) => setForm((prev) => ({ ...prev, [field]: event.target.value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      await api.post('/api/places', { ...form, category_id: Number(form.category_id) })
      navigate('/places/mine')
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="submit-place-page">
      <h1>Submit a Place</h1>
      <p>Your submission will be reviewed by an admin before it appears publicly.</p>

      {error && <p className="error">{error}</p>}

      <form onSubmit={handleSubmit}>
        <label>
          Name
          <input type="text" value={form.name} onChange={handleChange('name')} required />
        </label>

        <label>
          Category
          <select value={form.category_id} onChange={handleChange('category_id')} required>
            <option value="">Select a category</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>{category.name}</option>
            ))}
          </select>
        </label>

        <label>
          Description
          <textarea value={form.description} onChange={handleChange('description')} rows={3} />
        </label>

        <label>
          Address
          <input type="text" value={form.address} onChange={handleChange('address')} />
        </label>

        <label>
          Phone
          <input type="text" value={form.phone} onChange={handleChange('phone')} />
        </label>

        <label>
          Opening hours
          <input type="text" value={form.opening_hours} onChange={handleChange('opening_hours')} />
        </label>

        <label>
          Image URL
          <input type="text" value={form.image_url} onChange={handleChange('image_url')} />
        </label>

        <label>
          Google Maps link
          <input type="text" value={form.google_maps_link} onChange={handleChange('google_maps_link')} />
        </label>

        <button type="submit" disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit Place'}
        </button>
      </form>
    </div>
  )
}

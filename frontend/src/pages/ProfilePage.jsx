import { useState } from 'react'
import { Save, Mail, ShieldCheck } from 'lucide-react'
import { api } from '../api/client'
import { useAuth } from '../hooks/useAuth'

export default function ProfilePage() {
  const { user, updateUser } = useAuth()
  const profile = user.profile || {}

  const [bio, setBio] = useState(profile.bio || '')
  const [course, setCourse] = useState(profile.course || '')
  const [yearOfStudy, setYearOfStudy] = useState(profile.year_of_study || '')
  const [phone, setPhone] = useState(profile.phone || '')
  const [avatar, setAvatar] = useState(profile.avatar || '')
  const [message, setMessage] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setMessage('')
    setSubmitting(true)

    try {
      const updated = await api.put('/api/profile', {
        bio,
        course,
        year_of_study: yearOfStudy ? Number(yearOfStudy) : null,
        phone,
        avatar,
      })
      updateUser({ profile: updated })
      setMessage('Profile updated!')
    } catch (err) {
      setMessage(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="profile-page">
      <div className="page-header">
        <h1>{user.username}</h1>
      </div>

      <div className="fact-grid" style={{ marginTop: 0 }}>
        <div className="fact">
          <Mail size={17} />
          <div>
            <span className="fact-label">Email</span>
            <span className="fact-value">{user.email}</span>
          </div>
        </div>
        <div className="fact">
          <ShieldCheck size={17} />
          <div>
            <span className="fact-label">Role</span>
            <span className="fact-value" style={{ textTransform: 'capitalize' }}>{user.role}</span>
          </div>
        </div>
      </div>

      {message && <p className="hint">{message}</p>}

      <form onSubmit={handleSubmit} className="card-form">
        <label>
          Bio
          <textarea value={bio} onChange={(e) => setBio(e.target.value)} rows={3} />
        </label>
        <label>
          Course
          <input type="text" value={course} onChange={(e) => setCourse(e.target.value)} />
        </label>
        <label>
          Year of study
          <input type="number" value={yearOfStudy} onChange={(e) => setYearOfStudy(e.target.value)} min={0} />
        </label>
        <label>
          Phone
          <input type="text" value={phone} onChange={(e) => setPhone(e.target.value)} />
        </label>
        <label>
          Avatar URL
          <input type="text" value={avatar} onChange={(e) => setAvatar(e.target.value)} />
        </label>
        <button type="submit" disabled={submitting} className="btn-primary icon-btn">
          <Save size={15} /> {submitting ? 'Saving...' : 'Save Profile'}
        </button>
      </form>
    </div>
  )
}

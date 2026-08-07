import { createContext, useState, useEffect } from 'react'
import { api } from '../api/client'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')

    if (!token) {
      setLoading(false)
      return
    }

    // re-validate the stored token against the API on every load rather than trusting
    // it blindly - it may have expired or been revoked server-side since it was saved
    api
      .get('/api/auth/me')
      .then((data) => setUser(data))
      .catch(() => {
        localStorage.removeItem('token')
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  async function login(username, password) {
    const data = await api.post('/api/auth/login', { username, password })
    localStorage.setItem('token', data.access_token)
    setUser(data.user)
  }

  async function register(username, email, password) {
    await api.post('/api/auth/register', { username, email, password })
  }

  function logout() {
    localStorage.removeItem('token')
    setUser(null)
  }

  function updateUser(updatedFields) {
    setUser((prev) => ({ ...prev, ...updatedFields }))
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  )
}

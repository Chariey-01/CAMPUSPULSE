import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/')
  }

  return (
    <nav className="navbar">
      <Link to="/" className="brand">CampusPulse</Link>
      <div className="nav-links">
        {user ? (
          <>
            <Link to="/places/new">Submit Place</Link>
            <Link to="/places/mine">My Places</Link>
            <Link to="/bookmarks">Bookmarks</Link>
            <Link to="/visit-plans">Visit Plans</Link>
            {user.role === 'admin' && <Link to="/admin">Admin</Link>}
            <Link to="/profile">{user.username}</Link>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  )
}

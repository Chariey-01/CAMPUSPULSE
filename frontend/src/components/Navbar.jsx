import { useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import {
  Compass,
  Menu,
  X,
  PlusCircle,
  Building2,
  Bookmark,
  CalendarCheck,
  ShieldCheck,
  LogOut,
} from 'lucide-react'
import { useAuth } from '../hooks/useAuth'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)

  function handleLogout() {
    setMenuOpen(false)
    logout()
    navigate('/')
  }

  function linkClass({ isActive }) {
    return isActive ? 'active' : ''
  }

  return (
    <nav className="navbar">
      <NavLink to="/" className="brand" onClick={() => setMenuOpen(false)}>
        <Compass size={20} strokeWidth={2.2} />
        CampusPulse
      </NavLink>

      <button type="button" className="nav-toggle" onClick={() => setMenuOpen((v) => !v)} aria-label="Toggle menu">
        {menuOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
        {user ? (
          <>
            <NavLink to="/places/new" className={linkClass} onClick={() => setMenuOpen(false)}>
              <PlusCircle size={15} style={{ marginRight: 6 }} /> Submit Place
            </NavLink>
            <NavLink to="/places/mine" className={linkClass} onClick={() => setMenuOpen(false)}>
              <Building2 size={15} style={{ marginRight: 6 }} /> My Places
            </NavLink>
            <NavLink to="/bookmarks" className={linkClass} onClick={() => setMenuOpen(false)}>
              <Bookmark size={15} style={{ marginRight: 6 }} /> Bookmarks
            </NavLink>
            <NavLink to="/visit-plans" className={linkClass} onClick={() => setMenuOpen(false)}>
              <CalendarCheck size={15} style={{ marginRight: 6 }} /> Visit Plans
            </NavLink>
            {user.role === 'admin' && (
              <NavLink to="/admin" className={linkClass} onClick={() => setMenuOpen(false)}>
                <ShieldCheck size={15} style={{ marginRight: 6 }} /> Admin
              </NavLink>
            )}
            <NavLink to="/profile" className={`nav-user ${linkClass({ isActive: false })}`} onClick={() => setMenuOpen(false)}>
              {user.username}
            </NavLink>
            <button type="button" onClick={handleLogout} className="icon-btn btn-sm">
              <LogOut size={14} /> Logout
            </button>
          </>
        ) : (
          <>
            <NavLink to="/login" className={linkClass} onClick={() => setMenuOpen(false)}>
              Login
            </NavLink>
            <NavLink to="/register" className="btn-primary btn-sm" onClick={() => setMenuOpen(false)}>
              Register
            </NavLink>
          </>
        )}
      </div>
    </nav>
  )
}

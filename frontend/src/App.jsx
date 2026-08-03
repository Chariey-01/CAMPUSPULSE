import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import HomePage from './pages/HomePage'
import PlaceDetailPage from './pages/PlaceDetailPage'
import SubmitPlacePage from './pages/SubmitPlacePage'
import MyPlacesPage from './pages/MyPlacesPage'
import BookmarksPage from './pages/BookmarksPage'
import VisitPlansPage from './pages/VisitPlansPage'
import ProfilePage from './pages/ProfilePage'
import AdminDashboardPage from './pages/AdminDashboardPage'

function App() {
  return (
    <>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/places/:id" element={<PlaceDetailPage />} />
          <Route
            path="/places/new"
            element={
              <ProtectedRoute>
                <SubmitPlacePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/places/mine"
            element={
              <ProtectedRoute>
                <MyPlacesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/bookmarks"
            element={
              <ProtectedRoute>
                <BookmarksPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/visit-plans"
            element={
              <ProtectedRoute>
                <VisitPlansPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <ProtectedRoute adminOnly>
                <AdminDashboardPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
    </>
  )
}

export default App

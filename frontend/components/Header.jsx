import { Link, useNavigate } from 'react-router-dom'
import { useUser, useClerk } from '@clerk/clerk-react'

export default function Header() {

  const { isLoaded, isSignedIn, user } = useUser()
  const clerk = useClerk()
  const navigate = useNavigate()

  const displayName =
    user?.firstName ||
    user?.fullName ||
    user?.primaryEmailAddress?.emailAddress ||
    user?.emailAddresses?.[0]?.emailAddress ||
    'User'

  const handleSignOut = async () => {
    try {
      await clerk.signOut()
      navigate('/', { replace: true })
    } catch (err) {
      console.error('Sign out failed', err)
    }
  }

    return(
    <header className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
      
      {/* Logo */}
      <a href="#" className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 transition-colors">
        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-sm">UQ</span>
        </div>
        <span className="text-xl font-semibold">UniQuest</span>
      </a>

      {/* Navigation */}
       {isLoaded && isSignedIn ? (
            <nav className="hidden md:flex items-center space-x-6">
              <Link to="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors">
                Dashboard
              </Link>
              <a href="#universities" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors">
                Universities
              </a>
              <a href="#scholarships" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors">
                Scholarships
              </a>
              <a href="#ai-assistant" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors">
                AI Assistant
              </a>
            </nav>
          ) : (
            <div className="hidden md:flex items-center space-x-6" aria-hidden>
              {/* empty placeholder to keep layout consistent when logged out */}
            </div>
          )}

      {/* Auth menu */}
          <div className="hidden md:flex items-center space-x-4">
            {isLoaded && isSignedIn ? (
              <>
                <span className="text-sm text-gray-700">Hello, {displayName}</span>
                <button
                  onClick={handleSignOut}
                  className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-sm text-gray-700 hover:text-blue-600 transition-colors">
                  Login
                </Link>
                <Link to="/register" className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
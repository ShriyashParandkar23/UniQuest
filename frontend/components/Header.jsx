import { Link } from 'react-router-dom';

export default function Header() {
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
      <nav className="hidden md:flex items-center space-x-6">
        <a href="#dashboard" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors">
          Dashboard
        </a>
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

      {/* User menu (Logged in version) */}
      {/*<div className="hidden md:flex items-center space-x-4">
        <span className="text-sm text-gray-700">
          Hello, Sarah
        </span>
        <a href="#logout" className="text-sm text-gray-500 hover:text-gray-700 transition-colors">
          Logout
        </a>
      </div>*/}

      {/* Guest menu (Uncomment this block and comment the above to simulate logged-out view) */}
      {
      <div className="hidden md:flex items-center space-x-4">
        <Link to="/login" className="text-sm text-gray-700 hover:text-blue-600 transition-colors">
          Login
        </Link>
        <Link to="/register" className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
          Sign Up
        </Link>
      </div>
      }
    </div>
  </div>
</header>
    );
}
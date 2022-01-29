import { FiHeart, FiVideo } from 'react-icons/fi'
import { Link } from 'react-router-dom'
import { useLocation } from 'react-router'

const Menu = () => {
  const location = useLocation()

  return (
    <div
      className="fixed bottom-0 left-0 right-0 h-20 flex justify-evenly items-center z-50 bg-white"
      style={{ boxShadow: '0 25px 50px 12px rgba(0, 0, 0, 0.4)' }}
    >
      <Link
        className={`flex flex-col items-center ${
          location.pathname === '/recommendations/discover'
            ? 'text-red-600'
            : 'text-gray-500 hover:text-gray-700 transition-all'
        }`}
        to="discover"
      >
        <FiVideo size="2rem" />
        <p>Discover</p>
      </Link>
      <Link
        className={`flex flex-col items-center ${
          location.pathname === '/recommendations/liked'
            ? 'text-red-600'
            : 'text-gray-500 hover:text-gray-700 transition-all'
        }`}
        to="liked"
      >
        <FiHeart size="2rem" />
        <p>Liked</p>
      </Link>
    </div>
  )
}

export default Menu

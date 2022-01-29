import { FiUser } from 'react-icons/fi'
import { Link } from 'react-router-dom'
import logo from './../logo.png'
import uiState from '../state/UI'

const Header = ({ title }) => {
  return (
    <div
      className="fixed flex justify-between items-center w-full px-5 md:px-12 py-4 bg-gradient-to-b from-white z-50"
      style={{ backdropFilter: 'blur(8px)', WebkitBackdropFilter: 'blur(8px)' }}
    >
      <Link to="/">
        <img src={logo} alt="logo" className="w-10" />
      </Link>
      <h1 className="font-extrabold text-3xl self-end">{title}</h1>
      <div className="flex justify-end w-10">
        <FiUser
          className="cursor-pointer hover:text-blue-800"
          size="2rem"
          onClick={() => uiState.setShowLogin(true)}
        />
      </div>
    </div>
  )
}

export default Header

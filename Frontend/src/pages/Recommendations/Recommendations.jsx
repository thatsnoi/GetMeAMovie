import { observer } from 'mobx-react-lite'
import Menu from './pages/components/Menu'
import { Routes, Route } from 'react-router'
import Discover from './pages/Discover/Discover'
import Liked from './pages/Liked/Liked'
import Popup from '../../components/Popup'
import { FiInfo } from 'react-icons/fi'
import Button from '../../components/Button'
import { useState, useEffect } from 'react'
import uiState from '../../state/UI'

const Recommendations = observer(() => {
  const [showInstructions, setShowInstructions] = useState(true)

  useEffect(() => {
    if (showInstructions) {
      uiState.setHeight('calc(100vh - 10rem)')
    } else {
      uiState.setHeight('calc(100% - 20rem)')
    }
  }, [showInstructions])

  return (
    <div className="overflow-y-hidden h-full w-full -mt-20 ">
      <Routes>
        <Route path="/discover" element={<Discover />}></Route>
        <Route path="/liked" element={<Liked />} />
      </Routes>
      {showInstructions && (
        <Popup>
          <FiInfo className="text-blue-900" size="3rem" />
          <p className="text-center font-medium mt-2">
            Swipe right if you would like to watch the movie shown and swipe
            left if you don't!{' '}
            <span className="hidden md:block">
              Alternatively, you can use your arrow keys on desktop.
            </span>
            Click on a movie card if you want to see more details.
          </p>
          <Button
            className="bg-blue-800 hover:bg-blue-900 mt-5"
            onClick={() => {
              setShowInstructions(false)
            }}
          >
            Start
          </Button>
        </Popup>
      )}
      <Menu />
    </div>
  )
})

export default Recommendations

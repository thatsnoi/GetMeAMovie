import { Routes, Route, useLocation } from 'react-router'
import Header from './components/Header'
import Filter from './pages/Filter/Filter'
import Recommendations from './pages/Recommendations/Recommendations'
import SelectMovies from './pages/SelectMovies/SelectMovies'
import { useEffect, useState } from 'react'
import uiState from './state/UI'
import { observer } from 'mobx-react-lite'
import Popup from './components/Popup'
import { FiInfo } from 'react-icons/fi'
import Button from './components/Button'

const App = observer(() => {
  const location = useLocation()
  const [title, setTitle] = useState()

  useEffect(() => {
    switch (location.pathname) {
      case '/recommendations/discover':
        setTitle('Discover')
        break
      case '/recommendations/liked':
        setTitle('Liked')
        break
      default:
        setTitle('GetMeAMovie')
    }
  }, [location.pathname])

  return (
    <>
      {/* <Menu /> */}

      <div className="flex flex-col h-full overflow-hidden">
        <Header title={title} />
        <div
          className="flex relative mt-20 justify-start md:justify-center"
          style={{ height: uiState.height }}
        >
          {uiState.showLogin && (
            <Popup>
              <FiInfo className="text-blue-900" size="3rem" />
              <p className="text-center font-medium mt-2">Coming Soon!</p>
              <Button
                className="bg-blue-800 hover:bg-blue-900 mt-5"
                onClick={() => {
                  uiState.setShowLogin(false)
                }}
              >
                OK
              </Button>
            </Popup>
          )}
          <Routes>
            <Route path="/" element={<Filter />} />
            <Route path="/selectmovies" element={<SelectMovies />} />
            <Route path="/recommendations/*" element={<Recommendations />} />
          </Routes>
        </div>
      </div>
    </>
  )
})

export default App

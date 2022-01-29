import { observer } from 'mobx-react-lite'
import Age from './components/Age/Age'
import Genres from './components/Genres/Genres'
import Length from './components/Length/Length'
import Platforms from './components/Platforms/Platforms'
import selectMovies from '../../state/SelectMovies'
import { useNavigate } from 'react-router-dom'
import Button from '../../components/Button'
import { useEffect, useState } from 'react'
import filter from '../../state/Filter'
import Popup from '../../components/Popup'
import { FiAlertCircle } from 'react-icons/fi'

const Filter = observer(() => {
  const navigate = useNavigate()
  const [warning, setWarning] = useState(undefined)

  useEffect(() => {
    selectMovies.clear()
    filter.clear()
  }, [])

  return (
    <div className="flex flex-col space-y-5 justify-start md:justify-between items-start md:items-center w-full mx-0 md:px-8 max-w-none md:max-w-3xl pb-20">
      <div className="space-y-5 block md:flex flex-col items-start md:items-center md:space-y-10 w-full">
        <Genres />
        <Platforms />
        <Length />
        <Age />
      </div>

      <div className="flex w-full items-center justify-center">
        <Button
          onClick={async () => {
            if (filter.genres.length === 0) {
              setWarning('Please select at least 1 genre.')
            } else if (filter.platforms.length === 0) {
              setWarning('Please select at least 1 plaform.')
            } else {
              await selectMovies.getMovies()
              navigate('/selectmovies')
            }
          }}
          className="bg-blue-800 fixed bottom-5 hover:bg-blue-900"
          loading={selectMovies.isLoading}
        >
          Search
        </Button>
      </div>
      {warning && (
        <Popup>
          <FiAlertCircle className="text-red-900" size="3rem" />
          <p className="text-center font-medium mt-2">{warning}</p>
          <Button
            className="bg-blue-800 hover:bg-blue-900 mt-5"
            onClick={() => {
              setWarning(undefined)
            }}
          >
            OK
          </Button>
        </Popup>
      )}
    </div>
  )
})

export default Filter

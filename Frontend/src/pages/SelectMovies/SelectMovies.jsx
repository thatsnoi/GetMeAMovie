import { observer } from 'mobx-react-lite'
//import { useNavigate } from 'react-router'
import selectMovies from '../../state/SelectMovies'
import Movie from './components/Movie'
import { useEffect, useState } from 'react'
import usePageBottom from '../../utils/usePageBottom'
import ReactLoading from 'react-loading'
import Button from '../../components/Button'
import { useNavigate } from 'react-router'
import recommendations from '../../state/Recommendations'
import Popup from '../../components/Popup'
import { FiAlertCircle } from 'react-icons/fi'

const SelectMovies = observer(() => {
  const isPageBottom = usePageBottom()
  const navigate = useNavigate()

  const [warning, setWarning] = useState(undefined)
  useEffect(() => {
    if (
      isPageBottom &&
      selectMovies.page <= selectMovies.maxPages &&
      !selectMovies.isLoading
    ) {
      selectMovies.getMovies()
    }
  }, [isPageBottom])

  return (
    <div className="md:px-8">
      <h1 className="font-extrabold pb-2 text-2xl pl-5">Select Movies</h1>
      <p className="font-medium pb-2 text-md text-gray-600 pl-5 -mt-2">
        Tap once to like and twice to dislike!
      </p>
      <div className="relative p-5 pt-2 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2 lg:gap-5 mb-20">
        {selectMovies.movies.map((movie, index) => (
          <Movie
            id={movie.id}
            imageUrl={movie.thumbnail}
            title={movie.title}
            year={movie.year}
            key={index}
          />
        ))}
        {selectMovies.isLoading && (
          <div className="col-span-full flex justify-center items-center p-4 pb-0">
            <ReactLoading color="black" type="spin" width={30} />
          </div>
        )}
        <div className="fixed bottom-0 pb-5 pt-5 left-0 right-0 flex z-50 items-center justify-center bg-gradient-to-t from-gray-800 bg-opacity-80">
          <Button
            onClick={async () => {
              if (selectMovies.selectedMovies.length < 3) {
                setWarning('Please rate at least 3 movies.')
              } else {
                await recommendations.getInitialMovies(
                  selectMovies.selectedMovies
                )
                navigate('/recommendations/discover')
              }
            }}
            loading={recommendations.isLoading}
            className="bg-blue-600 hover:bg-blue-700"
          >
            Proceed
          </Button>
        </div>
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

export default SelectMovies

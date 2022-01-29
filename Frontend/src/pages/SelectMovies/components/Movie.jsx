import { FiHeart, FiThumbsDown } from 'react-icons/fi'
import { observer } from 'mobx-react-lite'
import selectMovies from '../../../state/SelectMovies'

const Movie = observer(({ title, imageUrl, year, id }) => {
  return (
    <div
      className={`relative cursor-pointer flex p-2 items-end rounded-xl h-64 lg:h-80 border border-gray-300 backdrop-blur-2xl`}
      style={{
        WebkitBackgroundSize: 'cover',
        MozBackgroundSize: 'cover',
        OBackgroundSize: 'cover',
        backgroundSize: 'cover',
        backgroundImage: `url("${imageUrl}")`,
      }}
      onClick={() => selectMovies.toggleMovieRating(id)}
    >
      <div className="flex flex-col w-full" style={{ zIndex: 45 }}>
        <p className="text-gray-300 font-bold text-lg z-30 truncate -mb-2">
          {year}
        </p>
        <p className="text-white font-bold text-xl z-30 truncate">{title}</p>
      </div>
      <div className="absolute bottom-0 left-0 right-0 top-0 flex justify-center items-center">
        {selectMovies.findMovieRating(id) ? (
          <FiHeart className="text-red-200 text-5xl" style={{ zIndex: 45 }} />
        ) : selectMovies.findMovieRating(id) === 0 ? (
          <FiThumbsDown
            className="text-gray-200 text-5xl"
            style={{ zIndex: 45 }}
          />
        ) : null}
      </div>
      <div className="absolute bottom-0 left-0 right-0 h-44 bg-gradient-to-t from-gray-800 rounded-b-xl z-40"></div>
      <div
        className={`absolute z-30 top-0 left-0 right-0 bottom-0 rounded-xl opacity-70 ${
          selectMovies.findMovieRating(id)
            ? 'bg-red-800'
            : selectMovies.findMovieRating(id) === 0
            ? 'bg-gray-800'
            : ''
        }`}
      ></div>
    </div>
  )
})

export default Movie

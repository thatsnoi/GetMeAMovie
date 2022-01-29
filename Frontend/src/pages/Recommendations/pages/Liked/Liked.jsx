import { observer } from 'mobx-react-lite'
import Pill from './components/Pill'
import recommendations from '../../../../state/Recommendations'
import { timeConvert } from '../../../../utils/utils'
import { FiTrash2, FiTv } from 'react-icons/fi'
import { useEffect } from 'react'

const Liked = observer(() => {
  useEffect(() => {
    recommendations.setShowMovieDetails(undefined)
    recommendations.showContent = false
  })

  return (
    <div className="flex flex-col h-full overflow-y-scroll mt-20 pl-1 pr-4 md:px-8 lg:px-16 xl:px-32 pb-32 space-y-5">
      {recommendations.likedMovies.map((movie, index) => {
        return (
          <div
            className="flex items-center justify-between lg:justify-center space-x-4 lg:space-x-8"
            key={index}
          >
            <div
              className={`relative hidden cursor-pointer lg:flex p-2 items-end rounded-full h-20 w-20 border shadow-2xl`}
              style={{
                WebkitBackgroundSize: 'cover',
                MozBackgroundSize: 'cover',
                OBackgroundSize: 'cover',
                backgroundSize: 'cover',
                backgroundImage: `url("${movie.thumbnail}")`,
              }}
            ></div>
            <div className="flex flex-col justify-start w-64 sm:w-96 lg:w-96">
              <div className="flex items-baseline space-x-2">
                <h2 className="font-bold text-xl truncate">
                  {movie.title + ' '}
                </h2>
                <p className="font-bold text-lg text-gray-600">{movie.year}</p>
              </div>

              <div className="flex pt-1 overflow-scroll flex-wrap lg:w-96">
                {
                  movie.genres.map((genre, i) => {
                    return <Pill key={i}>{genre}</Pill>
                  })[0]
                }
                <Pill>{movie.averageUserScore}</Pill>
                <Pill>{timeConvert(movie.duration)}</Pill>
              </div>
            </div>
            <div className="flex space-x-2 pt-2">
              <FiTv className="text-blue-700 cursor-pointer" size="1.5rem" />
              <FiTrash2
                className="text-red-700 cursor-pointer"
                size="1.5rem"
                onClick={() => recommendations.removeLikedMovie(movie.id)}
              />
            </div>
          </div>
        )
      })}
    </div>
  )
})
export default Liked

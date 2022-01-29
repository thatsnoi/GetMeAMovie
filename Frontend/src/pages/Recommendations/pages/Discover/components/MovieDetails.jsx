import { observer } from 'mobx-react-lite'
import ReactPlayer from 'react-player'
import recommendations from '../../../../../state/Recommendations'
import netflixLogo from './../logos/Netflix.png'
import primevideoLogo from './../logos/primevideo.png'

const MovieDetails = observer(() => {
  const movie = recommendations.getMovie(recommendations.showMovieDetails)

  return (
    <>
      {movie && recommendations.showContent && (
        <div
          className={
            'pt-32 px-5 md:px-8 lg:px-16 xl:px-20 w-full overflow-y-scroll space-y-4 lg:space-y-6 pb-40 sm:pb-20'
          }
          style={{ height: 'calc(100vh-5rem)' }}
        >
          <div className="flex flex-col space-y-2">
            <h3 className="font-extrabold text-2xl">About</h3>
            <p className="font-medium text-md text-gray-600  -mt-2">
              {movie.description}
            </p>
          </div>

          <div className="flex flex-col space-y-2">
            <h3 className="font-extrabold text-2xl">Trailer</h3>
            <div className="w-full" style={{ maxWidth: '500px' }}>
              <div className="w-full relative" style={{ paddingTop: '56.25%' }}>
                <ReactPlayer
                  url={movie.trailer}
                  width="100%"
                  height="100%"
                  className="absolute top-0 left-0"
                />
              </div>
            </div>
          </div>

          <div className="flex flex-col space-y-2">
            <h3 className="font-extrabold text-2xl">Actors</h3>
            <div className="flex flex-col space-y-2">
              {movie.cast.map((actor) => {
                return (
                  <div className="flex space-x-2 items-center">
                    <div
                      className={`relative cursor-pointer lg:flex p-2 items-end rounded-full h-20 w-20 border shadow-2xl`}
                      style={{
                        WebkitBackgroundSize: 'cover',
                        MozBackgroundSize: 'cover',
                        OBackgroundSize: 'cover',
                        backgroundSize: 'cover',
                        backgroundImage: `url("${actor.image}")`,
                      }}
                    ></div>
                    <div>
                      <p className="font-bold text-xl ">{actor.name}</p>
                      <p className="font-medium text-gray-700 text-xl ">
                        <span className="font-normal">as</span>
                        {' ' + actor.role}
                      </p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          <div className="flex flex-col space-y-2">
            <h3 className="font-extrabold text-2xl">Director</h3>
            <p className="font-medium text-gray-700 text-xl ">
              {movie.director}
            </p>
          </div>

          <div className="flex flex-col space-y-2">
            <h3 className="font-extrabold text-2xl">Watch On</h3>
            <div className="flex space-x-4">
              {movie.platforms?.map((platform) => {
                let logo
                switch (platform) {
                  case 'NETFLIX':
                    logo = netflixLogo
                    break
                  case 'PRIME':
                    logo = primevideoLogo
                    break
                  default:
                    break
                }
                if (!logo) return null
                return (
                  <img
                    src={logo}
                    alt="Netflix"
                    className="p-1"
                    style={{ objectFit: 'contain', height: '2rem' }}
                  />
                )
              })}
            </div>
          </div>
        </div>
      )}
    </>
  )
})

export default MovieDetails

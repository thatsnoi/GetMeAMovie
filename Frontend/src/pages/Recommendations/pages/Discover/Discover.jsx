import { observer } from 'mobx-react-lite'
import recommendations from '../../../../state/Recommendations'
import End from './components/End'
import MovieDetails from './components/MovieDetails'
import { Stack } from './components/Stack'

const Discover = observer(() => {
  return (
    <>
      <Stack
        onVote={(movie, vote) => {
          recommendations.showContent = false
          recommendations.setShowMovieDetails(undefined)
          if (vote) {
            recommendations.addLikedMovie(movie)
          }
        }}
      />
      <MovieDetails />
      <End />
    </>
  )
})

export default Discover

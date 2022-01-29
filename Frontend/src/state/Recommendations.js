import { makeAutoObservable } from 'mobx'
import { makePersistable } from 'mobx-persist-store'
import axios from 'axios'
import filter from './Filter'
import getCountryCode from '../utils/getCountryCode'

class Recommendations {
  movieStack = []
  likedMovies = []
  isLoading = false
  showMovieDetails = undefined
  showContent = false

  constructor() {
    makeAutoObservable(this)
    makePersistable(this, {
      name: 'RecommendationsStore',
      properties: ['movieStack', 'likedMovies'],
      storage: window.localStorage,
    })
  }

  async setShowMovieDetails(id) {
    this.showMovieDetails = id
  }

  async toggleShowContent() {
    this.showContent = !this.showContent
  }

  async getInitialMovies(selectedMovies) {
    try {
      this.isLoading = true
      const payload = {
        selectedMovies: selectedMovies.map((movie) => {
          return {
            movieId: movie.id,
            valoration: movie.preferenceDegree === 5 ? 1 : -1,
          }
        }),
        filter: {
          genres: filter.genres.map((x) => x.toUpperCase()),
          minLength: filter.length.min,
          maxLength: filter.length.max,
          platforms: filter.platforms.map((x) => x.toUpperCase()),
          region: await getCountryCode(),
          minAge: filter.age.min,
          maxAge: filter.age.max,
        },
      }
      const response = await axios.post(
        'https://getmeamovie-api-staging.herokuapp.com/recommendations',
        payload
      )
      this.movieStack = response.data.map((movie) => {
        return {
          ...movie,
          id: movie.movieId,
        }
      })
      this.likedMovies = []
      this.isLoading = false
      return this.movies
    } catch (error) {
      alert('An error has occured')
      throw new Error(error)
    }
  }

  getMovie(id) {
    return this.movieStack.find((x) => x.id === id)
  }

  pop() {
    return this.movieStack.pop()
  }

  addLikedMovie(movie) {
    this.likedMovies.push(movie)
  }

  removeLikedMovie(id) {
    this.likedMovies = this.likedMovies.filter((movie) => movie.id !== id)
  }
}

const recommendations = new Recommendations()
export default recommendations

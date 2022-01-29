import axios from 'axios'
import { makeAutoObservable } from 'mobx'
import filter from './Filter'
import { makePersistable } from 'mobx-persist-store'
import getCountryCode from '../utils/getCountryCode'

class SelectMovies {
  movies = []
  page = 1
  maxPages = 2
  isLoading = false
  selectedMovies = []

  constructor() {
    makeAutoObservable(this)
    makePersistable(this, {
      name: 'SelectMoviesStore',
      properties: ['movies', 'selectedMovies', 'page', 'maxPages'],
      storage: window.localStorage,
    })
  }

  toggleMovieRating(id) {
    const index = this.selectedMovies.findIndex((movie) => movie.id === id)
    const movie = this.selectedMovies[index]
    if (movie) {
      if (movie.preferenceDegree === 0) {
        this.selectedMovies.splice(index, 1)
      } else {
        this.selectedMovies[index] = {
          id: id,
          preferenceDegree: movie.preferenceDegree === 5 ? 0 : 5,
        }
      }
    } else {
      this.selectedMovies.push({
        id: id,
        preferenceDegree: 5,
      })
    }
  }

  findMovieRating(id) {
    return this.selectedMovies.find((movie) => movie.id === id)
      ?.preferenceDegree
  }

  async getMovies() {
    try {
      if (this.page > this.maxPages) {
        return this.movies
      }
      this.isLoading = true
      const response = await axios.post(
        'https://getmeamovie-api-staging.herokuapp.com/movies',
        {
          filter: {
            genres: filter.genres.map((x) => x.toUpperCase()),
            minLength: filter.length.min,
            maxLength: filter.length.max,
            platforms: filter.platforms.map((x) => x.toUpperCase()),
            minAge: filter.age.min,
            maxAge: filter.age.max,
            region: await getCountryCode(),
          },
          page: this.page,
        }
      )
      this.movies = [
        ...this.movies,
        ...response.data.filteredMovies.map((movie) => {
          return {
            ...movie,
            id: movie.movieId,
          }
        }),
      ]

      this.maxPages = response.data.maxPages
      this.page++
      this.isLoading = false
      return this.movies
    } catch (error) {
      alert('An error has occured')
      throw new Error(error)
    }
  }

  async clear() {
    this.movies = []
    this.page = 1
    this.maxPages = 2
    this.isLoading = false
    this.selectedMovies = []
  }
}

const selectMovies = new SelectMovies()
export default selectMovies

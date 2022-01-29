import { makeAutoObservable } from 'mobx'
import { makePersistable } from 'mobx-persist-store'

class Filter {
  genres = []
  platforms = []
  length = {
    min: 0,
    max: 200,
  }
  age = {
    min: 0,
    max: 18,
  }

  constructor() {
    makeAutoObservable(this)
    makePersistable(this, {
      name: 'FilterStore',
      properties: ['genres', 'platforms', 'length', 'age'],
      storage: window.localStorage,
    })
  }

  toggleGenre(genre) {
    const _genre = this.genres.find((g) => g === genre)
    if (_genre) {
      this.genres = this.genres.filter((g) => g !== genre)
    } else {
      this.genres = [...this.genres, genre]
    }
    return this.genres
  }

  togglePlatform(platform) {
    const _platform = this.platforms.find((p) => p === platform)
    if (_platform) {
      this.platforms = this.platforms.filter((p) => p !== platform)
    } else {
      this.platforms = [...this.platforms, platform]
    }
    return this.platforms
  }

  setLength(length) {
    this.length = length;

    return this.length
  }

  setAge(age) {
    this.age = age;

    return this.age;
  }

  clear() {
    this.genres = []
    this.platforms = []
    this.length = {
      min: 0,
      max: 200,
    }
    this.age = {
      min: 0,
      max: 18,
    }
  } 
}

const filter = new Filter()
export default filter
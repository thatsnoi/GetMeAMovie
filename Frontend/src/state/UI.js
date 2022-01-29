import { makeAutoObservable } from 'mobx'

class UI {
  height = 'calc(100% - 20rem)'
  showLogin = false

  constructor() {
    makeAutoObservable(this)
  }

  setHeight(height) {
    this.height = height
  }

  setShowLogin(state) {
    this.showLogin = state
  }
}

const uiState = new UI()
export default uiState

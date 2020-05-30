import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    inputData: null
  },
  getters: {
    getUserInputData(state) {
      return state.inputData;
    }
  },
  mutations: {
    changeUserInputData(state, payload) {
      state.inputData = payload.data
    }
  },
  actions: {
  },
  modules: {
  }
})

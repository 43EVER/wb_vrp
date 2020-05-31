import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    inputData: null,
    solverData: {
      routes: []
    },
  },
  getters: {
    getUserInputData(state) {
      return state.inputData;
    },

    getSolverOutputData(state) {
      return state.solverData ? state.solverData : {
        routes: []
      };
    }
  },
  mutations: {
    changeUserInputData(state, payload) {
      state.inputData = payload.data
    },

    changeSolverOutputData(state, payload) {
      state.solverData = payload.data
    }
  },
  actions: {
  },
  modules: {
  }
})

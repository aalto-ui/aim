import Vue from 'vue'
import Vuex from 'vuex'
import _ from 'lodash'

import metricConfig from '../config/metrics.json'

Vue.use(Vuex)

const initialState = () => {
  return {
    results: {},
    preview: '',
    fetching: {},
    fetchingCount: 0,
    fetchedCount: 0,
    validationError: false,
    generalError: false,
    display: {
      input: true,
      metrics: false,
      progressBar: false,
      summary: false,
      preview: false,
      results: false
    }
  }
}

const getters = {
  resultsFormatted (state) {
    const results = {}
    const metrics = metricConfig.metrics
    for (const key in state.results) {
      if (state.results.hasOwnProperty(key)) {
        const metricResults = []
        state.results[key].forEach((result, index) => {
          if (metrics[key].results[index].type === 'float') {
            result = parseFloat(result).toFixed(2)
          }
          metricResults.push({
            id: metrics[key].results[index].id,
            result: {
              name: metrics[key].results[index].name,
              description: metrics[key].results[index].description
            },
            value: result,
            _show_details: false
          })
        })
        results[key] = metricResults
      }
    }
    return results
  },
  fetchingMetrics (state) {
    // console.dir(_.keys(state.fetching))
    return _.keys(state.fetching)
  },
  progress (state) {
    let currentProgress = state.fetchedCount + 1
    if (state.preview !== '') {
      currentProgress++
    }
    return currentProgress
  },
  maxProgress (state) {
    return state.fetchingCount + 2
  }
}

const actions = {
  pushResult (context, data) {
    context.commit('pushResult', {
      metric: data.metric,
      result: data.result
    })
    context.commit('increaseFetchedCount')
    context.commit('updateProgressBarVisibility')
    context.commit('updateSummary')
  },
  pushPreview (context, data) {
    context.commit('pushPreview', data.preview)
    context.commit('updateProgressBarVisibility')
  },
  pushValidationError (context, data) {
    console.error(data.message)
    context.commit('pushValidationError')
  },
  pushGeneralError (context, data) {
    console.error(data.message)
    context.commit('pushGeneralError')
  }
}

const mutations = {
  SOCKET_ONOPEN (state, event) {
    // console.log('Socket connected')
  },
  SOCKET_ONCLOSE (state, event) {
    // console.log('Socket closed')
  },
  SOCKET_ONERROR (state, event) {
    // console.error(event)
  },
  SOCKET_ONMESSAGE (state, message) {
    // console.log(message)
  },
  SOCKET_RECONNECT (state, count) {
    // console.info('Reconnecting, attempt ' + count)
  },
  SOCKET_RECONNECT_ERROR (state) {
    // console.error('Reconnection error')
    this.commit('resetState')
    state.display.input = false
    state.generalError = true
  },
  pushResult (state, payload) {
    Vue.set(state.display, 'results', true)
    const result = {}
    result[payload.metric] = payload.result
    state.results = _.merge({}, state.results, result)
    let newFetching = _.omit(state.fetching, payload.metric)
    state.fetching = newFetching
  },
  increaseFetchedCount (state) {
    state.fetchedCount++
  },
  updateSummary (state) {
    // console.log(state.fetchedCount)
    // console.log(state.fetchingCount)
    document.getElementById('service_title').scrollIntoView()
    if (state.fetchedCount === state.fetchingCount) {
      // console.log('finish loading :)')
    }
  },
  updateProgressBarVisibility (state) {
    if (state.fetchedCount === state.fetchingCount) {
      state.display = {
        input: state.display.input,
        // results: state.display.results,
        metrics: false,
        summary: true,
        results: true,
        preview: state.display.preview,
        progressBar: false
      }
    }
  },
  pushPreview (state, payload) {
    Vue.set(state.display, 'preview', true)
    state.preview = payload
    document.getElementById('service_title').scrollIntoView()
  },
  pushValidationError (state, payload) {
    this.commit('resetState')
    state.validationError = true
  },
  pushGeneralError (state, payload) {
    this.commit('resetState')
    state.display.input = false
    state.generalError = true
  },
  fetchResults (state, metrics) {
    state.fetching = metrics
    // console.log('---- metrics')
    // console.log(metrics)
    state.fetchingCount = _.size(
      _.pickBy(metrics, function (value, key) {
        return value
      })
    )
    state.fetchedCount = 0
    state.display = {
      input: false,
      metrics: false,
      progressBar: true,
      preview: false,
      summary: true,
      results: false
    }
  },
  showMetrics (state) {
    Vue.set(state.display, 'metrics', true)
  },
  hideMetrics (state) {
    Vue.set(state.display, 'metrics', false)
  },
  hideValidationError (state) {
    Vue.set(state, 'validationError', false)
  },
  resetState (state) {
    const reset = initialState()
    for (const key in state) {
      Vue.set(state, key, reset[key])
    }
  }
}

export default new Vuex.Store({
  state: initialState(),
  getters,
  actions,
  mutations
})

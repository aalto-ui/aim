// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'

import store from './store'

import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
library.add(fas)
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false

import 'vue-awesome/icons/check'
import 'vue-awesome/icons/star'
import 'vue-awesome/icons/star-o'
import 'vue-awesome/icons/question-circle'
import 'vue-awesome/icons/file-pdf-o'
import Icon from 'vue-awesome/components/Icon'

Vue.component('icon', Icon)

import VueNativeSock from 'vue-native-websocket'
const sockOptions = {
  reconnection: true,
  reconnectionAttempts: 3,
  format: 'json',
  store
}

Vue.use(VueNativeSock, process.env.WS_URL, sockOptions)

Vue.use(BootstrapVue)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App },
  store
})

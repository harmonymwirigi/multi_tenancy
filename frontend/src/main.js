// // The Vue build version to load with the `import` command
// // (runtime-only or standalone) has been set in webpack.base.conf with an alias.
// import Vue from 'vue'
// import App from './App'
// import router from './router'
// import 'bootstrap'
// import 'bootstrap/dist/css/bootstrap.min.css'
// import axios from 'axios';
// import VueLodash from 'vue-lodash'
// import VueSession from 'vue-session'
// import Vuex from 'vuex'
// import { store } from './store'

// //momentjs
// import moment from 'moment'
// Vue.prototype.$moment = moment

// //guill vue
// import VueQuillEditor from 'vue-quill-editor'
// // require styles
// import 'quill/dist/quill.core.css'
// import 'quill/dist/quill.snow.css'
// import 'quill/dist/quill.bubble.css'

// import './helpers.js'

// Vue.use(Vuex)
// Vue.use(VueLodash, { name: 'lodash' })
// Vue.use(VueSession)
// Vue.use(VueQuillEditor, /* { default global options } */) //component <quill-editor/>

// Vue.config.productionTip = false
// //vuex
// Vue.prototype.$store =  store
// //axios
// Vue.prototype.$http = axios

// //helpers
// Vue.prototype.$humanizeDate = function(date_time){
//   return this.$moment((new Date(date_time))).format("DD/MMM/YY")
// },

// Vue.prototype.$fileDownload = require('js-file-download');

// //DOMAINS
// // var current_host = 'https://admin.methodistkenya.org'
// // var current_host = window.location.hostname //un comment this in production
// var current_host = 'ruaraka.localhost'//for dev env local use only, comment out in production

// Vue.prototype.$host_name = current_host.split('.')[1]

// var name = current_host.split('.')[1]
// var tld = current_host.split('.')[2]
// var api_server = `https://${name}.${tld}` // + ":8000"

// Vue.prototype.$DOMAIN = { value : api_server }
// Vue.prototype.$BASE_URL = { value :localStorage.getItem('base_url_value'),toString:function(){return this.value}}

// /* eslint-disable no-new */
// new Vue({
//   el: '#app',
//   router,
//   components: { App },
//   template: '<App/>'
// })

//updated code

// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
// import Vue from 'vue'
// import App from './App'
// import router from './router'
// import 'bootstrap'
// import 'bootstrap/dist/css/bootstrap.min.css'
// import axios from 'axios';
// import VueLodash from 'vue-lodash'
// import VueSession from 'vue-session'
// import Vuex from 'vuex'
// import { store } from './store'

// //momentjs
// import moment from 'moment'
// Vue.prototype.$moment = moment

// //guill vue
// import VueQuillEditor from 'vue-quill-editor'
// // require styles
// import 'quill/dist/quill.core.css'
// import 'quill/dist/quill.snow.css'
// import 'quill/dist/quill.bubble.css'

// import './helpers.js'

// Vue.use(Vuex)
// Vue.use(VueLodash, { name: 'lodash' })
// Vue.use(VueSession)
// Vue.use(VueQuillEditor, /* { default global options } */) //component <quill-editor/>

// Vue.config.productionTip = false
// //vuex
// Vue.prototype.$store =  store

// // Configure axios for CORS and credentials
// axios.defaults.withCredentials = true
// axios.defaults.headers.common['Content-Type'] = 'application/json'

// //axios
// Vue.prototype.$http = axios

// //helpers
// Vue.prototype.$humanizeDate = function(date_time){
//   return this.$moment((new Date(date_time))).format("DD/MMM/YY")
// },

// Vue.prototype.$fileDownload = require('js-file-download');

// //DOMAINS - Updated for local development
// var current_host = window.location.hostname
// console.log('Current host:', current_host) // Debug log

// // Handle localhost development vs production
// if (current_host === 'localhost' || current_host === '127.0.0.1') {
//   // Local development setup
//   Vue.prototype.$host_name = 'new_church' // Your church/tenant name
//   // var api_server = 'http://ruaraka.localhost:8000' 
//   var api_server = 'http://localhost:8000'// Your backend URL
// } else {
//   // Production setup (your existing logic)
//   Vue.prototype.$host_name = current_host.split('.')[1]
//   var name = current_host.split('.')[1]
//   var tld = current_host.split('.')[2]
//   var api_server = `https://${name}.${tld}` // + ":8000"
// }

// Vue.prototype.$DOMAIN = { value : api_server }
// Vue.prototype.$BASE_URL = { value :localStorage.getItem('base_url_value'),toString:function(){return this.value}}

// console.log('API Server:', api_server) // Debug log

// /* eslint-disable no-new */
// new Vue({
//   el: '#app',
//   router,
//   components: { App },
//   template: '<App/>'
// })


// import Vue from 'vue'
// import App from './App'
// import router from './router'
// import 'bootstrap'
// import 'bootstrap/dist/css/bootstrap.min.css'
// import axios from 'axios'
// import VueLodash from 'vue-lodash'
// import VueSession from 'vue-session'
// import Vuex from 'vuex'
// import { store } from './store'

// // moment.js
// import moment from 'moment'
// Vue.prototype.$moment = moment

// // Quill editor
// import VueQuillEditor from 'vue-quill-editor'
// import 'quill/dist/quill.core.css'
// import 'quill/dist/quill.snow.css'
// import 'quill/dist/quill.bubble.css'

// // Custom helpers
// import './helpers.js'

// Vue.use(Vuex)
// Vue.use(VueLodash, { name: 'lodash' })
// Vue.use(VueSession)
// Vue.use(VueQuillEditor)

// Vue.config.productionTip = false

// // Vuex store access globally
// Vue.prototype.$store = store

// // Axios setup
// axios.defaults.withCredentials = true
// axios.defaults.headers.common['Content-Type'] = 'application/json'
// Vue.prototype.$http = axios

// // Date formatting helper
// Vue.prototype.$humanizeDate = function(date_time) {
//   return this.$moment(new Date(date_time)).format("DD/MMM/YY")
// }

// // File download helper
// Vue.prototype.$fileDownload = require('js-file-download')

// // === DOMAIN HANDLING ===
// let current_host = window.location.hostname

// // Handle development fallback
// if (current_host === 'localhost' || current_host === '127.0.0.1') {
//   current_host = 'ruaraka.localhost' // fallback for dev
// }

// // Split and guard
// const parts = current_host.split('.')
// const name = parts[0] || 'app'
// const tld = parts[1] || 'localhost'

// // Use http for localhost, https otherwise
// const protocol = (tld === 'localhost') ? 'http' : 'https'
// const api_server = `${protocol}://${name}.${tld}${(tld === 'localhost') ? ':8000' : ''}`

// // Host name for tenant subdomain
// Vue.prototype.$host_name = name

// // Set globally accessible domain and base URL
// Vue.prototype.$DOMAIN = { value: api_server }
// Vue.prototype.$BASE_URL = {
//   value: localStorage.getItem('base_url_value'),
//   toString: function () { return this.value }
// }

// // Debug logs
// console.log('API Server:', api_server)
// console.log('Host Name:', Vue.prototype.$host_name)

// // === CREATE APP INSTANCE ===
// new Vue({
//   el: '#app',
//   router,
//   components: { App },
//   template: '<App/>'
// })



//updated code:

import Vue from 'vue'
import App from './App'
import router from './router'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import axios from 'axios'
import VueLodash from 'vue-lodash'
import VueSession from 'vue-session'
import Vuex from 'vuex'
import { store } from './store'

import moment from 'moment'
Vue.prototype.$moment = moment

import VueQuillEditor from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import './helpers.js'

Vue.use(Vuex)
Vue.use(VueLodash, { name: 'lodash' })
Vue.use(VueSession)
Vue.use(VueQuillEditor)

Vue.config.productionTip = false

Vue.prototype.$store = store
Vue.prototype.$http = axios

Vue.prototype.$fileDownload = require('js-file-download')
Vue.prototype.$humanizeDate = function(date_time) {
  return this.$moment(new Date(date_time)).format("DD/MMM/YY")
}

// Environment variables from Webpack
const api_server = process.env.BASE_API
let tenant_name = process.env.DEFAULT_TENANT

const host_parts = window.location.hostname.split('.')
if (process.env.NODE_ENV === 'production' && host_parts.length >= 3) {
  tenant_name = host_parts[0] // Get subdomain like 'ruaraka'
}

Vue.prototype.$host_name = tenant_name
Vue.prototype.$DOMAIN = { value: api_server }
Vue.prototype.$BASE_URL = {
  value: localStorage.getItem('base_url_value'),
  toString() { return this.value }
}

// Debug logs
console.log('Tenant:', tenant_name)
console.log('API:', api_server)

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

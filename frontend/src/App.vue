<template>
  <div >
	<section class="navbar navbar-expand-lg navbar-light sticky-top bg-white" v-if="checkLoggedIn()">
	  <button class="btn btn-light ml-3" type="button" v-on:click="openNav()">
		 <i class="fas fa-bars"></i>
	  </button>
	  <!-- select logo  -->
	  <img class="ml-4 " style="width: 150px ;height: auto" src="@/assets/text_logo.png" alt="logo not found"
			v-if="$host_name == 'my-domain' || $host_name == 'anvilchurch'" >
		<img class="ml-4 " style="width: 200px ;height: auto ;border-radius: 5px"
				src="@/assets/methodist_text_logo.png" alt="logo not found"
				v-if="$host_name == 'methodistkenya' " >
	  <div class="mt-2 col-sm-12 col-lg-8">
		  <generalsearch />
	  </div>
	</section>
	<nav>
	  <div id="anvil-side-nav" class="sidenav shadow-lg bg-white rounded">
		<div class="row">
			<a href="javascript:void(0)" class="closebtn text-secondary" v-on:click="closeNav()">&times;</a>
			<h3 class="ml-4 mr-2 d-flex flex-wrap font-weight-bold" id=church-name-heading> church</h3>
			<h5 class="ml-1 dropdown-item">{{username}}</h5>
			<router-link class="ml-1 dropdown-item"
									:to="{name: 'credentialsReset'}">
									<span  v-on:click="closeNav()">
											<i class="far fa-edit"></i> change credentials
									</span>
			</router-link>
			<a 	href="#"
					class="ml-1 dropdown-item"
					v-on:click="logOut(); closeNav()"
					>
				<i class="fas fa-sign-out-alt"></i>
				log out
			</a>
		</div>
		<hr>
		<!-- members nav on mobile -->
		<router-link class="nav-link" :to="{name: 'memberList'}">
		  <span  v-on:click="doAJAX(); closeNav()">
			  <i class="text-dark far fa-user"></i>
			  members
		  </span>
		</router-link>
		<!-- groups side nav -->
		<router-link class="nav-link" :to="{name: 'groupsLanding'}">
		  <span  v-on:click="doAJAX(); closeNav()">
			<i class="text-dark fas fa-users"></i>
			groups
		  </span>
		</router-link>
		<!-- events side nav -->
		<router-link class="nav-link" :to="{name: 'events'}">
		  <span  v-on:click="doAJAX(); closeNav()">
			<i class="text-dark fas fa-calendar-alt"></i>
		  events
		</span>
		</router-link>
		<!-- finace side nav -->
		<router-link class="nav-link" :to="{name: 'generalFinance'}">
		  <span  v-on:click="doAJAX(); closeNav()">
			<i class="text-dark fas fa-money-bill-alt"></i>
		  finances
		</span>
		</router-link>
		<hr>
		<!-- more side nav -->
		<router-link class="nav-link" :to="{name: 'services'}">
		<span  v-on:click="doAJAX(); closeNav()">
		  <i class="text-dark fas fa-church"></i>
		  services
		</span>
		</router-link>
		<hr>
		<router-link class="nav-link" :to="{name: 'smsAnalytics'}">
		<span  v-on:click="doAJAX(); closeNav()">
			<i class="text-dark fas fa-sms"></i>
			sms outbox
		</span>
		</router-link>
		<router-link class="nav-link" :to="{name: 'news'}">
		<span  v-on:click="doAJAX(); closeNav()">
			<i class="text-dark far fa-newspaper"></i>
		  news & announcements
		</span>
		</router-link>
		<hr>
		<router-link class="nav-link" :to="{name: 'myAccount'}">
		<span  v-on:click="doAJAX(); closeNav()">
		 <i class="text-dark fas fa-cogs"></i>
		  account & website
		</span>
		</router-link>
		<hr>
	  </div>
	</nav>
	<!-- nav frost overlay -->
	<div id="nav-frost-overlay" class="d-none nav-frost-overlay"></div>
	<!-- loader overlay -->
	<div class="vld-parent">
		<loading :active.sync="isLoading"
				:can-cancel="true"
				:on-cancel="onCancel"
				:is-full-page="fullPage">
		</loading>
	</div>
  <!-- the entire app lives here -->
  <section id="main-app" >
	  <router-view />
  </section>
  </div>
</template>

<!-- <script>
import router from "./router";
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
import generalsearch from '@/subcomponents/generalsearch.vue'
export default {
  name: 'App',
  data () {
		return{
		  fullPage: true,
		  client_detail_available :false,
		  church_detail : JSON.parse(localStorage.getItem('church_details')),
		  // DOM
		  anvil_side_nav:null,
		  main_app:null,
		  nav_frost_overlay:null
		}
  },
  components: {
	  Loading,generalsearch
  },
  created(){
	//clear local storage except these
	var church_id = localStorage.getItem('church_id')
	var church_details = localStorage.getItem('church_details')
	var base_url_value = localStorage.getItem('base_url_value')
	var default_message = localStorage.getItem('default_message')

	localStorage.clear()

	if (church_id != 'null'){
		localStorage.setItem('church_id',church_id)
	}
	if(church_details != 'null'){
		localStorage.setItem('church_details',church_details)
	}
	if(base_url_value != 'null'){
		localStorage.setItem('base_url_value',base_url_value)
	}
	if(default_message != 'null'){
		localStorage.setItem('default_message',default_message)
	}

	this.username = this.$session.get("username")
	this.checkLoggedIn()
  },
  // when DOM is ready
  mounted(){
	//show nav menu
	this.anvil_side_nav = document.getElementById("anvil-side-nav")
	this.main_app = document.getElementById("main-app")
	this.nav_frost_overlay = document.getElementById("nav-frost-overlay")

	if (this.church_detail){
	  var church_name_heading = document.getElementById("church-name-heading")
	  church_name_heading.innerHTML = this.church_detail[0].name
	}
  },

  computed: {
	username:{
	  get() {
		return this.$store.getters.logged_in_member
	  },
	  set(value){
		this.$store.commit('logged_in_member', value)
	  }
	},
	isLoading :{
	  get(){
		return this.$store.getters.isLoading
	  },
	  set(value){
		this.$store.commit('isLoading', value)
	  }

	  }
  },
  methods: {
	checkLoggedIn() {
	  if (!this.$session.has("token")) {
		  router.push("/login")
		  return false
	  }
	  this.$store.dispatch('update_logged_in_member', this.$session.get("username"))
	  return true
	},
	logOut() {
	  this.$session.destroy()
	  router.push("/login")
	},
	onCancel() {
	  console.log('User cancelled the loader.')
	},
	doAJAX : function (){
	  this.isLoading = true
	},
	/* Set the width of the side navigation to 250px */
	openNav:function() {
	  this.anvil_side_nav.style.width = "300px"
	  this.main_app.style.marginLeft = "100px"
	  this.nav_frost_overlay.classList.add("bg-frost")
	  this.nav_frost_overlay.classList.remove("d-none")
	},

	/* Set the width of the side navigation to 0 */
	closeNav:function() {
	  this.anvil_side_nav.style.width = "0"
	  this.main_app.style.marginLeft = "0"
	  this.nav_frost_overlay.classList.remove("bg-frost")
	  this.nav_frost_overlay.classList.add("d-none")

	}
  }
}
</script> -->
<script>
import router from "./router";
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
import generalsearch from '@/subcomponents/generalsearch.vue'
export default {
  name: 'App',
  data () {
		return{
		  fullPage: true,
		  client_detail_available :false,
		  church_detail : JSON.parse(localStorage.getItem('church_details')),
		  // DOM
		  anvil_side_nav:null,
		  main_app:null,
		  nav_frost_overlay:null
		}
  },
  components: {
	  Loading,generalsearch
  },
  created(){
	//clear local storage except these
	var church_id = localStorage.getItem('church_id')
	var church_details = localStorage.getItem('church_details')
	var base_url_value = localStorage.getItem('base_url_value')
	var default_message = localStorage.getItem('default_message')

	localStorage.clear()

	if (church_id != 'null'){
		localStorage.setItem('church_id',church_id)
	}
	if(church_details != 'null'){
		localStorage.setItem('church_details',church_details)
	}
	if(base_url_value != 'null'){
		localStorage.setItem('base_url_value',base_url_value)
	}
	if(default_message != 'null'){
		localStorage.setItem('default_message',default_message)
	}

	this.username = this.$session.get("username")
	this.checkLoggedIn()
  },
  // when DOM is ready
  mounted(){
	//show nav menu
	this.anvil_side_nav = document.getElementById("anvil-side-nav")
	this.main_app = document.getElementById("main-app")
	this.nav_frost_overlay = document.getElementById("nav-frost-overlay")

	if (this.church_detail){
	  var church_name_heading = document.getElementById("church-name-heading")
	  church_name_heading.innerHTML = this.church_detail[0].name
	}
  },

  computed: {
	username:{
	  get() {
		return this.$store.getters.logged_in_member
	  },
	  set(value){
		this.$store.commit('logged_in_member', value)
	  }
	},
	isLoading :{
	  get(){
		return this.$store.getters.isLoading
	  },
	  set(value){
		this.$store.commit('isLoading', value)
	  }

	  }
  },
  methods: {
	checkLoggedIn() {
	  if (!this.$session.has("token")) {
		  // Check if we're not already on the login page to avoid redundant navigation
		  if (this.$route.path !== "/login") {
			  this.$router.push("/login").catch(err => {
				  // Ignore navigation duplicated errors
				  if (err.name !== 'NavigationDuplicated') {
					  throw err
				  }
			  })
		  }
		  return false
	  }
	  this.$store.dispatch('update_logged_in_member', this.$session.get("username"))
	  return true
	},
	logOut() {
	  this.$session.destroy()
	  // Use router.replace to avoid adding to history and prevent back button issues
	  this.$router.replace("/login").catch(err => {
		  if (err.name !== 'NavigationDuplicated') {
			  throw err
		  }
	  })
	},
	onCancel() {
	  console.log('User cancelled the loader.')
	},
	doAJAX : function (){
	  this.isLoading = true
	},
	/* Set the width of the side navigation to 250px */
	openNav:function() {
	  this.anvil_side_nav.style.width = "300px"
	  this.main_app.style.marginLeft = "100px"
	  this.nav_frost_overlay.classList.add("bg-frost")
	  this.nav_frost_overlay.classList.remove("d-none")
	},

	/* Set the width of the side navigation to 0 */
	closeNav:function() {
	  this.anvil_side_nav.style.width = "0"
	  this.main_app.style.marginLeft = "0"
	  this.nav_frost_overlay.classList.remove("bg-frost")
	  this.nav_frost_overlay.classList.add("d-none")

	}
  }
}
</script>

<style lang="scss">
/* SCSS only — DO NOT include any JS */
@import "@/assets/styles/church-is.scss";

body {
  background-color: $main-bg-color;
}
</style>






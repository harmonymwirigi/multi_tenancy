<template>
    <div class="groupsLanding">
    <nav aria-label="breadcrumb" class="p-5">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><span class="backButton">
                  <router-link style="text-decoration: none" :to="{name: 'Home'}">
                    Home
                  </router-link></span></li>
                <li class="breadcrumb-item active" aria-current="page">groups</li>
            </ol>
    </nav>
    <section class="p-5">
      <div class="row">
        <div class="col-12 ml-3 mb-3">
            <h3 class="row">
              <b>
                Groups
              </b>
            </h3>
			<div class="d-flex justify-content-between">
				<div class="d-flex">
					<a class="stat-item btn btn-outline-secondary dropdown-toggle"
					   data-toggle="collapse" href="#statsTab" role="button" aria-expanded="false" aria-controls="statsTab">
						stats
					</a>
				</div>
				<div class="btn-group">
					<a class="add-button"
						href="#" data-toggle="modal"
						v-on:click="switchToGroup()"
						data-target="#addModal" style="text-decoration: none">
					  + Add group
					</a>
					<button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split"
							id="dropdownMenuReference" data-toggle="dropdown"
							aria-haspopup="true" aria-expanded="false" data-reference="parent">
						<span class="sr-only">Toggle Dropdown</span>
					</button>
					<div class="dropdown-menu border-success text-capitalize"
						aria-labelledby="dropdownMenuReference"
						style="z-index:99999">
						<router-link class="dropdown-item" style="text-decoration: none" :to="{name: 'randomMessage'}">
						  Text random numbers
						</router-link>
					</div>
				</div>
			</div>
        </div>
        <section class="collapse col-12" id="statsTab" style="max-width: 500px">
            <div class="card card-body">
                <groupstats msg="expenditure stats"/>
            </div>
        </section>
      </div>
      <hr>
    </section>
    <div class="continer">
      <div>
              <div v-if="independent_groups" class="p-5 mt-4 d-flex flex-wrap" >
                  <div class="border rounded mt-3 ml-3" v-for="data in independent_groups.response">
                      <router-link  :to="`/groupDetail/`+ data.id" class="list-group-item list-group-item-action border-0" >
                      <span class="">
                        <div>
                            <i class="fas fa-users"></i>
                            <span class="text-dark">{{data.name}}</span>
							<p>{{data.description}}</p>
                        </div>
                        <span class="text-muted font-weight-bold">
                          {{data.number_of_members}} members
                        </span>
                      </span>
                    </router-link>
                  </div>

        	 </div>
        <section>
          <!-- Modal add group -->
          <div class="modal fade" id="addModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalCenterTitle">add {{group_type}}</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                            <label for="addGroup"> name</label>
                            <input type="text" class="form-control" maxlength="20" v-model="name"></input>
                            <p v-if="name_errors.length">
                                    <ul>
                                            <small><li v-for="error in name_errors"><p class="text-danger">{{ error }}</p></li></small>
                                    </ul>
                            </p>
                    </div>
                    <div class="form-group">
                        <label for="addGroupDescription">description</label>
                        <textarea class="form-control" maxlength="50"
                                  id="addGroupDescription" rows="3" v-model="description"></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success" v-on:click="addGroup()">
                      <b>+</b> add
                      <span v-if="adding_group"
                            class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                      </span>
                    </button>
                </div>
                </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
  </template>

<script>
import router from "../../router";
import groupstats from '@/subcomponents/statistics/groupstats.vue'
export default {
  name: 'groupsLanding',
  components: { groupstats },
  data () {
    return {
      groups: null,independent_groups: null,
      foundItems: null,foundItems_independent: null,
      fetch_data_error: [],
      //add group
      adding_group: false,
      group_type: 'group',
      name: '',name_errors: [],description: '',
      add_group_error: null
    }
  },
  created() {
        this.checkLoggedIn()
        this.fetchData()
    },
  watch: {
        '$route': 'fetchData'
    },
  methods: {
    checkLoggedIn() {
      if (!this.$session.has("token")) {
          router.push("/login")
      }
    },
    scrollToElement: function(element){
      	document.getElementById(element).scrollIntoView();
    },
    fetchData() {
		this.fetch_data_error = []
		this.$store.dispatch('update_isLoading', true)
		// try local storage
		this.groups = JSON.parse(localStorage.getItem('group_list'))
		if (this.groups){
				var array = this.groups.response
				this.foundItems = array.length
				this.$store.dispatch('update_isLoading', false)
		}

		const currentVersion = this.$store.getters.group_list_version
		var version  = localStorage.getItem('group_list_version')

		//else try the network
		if (!version || version <= currentVersion) {
			this.$http.get(this.$BASE_URL + '/api/groups/group-of-church-groups-list')
			.then(response => {
				this.groups = {"response": response.data }
				var array = this.groups.response
				this.foundItems = array.length

				localStorage.setItem('group_list',JSON.stringify({"response": response.data }))
				localStorage.setItem('group_list_version', currentVersion)
				this.$store.dispatch('update_isLoading', false)
			})
			.catch((err) => {
				this.fetch_data_error.push(err)
				this.$store.dispatch('update_isLoading', false)
			})
		}

		// get independent groups
		this.$store.dispatch('update_isLoading', true)
		this.independent_groups = JSON.parse(localStorage.getItem('group_list_independent'))
		if (this.independent_groups){
				var array = this.independent_groups.response
				this.foundItems_independent = array.length
				this.$store.dispatch('update_isLoading', false)
		}

		if (!version || version < currentVersion) {
        this.$http.get(this.$BASE_URL + '/api/groups/church-groups-not-in-group/')
        .then(response => {
            this.independent_groups = {"response": response.data }
            var array = this.independent_groups.response
            this.foundItems_independent = array.length
            localStorage.setItem('group_list_independent',JSON.stringify({"response": response.data }))
            this.$store.dispatch('update_isLoading', false)

        })
        .catch((err) => {
            this.fetch_data_error.push(err)
            this.$store.dispatch('update_isLoading', false)
        })
      }
    },
    switchToFolder: function(){
      	this.group_type = 'folder'
	},
	switchToGroup: function(){
      	this.group_type = 'group'
    },
    addGroup: function(){

        var url = ''
        this.name_errors = [],
        this.description_errors = []

        if (! this.name){
            this.name_errors.push('you must have a name for the group')
        }
        if (! this.description){
            this.description = 'none given'
        }
        if (this.group_type == 'folder'){
          url = '/api/groups/group-of-church-groups-list/'
        }
        if (this.group_type == 'group'){
          url = '/api/groups/add-group/'
        }
        this.isLoading = true
        this.adding_group = true
        this.$http({ method: 'post', url: this.$BASE_URL + url,
        data: {
            group: null,
            name: this.name,
            description: this.description
        }
        }).then(response => {
            this.name = ''
            this.description = ''
            if (this.group_type == 'folder'){
              alert("folder succesfully added")
            }
            if (this.group_type == 'group'){
              this.adding_group = false
			  alert("group succesfully added")
			  //update localstorage
              var new_version = parseInt(localStorage.getItem('group_list_version')) + 1
			  this.$store.dispatch('update_group_list_version', new_version)
			  this.fetchData()
            }
        })
            .catch((err) => {
            this.adding_group=false
            this.group_type = 'group'
            alert("an error occured while trying to add group")
        })
    }

  }
}
</script>


<style >
</style>

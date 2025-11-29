<template>
    <div>           
        <div class="row">
        <div class="col">
        <h3 >
            <img style="width: 30px ;height: auto" src="@/assets/icons/icons8-folder-48.png">
            {{group_name}} / groups
        </h3>        
        <hr/>
        <div class="col-8 center-div" v-if = "fetch_data_error.length > 0 && group_name">
            <div class = "center-div" >
                    <img style = "height: 64px "src="@/assets/icons/icons8-wi-fi-off-64.png">
                    <p class="text-info">check your connection</p>
            </div>
        </div>
        <div v-if = "fetch_data_error.length == 0">
        found <span class="badge badge-pill badge-secondary">{{foundItems}}</span>        
        <p></p>
        <table v-if="groups" class="table">                     
            <tbody>
                <tr v-for = "data in groups.response ">                    
                <td>
                    <router-link class="text-secondary" style="text-decoration: none;"  :to="`/groupDetail/`+ data.id ">
                        <img style="width: 30px ;height: auto" src="@/assets/icons/icons8-user-groups-48.png">                     
                        {{data.name}}
                    </router-link>
                </td>
                <td></td>
                <td></td>
                <td> 
                    <p>                         
                        <span class="badge badge-pill badge-secondary">{{data.number_of_members}}</span>
                    </p>
                </td>
                </tr>             
            </tbody>
        </table>
        </div>
        </div>
        <div class="col-sm-10 col-md-8 col-lg-3 text-right">            
            <button v-if="group_name" class="btn btn-success" data-toggle="modal" data-target="#addGroup">
                <b>+</b> add to {{group_name}}
            </button>           
        </div>
        </div>
        
        <!-- Modal add group -->
        <div class="modal fade" id="addGroup" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
            <div class="modal-header">                
                <h5 class="modal-title text-capitalize" id="exampleModalCenterTitle">add group to {{group_name}} folder</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close" v-on:click="fetchData()">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">                    
                <div class="form-group">
                        <label for="addGroup"> group name</label>
                        <input type="text" class="form-control" maxlength="20" id="addGroup" v-model="name"></input>
                        <p v-if="name_errors.length">
                                <ul>
                                        <small><li v-for="error in name_errors"><p class="text-danger">{{ error }}</p></li></small>
                                </ul>
                        </p>
                </div>
                <div class="form-group">
                    <label for="addGroupDescription">description</label>
                    <textarea class="form-control" id="addGroupDescription" 
                                maxlength="50"  rows="3" v-model="description"></textarea>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal" v-on:click="fetchData()">Close</button>
                <button type="button" class="btn btn-success" v-on:click="addGroup()">
                    <b>+</b> add group
                    <span v-if="adding_group"
                        class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                    </span>
                </button>
            </div>
            </div>
        </div>
        </div>
    </div>
  </template>

<script>
import router from "../../router";
export default {
  name: 'groupList',
  data () {
    return {
        group_name: 'church',
        groups: null,
        foundItems: null,
        fetch_data_error: [],
        name: '',name_errors: [],description: '',
        add_group_error: null,
        adding_group:false
    }
  },
  created() {
        this.checkLoggedIn()
        if (this.$route.params.id){
            this.fetchData()
        }        
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
        fetchData() {            
            this.$store.dispatch('update_isLoading', true)
            this.group_name = this.$route.params.group_name                                
            this.fetch_data_error = []
            this.$http.get(this.$BASE_URL + '/api/groups/church-groups-in-group/' + this.$route.params.id + '/')
            .then(response => {
                this.groups = {"response": response.data } 
                var array = this.groups.response
                this.foundItems = array.length
                this.$store.dispatch('update_isLoading', false)
            })
            .catch((err) => {
                this.fetch_data_error.push(err)
                this.$store.dispatch('update_isLoading', false)
            })
            
        },
        addGroup: function(){
            this.name_errors = [],
            this.description_errors = []

            if (! this.name){
                this.name_errors.push('you must have a name for the group')
            }
            if (! this.description){
                this.description = 'none given'
            }            
            this.adding_group = true
            this.$http({ method: 'post', url: this.$BASE_URL + '/api/groups/add-group/',
            data: {
                group: this.$route.params.id,
                name: this.name,
                description: this.description
            }
            }).then(response => {                 
                this.name = ''
                this.description = ''
                this.adding_group = false
                alert("group succesfully added")
            })
            .catch((err) => {
                this.adding_group = false
                alert("error occured while trying to add group" + err)
            })            
        }
      
    }

}
</script>


<style >
</style>
<template>
    <div >
        <nav aria-label="breadcrumb" class="continer">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li>
                <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'memberList'}">members</router-link></span></li>
                <li class="breadcrumb-item active" aria-current="page">assign roles</li>
            </ol>
          </nav>
          <div class="continer">
            <div class="row">
                <div class="col-12 col-sm-10 col-md-8 col-lg-2">                   
                        <a href="#" v-if="member_found" v-on:click="backToSearch()" role="button" aria-expanded="false">
                            <div class="moreButton">                                
                                <b> back to search</b>
                            </div>
                        </a>
                </div>
                <div class="col">
                    <div class="form-group" v-if="! member_found">
                        <label class=""><b>search member:</b></label>

                        <div class="">                       
                              <input type="text" class=" form-control" placeholder="type to search member" v-model="memberSearch" autofocus>   
                              <div style="padding: 10px 10px 10px 10px" class="text-info" >{{memberSearch_status}}</div> 

                              <div class="pre-scrollable searchedItemsDiv border " style="  max-height: 185px; overflow-y: scroll;" v-if="showMemberInput">
                                <table class="table border-0" >
                                <tbody>
                                    <tr class="searchedItem border-0" v-for="data in found_members.response">
                                    <a href="#" style="text-decoration: none" v-on:click="selectMember(data.member.id,data.member.first_name,data.member.last_name)"> 
                                    <td class="border-0">
                                        
                                            <img v-if = "data.gender == 'M'" style = "height: 32px "src="@/assets/avatars/icons8-user-male-skin-type-4-40.png">
                                            <img v-if = "data.gender == 'F'" style = "height: 32px "src="@/assets/avatars/icons8-user-female-skin-type-4-40.png">
                                            <img v-if = "data.gender == 'R'" style = "height: 32px "src="@/assets/avatars/icons8-contacts-96.png">
                                            
                                        <span class = "text-secondary">{{data.member.first_name}} {{data.member.last_name}}</span>                                                                      
                                        </td>
                                    </a>                                                                                                                                  
                                    </tr>
                                </tbody>
                                </table>
                            </div>                                                    
                        </div>                                                                   
                      </div>
                     

                    <div v-if = "member_found">                                            
                        <div  >                    
                            <div>
                                <h3> {{memberSearch_status}} </h3>
                            </div>                            
                            <div class="row">
                              <div style="padding: 10px">                                                              
                                <div class=" row">   
                                    <div class="alert alert-warning alert-dismissible fade show" role="alert" v-if="assigned_roles.length > 0">                                    
                                        <p v-for="data in assigned_roles">
                                        <strong >role :{{data.role.role}}</strong> {{data.role.description}}
                                        </p>
                                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>                                    
                                    <table class="table">
                                        <thead>
                                            <tr> </tr>
                                            <tr></tr>
                                            <tr></tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <th></th>
                                                <th> role</th>                                                
                                                <th><small> member admin</small></th>
                                                <th><small> group admin</small></th>
                                                <th><small> event admin</small></th>
                                                <th><small> projects admin</small></th>
                                                <th><small> finance admin</small></th>
                                                <th><small> site admin</small></th>
                                            </tr>                                             
                                            <tr v-for="data in roles.response">
                                                <td>
                                                <span v-for="data2 in roles_for_member.response">                                                                                                                                                            
                                                    <span v-if =" data2.role.role == data.role">
                                                        <input multiple class="form-check-input" type="checkbox" :value=data.id v-model="selected_role" disabled >
                                                    </span>
                                                    <span v-else>
                                                        <input multiple class="form-check-input" type="checkbox" :value=data.id v-model="selected_role">
                                                    </span>
                                                </span>
                                                <span v-if = "! member_has_roles"><input multiple class="form-check-input" type="checkbox" :value=data.id v-model="selected_role"> </span>
                                               </td>                                                                                           
                                                <td>{{data.role}}</td>                                                
                                                <td v-if="data.member_admin"><span class="badge badge-pill badge-success"> yes</span> </td>
                                                <td v-else><span class="badge badge-pill badge-danger">no</span></td>
                                                <td v-if="data.member_admin"><span class="badge badge-pill badge-success"> yes</span> </td>
                                                <td v-else><span class="badge badge-pill badge-danger">no</span></td>
                                                <td v-if="data.event_admin"><span class="badge badge-pill badge-success"> yes</span> </td>
                                                <td v-else><span class="badge badge-pill badge-danger">no</span></td>
                                                <td v-if="data.projects_admin"><span class="badge badge-pill badge-success"> yes</span> </td>
                                                <td v-else><span class="badge badge-pill badge-danger">no</span></td>
                                                <td v-if="data.finance_admin"><span class="badge badge-pill badge-success"> yes</span> </td>                                                
                                                <td v-else><span class="badge badge-pill badge-danger">no</span></td>
                                                <td v-if="data.site_admin"><span class="badge badge-pill badge-success"> yes</span> </td>
                                                <td v-else><span class="badge badge-pill badge-danger">no</span></td>
                                            </tr>                                                                               
                                        </tbody>
                                    </table>
                            </div>                                                           
                              </div>                                                        
                            </div>                            
                        </div>
                    </div>          
                    <hr/>          
                    <div style="padding: 0px 0px 25px 0px" v-if = "member_found">
                            <a href="#" v-on:click = "assignRoles()" style="text-decoration: none" aria-disabled="true">
                                <div class="add-button">
                                    {{assign_button_text}}
                                </div>
                            </a>
                    </div>     
                </div>
                <div class="col-12 col-sm-10 col-md-8 col-lg-3">  
                    <div class="btn-group" style="padding: 0px 0px 25px 0px" v-if="member_found">
                        <a href="#" data-toggle="modal" data-target="#addRole" style="text-decoration: none">
                            <div class="add-button">
                                <b>+</b> add role
                            </div>
                        </a>
                        <button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
                            <span class="sr-only">Toggle Dropdown</span>
                        </button>
                        <div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">                                    
                            <a class="dropdown-item" href="#" data-toggle="modal" data-target="#addIncome"><b>+</b> manage roles</a>                                                                
                        </div>
                    </div>                   
                </div>
                <!-- add role Modal -->
                <div class="modal fade" id="addRole" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalCenterTitle">add a role</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                            </div>
                            <div class="modal-body">                                   
                                    <form >
                                            <div class=" row form-group">
                                            <label class="col-3"><b>name:</b></label>
                                            <input type="text" class="col-8 form-control" placeholder="enter name of the role" v-model="role_name">                                        
                                            </div>
                                            <div class="row form-group">
                                                    <label class="col-3"><b>description:</b></label>
                                                    <textarea type="text" class="col-8 form-control" rows='3' v-model="role_description"></textarea>                                                   
                                            </div>  
                                            <hr/>
                                            <div class="form-check form-check-inline">
                                                 <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value=true v-model="member_admin">
                                                 <label class="form-check-label" for="inlineCheckbox1">member admin</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                  <input class="form-check-input" type="checkbox" id="inlineCheckbox2" value=true v-model="site_admin">
                                                  <label class="form-check-label" for="inlineCheckbox2">website admin</label>
                                            </div>  
                                            <div class="form-check form-check-inline">
                                                 <input class="form-check-input" type="checkbox" id="inlineCheckbox2" value=true v-model="group_admin">
                                                  <label class="form-check-label" for="inlineCheckbox2">group admin</label>
                                            </div> 
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value=true v-model="events_admin">
                                                <label class="form-check-label" for="inlineCheckbox1">events admin</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                    <input class="form-check-input" type="checkbox" id="inlineCheckbox2" value=true v-model="projects_admin">
                                                    <label class="form-check-label" for="inlineCheckbox2">projects admin</label>
                                            </div>  
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="checkbox" id="inlineCheckbox2" value=true v-model="finance_admin">
                                                    <label class="form-check-label" for="inlineCheckbox2">finance admin</label>
                                            </div>                                                                                                                                                                  
                                    </form>
                            </div>
                            <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-success" disabled v-if="! enable_role_button"><b>+</b> add role </button>
                            <button type="button" class="btn btn-success" v-if="enable_role_button" v-on:click="addRole()"> {{add_role_button_text}} </button>
                            </div>
                        </div>
                        </div>
                </div>
            </div>
          </div>
    </div>
</template>

<script>

import router from "../../router";

export default {
    name: 'adminRoles',
    data () {
        return{
            //fetching data
            fetch_data_error: [],
            roles: null,            
            roles_for_member: null, 
            //search member  
            member_has_roles: false,         
            memberSearch: '',found_members:[],
            memberSearch_status: '',selectedMember: null,
            showMemberInput: false,
            member_found: false,
            //add role
            role_name: null,
            role_description: null,
            enable_role_button: false,
            add_role_button_text: '+ add role',
            added_role: [],    
            //assign roles 
            selected_role: [],
            assign_button_text: 'assign role(s)',
            member_admin: false,
            site_admin: false,
            group_admin: false,
            event_admin: false,
            projects_admin: false,
            finance_admin: false,
            assigned_roles: []       
        }
    },
    created () {
        this.fetchdata()
        this.debouncedGetAnswer = _.debounce(this.getAnswer, 1000)
    },
    watch: {
    // whenever member search changes, this function will run
    memberSearch: function () {
        if (this.memberSearch.length > 0){
            this.member_has_roles = false
            this.selected_role = []
            this.showMemberInput = true
            this.memberSearch_status = 'typing...'
            this.debouncedGetAnswer()
        }else{
            this.memberSearch_status = ''
            this.found_members = []
            this.showMemberInput = false
            this.fetchData()
            this.enable_role_button = false
        }
    },
    role_name: function (){
        if (this.role_name.length > 0 && this.role_description.length > 0){
            this.enable_role_button = true
        }
    },
    role_description: function (){
        if (this.role_description.length > 0 && this.role_name.length > 0){
            this.enable_role_button = true
        }
    }
    
     },
     methods: {
    //fetch data
        fetchdata () {
            this.fetch_data_error = []
            this.$http.get(this.$BASE_URL +'/api/members/role-list/')
                .then(response => {
                this.roles = {"response": response.data } 
                })
                .catch((err) => {
                    this.fetch_data_error.push(err)
                })                  
            
        },
    //search for member
        get_roles_for_member: function (){            
            this.$http.get(this.$BASE_URL +'/api/members/roles-for-member/'+ this.selectedMember + '/')
                .then(response => {
                this.roles_for_member = {"response": response.data } 
                var count = 0
                for (var data in this.roles_for_member.response){
                    count = count + 1                    
                }
                if (count > 0){
                    this.member_has_roles = true
                }                
                })
                .catch((err) => {                    
                    this.fetch_data_error.push(err)
                })
        },
        backToSearch: function () {
            this.member_found = false
            this.memberSearch = ''
        },
        getAnswer: function () {
          var vm = this
          if (this.memberSearch.length > 0){
            this.found_members = []
            this.memberSearch_status = 'searching...'
            this.$http.get(this.$BASE_URL + '/api/members/filter-by-first_name/' + this.memberSearch +'/')
              .then(function (response) {
                vm.found_members = {"response": response.data } 
                vm.memberSearch_status = ''
              })
              .catch(function (error) {
              })
            }
        },
        selectMember: function(id,first_name,last_name) {
          this.selectedMember = id          
          this.memberSearch_status = ':' + first_name + ' ' + last_name + ''
          this.showMemberInput = false
          this.member_found = true
          this.get_roles_for_member()
        },
    //add role        
        addRole: function() {
            this.enable_role_button = false
            this.add_role_button_text = 'adding role...'            
            this.$http({ method: 'post', url: this.$BASE_URL + '/api/members/role-list/',
                data: {
                  role: this.role_name,
                  description: this.role_description,  
                  member_admin: this.member_admin,
                  site_admin: this.site_admin,
                  group_admin: this.group_admin,
                  event_admin: this.event_admin,
                  projects_admin: this.projects_admin,
                  finance_admin: this.finance_admin               
                }
              }).then(response => {

                this.added_role.push(response.data)                    
                this.role_name = ''
                this.role_description = '' 
                this.add_role_button_text = '+ add role'
                alert("role succesfuly added")
                this.fetchdata()                    
                })
                .catch((err) => {
                    
                })                
        },
        assignRoles: function(){            
            for (var id in this.selected_role){                
            this.assign_button_text = "assigning roles..."
            this.$http({
                method: 'post',
                url: this.$BASE_URL + '/api/members/add-role-for-member/',
                data: {
                   member_id: this.selectedMember,
                   role_id: this.selected_role[id]                  
                }
              }).then(response => {
                    this.assigned_roles.push(response.data)
                    this.assign_button_text = "assign role(s)"
                    this.selected_role = []                    
                    alert("successfully assigned roles")
                    this.fetchdata()
                })
                .catch((err) => {                    
                }) 
            }
        }
    }
}
</script>


<style >
</style>
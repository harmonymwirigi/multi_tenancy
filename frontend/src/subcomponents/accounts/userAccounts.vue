<!-- Child.vue -->
<template>
    <div class="row">   
        <!-- this compnent requires text message modal -->
        <textmessage :memberIds="member_in_focus"/>                        
        <div v-if="admins" class="col-sm-12 col-lg-9">            
            <h3 class="font-weight-bold mb-5 ">user accounts</h3>            
            <table class="table table-responsive-sm table-borderless">
                <thead>
                  <tr>                    
                    <th scope="col">name</th>
                    <th scope="col">role</th>
                    <th scope="col">description</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="admin in admins" class="text-muted">                                        
                    <td>{{admin.member_full_name}}</td>
                    <td>{{admin.role_name}}</td>
                    <td>{{admin.role_description}}</td>
                    <td v-if="access_level == 0">
                            <div class="btn-group">
                                <a href="#" style="text-decoration: none">
                                    <div class="text-success">
                                        actions
                                    </div>
                                </a>
                                <button type="button" class="ml-1 btn btn-light dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
                                        <span class="sr-only">Toggle Dropdown</span>
                                </button>
                                <div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">                                                                
                                    <a class="dropdown-item d-flex flex-column justify-content-center" 
                                        href="#" data-toggle="modal"
                                        data-target="#textModalCenter"
                                        @click="member_in_focus = []; member_in_focus.push(admin.user_id)">
                                        send 'made admin' message 
                                        <small class="text-muted">send message to user to inform them<br/>
                                            that they are now admin in the site
                                        </small>
                                    </a>                                
                                    <a class="dropdown-item d-flex flex-column justify-content-center" 
                                        href="#" data-toggle="modal"
                                        data-target="#textModalCenter"
                                        @click="member_in_focus = []; member_in_focus.push(admin.user_id)">
                                        send password reset message 
                                        <small class="text-muted">send message to user to inform them<br/>
                                             that their password has been reset
                                        </small>
                                    </a>   
                                    <a class="dropdown-item d-flex flex-column justify-content-center" 
                                        href="#" 
                                        data-toggle="modal"
                                        data-target="#resetPasswordModal"
                                        @click="member_in_focus = []; member_in_focus.push(admin.user_id)">
                                        reset user's password
                                        <small class="text-muted">this will reset user password back <br/>
                                                to starter password 'changeMe'<br/>
                                                only use this feature when a user has lost their password
                                        </small>
                                    </a>                                                                                           
                                </div>
                            </div> 
                    </td>
                  </tr>                  
                </tbody>
              </table>
        </div>
        <div class="col-sm-12 col-lg-3">
            <div class="btn-group">
                <a href="#" data-toggle="modal" data-target="#addUserModal" style="text-decoration: none">
                    <div class="add-button">
                        + add user
                    </div>
                </a>
                <button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
                        <span class="sr-only">Toggle Dropdown</span>
                </button>
                <div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">                            
                    <a class="dropdown-item" 
                        href="#" data-toggle="modal"
                        data-target="#addRoleModal">
                        + add role
                    </a> 
                    <a class="dropdown-item" 
                        href="#" data-toggle="modal"
                        data-target="#manageRolesModal">
                        manage roles
                    </a>                                                                
                </div>
            </div>            
        </div>

        <!-- modals -->
        <!-- assign roles to user -->
        <div class="modal fade" id="addUserModal" tabindex="-1" role="dialog" aria-labelledby="addUserModal" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Add User</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="form-group row mb-3">
                        <label class="col-3 font-weight-bold" for="exampleFormControlInput1">member</label>
                        <searchmember class="col-9" v-on:memberSelected="onMemberSelected"/>
                    </div> 
                    <div class="form-group row mb-3">
                        <label class="col-3 font-weight-bold">role</label>
                        <div class="p-3 col-9">
                            <select v-if="roles" class="form-control" v-model="selected_role">
                                    <option v-for="role in roles" :value="role.id">{{role.role}}</option>                                
                            </select>
                        </div>                       
                    </div>                    
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success" @click="assignRoles()">
						add user
						<span v-if="adding" 
						class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
					 	</span>
					</button>
                </div>
                </div>
            </div>
        </div>

         <!-- add role Modal -->
         <div class="modal fade" id="addRoleModal" tabindex="-1" role="dialog" aria-labelledby="addRoleModal" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalCenterTitle">add a role</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    </div>
                    <div class="modal-body">                                
                            <form>
                                <div class=" row form-group">
                                    <label class="col-3"><b>name:</b></label>
                                    <input type="text" class="col-8 form-control" placeholder="enter name of the role" v-model="role_name">                                        
                                </div>
                                <div class="row form-group">
                                        <label class="col-3"><b>description:</b></label>
                                        <textarea type="text" class="col-8 form-control" maxlength="50" rows='3' v-model="role_description"></textarea>                                                   
                                </div>      
                                <div class="row">
                                    <label class="col-3"><b>access level</b></label>
                                    <select class="col-8 form-control" v-model="permission_level">
                                        <option value=0>can view, add and edit everything</option>
                                        <option value=1>can view, add and edit finances</option>
                                        <option value=2>can view finances (can't edit)</option>
                                        <option value=3>can view finances stats (can't view specifics)</option>                                                                                
                                    </select>
                                </div>                                                                                                                                                                                                                      
                            </form>
                    </div>
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>                        
                    <button type="button" class="btn btn-success" v-on:click="addRole()">
                        add role
					   <span v-if="adding" 
					   	class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                    	</span>
                    </button>
                    </div>
                </div>
                </div>
         </div> 

        <!-- reset password modal -->
        <div class="modal fade" id="resetPasswordModal" tabindex="-1" role="dialog" aria-labelledby="addRoleModal" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title" id="exampleModalCenterTitle">reset password</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
                </div>
                <div class="modal-body">                                
                    <p class="text-danger">
                        <span>this will reset user password back <br/>
                            to starter password 'changeMe'<br/>
                            only use this feature when a user has lost their password
                        </span>
                    </p>                
                </div>
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>                        
                <button type="button" class="btn btn-success" v-on:click="resetPassword(member_in_focus[0])">
                    reset password
                    <span v-if="adding" 
                        class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                    </span>
                </button>
                </div>
            </div>
            </div>
        </div>
         
         <!-- manage role Modal -->
         <div class="modal fade" id="manageRolesModal" tabindex="-1" role="dialog" aria-labelledby="addRoleModal" aria-hidden="true">
            <div class="modal-dialog modal-xl modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title" id="exampleModalCenterTitle">manage roles</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
                </div>
                <div class="modal-body ">                                                        
                        <table class="table table-borderless table-responsive-sm">
                            <thead>
                              <tr>                    
                                <th scope="col" ></th>
                                <th scope="col" class="d-flex flex-column justify-content-start">
                                    <div >
                                        access level
                                    </div>
                                </th>
                                <th scope="col">
                                    <div class="col-lg-6 col-sm-12 d-flex flex-column justify-content-center">
                                            <span>is group role</span>
                                            <small class="text-muted">sets whether you want this role to appear 
                                            in options when adding members to church groups</small>
                                    </div> 
                                </th>                                
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="role in roles" class="text-muted">                                        
                                <td>{{role.role}}</td>
                                <td><small>
                                    <span class="text-primary">currently: </span>
                                    <span v-if="role.permission_level == 0">
                                            can view, add and edit everything
                                    </span>
                                    <span v-if="role.permission_level == 1">
                                            can view, add and edit finances
                                    </span>
                                    <span v-if="role.permission_level == 2">
                                            can view finances (can't edit)
                                    </span>
                                    <span v-if="role.permission_level == 3">
                                            can view finances stats (can't view specifics)
                                    </span>                                                                       
                                    </small> 
                                    <select class="col-8 form-control" v-model="updated_permision_levels[role.id]">
                                        <option value=0 >can view, add and edit everything</option>
                                        <option value=1>can view, add and edit finances</option>
                                        <option value=2>can view finances (can't edit)</option>
                                        <option value=3>can view finances stats (can't view specifics)</option>                                                                                
                                    </select>
                                </td>
                                <td>
                                    <label class="anvil-checkbox">
                                            <input  type="checkbox" 
                                                    v-if="role.is_group_role" checked
                                                    value="false"
                                                    v-model="updated_roles[role.id]">
                                            <input  type="checkbox" 
                                                    v-if="! role.is_group_role"
                                                    value="true"
                                                    v-model="updated_roles[role.id]">
                                            <span class="anvil-checkmark"></span>
                                    </label>
                                </td>
                                <td>
                                    <button class="btn btn-outline-success" @click="updateRole(role.id)">
                                        update
                                        <span v-if="adding && updating_role_id == role.id" 
					   	                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                        </span>
                                    </button>
                                </td>
                              </tr>                  
                            </tbody>
                          </table>
                </div>                
            </div>
            </div>
     </div> 
    </div>            
</template>

<script>
import searchmember from '@/subcomponents/searchmember.vue'
import textmessage from '@/subcomponents/textmessage.vue'
export default {
name: 'userAccounts',   
components: { searchmember,textmessage },
data() {
    return {            
        access_level: this.$session.get('access_level'),
        member_in_focus: [],
        test: false,
        updated_roles:{},
        updated_permision_levels:{},
        roles: null,
        admins: null,
		selected_member:null,
		//add role
		adding:false,
		role_name:null,
		role_description:null,
		permission_level:null,
        updating_role_id:null,
		//assign role to member
		selected_role:null
    }
},
mounted(){
    this.getRoles()
    this.getMembersWithAdminRoles()    
},
methods: { 
    onMemberSelected (value) {
        this.selected_member = value        
    },
    getRoles: function(){
        this.$store.dispatch('update_isLoading', true)
        this.$http({
            // headers: {
            // // Set your Authorization to 'JWT', not Bearer!!!
            //   Authorization: `Bearer ${this.$session.get('token')}`,              
            // },
            method: 'get',
            url: this.$BASE_URL + '/api/members/role-list/',
        }).then((response) => {
            this.roles = response.data
            this.$store.dispatch('update_isLoading', false)
        }).catch((err) => {
            alert(err)
            this.$store.dispatch('update_isLoading', false)
        })
    },
    //get members with admin roles
    getMembersWithAdminRoles: function(){
        this.$store.dispatch('update_isLoading', true)
        this.$http({
            headers: {
            // Set your Authorization to 'JWT', not Bearer!!!
              Authorization: `Bearer ${this.$session.get('token')}`,              
            },
            method: 'get',
            url: this.$BASE_URL + '/api/members/members-with-admin-roles/',
        }).then((response) => {
            this.admins = response.data
            this.$store.dispatch('update_isLoading', false)
        }).catch((err) => {
            alert(err)
            this.$store.dispatch('update_isLoading', false)
        })
    },
    addRole: function() {
		this.adding = true
        this.$http({ 
            method: 'post',
            url: this.$BASE_URL + '/api/members/role-list/',
            data: {
                role: this.role_name,
                description: this.role_description,  
                permission_level: this.permission_level              
            }
            }).then((response) => {            
				this.adding = false
                this.role_name = ''
                this.role_description = '' 
                this.getRoles()
                alert("role succesfuly added")                     
            })
            .catch((err) => {
				this.adding = false
                alert(err)
            })                
    },
    // assign roles
    assignRoles: function(){  
		this.adding = true                                
        this.$http({
            method: 'post',
            url: this.$BASE_URL + '/api/members/add-role-for-member/',
            data: {
                member: this.selected_member,
                role: this.selected_role                  
            }
            }).then(response => {                                
				this.selected_role = null          
				this.adding = false
                this.getMembersWithAdminRoles()
                alert("admin user added")                                
            })
            .catch((err) => {
				alert(err)
				this.adding = false
            }) 
        
    },
    //update roles
    updateRole: function(role_id){ 
        this.updating_role_id = role_id
        this.adding = true       
        var data
        if (this.updated_permision_levels[role_id] != null){
            data = { permission_level: this.updated_permision_levels[role_id] }
        }
        if (this.updated_roles[role_id] != null){
            data = {  is_group_role: this.updated_roles[role_id] }
        }
        if (this.updated_permision_levels[role_id] != null && this.updated_roles[role_id] != null){
            data={
                permission_level: this.updated_permision_levels[role_id],
                is_group_role:this.updated_roles[role_id]
            }
        }
        //add role id to data        
        data['role_id'] = role_id        
        this.$http({
            method:'patch',
            url: this.$BASE_URL + '/api/members/role-list/',
            data:data
        }).then(()=>{
            this.adding = false
            alert('update successful')
            this.getRoles()
        }).catch((err)=>{
            this.adding = false
            alert(err)
        })
    },
    //reset password.
    resetPassword: function(user_id){
        this.adding = true
        this.$http({
            headers: {
            // Set your Authorization to 'JWT', not Bearer!!!
              Authorization: `Bearer ${this.$session.get('token')}`,              
            },
            method: 'post',
            url: this.$BASE_URL + '/api/members/reset-password/',
            data:{user_id:user_id}
        }).then(()=>{
            alert("password for user reset to starter password 'ChangeMe'")
            this.adding = false
        }).catch((err)=>{
            alert(err)
            this.adding = false
        })
    }
}
}
</script>
<template>
    <div class="memberDetail">
        <nav aria-label="breadcrumb" class="continer">
        <ol class="breadcrumb">
			<li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li>
			<li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'memberList'}">members</router-link> </span></li>
			<li class="breadcrumb-item active" aria-current="page">member detail</li>
        </ol>
        </nav>
        <section class="continer">
			<div class="row">
				<div class="col" v-if="member_info != null">
				<h3 class="row" v-for="data in member_info.member">
				{{data.member.first_name}} {{data.member.last_name}}
				</h3>
				</div>
			</div>
			<hr>
        </section>
        <section class="continer">
        <div class="row">
        <!-- NAVIGATION ON THE LEFT -->
        <div class="col-sm-12 col-md-8 col-lg-3">                        
			<nav class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
				<a class="nav-link active list-group-item list-group-item-action border-0" id="pill-detail-tab" data-toggle="pill" href="#pill-detail" role="tab" aria-controls="pill-detail" aria-selected="true">
					<img class="church-is-menu" src="@/assets/icons/icons8-contacts-208.png"> detail
				</a>                                                                
				<a class="nav-link list-group-item list-group-item-action border-0" id="pill-groups-tab" data-toggle="pill" href="#pill-groups" role="tab" aria-controls="pill-groups" aria-selected="false" v-on:click = "getMemberGroups()">
					<img class="church-is-menu" src="@/assets/icons/icons8-user-groups-filled-50.png"> groups
				</a>                        
				<a class="nav-link list-group-item list-group-item-action border-0" id="pill-contributions-tab" data-toggle="pill" href="#pill-contributions" role="tab" aria-controls="pill-contributions" aria-selected="false" v-on:click = "getMemberFinances()">
					<img class="church-is-menu" src="@/assets/icons/icons8-donate-filled-50.png"> finances
				</a>
				<a class=" d-none nav-link list-group-item list-group-item-action border-0" id="pill-roles-tab" data-toggle="pill" href="#pill-roles" 
					role="tab" aria-controls="pill-roles" aria-selected="false">
					<img class="church-is-menu" src="@/assets/icons/icons8-admin-settings-male-30.png"> roles
				</a> 
				<a class="nav-link list-group-item list-group-item-action border-0" 
				data-toggle="modal" data-target="#deleteMemberModal">
						<img class="church-is-menu" src="@/assets/icons/icons8-cancel-26.png"> delete
				</a> 
			</nav>
        </div>
        <!-- CONTENT ON THE RIGHT -->                
        <div class="col">
			<div class="tab-content" id="v-pills-tabContent">
				<!-- member detail -->
				<div class="tab-pane fade show active" id="pill-detail" role="tabpanel" aria-labelledby="pill-detail-tab">                                
					<hr class="d-sm-block d-lg-none">
					<memberdetail/>                                       
				</div>
				<!-- member groups -->
				<div class="tab-pane fade" id="pill-groups" role="tabpanel" aria-labelledby="pill-groups-tab">
						<hr class="d-sm-block d-lg-none">
						<h3> Church Groups</h3>
						<table class="table table-responsive-sm table-borderless" v-if = "groups_selected == true">
						<thead class=""  v-if = "church_groups.response.length > 0">
							<tr>
								<th>group</th>
								<th>joined</th>
								<th>role</th>
							</tr>
						</thead>
							<tr class="text-muted" v-for = "data in church_groups.response">
								<td>                                                                
									<router-link class="text-secondary" :to="`/groupDetail/`+ data.church_group.id ">
										<img style="width: 30px ;height: auto" src="@/assets/icons/icons8-user-groups-48.png">                     
										{{data.church_group_name}}
									</router-link>
								</td>
								<td>{{$humanizeDate(data.date_joined)}}</td>
								<td>{{data.role_name}}</td>
							</tr>

						</table>
						<div v-if = "groups_selected == true">
							<div v-if = "church_groups.response.length == 0 ">
								<p class="text-muted">member belongs to none. </p>
							</div>
						</div>
				</div>
				<!-- member finances -->
				<div class=" tab-pane fade" id="pill-contributions" role="tabpanel" aria-labelledby="pill-contributions-tab">
						<div class="row">
						<div class="col-2"></div>
						<div class="col-lg-8 col-sm-12">
						<!-- navigation -->
						<hr class="d-sm-block d-lg-none">
						<ul class="row nav nav-pills mb-3 mt-3" id="pills-tab" role="tablist">
							<li class="nav-item">
									<a class="nav-link active" id="pills-home-tab" data-toggle="pill" href="#pills-home" role="tab" aria-controls="pills-home" aria-selected="true">Contributions</a>
							</li>
							<li class="nav-item">
									<a class="nav-link" id="pills-profile-tab" data-toggle="pill" href="#pills-profile" role="tab" aria-controls="pills-profile" aria-selected="false">Pledges</a>
							</li>
							<li class="nav-item">
									<a class="nav-link" id="pills-tithes-tab" data-toggle="pill" href="#pills-tithes" role="tab" aria-controls="pills-tithes" aria-selected="false">Tithes</a>
							</li>
							<li class="nav-item">
									<a class="nav-link" id="pills-offerings-tab" data-toggle="pill" href="#pills-offerings" role="tab" aria-controls="pills-offerings" aria-selected="false">Offerings</a>
							</li>
						</ul>
						</div>
						<div class="col-2"></div>
						</div>
						<section class="tab-content" id="pills-tabContent">
								<div class="tab-pane fade show active" id="pills-home" role="tabpanel" aria-labelledby="pills-home-tab" v-if="finances_selected">
									<h3 >Contributions</h3>
									<table class="table table-responsive-sm table-borderless">
										<thead>
										<tr>
											<th>project</th>
											<th>amount</th>
											<th>date</th>
										</tr>
										</thead>
										<tbody>
										<tr v-for = "data in contribution_info.contribution">
											<td>{{data.project.name}}</td>
											<td><p class="text-muted">{{humanize(data.amount)}}</p></td>
											<td>{{$humanizeDate(data.recorded_at)}}</td>
										</tr>
										</tbody>
									</table>
									<p class="text-muted" v-if="! contribution_info.contribution.length">
											found no contributions by member
									</p>
								</div>
								<div class="tab-pane fade" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile-tab" v-if="finances_selected">
									<h3>Pledges</h3>
									<table class="table table-responsive-sm table-borderless">
											<thead>
												<tr>
												<th>project</th>
												<th>pledged</th>
												<th>raised</th>
												<th>remaining</th>
												<th>percentage funded</th>
												</tr>
											</thead>
											<tbody>
												<tr v-for = "data in pledges_info.pledges">
												<td>{{data.project.name}} </td>
												<td>{{humanize(data.amount)}}</td>
												<td><p class="text-muted">{{humanize(data.amount_so_far)}}</p></td>
												<td><p  class="text-danger">{{humanize(data.remaining_amount)}}</p></td>
												<td><span class="text-muted">{{data.percentage_funded}}</span></td>

												</tr>
											</tbody>
									</table>
									<p class="text-muted" v-if="! pledges_info.pledges.length">
										found no pledges by member.
									</p>
								</div>
								<div class="tab-pane fade" id="pills-tithes" role="tabpanel" aria-labelledby="pills-tithes-tab" v-if = "finances_selected">
									<h3>Tithes</h3>                                                    
									<table class="table table-responsive-sm table-borderless">
										<thead>
										<tr>
											<th>amount</th>
											<th>narration</th>
											<th>date</th>
										</tr>
										</thead>
										<tbody>
										<tr v-for = "data in tithe_info.tithes">
											<td><p class="text-muted">{{humanize(data.amount)}}</p></td>
											<td > {{data.narration}}</td>
											<td>{{$humanizeDate(data.date)}}</td>
										</tr>
										</tbody>
									</table>
									<p class="text-muted" v-if="!tithe_info.tithes.length">
										found no tithe by member this month.
									</p>
								</div>
								<div class="tab-pane fade" id="pills-offerings" role="tabpanel" aria-labelledby="pills-offerings-tab" v-if = "finances_selected">
										<h3>Offerings </h3>                                                                
										<table class="table table-responsive-sm table-borderless">
											<thead>
											<tr>
												<th>amount</th>
												<th>narration</th>
												<th>date</th>
											</tr>
											</thead>
											<tbody>
											<tr v-for = "data in offering_info.offerings">
													<td><p class="text-muted">{{humanize(data.amount)}}</p></td>
													<td> {{data.narration}}</td>
													<td>{{$humanizeDate(data.date)}}</td>
											</tr>
											</tbody>
										</table>
										<p class="text-muted" v-if="!offering_info.offerings.length">
											found no offering by member.
										</p>
								</div>
						</section>
				</div>                               
			</div>
        </div>
        </div>
        </section>  
        <!-- Modals  -->
        <section>               
			<!-- delete member Modal -->
			<div class="modal fade" id="deleteMemberModal" tabindex="-1" role="dialog" aria-labelledby="deleteMemberModal" aria-hidden="true">
							<div class=" modal-dialog modal-dialog-centered" role="document">
							<div class="modal-content">
									<div class="modal-header">
									<h5 class="modal-title" >delete member</h5>
									<button type="button" class="close" data-dismiss="modal" aria-label="Close">
											<span aria-hidden="true">&times;</span>
									</button>
									</div>
									<div class="modal-body border text-danger">
											
											Are you sure you want to delete this member??

											<p class="mt-2 small">
															all data about the member will be lost, 
															this is irrreversible
											</p>
											
											
									</div>
									<div class="modal-footer">
									<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
									<button type="button" class="btn btn-danger" v-on:click="deleteMember()">
											delete
											<span v-if="deleting_member"
													class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
											</span>
									</button>
									</div>
							</div>
							</div>
			</div>
        </section>     
    </div>
  </template>

<script>
import router from "../../router";
import memberdetail from '@/subcomponents/members/memberdetail'
export default {
  components: { memberdetail },
  name: 'memberDetail',
  data () {
    return {  
        member_info:null,
        //groups        
        groups_selected: false,
        church_groups: null,
        //finances
        finances_selected: false, contribution_info:null, pledges_info: null,
        offering_info: null,tithe_info: null,tithe_stats: null,offering_stats: null,
        family_tree: null,
        // roles
        //fetching data
        fetch_data_error: [],
        roles: null,            
        roles_for_member: null, 
        //add role                                        
        //assign roles 
        selected_role: [],
        assign_button_text: 'assign role(s)',        
        assigned_roles: [] ,
        deleting_member: false,
    }
  },
  created() {   
        this.getMemberInfo()             
        this.getRoleForMember()
    },
  methods: {
        humanize: function(x) {
                return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        getMemberInfo: function(){
                //member personal detail
                this.$http.get(this.$BASE_URL + '/api/members/member/'+this.$route.params.id+'/')
                .then(response => {
                        this.member_info = {"member": response.data }
                })
                .catch(error=> {
                
                })
        },
        getMemberGroups: function(){
			this.$store.dispatch('update_isLoading', true)
			this.groups_selected = true
			this.$http.get(this.$BASE_URL + '/api/groups/church-groups-for-a-member/'+this.$route.params.id+'/')
			.then(response => {
					this.church_groups = {"response": response.data }
					this.groups_loading = false
					this.$store.dispatch('update_isLoading', false)
			})
			.catch(error=> {
			this.groups_errors.push(error)
			this.$store.dispatch('update_isLoading', false)
			})
        },
        getMemberFinances: function() {
			this.$store.dispatch('update_isLoading', true)
			this.finances_selected = true
			this.$http.get(this.$BASE_URL + '/api/projects/contributions-by-member/'+this.$route.params.id+'/')
			.then(response => {
				this.contribution_info = {"contribution": response.data }

			})
			.catch(error=> {

			})
			this.$http.get(this.$BASE_URL + '/api/projects/pledges-by-member/'+this.$route.params.id+'/')
			.then(response => {
				this.pledges_info = {"pledges": response.data }
			})
			.catch(error=> {

			})
			this.$http.get(this.$BASE_URL + '/api/finance/tithe-stats-for-member/'+this.$route.params.id+'/')
			.then(response => {
			this.tithe_stats = {"stats": response.data }
			})
			.catch(error=> {

			})
			this.$http.get(this.$BASE_URL + '/api/finance/tithe-for-member/'+this.$route.params.id+'/')
			.then(response => {
			this.tithe_info = {"tithes": response.data }
			})
			.catch(error=> {

			})
			this.$http.get(this.$BASE_URL + '/api/finance/offering-stats-for-member/'+this.$route.params.id+'/')
			.then(response => {
			this.offering_stats = {"stats": response.data }
			})
			.catch(error=> {

			})
			this.$http.get(this.$BASE_URL + '/api/finance/offerings-by-member/'+this.$route.params.id+'/')
			.then(response => {
			this.offering_info = {"offerings": response.data }
			this.$store.dispatch('update_isLoading', false)
			})
			.catch(error=> {
			this.$store.dispatch('update_isLoading', false)
			})

        },
        // roles
        getRoles: function () {
            this.fetch_data_error = []
            this.$http.get(this.$BASE_URL +'/api/members/role-list/')
                .then(response => {
                this.roles = {"response": response.data } 
                })
                .catch((err) => {
                    this.fetch_data_error.push(err)
                })                  
            
        },
        getRoleForMember: function (){  
            this.$http.get(this.$BASE_URL +'/api/members/roles-for-member/'+ this.$route.params.id + '/')
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
        // assign roles
        assignRoles: function(){
            for (var id in this.selected_role){                
            this.assign_button_text = "assigning roles..."
            this.$http({
                method: 'post',
                url: this.$BASE_URL + '/api/members/add-role-for-member/',
                data: {
                   member_id: this.$route.params.id,
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
        },
        
        deleteMember: function(){
                //delete member personal detail                
                this.deleting_member = true
                this.$http.delete(this.$BASE_URL + '/api/members/member/'+this.$route.params.id+'/')
                .then(response => {
                        this.deleting_member = false                                                                       
                        alert("member deleted")                
                        localStorage.removeItem("member_list_version");
                        localStorage.removeItem("member_list");
                        location.reload()
                })
                .catch((err)=> {
                        alert(err)
                        this.deleting_member = false
                })
        },

    }

}
</script>


<style >
</style>

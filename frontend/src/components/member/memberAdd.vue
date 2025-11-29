<template>
    <div class="memberAdd">
    <nav aria-label="breadcrumb" class="continer">
		<ol class="breadcrumb">
			<li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li>
			<li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'memberList'}">members</router-link></span></li>
			<li class="breadcrumb-item active" aria-current="page">add member</li>
		</ol>
    </nav>
    <div class="continer">
		<div class="row">              
			<div class="col-12 col-sm-12 col-lg-8">                
			<div v-if="add_member_error.length > 0 "role="alert">
				<!-- if no connection -->
				<div class="col">
					<img style = "height: 64px "src="@/assets/icons/icons8-wi-fi-off-64.png">
					<p class="text-info">check your connection</p>
					</div class="col">
					<div>
					<strong>add member will not work without a connection !</strong>
					<p>check your connection and try again.</p>
					<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
					</button>
					</div>
				</div>                        
				<!-- PERSONAL DETAILS -->                       
				<section class="mx-auto col-lg-8 col-sm-12" v-if= "form_in_view == 'personal_detail_form'">                               
						<!-- first_name last name and surname -->						
						<div class="ml-0 mb-3">
							<h2 class="text-muted">Personal detail</h2>						                                       
						</div>
						<div v-if="! added_member.length">
							<div class="row">
									<div class="col">
									<div class="mb-3 form-group">								
										<input type="text" class="form-control"  placeholder="First Name" v-model="first_name" autofocus>
										<p v-if="first_name_errors.length">
											<ul>
												<small><li v-for="error in first_name_errors"><p class="text-danger">{{ error }}</p></li></small>
											</ul>
										</p>
									</div>
									<div class="form-group">								
										<input type="text" class="form-control"  placeholder="Middle Name" v-model="middle_name" >                                                                
									</div>
									<div class="form-group">								
										<input type="text" class="form-control"  placeholder="Last Name" v-model="last_name" >
										<p v-if="last_name_errors.length">
											<ul>
												<small><li v-for="error in last_name_errors"><p class="text-danger">{{ error }}</p></li></small>
											</ul>
										</p>
									</div>
									</div>
							</div>                                
							<!-- gender -->
							<div>
								<div class="row">
									<div class="checkbox col">
										<div class="radio">
											<label><input type="radio" value = "M" v-model = "gender" > Male</label>
										</div>
										<div class="radio">
											<label><input type="radio" value = "F" v-model = "gender"> Female</label>
										</div>
										<p v-if="gender_errors.length">
										<ul>
											<small><li v-for="error in gender_errors"><p class="text-danger">{{ error }}</p></li></small>
										</ul>
										</p>
									</div>
								</div>
							</div>	
						</div>		
						<div v-else class="d-flex">
							<span class="p-2">{{added_member[0].member.first_name}} {{added_member[0].member.last_name}}</span>
							<button class="ml-4 btn btn-outline-success" @click="resetForm()">Add New</button>
						</div>									
				</section>   

				<!-- MEMBER CONTACT -->
				<section class="mb-5 mx-auto col-lg-8 col-sm-12" v-if = "form_in_view == 'personal_detail_form'">
					<!-- head -->
					<hr>
					<div class="ml-0 mb-3">
						<h2 class="text-muted">Contact</h2>						                                       
					</div>
					<!-- contact input -->
					<div v-if="! added_contact">                                
						<div class="row" >
							<div class="col">
							<div class="form-group">
								<label><b>email :</b></label>
								<input type="email" class="form-control"  placeholder="example@gmail.com" v-model = "email">
							</div>
							<div class="form-group">                
								<div class="row">									
									<span class="col-12">
										<label><b>phone number :</b></label>
										<input type="text" class="form-control"  placeholder="0712345678" v-model = "phone_number">
									</span>
								</div>
								<p v-if="phone_number_errors.length">
									<ul>
										<small><li v-for="error in phone_number_errors"><p class="text-danger">{{ error }}</p></li></small>
									</ul>
								</p>
								<p v-if="phone_number_OK.length">
									<ul>
										<small><li v-for="error in phone_number_OK"><p class="text-success">{{ error }}</p></li></small>
									</ul>
								</p>
							</div>
							<div class="form-group">
								<label><b>postal address :</b></label>
								<input type="text" class="form-control"  placeholder="123-456" v-model="postal_address">
							</div>
							</div>
						</div>                            
					</div>
					<!-- added contact -->
					<div v-if = "added_contact">                                                
						<p>email: <span class="text-muted">{{added_contact.member.member.email}}</span></p>
						<p>phone number: <span class="text-muted">{{added_contact.member.phone_number}}</span></p>
					</div>										
				</section> 

				<!-- MEMBER AGE  -->                        
				<section class="mb-5 mx-auto col-lg-8 col-sm-12" v-if = "form_in_view == 'personal_detail_form' ">
						<!-- head -->
						<hr>
						<div class="ml-0 mb-3">
							<h2 class="text-muted">Age</h2>						                                       
						</div>
						<!-- age input -->
						<div v-if="! added_age" class="row">
							<div class="col">
								<div class="form-group">
									<label><b>date of birth :</b></label>
									<input type="date" name="bday" max="3000-12-31" 
									min="1000-01-01" class="form-control" v-model="d_o_b"> 
								</div>                                         
							</div>
						</div>
						<div v-if="added_age">
							<p>date of birth: <span class="text-muted">{{added_age.d_o_b}}</span></p>
						</div>												
				</section>      

				<!-- MEMBER MARITAL STATUS -->
				<section class="mx-auto col-lg-8 col-sm-12" v-if = "form_in_view == 'personal_detail_form'">
						<hr>
						<div class="ml-0 mb-3">
							<h2 class="text-muted">Marital status</h2>						                                       
						</div>
						<!-- marital status input -->
						<div v-if="! added_marital_status" class="">
							<div class="row">
								<div class="col">
									<div class="radio">
										<label>
										<input type="radio" name="optradio" value="S" v-model="marital_status"> single</label>
									</div>
									<div class="radio">
										<label><input type="radio" name="optradio" value="M" v-model="marital_status"> married</label>
									</div>
									<div class="radio">
										<label><input type="radio" name="optradio" value="D" v-model="marital_status"> divorced</label>
									</div>
									<div class="radio">
										<label><input type="radio" name="optradio" value="W" v-model="marital_status"> widowed</label>
									</div>
								</div>
							</div>
						</div>
						<div v-if="added_marital_status">                                        
							<p>marital status: 
								<span v-if="added_marital_status.status == 'S'">Single</span>
								<span v-if="added_marital_status.status == 'M'">Married</span>
								<span v-if="added_marital_status.status == 'D'">Divorced</span>
								<span v-if="added_marital_status.status == 'W'">Widowed</span>
							</p>
						</div>						
				</section>                                                       

				<!-- MEMBER RESIDENCE -->
				<section class="mx-auto col-lg-8 col-sm-12" v-if = "form_in_view == 'personal_detail_form'">
						<hr>
						<div class="ml-0 mb-3">
							<h2 class="text-muted">Residence</h2>						                                       
						</div>
						<!-- residence input -->
						<div v-if="! added_residence" class="">                                
							<div class="row" >
								<div class="col">
								<div class="form-group">
									<label><b>home town :</b></label>
									<input type="text" class="form-control"  placeholder="e.g Nakuru,Nairobi" v-model="home_town">
								</div>
								<div class="form-group">
									<label><b>road :</b></label>
									<input type="text" class="form-control"  placeholder="e.g Mombasa road" v-model="road">
								</div>
								<div class="form-group">
									<label><b>street / drive :</b></label>
									<input type="text" class="form-control"  placeholder="e.g lumumba drive" v-model="street">
								</div>
								<div class="form-group">
									<label><b>estate / area name :</b></label>
									<input type="text" class="form-control"  placeholder="e.g Kamkunji,Kaloleni" v-model="estate">
								</div>
								<div class="form-group">
									<label for="exampleFormControlTextarea1"><b>description</b></label>
									<textarea class="form-control" id="exampleFormControlTextarea1" rows="3" v-model="description"></textarea>
									</div>
								</div>
							</div>                            
						</div>
						<div v-if="added_residence">                                        
							<p>town: <span class="text-muted">{{added_residence.town}}</span></p>
							<p>road: <span class="text-muted">{{added_residence.road}}</span></p>
							<p>street: <span class="text-muted">{{added_residence.street}}</span></p>
							<p>description: <span class="text-muted">{{added_residence.description}}</span></p>
						</div>
						<!-- buttons -->
						<div class="ml-2 d-flex justify-content-end">
							<button v-if="!added_residence" class="btn btn-success" @click="addMember()">
								{{add_button_text}}
								<span   v-if="adding_member_detail"
									class="spinner-border spinner-border-sm" 
									role="status" 
									aria-hidden="true">
								</span>                                              
							</button>
							<button class="ml-2 btn btn-outline-success"
								v-if="added_member.length"
								@click="form_in_view = 'groups_form'">
								Assign groups
							</button>
						</div>
				</section>                    
					<!-- MEMBER GROUP   -->                        
				<section class="mx-auto col-lg-8 col-sm-12" v-if = "form_in_view == 'groups_form' ">
					<!-- head -->
					<div class="ml-0 mb-5">
							<a  style="cursor: pointer" class="text-primary" @click="form_in_view='personal_detail_form'">
								<img style="height: 20px" src="@/assets/icons/icons8-back-filled-50.png" alt="back">
								back
							</a>
							<h4 class="mt-3 text-muted">Assign groups for
								{{added_member[0].member.first_name}}
								{{added_member[0].member.last_name}}
							</h4>
					</div>
					<!-- group input					 -->
					<div v-for="folder, group in folders" v-if="! groups_added_into.length">
						<h4 class="text-capitalize">{{folder[0].folder_name}}</h4>
						<hr>
						<div v-for="group in folder">													
							<label class="anvil-checkbox">
								<input multiple type="checkbox" :value=group.id v-model="group_ids">
								<span class="anvil-checkmark"></span>
								<span class="ml-5">{{group.name}}</span>
							</label>
						</div>
					</div>					
					<div v-if="groups_added_into.length">
						<ul>
							<li class="text-muted" v-for="group in groups_added_into">
								{{group.church_group_name}}
								as 
								{{group.role_name}}
							</li>
						</ul>
					</div> 
					<!-- buttons -->
					<div class="ml-2 d-flex justify-content-end">
						<button v-if="! groups_added_into.length" class="btn btn-success" @click="addMemberToGroup()">
							+ add member to groups
							<span   v-if="adding_member_detail"
								class="spinner-border spinner-border-sm" 
								role="status" 
								aria-hidden="true">
							</span> 
						</button>                                        
					</div>
				</section>
			</div>
		</div>
		</div>
    </div>
  </template>

<script>
import axios from 'axios'
export default {
  name: 'memberAdd',
  data () {
    return {
		//add button text
		add_button_text: "+ Add Member",
        //select form in view
        form_in_view: 'personal_detail_form',
        //contact
        email: '',
        country_code: '',
        contact: ' ',postal_address: '',
        phone_number: '',phone_number_errors: [],phone_number_OK: [],
        added_contact:null,
        //names and gender
        first_name: '',first_name_errors: [],
        last_name: '',last_name_errors: [],
        middle_name: null,
        gender: '',gender_errors: [],
        added_member: [],
        add_member_error: [],
        added_member_id: null,                
        //date of birth        
        d_o_b: '',added_age:null,
        //residence
        home_town: '', road: '', street: '',
        estate: '', description: '',
        added_residence:null,
        //marital status
        marital_status: '',
        added_marital_status:null,
        //add member
        adding_member_detail: false,
        //add member to group.
        groups:null, 
        group_ids: [],
        groups_added_into:[]
    }
  },
 created(){
        this.getGroups()
 },
  watch: {        
        phone_number: function(){
			if (this.phone_number.isNaN){
				this.phone_number_errors = []
				this.phone_number_errors.push(" phone number should be numbers only")
			}
			if (this.phone_number.length > 10){
				this.phone_number_OK = []
				this.phone_number_errors = []
				this.phone_number_errors.push("number too long")
			}
			if (this.phone_number.length < 10){
				this.phone_number_OK = []
				this.phone_number_errors = []
				this.phone_number_errors.push("number too short")
			}
			if (this.phone_number.length == 10){
				this.phone_number_errors = []
				this.phone_number_OK.push(" number OK")
			}
        },
        day: function (){
			if (this.month == 0){
				this.date_errors = []
				this.date_errors.push("input month first")
			}
			if (this.day > 0 && this.day > 30){
				this.date_errors = []
				this.date_errors.push("day must between 1 & 30")
			}
        },
        month: function (){
			if (this.year == 0){
				this.date_errors = []
				this.date_errors.push("input year first")
			}
			if (this.month > 0 && this.month > 12){
				this.month
			}
        },
        year: function (){

        }
        
  },
  computed:{
	folders(){		
		return this.groupBy(this.groups.response, 'group')
		}
  },
  methods: {   
	resetForm: function(){
        //contact
        this.added_contact = null
        //names and gender		
        this.added_member = []
        this.add_member_error = []
        this.added_member_id = null
        //date of birth        		
		this.added_age = null
        //residence       
        this.added_residence = null
        //marital status    
        this.added_marital_status = null
        //add member
		this.adding_member_detail = false    
		//add button text    
		this.add_button_text = "+ Add Member"
	},
    addMember: function(){
		if (! this.added_member.length){
			this.first_name_errors = []
			this.last_name_errors = []
			this.gender_errors = []

			if (! this.first_name){
				this.first_name_errors.push('you must enter the first name')
				alert('you must enter the first name')
				return false;
			}
			if (this.first_name.split(' ').length > 1){
				this.first_name_errors.push('first name must be one word only')
				alert('first name must be one word only')
				return false;
			}
			if(! this.last_name){
				this.last_name_errors.push('you must enter a last name')
				alert('you must enter a last name')
				return false;
			}
			if (this.last_name.split(' ').length > 1){
				this.last_name_errors.push('last name must be one word only')
				alert('last name must be one word only')
				return false;
			}
			if (! this.gender ){
				this.gender_errors.push('select gender')
				alert('select gender')
				return false;
			}
			this.added_contact = null
			this.added_age = null
			this.added_marital_status = null
			this.added_residence = null
			this.adding_member_detail = true
			this.groups_added_into = []
			
			this.$http({
				method: 'post',
				url: this.$BASE_URL + '/api/members/add-member/',
				data: {
					first_name: this.first_name,
					middle_name:this.middle_name,
					last_name: this.last_name,
					gender: this.gender,
					email: this.email         
				}
			}).then(response => {                
				this.added_member.push(response.data )  
				this.added_member_id = this.added_member[0].member.id
				this.addOtherDetails()
				//update local storage
				var new_version = parseInt(localStorage.getItem('member_list_version')) + 1
				this.$store.dispatch('update_member_list_version', new_version)
				alert("member added succesfully")  
				//reset detail
				this.gender_male = false
				this.gender_female = false
				this.last_name = ''
				this.first_name = ''                                                             
				this.adding_member_detail = false               
				this.add_button_text = "update details"
			}).catch((err) => {
				this.add_member_error.push(err)
			})
		}
		else{
			this.addOtherDetails()
		}
        
    },
    addContact: function(){
        if (this.phone_number_OK.length > 0){
			this.adding_member_detail = true
			this.$http({
				method:'post',
				url: this.$BASE_URL + '/api/members/add-member-contact/',
				data: {
					member_id: this.added_member_id,
					postal_address: this.postal_address,
					phone: this.phone_number,
					contact: this.contact
				}
			}).then((response)=>{
				this.added_contact = response.data
				this.adding_member_detail = false
				this.email = ''
				this.country_code = ''
				this.contact = ''
				this.postal_address = ''
				this.phone_number = ''
				this.phone_number_errors = []
				this.phone_number_OK = []
				alert("contact added")

			}).catch((err)=>{
				alert(err)
				this.adding_member_detail = false
				this.email = ''
				this.country_code = '+254'
				this.contact = ''
				this.postal_address = ''
				this.phone_number = ''
				this.phone_number_errors = []
				this.phone_number_OK = []
			})  
        }           
    },
    addDateOfBirth: function(){
        if (this.d_o_b.length > 0){
			this.adding_member_detail = true
			this.$http({
				method:'post',
				url: this.$BASE_URL + '/api/members/add-member-d_o_b/',
				data: {
					member_id: this.added_member_id,
					d_o_b: this.d_o_b                        
				}
			}).then((response)=>{
				this.added_age = response.data
				this.adding_member_detail = false
				this.d_o_b = ''
				alert("date of birth added")
			}).catch((err)=>{
				alert(err)
				this.adding_member_detail = false
				this.d_o_b = ''
			})
        }       
    },
    addMaritalStatus: function(){
        if (this.marital_status.length > 0){
			this.adding_member_detail = true
			this.$http({
				method:'post',
				url: this.$BASE_URL + '/api/members/add-member-marital-status/',
				data: {
					member_id: this.added_member_id,
					status: this.marital_status                      
				}
			}).then((response)=>{
				this.added_marital_status = response.data
				this.adding_member_detail = false
				this.marital_status = ''
				alert("marital status added")
			}).catch((err)=>{
				alert(err)
				this.adding_member_detail = false
				this.marital_status = ''
			})
        }       
    },
    addResidence: function(){
        if (this.home_town.length > 0
			|| this.road.length > 0
			|| this.street.length > 0
			|| this.estate.length > 0
			|| this.description > 0){
					
			this.$http({
				method:'post',
				url: this.$BASE_URL + '/api/members/add-member-residence/',
				data: {
					member_id: this.added_member_id,
					town: this.home_town,
					road: this.road,
					street: this.street,
					description: this.description
				}
			}).then((response)=>{
				this.added_residence = response.data
				this.home_town = ''
				this.road = ''
				this.street = ''
				this.description = ''
				alert("residence added")
			}).catch((err)=>{
				alert(err)
				this.home_town = ''
				this.road = ''
				this.street = ''
				this.description = ''
			})
        }
	},
	addOtherDetails: function(){		
		this.addContact()
		this.addDateOfBirth()
		this.addMaritalStatus()
		this.addResidence()
	},
	groupBy: function(array, key){
		const result = {}
		array.forEach(item => {
			if (!result[item[key]]){
			result[item[key]] = []
			}
			result[item[key]].push(item)
		})
		return result
	},
    // get  groups
    getGroups: function(){      
      const currentVersion = this.$store.getters.group_list_version
      var version  = localStorage.getItem('group_list_version')

      this.groups = JSON.parse(localStorage.getItem('group_list_all'))

      if (!version || version <= currentVersion) {
        this.$http.get(this.$BASE_URL + '/api/groups/church-group-list/')
          .then(response => {
              this.groups = {"response": response.data }
              localStorage.setItem('group_list_all',JSON.stringify({"response": response.data }))
          })
          .catch((err) => {
              this.fetch_data_error.push(err)
          })
      }      
    },
    //add member to selected groups.
    addMemberToGroup: function(){          
        for (var group_id in this.group_ids){
			this.adding_member_detail = true
			this.$http({ 
				method: 'post',
				url: this.$BASE_URL + '/api/groups/add-member-to-group/',
				data: {           
					church_group: parseInt(this.group_ids[group_id]),
					member: this.added_member_id,
					role: null
				}
			}).then(response => {
				this.adding_member_detail = false                                    
				this.selectedMember = null
				this.groups_added_into.push(response.data)                       
			}).catch((err) => {
				this.adding_member_detail = false            
				alert(err)            
			})
        }                                               
    }

    
}
}
</script>


<style >
</style>
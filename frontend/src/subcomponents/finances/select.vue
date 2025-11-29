<!-- Child.vue -->
<template>
    <div class="d-flex d-flex-column">                    
        <div class="anvil-select row form-group">             
                <select class="col-4 custom-select border-0 shadow-0 font-weight-bold"
                        v-model = "selected_input"
                        style="outline: none;
                               box-shadow:none !important;">
                        <option value="member_input" v-if="fields.includes('member')" selected>member</option>
                        <option value="group_input" v-if="fields.includes('group')">group</option>
                        <option value="service_input" v-if="fields.includes('service')">service</option>
                        <option value="none_member_input" v-if="fields.includes('non_member')">non member</option>
                </select>  
                
                <div class="col-8 height-smooth">
                    <!-- member -->
                    <searchmember v-if="selected_input == 'member_input'" v-on:memberSelected="onMemberSelected" />                                                                        
                    <!-- groups -->
                    <select v-if="selected_input == 'group_input'" class="ml-4 col-12 form-control" v-model="selected_group" >                            
                            <option v-for="data in groups.response" :value="data.id" >{{data.name}}</option>
                    </select> 
                    <!-- service                  -->                    
                    <div v-if="selected_input == 'service_input'" >
                            <select class="ml-3 form-control" v-model="service_type" >
                                    <option v-for="data in service_types.response" :value="data.id" >{{data.name}}</option>
                            </select>
                            <label class="ml-4 mt-3">date</label>
                            <div class="ml-3 input-group form-group" style="padding: 0px" >
                                <input type="date" name="bday" max="3000-12-31" 
                                       min="1000-01-01" class="form-control" v-model="date">                                                                                                                      
                            </div>   
                            <span v-if="searching_for_service">
                                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true">                                
                                </span> searching ...
                            </span>                            
                            <p v-if="found_service.length ">
                                    <ul v-if="found_service.length > 0">
                                            <small><li>
                                                <p class="text-success"> found a service on that date, proceed</p></li></small>
                                    </ul>
                                </p> 
                            <p v-if="found_service.length == 0 && searched_for_service">
                                    <ul >
                                            <small>
                                                <li >
                                                    <p class="text-danger"> NO service found on that date</p>
                                                    <p>select the date when you had the service                                                            
                                                    </p>
                                                </li>
                                            </small>
                                    </ul>
                            </p> 

                    </div>
                    <!-- non-member -->
                    <div class=" row form-group"  v-if="selected_input == 'none_member_input'">                            
                            <input type="text" class="form-control" placeholder="enter name" v-model = "name_if_not_member">                                        
                    </div>
                    <div class=" row form-group" v-if="selected_input == 'none_member_input'">                                                  
                            <div class="">
                                    <div class="row">
                                            <span class="col-4">
                                                    <label>code :</label>
                                                    <input class="form-control" type="text" placeholder="+254" v-model = "country_code">
                                            </span>
                                            <span class="col-8">
                                                    <label>phone number :</label>
                                                    <input type="text" class="form-control"  placeholder="712345678" v-model = "phone_number">
                                            </span>
                                            <div style="padding: 5px">
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
                                    </div>                                                                 
                            </div>                                                                                                                                         
                    </div>  
                </div>                                                           
        </div>
        
    </div>
</template>
<script>
import searchmember from '@/subcomponents/searchmember.vue'
export default {
name: 'textmessage',
components: { searchmember },
data() {
    return {    
       selected_input: "member_input",   
       selectedMember:null, 
        //select group
       selected_group:null,
       groups:null,
      // service
       service_type: null,
       service_types: null,
       found_service: [],
       searching_for_service :false,
       searched_for_service: false,
       date:'',
       offering_date_errors: [], service_type_errors: [],
       //non member
       name_if_not_member: '',
       phone_number: '',
       phone_number_errors: [], phone_number_OK: [],
    }
},
props:{
    fields:null
},
created(){
    this.getGroups()
    this.getServiceTypes()
},
watch:{
    selected_group:function(){
        this.emitToParent("groupSelected",this.selected_group)
    },
    selected_input: function(){
         this.emitToParent("inputChanged",this.selected_input)
    } ,
    date: function(){      
        this.searched_for_service = false      
        this.found_service = []
        this.service_type_errors = []
        if (this.service_type == null){
            this.service_type_errors.push("select a type of service")
            return
        }                           
        this.checkForService()          
    },
    service_type: function(){
        this.searched_for_service = false
        this.found_service = []
        if (this.date.length > 0){                
            if (this.date == null){                    
                return
            }                           
            this.checkForService()               
        }
    },
},
methods: {
    // Define the method that emits data to the parent as the first parameter to `$emit()`.
    // This is referenced in the <template> call in the parent. The second parameter is the payload.
    emitToParent (event,data) {              
        this.$emit(event, data)
    },
    onMemberSelected (value) {
        this.selectedMember = value
        this.emitToParent('memberSelected',this.selectedMember)
    },
    //get groups
    getGroups: function(){
      // get  groups     
      this.$http.get(this.$BASE_URL + '/api/groups/church-group-list/')
          .then(response => {
              this.groups = {"response": response.data }                                        
          })
          .catch((err) => {
              this.fetch_data_error.push(err)          
          })
      
    },
    //get service types
    getServiceTypes: function(){        
        this.$http.get(this.$BASE_URL + '/api/services/service-types/')
            .then(response => {
                this.service_types =  {"response":response.data}                
            })
            .catch((err) => {
                this.found_service = []                
            })
    },
    //check for service on a date
    checkForService: function(){  
        this.searching_for_service = true         
        this.$http.get(this.$BASE_URL + '/api/services/service-on-date/' + this.date +'/of-type/' + this.service_type + '/')
        .then(response => {                    
            this.found_service = response.data   
            this.emitToParent('serviceFound',this.found_service)                               
            this.searched_for_service = true
            this.searching_for_service = false
        })
        .catch((err) => {
            this.fetch_data_error.push(err)
            this.searching_for_service = false
        })
                
    },
    
}
}
</script>
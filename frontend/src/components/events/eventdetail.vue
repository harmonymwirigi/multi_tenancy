<template>
        <div>
            <nav aria-label="breadcrumb" class="continer">
                    <ol class="breadcrumb">
                            <li class="breadcrumb-item">
                                <span class="backButton">
                                    <router-link style="text-decoration: none" :to="{name: 'Home'}">
                                        Home
                                    </router-link>
                                </span>  
                            </li>
                            <li class="breadcrumb-item">
                                    <span class="backButton">
                                        <router-link style="text-decoration: none" :to="{name: 'events'}">
                                            events
                                        </router-link>
                                    </span>  
                            </li>
                            <li class="breadcrumb-item active" aria-current="page">{{event[0].title}}</li>
                    </ol>
            </nav>        
            <!-- continer -->
            <div class="continer">
                <div class="row">
                    <!-- content -->
                    <div class="col">
                        <div>
                            <h3>{{event[0].title}}</h3>
                            <h5>{{event[0].start}} 
                                <span class="text-muted">---to---</span>
                                 {{event[0].end}}
                            </h5>
                        </div>                                               
                        <span class="mr-2 text-muted" v-for="group in groups">                            
                           {{group.group.name}}  expected to attend 
                        </span>  
                        <div class="text-left mt-2">
                            <div class="text-center text-muted col-lg-3 col-sm-8 border border-secondary rounded">
                                <h1>{{event[0].attendees}} </h1>
                                People attended
                            </div>                            
                        </div>                        
                        <hr/>
                        <div v-if="!groups.length" class="text-center text-muted">
                            <h3>Oops!</h3>
                            <h5>No group selected to attend event</h5>
                            <p>you need to select a group so that we can generate a check in register</p>
                            <button type="button" class="btn btn-success" 
                                    data-toggle="modal" data-target="#addAttendingGroupModal">
                                Add attending group
                                <span v-if="adding_group"
                                    class="d-none spinner-border spinner-border-sm" 
                                    role="status" 
                                    aria-hidden="true">                                                                                       
                                </span>
                            </button>
                        </div>
                        <!-- members expected to attend event-->
                        <ul v-if="group_members" class="list-group list-group-flush">
                            <li class="list-group-item" v-for="item in group_members">                                
                                <div class="row">
                                    <!-- member list -->
                                    <div class="col">                                        
                                           
                                            <router-link :to="`/memberDetail/`+ item.member.member.id">
                                                <span class = "text-secondary">{{item.member.member.first_name}} {{item.member.member.last_name}}</span>
                                            </router-link>   
                                    </div>
                                    <!-- action button -->
                                    <div class="col text-right">
                                        <div v-if="! attended_member_ids.includes(item.member.member.id)">
                                            <button type="button" class="btn btn-sm btn-success" v-on:click="checkInMember(item.member.member.id)">
                                                Check In
                                                <span   
                                                        class="d-none spinner-border spinner-border-sm" 
                                                        role="status" 
                                                        aria-hidden="true"
                                                        :id="item.member.member.id + `_check_in_spinner`">                                                        
                                                </span>
                                            </button>
                                        </div>    
                                        <div v-else>
                                            <button disabled type="button" class="btn btn-sm btn-light">Checked</button>
                                        </div>   
                                                                         
                                    </div>
                                </div>                                                            
                            </li>                                                                                
                        </ul>
                        <div v-else class="text-muted text-center">            
                            <h5 v-if="groups.length">Getting Register ...</h5>
                        </div>
                    </div>
                    <!-- actions -->
                    <div class="col-lg-3 col-sm-12">
                        
                    </div>
                </div>                
            </div>
             <!-- Modal assign group -->
             <div class="modal fade" id="addAttendingGroupModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h5 class="modal-title" id="exampleModalCenterTitle">Add attending group</h5>
                          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                          </button>
                        </div>
                        <div class="continer mt-5 mb-5" v-if="groups_list">                                           
                          <label><b>select group :</b></label>
                          <select class=" form-control" v-model="group_id" >
                              <option v-for="data in groups_list.response" :value="data.id" >{{data.name}}</option>
                          </select>
                        </div>
                        <div class="modal-footer">
                          <button type="button" class="btn btn-secondary" data-dismiss="modal" >Close</button>
                          <button type="button" class="btn btn-success" v-on:click="addGroupAttendingEvent()">
                            add attending group
                            <span v-if="adding_group"
                                  class="spinner-border spinner-border-sm" 
                                  role="status" aria-hidden="true"></span>
                          </button>
                        </div>
                      </div>
                    </div>
                </div>
        </div>
    </template>
    
    <script>
    export default {
        name: 'smsAnalytics',
        data () {
            return{
               event: null,
               groups: null,
               group_members: null,
               expected_to_attend: 0,
               attended_members: null,               
               attended_member_ids: [],
               groups_list: null,
               //adding group
               adding_group: false,
               group_id: null
            }
        },
        created () {
           this.fetchData() 
           this.getMembersThatAttendedEvent()
        },
        watch:{
            groups: function(){
                if (! this.groups.length){
                    this.getGroups()
                }
            }
        },
        methods: {
            fetchData () {  
                this.$store.dispatch('update_isLoading', true)          
                this.$http.get(this.$BASE_URL + '/api/events/event/'+ this.$route.params.id +"/")
                    .then(response => {                    
                        this.event = response.data
                        this.$store.dispatch('update_isLoading', false)
                    })
                    .catch((err) => {
                        alert("error occured while fetching data")
                        this.$store.dispatch('update_isLoading', false)
                    })

                //get groups
                this.$store.dispatch('update_isLoading', true)   
                this.$http.get(this.$BASE_URL + '/api/events/get-groups-attending-event/'+ this.$route.params.id +"/")
                    .then(response => {                    
                        this.groups = response.data
                        this.getGroupMembers(this.groups[0].group.id)
                        this.expected_to_attend = this.groups[0].group.number_of_members
                        this.$store.dispatch('update_isLoading', false)
                    })
                    .catch((err) => {                        
                        this.$store.dispatch('update_isLoading', false)
                    })            
            },
            //get group members
            getGroupMembers: function(group_id){
                this.$store.dispatch('update_isLoading', true)
                this.$http.get(this.$BASE_URL + '/api/groups/church-group-members/'+ group_id +"/")
                    .then(response => {                    
                        this.group_members = response.data
                        this.$store.dispatch('update_isLoading', false)
                    })
                    .catch((err) => {                        
                        this.$store.dispatch('update_isLoading', false)
                    })

            },
            //get members that attended event
            getMembersThatAttendedEvent: function(){
                this.$store.dispatch('update_isLoading', true)
                this.$http.get(this.$BASE_URL + '/api/events/members-that-attended-event/'+ this.$route.params.id +"/")
                    .then(response => {                    
                        this.attended_members = response.data                        
                        for (var member in this.attended_members){
                            this.attended_member_ids.push(this.attended_members[member].member.member.id)
                        }
                        this.$store.dispatch('update_isLoading', false)
                    })
                    .catch((err) => {                        
                        this.$store.dispatch('update_isLoading', false)
                    })
            },
            //check in member.
            checkInMember: function(member_id){
                //show spinner
                var check_in_spinner = document.getElementById(member_id + "_check_in_spinner")
                check_in_spinner.classList.remove("d-none")
                //post
                this.$http.post(
                    this.$BASE_URL + '/api/events/record-member-that-attended-event/',
                    {
                        member_id:member_id,
                        event_id:this.$route.params.id
                    }
                ).then(response => {
                    this.getMembersThatAttendedEvent()
                    //hide spnner
                    var check_in_spinner = document.getElementById(member_id + "_check_in_spinner")
                    check_in_spinner.classList.add("d-none")
                }).catch(err =>{
                    alert(err)
                    var check_in_spinner = document.getElementById(member_id + "_check_in_spinner")
                    check_in_spinner.classList.add("d-none")
                })
            },
            //get groups list
            getGroups: function(){            
                this.groups_list = JSON.parse(localStorage.getItem('group_list'))
                const currentVersion = this.$store.getters.group_list_version
                var version  = localStorage.getItem('group_list_version')

                if (!version || version < currentVersion) {       
                    this.$http.get(this.$BASE_URL + '/api/groups/church-group-list/')
                    .then(response => {
                        this.groups_list = {'response':response.data}
                        localStorage.setItem('group_list',JSON.stringify({"response": response.data }))
                        localStorage.setItem('group_list_version', currentVersion)                         
                    })
                    .catch((err) => {
                        alert(err)          
                    })
                }
            
            },
            //add group attending event
            addGroupAttendingEvent: function(){
                this.adding_group = true
                this.$http.post(
                    this.$BASE_URL + '/api/events/add-group-attending-event/',
                    {
                        event_id:this.$route.params.id,
                        group_id:this.group_id
                    }
                ).then(()=>{
                    this.fetchData()
                    this.adding_group = false
                }).catch((err)=>{
                    alert(err)
                    this.adding_group = false
                })
            }
        }
    }
    </script>
    
    
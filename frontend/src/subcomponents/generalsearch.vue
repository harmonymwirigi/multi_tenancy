<template>
    <div class="child">
        <!-- general search -->         
                                     
            <div class="input-group">
                    <input type="text" class="form-control" v-model="generalSearch"
                            placeholder="search members,groups & events" >
                    <div class="input-group-append">
                      <span class="input-group-text" >
                            <img style="width: 20px ;height: auto" src="@/assets/icons/icons8-search-80.png">
                      </span>
                    </div>
            </div>             
            <div style="background-color: ghostwhite" class="text-info rounded" >{{search_status}}</div> 
            <div class="pre-scrollable searchedItemsDiv border " 
                style="min-width: 400px; 
                        max-height: 350px;
                         overflow-y: scroll;
                          position: absolute;
                           z-index: 3;
                            background-color: white"
                              v-if="showSearchResults">                

                <table class="table border-0 text-left" >                    
                    <tbody>
                    <!-- MEMBERS -->
                    <h6 class="ml-2 font-weight-bold" v-if="found_members.response.length">Members found</h6>
                    <!-- if no member matching pattern was found -->                    
                    <tr class="searchedItem border-0" v-for="data in found_members.response" style="cursor:pointer">   
                        <a>                                                                             
                            <td class="border-0"  v-on:click="hideSearchResults(`/memberDetail/`+ data.member.id)">
                            
                                <img v-if = "data.gender == 'M'" style = "height: 32px "src="@/assets/avatars/icons8-user-male-skin-type-4-40.png">
                                <img v-if = "data.gender == 'F'" style = "height: 32px "src="@/assets/avatars/icons8-user-female-skin-type-4-40.png">
                                <img v-if = "data.gender == 'R'" style = "height: 32px "src="@/assets/avatars/icons8-contacts-96.png">
                                
                                <span class = "text-secondary text-capitalize">
                                    {{data.member.first_name}} {{data.member.last_name}} 
                                    <small>( {{data.phone_number}} )</small>
                                </span>                                                                                                 
                            </td>    
                        </a>                                                                                                                                                    
                    </tr>
                    
                    <!-- GROUPS -->
                    <h6 class="ml-2 font-weight-bold" v-if="found_groups.length">Groups found</h6>                    
                    <tr class="searchedItem border-0" v-for="group in found_groups" style="cursor:pointer">                        
                        <router-link class="text-secondary" style="text-decoration: none;"  :to="`/groupDetail/`+ group.id ">
                            <td class="d-flex justify-content-between border-0"  v-on:click="hideSearchResults()">                        
                                {{group.name}} 
                                <span class="badge badge-pill badge-secondary ml-4">
                                    {{group.number_of_members}}                                 
                                </span>                                                                                                                        
                            </td>                       
                        </router-link>                                                                                                                                    
                    </tr>
                    
                    <!-- EVENTS -->
                    <h6 class="ml-2 font-weight-bold" v-if="found_events.length">Events found</h6>                   
                    <tr class="searchedItem border-0" v-for="event in found_events" style="cursor:pointer">    
                        <router-link class="text-secondary" style="text-decoration: none"  :to="`/eventDetail/`+ event.id + `/`">                     
                            <td class="ml-2 border-0 row"  v-on:click="hideSearchResults()">
                                <img style="width: 25px ;height: auto" src="@/assets/icons/icons8-schedule-64.png">
                                {{event.title}} 
                                <div class="ml-3 text-small">
                                    ({{$humanizeDate(event.start)}})
                                </div>                           
                            </td>  
                        </router-link>                                                                                                                                                      
                    </tr>
                    </tbody>
                </table>
                <!-- nothing found -->                
                <div class="text-center text-muted" v-if="! found_members.response.length & ! found_events.length & ! found_groups.length">
                    <h3>Oops!</h3>
                    <h5>nothing matching query found</h5>
                </div>
            </div>
    </div>
</template>
<script>
import router from "@/router";
export default {
name: 'generalsearch',
created () {        
    this.debouncedGetAnswer = _.debounce(this.getAnswer, 1000)
},
data() {
    return {
    generalSearch: '',
    showSearchResults: false, 
    //member search  
    found_members:[],
    search_status: '',     
    //group search
    found_groups:[],
    groupSearch_status:'',
    //events search
    found_events:[],
    eventSearch_status:''
    }
},
watch:{
    generalSearch: function () {        
        if (this.generalSearch.length > 0){            
            this.showSearchResults = true
            this.search_status = 'typing...'            
            this.debouncedGetAnswer()
        }else{        
            this.search_status = ''
            this.found_members = []
            this.found_events = []
            this.found_groups
            this.showSearchResults = false                
        }
    },

},
methods: {
    hideSearchResults: function(route){        
        this.showSearchResults = false
        this.generalSearch = ''
        router.push(route)        
        location.reload()
    },
    //search for member
    getAnswer: function () {
        var vm = this
        if (this.generalSearch.length > 0){
            this.found_members = []
            this.search_status = 'searching...'
            //search for member
            this.$http.get(this.$BASE_URL + '/api/members/filter-by-first_name/' + this.generalSearch +'/')
            .then(function (response) {
                vm.found_members = {"response": response.data } 
                vm.search_status = ''                
            })
            .catch(function (error) {
                vm.search_status = ''                  
            })
            //search for groups
            this.$http.get(this.$BASE_URL + '/api/groups/church-group-where-name-like/' + this.generalSearch +'/')
            .then(function (response) {
                vm.found_groups = response.data
                vm.groupSearch_status = ''                
            })
            .catch(function (error) {
                vm.groupSearch_status = ''  
                
            })
            //search for events
            this.$http.get(this.$BASE_URL + '/api/events/event-where-pattern-like/' + this.generalSearch +'/')
            .then(function (response) {
                vm.found_events = response.data
                vm.eventSearch_status = ''                
            })
            .catch(function (error) {
                vm.eventSearch_status = ''  
                
            })
        }
    },
}
}
</script>
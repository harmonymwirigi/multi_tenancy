<template>
        <div>
            <nav aria-label="breadcrumb" class="continer">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li>
                        <li class="breadcrumb-item active" aria-current="page">sermons</li>
                    </ol>
            </nav>        
            <div class = "continer">
                <div class="row">
                    <div  class = "col-12 col-sm-10 col-md-8 col-lg-2">
                            <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                                    <a class="action-list list-group-item list-group-item-action border-0 active" id="v-pills-income-tab" data-toggle="pill" href="#v-pills-today" role="tab" aria-controls="v-pills-today" aria-selected="true">today</a>
                                    <a class="action-list list-group-item list-group-item-action border-0" id="v-pills-expenditure-tab" data-toggle="pill" href="#v-pills-this-month" role="tab" aria-controls="v-pills-this-month" aria-selected="false" v-on:click="getSermonsThisMonth()">this month</a>  
                            </div>
                    </div>
                    <div class="col">
                            <div class="tab-content" id="v-pills-tabContent">
                       
                                    <div class="tab-pane fade show active" id="v-pills-today" role="tabpanel" aria-labelledby="v-pills-today-tab">
                                        <div v-if = "! sermons_available">
                                            no sermons available today
                                        </div>
                                        <div v-if = "sermons_available">
                                            <div v-for = "data in sermons_today.response">
                                                                                                
                                                <div>{{data.title}}</div>
                                                <hr/>
                                                <div class = "row">
                                                    <div class="col-12 col-sm-10 col-md-8 col-lg-2"><img :src="data.featured_image"></div>
                                                    <div class="col text-secondary">{{data.sermon}}</div>
                                                </div>
                                                <div>
                                                        <div class="card-body">
                                                                <p class="card-text text-muted">by --{{data.preached_by_member.member.first_name}} {{data.preached_by_member.member.last_name}}--</p>                                                                                                                            
                                                                <p class="card-text"><small class="text-muted">date - <b>{{data.date}}</b></small> </p>
                                                        </div>
                                                </div>
                                                <hr/>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="tab-pane fade show " id="v-pills-this-month" role="tabpanel" aria-labelledby="v-pills-this-month-tab">
                                            <div v-if = "this_month_selected">
                                                    <div v-for = "data in sermons_this_month.response">
                                                                                                        
                                                        <div>{{data.title}}</div>
                                                        <hr/>
                                                        <div class = "row">
                                                            <div class="col-12 col-sm-10 col-md-8 col-lg-2"><img :src="data.featured_image"></div>
                                                            <div class="col text-secondary">{{data.sermon}}</div>
                                                        </div>
                                                        <div>
                                                                <div class="card-body">
                                                                        <p class="card-text text-muted">by --{{data.preached_by_member.member.first_name}} {{data.preached_by_member.member.last_name}}--</p>                                                                                                                            
                                                                        <p class="card-text"><small class="text-muted">date - <b>{{data.date}}</b></small> </p>
                                                                </div>
                                                        </div>
                                                        <hr/>
                                                    </div>
                                            </div>
                                    </div>
                                </div>
                    </div>
                    <div class = "col-12 col-sm-10 col-md-8 col-lg-3" >
                            <div style="padding: 0px 0px 25px 10px">
                                    <a href="#" data-toggle="modal" data-target="#addSermon" style="text-decoration: none">
                                        <div class="add-button">
                                            + add sermon
                                        </div>
                                    </a>
                            </div>
                    </div>
                </div>
                <!-- add sermon -->
                <div class="modal fade" id="addSermon" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalCenterTitle">add sermon</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                            </div>
                            <div class="modal-body">                                                                                       
                                    <form>  
                                            <div class="row checkbox">
                                                    <div class="col-3"></div>
                                                    <div class="col-8">
                                                            <label><input type="checkbox" :value= true v-model = "non_member"> sermon by non-member </label>                                                            
                                                    </div>                                                                                                        
                                            </div>
                                            <hr/>          
                                            <div class=" row form-group" v-if="! non_member">                                                    
                                                <label class="col-3"><b>member:</b></label>
                                                <div class="col-8">
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
                                    </form>
                            </div>
                            <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal" v-on:click="">Close</button>
                            <button type="button" class="btn btn-success" v-on:click="addOffering()"><b>+</b> add sermon</button>
                            </div>
                        </div>
                        </div>
                </div>
            </div>
        </div>
    </template>
    
    <script>
    export default {
        name: 'sermons',
        data () {
            return{
                non_member: false,
                fetch_data_errors: null,
                sermons_available: false,
                sermons_today: null,
                this_month_selected: false,
                sermons_this_month: null,
            //search fro member
                memberSearch: '',found_members:[],
                memberSearch_status: '',selectedMember: null,
                showMemberInput: false
            }
        },
        created () {
           this.fetchData() 
           this.debouncedGetAnswer = _.debounce(this.getAnswer, 1000)
        },
        watch: {
        // watch for searching for member
        memberSearch: function () {        
                var array = this.memberSearch.split(" ")
                if (this.memberSearch.length > 0 && array.length == 1){
                    this.showMemberInput = true
                    this.memberSearch_status = 'typing...'                    
                    this.debouncedGetAnswer()
                }else{
                    this.memberSearch_status = ''
                    this.found_members = []
                    this.showMemberInput = false                
                }
            },
        },
        methods: {
            fetchData () {
                this.fetch_data_error = []
                this.$http.get(this.$BASE_URL + '/api/sermons/sermons-today/')
                    .then(response => {
                    this.sermons_today = {"response": response.data }
                    if (this.sermons_today.response.length > 0){
                        this.sermons_available = true
                    }
                    })
                    .catch((err) => {
                        this.fetch_data_error.push(err)
                    })
            },
            getSermonsThisMonth: function () {
                this.this_month_selected = true
                this.$http.get(this.$BASE_URL + '/api/sermons/sermons-this-month/')
                    .then(response => {
                    this.sermons_this_month = {"response": response.data }
                    })
                    .catch((err) => {
                        this.fetch_data_error.push(err)
                    }) 
            },
            //search for member
            getAnswer: function () {
            var vm = this
            if (this.memberSearch.length > 0){
                this.found_members = []
                this.memberSearch_status = 'searching...'
                this.$http.get(this.$BASE_URL + '/api/members/filter-by-first_name/' + this.memberSearch +'/')
                .then(function (response) {
                    vm.found_members = {"response": response.data } 
                    vm.memberSearch_status = '' 
                    console.log(vm.showMemberInput)
                    console.log(vm.found_members.response)                              
                })
                .catch(function (error) {
            
                })                
                }
            },
            selectMember: function(id,first_name,last_name) {                
                this.selectedMember = id          
                this.memberSearch =  first_name + ' ' + last_name 
                this.memberSearch_status = ''
                this.showMemberInput = false
            },
        }
    }
    </script>
    
    
    <style >
    </style>
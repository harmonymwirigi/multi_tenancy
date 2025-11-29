<template>
        <div>
            <nav aria-label="breadcrumb" class="continer">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li> 
                        <li class="breadcrumb-item active" aria-current="page">services</li>
                    </ol>
            </nav> 
            <div class = "continer">
                <div class = "row">
                    <div class = "col-12 col-sm-10 col-md-8 col-lg-2">
                            <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                                    <a class="action-list list-group-item list-group-item-action border-0 active" id="v-pills-expenditure-tab" data-toggle="pill" href="#v-pills-this-month" role="tab" aria-controls="v-pills-this-month" aria-selected="true" >all services</a>
                                    <a class="action-list list-group-item list-group-item-action border-0 " id="v-pills-income-tab" data-toggle="pill" href="#v-pills-today" role="tab" aria-controls="v-pills-today" aria-selected="false">services today</a>                                     
                            </div>
                    </div>
                    <div class = "col">
                            <div class="tab-content" id="v-pills-tabContent">
                                <!-- services today tab -->
                                    <div class="tab-pane fade show " id="v-pills-today" role="tabpanel" aria-labelledby="v-pills-today-tab">
                                        <div v-if = "! services_available">
                                            <div class="mb-5 text-center text-muted">
                                                <h3>Oops!</h3>
                                                <h5>There are no services in session today</h5>                                                
                                            </div>
                                            <hr>
                                        </div>
                                        <div v-if = "services_available">    
                                            <h3>Services Today</h3>                                                                                  
                                                <table class="table table-responsive-sm table-borderless">
                                                        <thead>
                                                            <tr>                                                            
                                                            <th scope="col">Service</th>                                                            
                                                            <th scope="col">venue</th>
                                                            <th scope="col">starts</th>
                                                            <th scope="col">ends</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody v-if="services_today">
                                                            <tr class="text-muted" v-for="data in services_today.response">                                                             
                                                                <td>
                                                                <router-link class="text-secondary"  
                                                                    :to="`/service-bookings/`+ data.service.id + `/`">                                                         
                                                                    {{data.service.type.name}} (today)
                                                                </router-link>
                                                                </td>                                                            
                                                                <td>{{data.service.venue}}</td>
                                                                <td>{{data.service.start}}</td>
                                                                    <td>{{data.service.end}}</td>
                                                            </tr>                                                              
                                                        </tbody>
                                                    </table>   
                                        </div>
                                    </div>
                               <!-- default is services in general tab -->
                                    <div class="tab-pane fade show active " id="v-pills-this-month" role="tabpanel" aria-labelledby="v-pills-this-month-tab">
                                        <h3>All Services </h3>
                                        <div v-if = "this_month_selected">
                                               <!-- table of services  -->
                                               <table class="table table-responsive-sm table-borderless">
                                                    <thead>
                                                        <tr>                                                            
                                                        <th scope="col">Service</th>                                                        
                                                        <th scope="col">venue</th>
                                                        <th scope="col">starts</th>
                                                        <th scope="col">ends</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody v-if="services_this_month">
                                                        <tr class="text-muted" v-for="data in services_this_month.response">                                                             
                                                            <td>
                                                            <router-link class="text-secondary"  
                                                                :to="`/service-bookings/`+ data.service.id + `/`">                                                         
                                                                {{data.service.type.name}} ({{$humanizeDate(data.service.date)}})
                                                            </router-link>
                                                            </td>                                                            
                                                            <td>{{data.service.venue}}</td>
                                                            <td>{{data.service.start}}</td>
                                                            <td>{{data.service.end}}</td>
                                                        </tr>                                                              
                                                    </tbody>
                                                </table>                                                
                                        </div>
                                    </div>
                            </div>
                    </div>
                    <div class = "col-12 col-sm-10 col-md-8 col-lg-3" >                          
                            <div class="btn-group" style="padding: 0px 0px 25px 10px">
                                    <a href="#" data-toggle="modal" data-target="#addService" style="text-decoration: none">
                                        <div class="add-button">
                                            <b>+</b> add service
                                        </div>
                                    </a>
                                    <button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
                                            <span class="sr-only">Toggle Dropdown</span>
                                    </button>
                                    <div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">                            
                                        <a class="dropdown-item" href="#" data-toggle="modal" data-target="#addServiceType"><b>+</b> add service type</a>                                                                
                                    </div>
                            </div>
                    </div>
                </div>
                <!-- add service -->
                <div class="modal fade" id="addService" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalCenterTitle">add service</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                            </div>
                            <div class="modal-body">  
                                <div class="row form-group">
                                        <label class="col-3"><b>type:</b></label>                                                                                                                                                     
                                        <select class="col-4 form-control" v-model="service_type" >
                                            <option v-for="data in service_types.response" :value="data.id" >{{data.name}}</option>
                                        </select>
                                        <a href=# class="col-2 text-success" data-toggle="modal" data-target="#addServiceType">
                                            <p class="mt-1">+ Add</p>
                                        </a>
                                        <p v-if="service_type_errors.length">
                                                <ul>
                                                        <small><li v-for="error in service_type_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                </ul>
                                        </p>
                                </div>                            
                                <div class="row form-group">
                                        <label class="col-3"><b>venue:</b></label>
                                        <input type="text" class=" col-8 form-control" placeholder="venue for the service" v-model="service_venue">                                                                                         
                                        <p v-if="service_venue_errors.length">
                                                <ul>
                                                        <small><li v-for="error in service_venue_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                </ul>
                                        </p>
                                </div>                                 
                                <div class="row form-group">
                                        <label class="col-3 "><b>date:</b></label>
                                        <div class="input-group form-group col-5" style="padding: 0px" >
                                            <input type="date" name="bday" max="3000-12-31" 
                                                   min="1000-01-01" class="form-control" v-model="service_date">                                                                                                                      
                                        </div>  
                                        <p v-if="service_date_errors.length">
                                                <ul>
                                                        <small><li v-for="error in service_date_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                </ul>
                                        </p>                                 
                                </div>                                 
                                <div class="row form-group">                                    
                                        <label class="col-3"><b>period:</b></label>
                                        <div class="col-8">
                                            <div class="d-flex form-group">
                                                    <div class="">
                                                            <label class="col-2">from</label>
                                                            <input type="time" class=" col-12 form-control" v-model="service_start"> 
                                                    </div>
                                                    <div class="ml-1">
                                                        <label class="col-2">to</label>
                                                        <input type="time" class=" col-12 form-control" v-model="service_end"> 
                                                    </div>
                                            </div>
                                        </div>
                                        <p v-if="service_period_errors.length">
                                                <ul>
                                                        <small><li v-for="error in service_period_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                </ul>
                                        </p>
                                </div>                                 
                                <div class="row form-group">
                                        <label class="col-3"><b>Lesson:</b></label>
                                        <input type="text" class=" col-8 form-control" placeholder="lesson to be taught" v-model="service_action">                                                                                                                                
                                </div>                                                           
                                <div class="row form-group">
                                        <label class="col-3"><b>description:</b></label>
                                        <input type="text" class=" col-8 form-control" placeholder="brief description of the lesson" v-model="service_value">                                                                                                                                 
                                </div> 
                                <div class="row form-group">
                                        <label class="col-3"><b>max attendance:</b></label>
                                        <input type="number" class=" col-8 form-control" v-model="service_max_attendance">                                                                                                                                
                                </div> 
                            </div>
                            <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal" >Close</button>
                            <button type="button" class="btn btn-success" v-on:click="addService()">
                                <b>+</b> add service
                                <span v-if="adding_service"
                                        class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                </span>
                            </button>
                            </div>
                        </div>
                        </div>
                </div>
                <!-- add service type -->
                <div class="modal fade" id="addServiceType" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalCenterTitle">add service type</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                            </div>
                            <div class="modal-body">                                 
                                    <form>                                            
                                            <div class="row form-group">
                                                    <label class="col-3"><b>name:</b></label>
                                                    <input  type="text" class=" col-8 form-control" 
                                                            v-model="service_type_name" placeholder="eg. main service">                                                    
                                                    <p v-if="service_type_name_errors.length">
                                                        <ul>
                                                                <small><li v-for="error in service_type_name_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                        </ul>
                                                    </p>
                                            </div>                                    
                                            <hr/>   
                                            <div class="row form-group">
                                                <label class="col-3"><b>describe:</b></label>
                                                <textarea type="text" class="col-8 form-control" rows='3' v-model="service_type_description"></textarea>                                                   
                                            </div>  
                                            <div class="row form-group">
                                                <label class="col-3"><b>starts:</b></label>
                                                <input type="time" class="col-8 form-control" v-model="service_start_time">                                                   
                                            </div>
                                            <div class="row form-group">
                                                <label class="col-3"><b>ends</b></label>
                                                <input type="time" class="col-8 form-control" v-model="service_end_time">                                                   
                                            </div> 
                                                                                                                         
                                    </form>
                            </div>
                            <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-success" v-on:click="addServiceType()">
                                <b>+</b> add service type
                                <span v-if="adding_service"
                                        class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                </span>
                            </button>
                            </div>
                        </div>
                        </div>
                        </div>
            </div>
        </div>
    </template>
    
    <script>
    export default {
        name: 'services',
        data () {
            return{
                fetch_data_error: [],
                services_today: null,
                services_available: false,
                this_month_selected: false,
                service_items: null,
                services_this_month: null,
                service_types: null,
            //add service
                adding_service: false,
                service_type: 0,service_type_errors: [],
                service_venue: null,service_venue_errors: [],
                service_date: null,service_date_errors: [],
                service_start: null,service_period_errors: [],
                service_end: null,
                service_action: null,service_action_errors: [],
                service_value: null,service_value_errors: [],
                service_max_attendance: null,
        //add service type
                service_type_name: '',
                service_type_description: '',
                service_type_name_errors: [],
                service_start_time:null,
                service_end_time:null,
                added_income_type: [],
            }
        },
        created () {
           this.fetchData() 
           this.getServiceTypes()
           this.getServicesThisMonth()
        },
        methods: {
            fetchData () {
                this.fetch_data_error = []
                this.$store.dispatch('update_isLoading', true)
                this.$http.get(this.$BASE_URL + '/api/services/services-today/')
                    .then(response => {
                    this.services_today = {"response": response.data }
                    if (this.services_today.response.length > 0){
                        this.services_available = true                        
                    }                                       
                    this.$store.dispatch('update_isLoading', false)
                    })
                    .catch((err) => {
                        this.fetch_data_error.push(err)
                        this.$store.dispatch('update_isLoading', false)
                    })            
            },
            getServicesThisMonth: function () {
                this.this_month_selected = true
                this.$store.dispatch('update_isLoading', true)
                this.$http.get(this.$BASE_URL + '/api/services/services-this-month/')
                    .then(response => {
                    this.services_this_month = {"response": response.data }
                    this.$store.dispatch('update_isLoading', false)
                    })
                    .catch((err) => {
                        this.fetch_data_error.push(err)
                        this.$store.dispatch('update_isLoading', false)
                    }) 
            },
            //get service types
            getServiceTypes: function(){
                this.$store.dispatch('update_isLoading', true)
                this.$http.get(this.$BASE_URL + '/api/services/service-types/')                
                    .then(response => {
                    this.service_types =  {"response":response.data}
                    this.$store.dispatch('update_isLoading', false)
                    })
                    .catch((err) => {
                        this.found_service = []
                        this.$store.dispatch('update_isLoading', false)
                    })
            },
            //check if add service form is okay
            checkAddServiceForm: function(){
                this.service_type_errors = []
                this.service_venue_errors = []
                this.service_date_errors = []
                this.service_period_errors = []                
                this.service_action_errors = []
                this.service_value_errors = []
                
                if (this.service_type > 0
                    && this.service_venue != null
                    && this.service_date != null
                    && this.service_start != null
                    && this.service_end != null){
                        return true
                    }
                if (this.service_type == 0){
                        this.service_type_errors.push("select service type")
                        return false
                }
                if (this.service_venue == null
                    || this.service_venue.length < 1){
                        this.service_venue_errors.push("enter service venue")
                        return false
                }
                if (this.service_date == null
                    || this.service_date.length < 1){
                        this.service_date_errors.push("enter service date")
                        return false
                }
                  if (this.service_start == null
                    || this.service_start.length < 1){
                        this.service_period_errors.push("enter service start time")
                        return false
                }
                if (this.service_end == null
                    || this.service_end.length < 1){
                        this.service_period_errors.push("enter service ending time")
                        return false
                }            
            },
            //add service 
            addService: function(){
                if (this.checkAddServiceForm()){
                    this.adding_service = true
                    this.$http({                        
                        method: 'post',
                        url: this.$BASE_URL + '/api/services/add-service/',
                        data: {
                            service_type_id: this.service_type,                                                                                               
                            venue: this.service_venue,                                
                            date: this.service_date,                        
                            start: this.service_start + ':00',
                            end: this.service_end   + ':00',                                                   
                            max_attendance: this.service_max_attendance
                        }
                        }).then(response => { 
                            this.adding_service = false                             
                            this.service_venue = null
                            this.service_date = null
                            this.service_start = null
                            this.service_end = null                                                              
                            alert("service succesfully added ")                     
                            this.addServiceItem(response.data.id)                    
                        })
                        .catch((err) => {
                            this.adding_service = false
                            alert("error, try again later")
                        }) 
                }
            },
            addServiceItem: function(service_id){
                this.adding_service = true
                this.$http({                        
                        method: 'post',
                        url: this.$BASE_URL + '/api/services/add-service-item/',
                        data: {
                                service_id: service_id,                                                                                               
                                action: this.service_action,                                
                                value: this.service_value                                                                                    
                        }
                        }).then(response => {                                                         
                            this.adding_service = false
                            this.fetchData()
                            this.getServicesThisMonth()
                            this.service_action = null
                            this.service_value = null
                        })
                        .catch((err) => {
                            this.adding_service = false
                            alert("error, try again later")
                        })
            },
            serviceTypeFormOkay: function(){  
            this.service_type_name_errors = []

            if (this.service_type_description.length < 1){
                this.service_type_description = "none given"
            }        
            if (this.service_type_name.length > 0){
                return true
            }
            if (this.service_type_name.length < 1){                
                this.service_type_name_errors.push("name required")
                return false
            }
        },
        addServiceType: function(){        
            if (this.serviceTypeFormOkay()){
                this.adding_service = true
                this.$http({                        
                        method: 'post',
                        url: this.$BASE_URL + '/api/services/service-types/',
                        data: {
                                name: this.service_type_name,                                
                                description: this.service_type_description,
                                start:this.service_start_time,
                                end:this.service_end_time                                                                         
                        }
                        }).then(response => {              
                               this.adding_service = false                
                               this.service_type_name = '',                               
                               this.service_type_description = '' 
                               alert("service type succesfully added")  
                               this.getServiceTypes()                    
                        })
                        .catch((err) => {
                            this.adding_service = false
                            alert("error, try again later") 
                        }) 
            }
        }
        }
    }
    </script>
    
    
    <style >
    </style>
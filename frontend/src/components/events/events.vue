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
                        <li class="breadcrumb-item active" aria-current="page">events</li>
                    </ol>
            </nav> 
            <div class = "continer">
                <div class="row">
                       <div class="col">
                           <!-- filters for events             -->
                            <div class="row">                                        
                                    <div class="col">                    
                                        <div class="row">
                                            <!-- list and calendar views -->
                                            <div class="col-6 col-lg-2">
                                                    <div class="form-group">                                    
                                                        <select class="form-control" v-model="view">
                                                            <option value="list">list</option>
                                                            <option value="calendar">calendar</option>                                        
                                                        </select>
                                                    </div>
                                            </div>   
                                              <!--add button on smaller devices -->
                                              <div class="col-6 btn-group d-sm-block d-md-none text-right">
                                                <div style="padding: 0px 0px 25px 10px">
                                                        <button class="btn btn-success" data-toggle="modal" data-target="#addEvent">                                                            
                                                                <b>+</b> add  event                                                
                                                        </button>
                                                </div>
                                            </div>                                         
                                        </div>
                                    </div>                                  
                            </div>
                            <!-- calendar view -->
                            <vue-cal  v-if="view == `calendar`"                          
                                :disable-views="['years', 'year']"
                                default-view="month"                
                                events-on-month-view="short"                        
                                :events="events"                        
                                style="height: 600px">
                            </vue-cal>
                            <!-- list view    -->
                            <div v-if="view == `list`">
                                <div v-for="event in events">
                                    <div class="card mb-5">        
                                        <div class="mt-3 ml-3">
                                            <img style="width: 45px ;height: auto" src="@/assets/icons/icons8-schedule-64.png">
                                        </div>
                                        <div class="card-body">
                                            <h5 class="card-title">                                       
                                                {{event.title}}
                                            </h5>
                                            <h5 class="text-muted">
                                                {{event.start}} ---> {{event.end}} 
                                                @ {{event.location}}                                        
                                            </h5>
                                            
                                            <p class="card-text text-muted">{{event.description}}</p>
                                            <div class="row">
                                                <div class="col text-right">                                                    
                                                    <span class="backButton">
                                                        <router-link class="text-primary" style="text-decoration: none"  :to="`/eventDetail/`+ event.id + `/`">                                                         
                                                            Mark register
                                                        </router-link>
                                                    </span>                                                    
                                                </div>                                           
                                            </div>                                   
                                        </div>
                                    </div>
                                </div>                                                
                            </div>
                       </div>
                       <!-- add button -->
                        <div class = "col-12 col-sm-10 col-md-8 col-lg-3 d-none d-lg-block" >
                                <div style="padding: 0px 0px 25px 10px">
                                        <a href="#" data-toggle="modal" data-target="#addEvent" style="text-decoration: none">
                                            <div class="add-button">
                                                <b>+</b> add upcoming event
                                            </div>
                                        </a>
                                </div>
                        </div>
                </div>
            </div>            
            <!--add event Modal -->
            <div class="modal fade" id="addEvent" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalCenterTitle">add an upcoming event</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close" v-on:click="fetchData()">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        </div>
                        <div class="modal-body">
                                <form>
                                        <div class=" row form-group">
                                            <label class="col-3"><b>title:</b></label>
                                            <input type="text" class="col-8 form-control" maxlength="20"
                                                    placeholder="enter title of event" v-model="event_title">                                        
                                            <p v-if="event_title_errors.length">
                                                <ul>
                                                        <small><li v-for="error in event_title_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                </ul>
                                            </p>
                                        </div>
                                        
                                        <div class="row form-group">
                                                <label class="col-3"><b>location:</b></label>
                                                <input type="text" class="col-8 form-control" maxlength="20"
                                                        placeholder="enter event location" v-model="event_location">                                        
                                                <p v-if="event_location_errors.length">
                                                    <ul>
                                                            <small><li v-for="error in event_location_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                    </ul>
                                                </p>
                                        </div>
                                        <hr/>
                                        <div class="form-group">
                                                <div class="row">
                                                        <label class="col-3"><b> start date:</b></label>
                                                        <div class="col-8">
                                                            <input type="date" name="bday" max="3000-12-31" 
                                                            min="1000-01-01" class="form-control" v-model="start_date"> 
                                                            <p v-if="start_date_errors.length">
                                                                <ul>
                                                                        <small><li v-for="error in start_date_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                                </ul>
                                                            </p>

                                                            <label class="col-3">from</label>                                                                                                                 
                                                            <input type="time" class=" col-8 form-control" v-model="start_time"> 

                                                            <p v-if="start_time_errors.length">
                                                                <ul>
                                                                        <small><li v-for="error in start_time_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                                </ul>
                                                            </p>
                                                        </div>
                                                </div>
                                        </div>
                                        <hr/> 
                                        <div class="form-group">
                                            <div class="row">
                                                    <label class="col-3"><b> end date:</b></label>
                                                    <div class="col-8">
                                                        <input type="date" name="bday" max="3000-12-31" 
                                                        min="1000-01-01" class="form-control" v-model="end_date"> 
                                                        <p v-if="end_date_errors.length">
                                                            <ul>
                                                                    <small><li v-for="error in end_date_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                            </ul>
                                                        </p>

                                                        <label class="col-3">to</label>
                                                        <input type="time" class=" col-8 form-control" v-model="end_time">                                                          
                                                    </div>
                                            </div>
                                        </div>                                                        
                                        <div class="row form-group">
                                                <label class="col-3"><b>description:</b></label>
                                                <textarea type="text" class="col-8 form-control" 
                                                        maxlength="150"
                                                        rows='3' v-model="event_description">
                                                </textarea>                                                   
                                        </div>                                                                                  
                            
                                </form>
                        </div>
                        <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal" v-on:click="fetchData()">Close</button>                       
                        <button type="button" class="btn btn-success" v-on:click="addEvent()">
                            {{add_event_button_text}}
                            <span v-if="adding_event"
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
    import VueCal from 'vue-cal'
    import 'vue-cal/dist/vuecal.css'

    export default {
        components: { VueCal },
        name: 'events',
        data () {
            return{
                //fetch data
                fetch_data_error: [],               
                events_available: false,
                add_event_button_text: 'add event',
                view: "list",
                //add event                
                event_title: '',event_title_errors: [],
                event_location: '',event_location_errors: [],                
                event_description: '',                
                start_date: '',start_time:'',start_date_errors:[], start_time_errors:[],
                end_date: '',end_time:'',end_time_errors:[], end_date_errors:[],
                added_event: [],
                adding_event:false,
                //events
                events: []


            }
        }, 
        created () {
           this.checkLoggedIn()
           this.fetchData() 
        },
        methods: {
            humanize: function(x) {
                return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            },
            checkLoggedIn() {
                if (!this.$session.has("token")) {
                    router.push("/login")
                }
            },
            fetchData () {
                this.$store.dispatch('update_isLoading', true)
                this.$http.get(this.$BASE_URL + '/api/events/event-list/')
                .then(response => {
                    this.events = response.data              
                    this.$store.dispatch('update_isLoading', false)        
                })
                .catch((err) => {
                    this.fetch_data_error.push(err)
                    this.$store.dispatch('update_isLoading', false)
                })
            },
            //check if the add event form is okay
            addEventFormOkay: function (){
                this.event_title_errors = []
                this.event_location_errors = []
                this.start_date_errors = []
                this.start_time_errors = []
                this.end_date_errors = []
                this.end_time_errors = []
                if (this.event_title.length > 0
                    && this.event_location.length > 0
                    && this.event_description.length > 0
                    && this.start_date.length > 0
                    && this.start_time.length > 0
                    && this.end_date.length > 0
                    && this.end_time.length > 0){
                        return true
                    }
                if (this.event_title.length == 0){
                    this.event_title_errors.push("a title to the event needed")
                    return false
                }
                if (this.event_location.length == 0){
                    this.event_location_errors.push("location of the event needed")
                    return false
                }
                if (this.event_description.length == 0){
                    this.event_description = "none given"                    
                }
                if (this.start_date.length == 0){
                    this.start_date_errors.push("select a starting date for the event")
                    return false
                }
                if (this.end_date.length == 0){
                    this.end_date_errors.push("select an ending date for the event")
                    return false
                }
                if (this.start_time.length != 4
                    || this.start_time.split(":") != 2 ){
                    this.start_time_errors.push("use HH:MM format for time")
                    return false
                }
                if (this.end_time.length != 4
                    || this.end_time.split(":") != 2 ){
                    this.end_time_errors.push("use HH:MM format for time")
                    return false
                }
            },
            addEvent: function (){                
                if (this.addEventFormOkay()){                    
                    this.adding_event = true                    
                    this.$http({                        
                        method: 'post',
                        url: this.$BASE_URL + '/api/events/add-event/',
                        data: {
                                title: this.event_title,                                                                                               
                                description: this.event_description,                                
                                location: this.event_location,                        
                                start_date: this.start_date,
                                start_time: this.start_time,
                                end_date: this.end_date,
                                end_time: this.end_time                            
                        }
                        }).then(response => {                              
                               this.event_title = ''
                               this.event_location = ''
                               this.event_description = ''
                               this.start_date = ''
                               this.start_time = ''
                               this.end_date = ''
                               this.end_time = ''                                                                                            
                               this.adding_event = false
                               alert("event succesfully added ")                                                    
                        })
                        .catch((err) => {
                            this.adding_event = false
                            alert("an error occurred when trying to add event, check your form and try again")
                        }) 
                }                       
            }
        }
    }
    </script>
    
    
    <style >
    </style>
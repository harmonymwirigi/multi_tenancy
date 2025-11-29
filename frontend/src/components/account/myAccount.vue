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
                    <li class="breadcrumb-item active" aria-current="page">church account</li>
                </ol>
        </nav>
        <!-- MAIN continer -->
        <section class="continer">                
            <div class="row">
                <div class="mb-5 col-sm-12 col-lg-3">
                    <!-- spacer div -->
                    <nav class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                            <a  
                                class="nav-link active list-group-item list-group-item-action border-0"
                                id="pill-detail-tab" 
                                data-toggle="pill" href="#pill-dashboard" role="tab"
                                aria-controls="pill-dashboard" aria-selected="true">
                                    <img class="church-is-menu" src="@/assets/icons/icons8-group-of-projects-filled-50.png"> 
                                    dashboard
                            </a>                                                                
                            <a 
                                class="nav-link list-group-item list-group-item-action border-0" 
                                id="pill-user-accounts-tab" data-toggle="pill" 
                                href="#pill-user-accounts" role="tab" aria-controls="pill-user-accounts"
                                aria-selected="false" @click="getPermissionGroups">
                                <img class="church-is-menu" src="@/assets/icons/icons8-contacts-208.png">
                                    user accounts
                            </a>                                                        
                    </nav>
                </div>
                <!-- content div -->
                <div 
                    class="tab-content col-sm-12 col-lg-9" 
                    id = "v-pills-tabContent"
                    v-if="client_detail_available">
                    <!-- DASHBOARD -->
                    <section  
                        class="tab-pane fade show active" 
                        id="pill-dashboard" role="tabpanel" aria-labelledby="pill-dashboard-tab">
                        <section class="row">
                                <div class="col-lg-6 col-sm-12">
                                    <h3 class="font-weight-bold">{{client_details[0].client.name}}</h3>
                                    <h6 class="card-subtitle text-muted mb-2">
                                            church code
                                            <span class="badge badge-light text-info">
                                                <h5>{{client_details[0].church_code}}</h5></span>                       
                                    </h6>
                                </div>
                                <div class="col-lg-6 col-sm-12">                                                                      
                                        <button disabled type="button" class="btn btn-success">
                                            SMS credit
                                        </button> 
                                        <p>mpesa paybill : 
                                            <i v-if="sms_credentials.length" class="text-muted">{{sms_credentials[0].at_mpesa_paybill}}</i>
                                        </p>                                    
                                        <p>mpesa account number : 
                                            <i v-if="sms_credentials.length"class="text-muted">{{sms_credentials[0].at_mpesa_acc_no}}</i>
                                        </p> 
                                </div>                           
                        </section>                           
                        <!-- numbers in boxes -->
                        <section class="d-flex justify-content-center">
                                <div class="row col text-left mt-2">
                                        <div class="mb-2 ml-3 text-center text-muted col-lg-2 col-sm-12 border border-secondary rounded">
                                            <h1 class="font-weight-bold">{{client_details[0].number_of_members}} </h1>
                                            members
                                        </div> 
                                        <div class="mb-2 ml-3 text-center text-muted col-lg-2 col-sm-12 border border-secondary rounded">
                                                <h1 class="font-weight-bold">{{client_details[0].number_of_sms}}</h1>
                                                sms delivered this month
                                        </div>                                             
                                        <div class="mb-2 ml-3 text-center text-muted col-lg-2 col-sm-12 border border-secondary rounded">
                                                <h1 class="font-weight-bold">{{client_details[0].site_visitors.this_month}}</h1>
                                                website visits this month<br/>
                                                <i>{{client_details[0].site_visitors.last_month}} last month</i>
                                        </div>                                 
                                                                    
                                </div> 
                        </section>
                        
                        <!-- church statements -->
                        <section class="mt-5">
                            <h3 class="font-weight-bold text-muted">Website Management</h3>
                            <a :href="`http://` + client_details[0].domain_url" target="_blank">
                                {{client_details[0].domain_url}}
                            </a>                            
                            <!-- church-statements -->
                            <section class="mt-5">
                                <h4>church statements</h4>
                                <h6 >mission statement</h6>
                                <article class="text-muted" >
                                                                    
                                    <textarea v-if="church_statements.length" 
                                                rows="3" class="form-control mb-2" v-model="mission_statement">
                                    </textarea> 
                                    <h5 class="text-muted text-center" v-if="! church_statements.length">
                                        <p>Oops!</p>
                                        <p>You have not added your church's mission statement</p>
                                        <button class="btn btn-outline-success" data-toggle="modal" data-target="#addVisionAndMisionStatement">
                                            + add mission statement
                                            <span v-if="updating"
                                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                            </span>
                                        </button>
                                    </h5>
                                    <div class="text-right" v-if="church_statements.length">
                                        <button class="btn btn-outline-success" v-on:click="editChurchStatements()">
                                            save
                                            <span v-if="updating"
                                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                            </span>
                                        </button>
                                    </div>
                                </article>

                                <h6 >vision statement</h6>
                                <article class="border border-light text-muted" >                                   
                                    <textarea v-if="church_statements.length" 
                                                rows="3" class="form-control mb-2" v-model="vision_statement">
                                    </textarea> 
                                    <h5 class="text-muted text-center" v-else>
                                        <p>Oops!</p>
                                        <p>You have not added your church's vision statement</p>
                                        <button class="btn btn-outline-success" data-toggle="modal" data-target="#addVisionAndMisionStatement">
                                            + add vision statement
                                            <span v-if="updating"
                                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                            </span>
                                        </button>
                                    </h5>
                                    <div class="text-right" v-if="church_statements.length">
                                        <button class="btn btn-outline-success" v-on:click="editChurchStatements()">
                                            save
                                            <span v-if="updating"
                                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                            </span>
                                        </button>
                                    </div>
                                </article>
                            </section>
                            <!-- church  about -->
                            <section>
                                <h4>About church</h4>
                                <article class="text-muted" >                                    
                                    <textarea v-if="church_about.length" 
                                                rows="3" class="form-control mb-2" v-model="about_church">
                                    </textarea> 
                                    <div class="text-right" v-if="church_about.length">
                                        <button class="btn btn-outline-success" v-on:click="editAbout()">
                                            save
                                            <span v-if="updating_about"
                                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                            </span>
                                        </button>
                                    </div>
                                    <h5 class="text-muted text-center" v-if="! church_about.length">
                                        <p>Oops!</p>
                                        <p>You have not added an about for your church</p>                                        
                                        <button class="btn btn-outline-success" data-toggle="modal" data-target="#addChurchAbout">
                                            + add
                                            <span v-if="updating"
                                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                            </span>
                                        </button>
                                    </h5>
                                </article>
                            </section>
                                <!-- church  core values -->
                            <section>
                                    <h4>church core values</h4>
                                    <article class="" >
                                        <p v-if="church_core_values.length">                                            
                                            <ul class="list-group list-group-flush text-muted">
                                                    <li class="list-group-item" v-for="value in church_core_values">
                                                        {{value.value}}
                                                    </li>                                                  
                                            </ul>
                                        </p>
                                        <div class="text-right" v-if="church_core_values.length">
                                                <button class="btn btn-outline-success" data-toggle="modal" data-target="#addChurchCoreValue">
                                                        + add
                                                        <span v-if="updating"
                                                            class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                                        </span>
                                                </button>
                                        </div>                                       
                                        <h5 class="text-muted text-center" v-if="! church_core_values.length">
                                            <p>Oops!</p>
                                            <p>You have not added your church's church core values</p>
                                            <button class="btn btn-outline-success" data-toggle="modal" data-target="#addChurchCoreValue">
                                                + add
                                                <span v-if="updating"
                                                    class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                                </span>
                                            </button>
                                        </h5>
                                    </article>
                            </section>
                            <!-- church periodic theme -->
                            <section>
                                    <h4>church periodic themes</h4>                                    
                                    <article class="" >
                                        <p v-if="church_periodic_themes.length">                                            
                                            <ul class="list-group list-group-flush text-muted">
                                                    <li class="list-group-item" v-for="theme in church_periodic_themes">
                                                        {{theme.theme}} 
                                                        <p>start: {{theme.start}} and end: {{theme.end}}</p>
                                                        <p></p>
                                                    </li>                                                  
                                            </ul>
                                        </p>
                                        <div class="text-right" v-if="church_periodic_themes.length">
                                                <button class="btn btn-outline-success" data-toggle="modal" data-target="#addThemeModal">
                                                        + add 
                                                        <span v-if="updating"
                                                            class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                                        </span>
                                                </button>
                                        </div>  
                                        <h5 class="text-muted text-center"  v-if="! church_periodic_themes.length">
                                            <p>Oops!</p>
                                            <p>You have not added your church's Periodic Theme</p>
                                            <button class="btn btn-outline-success" data-toggle="modal" data-target="#addThemeModal">
                                                + add theme
                                                <span v-if="updating"
                                                    class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                                </span>
                                            </button>
                                        </h5>
                                    </article>
                            </section>
                        </section>                        
                    </section>   

                    <!-- USER ACCOUNTS -->
                    <section  
                        class="tab-pane fade show active" 
                        id="pill-user-accounts" role="tabpanel" aria-labelledby="pill-user-accounts-tab">
                        <userAccounts/>
                    </section>                                         
                </div>
            </div>                
        </section>
        <!-- MODALS continer -->
        <section>
            <!-- mission and vision statements modal -->
            <div class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" 
                aria-labelledby="addVisionAndMisionStatement" aria-hidden="true"
                id="addVisionAndMisionStatement">
                <div class="modal-dialog modal-lg">                            
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Add Mission and vision statement</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                                <div class="form-group">
                                    <label for="missionSatementsTextArea">Mission statement</label>
                                    <textarea   class="form-control" 
                                                v-model="mission_statement"
                                                id="missionSatementsTextArea" 
                                                rows="3"></textarea>
                                </div>
                                <div class="form-group">
                                    <label for="missionSatementsTextArea">vision statement</label>
                                    <textarea  class="form-control" 
                                                v-model="vision_statement"
                                                id="missionSatementsTextArea" 
                                                rows="3"></textarea>
                                </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-outline-success" v-on:click="addMissionAndVisionStatements()">
                                + add statements
                                <span v-if="adding_web_content"
                                    class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                </span>
                            </button>
                        </div>
                    </div>                                  
                </div>
            </div>
            <!-- mission and vision statements modal -->
            <div class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" 
                aria-labelledby="addChurchAbout" aria-hidden="true"
                id="addChurchAbout">
                <div class="modal-dialog modal-lg">                            
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Add about church</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                                <div class="form-group">
                                    <label for="missionSatementsTextArea">About church</label>
                                    <textarea   class="form-control" 
                                                v-model="about_church"
                                                id="missionSatementsTextArea" 
                                                rows="3"></textarea>
                                </div>                                
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-outline-success" v-on:click="addAboutChurch()">
                                + add about
                                <span v-if="adding_web_content"
                                    class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                </span>
                            </button>
                        </div>
                    </div>                                  
                </div>
            </div>
            <!-- add about modal -->
            <div class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" 
            aria-labelledby="addChurchAbout" aria-hidden="true"
            id="addChurchAbout">
            <div class="modal-dialog modal-lg">                            
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Add about church</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                            <div class="form-group">
                                <label for="missionSatementsTextArea">About church</label>
                                <textarea   class="form-control" 
                                            v-model="about_church"
                                            id="missionSatementsTextArea" 
                                            rows="3"></textarea>
                            </div>                                
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-outline-success" v-on:click="addAboutChurch()">
                            + add about
                            <span v-if="adding_web_content"
                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                            </span>
                        </button>
                    </div>
                </div>                                  
            </div>
            </div>
            <!-- add core value modal-->
            <div class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" 
                    aria-labelledby="addChurchCoreValue" aria-hidden="true"
                    id="addChurchCoreValue">
                <div class="modal-dialog modal-lg">                            
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Add church core value</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                                <div class="form-group">
                                    <label for="missionSatementsTextArea">value</label>
                                    <input autofocus class="form-control" type="text" maxlength="20" v-model="core_value">
                                </div>                                
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-outline-success" v-on:click="addCoreValue()">
                                + add value
                                <span v-if="adding_web_content"
                                    class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                </span>
                            </button>
                        </div>
                    </div>                                  
                </div>
            </div>
            <!-- add theme modal -->
            <div class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" 
                    aria-labelledby="addThemeModal" aria-hidden="true"
                    id="addThemeModal">
                <div class="modal-dialog modal-lg">                            
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Add church theme</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                                <div class="form-group">
                                    <label class="font-weight-bold">Theme:</label>
                                    <textarea   class="form-control" 
                                                v-model="theme"
                                                id="missionSatementsTextArea" 
                                                rows="3">
                                    </textarea>
                                    <label class="font-weight-bold">Description:</label>
                                    <textarea   class="form-control" 
                                                v-model="description"
                                                id="missionSatementsTextArea" 
                                                rows="3">
                                    </textarea>
                                    <div class="row">
                                        <div class="col-6">
                                            <label class="font-weight-bold">starts:</label>
                                            <input class="form-control" type="date" v-model="start">
                                        </div>
                                        <div class="col-6">
                                            <label class="font-weight-bold">Ends:</label>
                                            <input class="form-control" type="date" v-model="end"> 
                                        </div>
                                    </div>                                       
                                </div>                                
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-outline-success" v-on:click="addTheme()">
                                + add theme
                                <span v-if="adding_web_content"
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
import userAccounts from '@/subcomponents/accounts/userAccounts'
export default {
    name: 'myAccount',
    components: {userAccounts},
    data () {
        return{
            church_id: localStorage.getItem('church_id'),
            client_detail_available :false,
            client_details : null,
            church_about: null,
            church_statements: null,
            church_core_values:null,
            church_periodic_themes:null,
            //add mission and vision
            adding_web_content: false,
            mission_statement: null,
            vision_statement: null,
            //add church about
            about_church: null,
            //add core value
            core_value: null,
            //add theme
            theme:null,
            description:null,
            start:null,
            end:null,
            //updating
            updating: false,
            updating_about:false,
            sms_credentials:[]

        }
    },
    created () {
        this.getClientDetail() 
        this.getChurchSMSCredentials()
        this.getChurchStatements()
        this.getChurchCoreValues()
        this.getChurchPeriodicTheme()
        this.getChurchAbout()
    },
    methods: {
        getClientDetail: function(){
            this.$store.dispatch('update_isLoading', true)
            this.client_detail_available = true     
            this.$http.get(this.$BASE_URL + '/api/clients/client-detail/' + this.church_id +'/')
                .then(response => {
                    this.client_details = response.data       
                    this.$store.dispatch('update_isLoading', false)                                   
                
                })
                .catch((err) => {                     
                    this.$store.dispatch('update_isLoading', false)      
                })
        },
        //church sms credentials
        getChurchSMSCredentials: function(){
            this.$store.dispatch('update_isLoading', true)                                
            this.$http.get(this.$BASE_URL + '/api/clients/church-sms-credentials/' + this.church_id +'/')
                .then(response => {
                    this.sms_credentials = response.data                   
                    this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {                              
                    alert(err)
                    this.$store.dispatch('update_isLoading', false)
                })
        },
        //church statements
        getChurchStatements: function(){
            this.$store.dispatch('update_isLoading', true)                
            var church_id = localStorage.getItem('church_id')
            this.$http.get(this.$BASE_URL + '/api/clients/church-statements/' + this.church_id +'/')
                .then(response => {
                    this.church_statements = response.data 
                    this.mission_statement = this.church_statements[0].mission                                         
                    this.vision_statement = this.church_statements[0].vision  
                    this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {                              
                    this.$store.dispatch('update_isLoading', false)
                })
        },
        //church core values
        getChurchCoreValues: function(){
            this.$store.dispatch('update_isLoading', true)                                
            this.$http.get(this.$BASE_URL + '/api/clients/church-core-values/' + this.church_id +'/')
                .then(response => {
                    this.church_core_values = response.data                                          
                    this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {                              
                    this.$store.dispatch('update_isLoading', false)
                })
        },
        //church periodic themes
        getChurchPeriodicTheme: function(){
            this.$store.dispatch('update_isLoading', true)                                
            this.$http.get(this.$BASE_URL + '/api/clients/church-periodic-themes/' + this.church_id +'/')
                .then(response => {
                    this.church_periodic_themes = response.data                                          
                    this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {                              
                    this.$store.dispatch('update_isLoading', false)
                })
        },
        //church periodic themes
        getChurchAbout: function(){
            this.$store.dispatch('update_isLoading', true)                                
            this.$http.get(this.$BASE_URL + '/api/clients/church-about/' + this.church_id +'/')
                .then(response => {
                    this.church_about = response.data   
                    this.about_church = this.church_about[0].about                                       
                    this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {                              
                    this.$store.dispatch('update_isLoading', false)
                })
        },
        //add church vision and mission statements
        addMissionAndVisionStatements: function(){  
            this.adding_web_content = true
            this.$http.post(
                this.$BASE_URL + '/api/clients/add-church-mission-and-vision-statements/',
                {
                    church_id: this.church_id,
                    mission: this.mission_statement,
                    vision: this.vision_statement
                }
            ).then((response)=>{
                this.adding_web_content = false
                this.getChurchStatements()
                this.mission = response.data
                alert("church statements added successfuly")
                        
            })
            .catch((err)=>{
                this.adding_web_content = false
                alert("Error: " + err + " make sure you have filled both fields" )
            })
        },
        //add church about
        addAboutChurch: function(){
            this.adding_web_content =  true
            this.$http.post(
                this.$BASE_URL + '/api/clients/add-church-about/',
                {
                    church_id: this.church_id,
                    about: this.about_church
                }
            ).then((response)=>{
                this.adding_web_content = false
                this.getChurchAbout()                
                this.about_church = null
                alert("About church for your site was successfully added")

            }).catch((err)=>{
                this.adding_web_content = false
                alert("error :" + err)
            })
        },
        //add church core value
        addCoreValue: function(){
            this.adding_web_content =  true
            this.$http.post(
                this.$BASE_URL + '/api/clients/add-church-core-value/',
                {
                    church_id: this.church_id,
                    value: this.core_value
                }
            ).then((response)=>{
                this.adding_web_content = false
                this.getChurchCoreValues()                
                this.core_value = null
                alert("value succesfully added")

            }).catch((err)=>{
                this.adding_web_content = false
                alert("error :" + err)
            })
        },
        //add theme 
        addTheme: function(){
            this.adding_web_content =  true
            this.$http.post(
                this.$BASE_URL + '/api/clients/add-theme/',
                {
                    church_id: this.church_id,
                    theme: this.theme,
                    description: this.description,
                    start:this.start,
                    end:this.end
                }
                ).then((response)=>{
                    this.adding_web_content = false
                    this.getChurchPeriodicTheme()                
                    this.theme = null
                    this.description = null
                    this.start = null
                    this.end = null
                    alert("theme succesfully added")

                }).catch((err)=>{
                    this.adding_web_content = false
                    alert("error :" + err + "make sure to fill all the fields") 
                })
        },
        //edit church statements
        editChurchStatements: function(){
            this.updating = true //this toggles the button spinners
            this.$http.patch(
                this.$BASE_URL + '/api/clients/update-church-statements/',
                {
                    church_id:this.church_id,
                    mission:this.mission_statement,
                    vision:this.vision_statement
                }  
            ).then((response)=>{
                this.updating = false
                this.getChurchStatements()
            }).catch((err)=>{                    
                this.updating = false
                alert("error: " + err)
            })
        },
        //edit about church:
        editAbout: function(){
            this.updating_about = true
            this.$http.patch(
                this.$BASE_URL + '/api/clients/update-about-church/',
                {
                    church_id:this.church_id,
                    about:this.about_church
                }
            ).then(()=>{
                this.updating_about = false
                this.getChurchAbout()                    
            }).catch((err)=>{
                this.updating_about = false
                alert("error :" + err)
            })
        }           
    }
}
</script>
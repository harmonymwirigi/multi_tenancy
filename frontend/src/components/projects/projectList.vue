<template>
    <div >
        <nav aria-label="breadcrumb" class="continer">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li>
                    <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'generalFinance'}">finances</router-link></span></li> 
                    <li class="breadcrumb-item active" aria-current="page">projects</li>
                </ol>
        </nav>
        <div class="continer">        
        <div class="row">
            <!-- NAVIGATION ON THE LEFT -->
            <div class="col-12 col-sm-10 col-md-8 col-lg-2">
                    <div class="d-none nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                            <a class="action-list list-group-item list-group-item-action border-0"  data-toggle="pill" href="#inProgress" role="tab" aria-controls="members" aria-selected="true">
                              <img style="width: 20px; height: auto" src="@/assets/icons/icons8-present-48.png">
                              in-progress
                            </a>
                            <a class="action-list list-group-item list-group-item-action border-0"  data-toggle="pill" href="#completed" role="tab" aria-controls="activity" aria-selected="false" v-on:click="getGroupActivity()">
                                <img style="width: 20px; height: auto" src="@/assets/icons/icons8-future-64.png">
                                completed
                            </a>
                    </div>
            </div>
            <!-- CONTENT AT CENTER -->
            <div class="tab-content col">
                    <div class="tab-pane fade show active" id="inProgress" role="tabpanel" aria-labelledby="profile-tab"></div>
                    <h3 class="font-weight-bold"> Projects</h3>
                    <hr>
                    <p class="text-center">
                        <a class="btn btn-sm btn-outline-secondary dropdown-toggle" data-toggle="collapse" href="#statsTab" role="button" aria-expanded="false" aria-controls="statsTab">
                                more stats
                        </a>
                    </p>
                    <div class="collapse" id="statsTab">
                            <div class="card card-body outline-0">
                                <projectstats msg="expenditure stats"/>
                            </div>
                            <!-- show this button on smaller devices -->
                            <div class="d-sm-block d-md-none">
                                    <a href="#" data-toggle="modal" data-target="#addProject" style="text-decoration: none">
                                        <div class="btn btn-success add-button">
                                            <b>+</b> add project
                                        </div>
                                    </a>
                            </div>
                    </div>                                                          
                    <div class="col-8 center-div" v-if = "fetch_data_error.length > 0">
                        <div class = "center-div" >
                                <img style = "height: 64px "src="@/assets/icons/icons8-wi-fi-off-64.png">
                                <p class="text-info">check your connection</p>
                        </div>
                    </div>
                    <div v-if = "fetch_data_error.length == 0">                                      
                        <span>
                                found <span class="mt-4 badge badge-pill badge-secondary">{{foundItems}}</span>
                        </span> 
                    <table class="mt-4 table table-responsive-sm table-borderless">                     
                        <thead>                        
                            <th>project name</th>
                            <th>required</th>
                            <th>percentage funded</th>
                        </thead>                                                
                        <tbody>
                            <tr  v-for = "data in projects.response ">                    
                                                          
                            <td>
                                <router-link class="text-secondary" style="text-decoration: none;"  :to="`/projectDetail/`+ data.id + `/`">                                                         
                                    {{data.name}}
                                </router-link>
                            </td>                            
                            <td>
                                    KSh {{humanize(data.required_amount)}}
                            </td>
                            <td class="text-secondary"> 
                                    {{data.percentage_funded}} %
                            </td>
                            <td>
                                <router-link class="text-muted" style="text-decoration: none;"  :to="`/projectDetail/`+ data.id + `/`">                                                         
                                    <img style="width: 20px ;height: auto" src="@/assets/icons/icons8-right-arrow-50.png">
                                </router-link>
                            </td> 
                            </tr>             
                        </tbody>
                    </table>
                </div>
            </div>
            <!-- ACTIONS ON THE RIGHT -->
            <div class="col-12 col-sm-10 col-md-5 col-lg-3">
                    <!-- add button top left -->
                    <div style="padding: 0px 0px 25px 10px">
                            <a href="#" data-toggle="modal" data-target="#addProject" style="text-decoration: none">
                                <div class="btn btn-success add-button">
                                    <b>+</b> add project
                                </div>
                            </a>
                    </div>

                    <!-- more actions  -->
                    <div class="list-group font-weight-bold">
                            <button type="button" class="d-flex justify-content-about font-weight-bold text-muted action-list list-group-item list-group-item-action border-0" data-toggle="modal" data-target="#exportToCSV" >
                              <img src="@/assets/icons/icons8-export-csv-30.png" style="width: 45px; height:auto"> Export To CSV
                            </button>                            
                    </div>


            </div>
            <!-- MODALS -->
            <!-- add project Modal -->
            <div class="modal fade" id="addProject" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalCenterTitle">add a project</h5>
                        <button type="button" class="close" data-dismiss="modal" v-on:click="fetchdata()" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        </div>
                        <div class="modal-body">
                                <form>
                                        <div class=" row form-group">
                                          <label class="col-3"><b>name:</b></label>
                                          <input type="text" class="col-8 form-control" placeholder="enter name of the project" v-model="project_name">                                        
                                        </div>
                                        <div class="row form-group">
                                                <label class="col-3"><b>description:</b></label>
                                                <textarea type="text" class="col-8 form-control" rows='3' v-model="project_description"></textarea>                                                   
                                        </div>
                                        
                                        <hr/>
                                        <div class="form-group">
                                                <div class="row">
                                                        <label class="col-3 "><b>start</b></label>
                                                        <div class="input-group form-group col-5" style="padding: 0px" >
                                                            <input type="date" name="bday" max="3000-12-31" 
                                                                   min="1000-01-01" class="form-control" v-model="start_date">                                                                                                                      
                                                        </div>
                                                </div>
                                        </div>
                                        <hr/>
                                        <div class="form-group">
                                                <div class="row">
                                                        <label class="col-3 "><b>end</b></label>
                                                        <div class="input-group form-group col-5" style="padding: 0px" >
                                                            <input type="date" name="bday" max="3000-12-31" 
                                                                   min="1000-01-01" class="form-control" v-model="ending_date">                                                                                                                      
                                                        </div>
                                                </div>
                                        </div>
                                        <hr/>
                                        <div class="row form-group">
                                                <label class="col-3"><b>required amount:</b></label>
                                                <input type="number" class=" col-3 form-control" placeholder="amount" v-model="amount">
                                                <div class="col-6 text-success" v-if ="amount > 0"><h3>KSh {{humanize(amount)}}</h3></div>                                                   
                                        </div>                                                                                   
                                </form>
                        </div>
                        <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal" v-on:click="fetchdata()">Close</button>                       
                        <button type="button" class="btn btn-success" v-on:click="addProject()">
                            <b>+</b>{{add_project_button_text}}
                            <span v-if="adding_project"
                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                            </span>
                        </button>
                        </div>
                    </div>
                    </div>
            </div>
            <!-- export to csv format -->
            <div class="modal fade" id="exportToCSV" tabindex="-1" role="dialog" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalCenterTitle">export projects data to CSV</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        </div>
                        <div class="modal-body">
                                <form>                                                                         
                                        <div class="form-group">                                                
                                                <div class="row">                                                        
                                                        <label class="col-3 "><b>date</b></label>
                                                        <div class="input-group form-group col-5" style="padding: 0px" >
                                                            <input type="date" name="bday" max="3000-12-31" 
                                                                   min="1000-01-01" class="form-control" v-model="csv_date">                                                                                                                      
                                                        </div>
                                                                                                                
                                                </div>
                                                <div class="row">                                                        
                                                        <label class="col-3 "><b></b></label>
                                                        <div class="input-group form-group col-5" style="padding: 0px" >
                                                                <small>export data is from selected date's month</small>                                                                                                                     
                                                        </div>
                                                                                                                
                                                </div>
                                        </div>
                                                                                                                         
                                </form>
                        </div>
                        <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>                       
                        <button type="button" class="btn btn-success" v-on:click="exportData()">
                            download CSV
                            <span v-if="exporting_data"
                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                            </span>
                        </button>
                        </div>
                    </div>
                    </div>
            </div>

        </div>
        </div>
    </div>
</template>

<script>
import router from "../../router";
import projectstats from '@/subcomponents/statistics/projectstats.vue'
export default {
    name : 'projectList',
    components: { projectstats },
    data () {
        return {
            projects: null,
            foundItems: null,
            fetch_data_error: [],
            enable_add_project_button: false,
            add_project_button_text: 'add project',
            //add project
            project_name: '',
            project_description: '',
            amount: null,
            start_year: '',start_month: '',start_day: '',
            start_date: '',
            ending_year: '',ending_month: '',ending_day: '',
            ending_date: '',
            added_project: [],
            adding_project: false,
            // exporting data
            csv_date: '',
            exporting_data:false


        }
    },
    created () {
        this.checkLoggedIn()
        this.fetchdata()
    },
    watch: {
            project_name: function(){  
                if ( this.project_name.length > 0                   
                     && this.project_description.length > 0
                     && this.start_date.length > 0
                     && this.ending_date.length > 0
                     && this.amount > 0){

                    this.enable_add_project_button = true
                }                
            },
            project_description: function(){ 
                if (this.project_name.length > 0                   
                     && this.project_description.length > 0 
                     && this.start_date.length > 0
                     && this.ending_date.length > 0
                     && this.amount > 0 ){

                    this.enable_add_project_button = true
                }                
            },
            start_date: function(){ 
                if (this.project_name.length > 0                    
                     && this.project_description.length > 0
                     && this.start_date.length > 0
                     && this.ending_date.length > 0
                     && this.amount > 0){

                    this.enable_add_project_button = true
                }                
            },
            amount: function(){ 
                if (this.project_name.length > 0                    
                     && this.project_description.length > 0
                     && this.start_date.length > 0
                     && this.ending_date.length > 0
                     && this.amount > 0){

                    this.enable_add_project_button = true
                }                
            },
            ending_date: function(){
                if (this.project_name.length > 0                    
                     && this.project_description.length > 0
                     && this.start_date.length > 0
                     && this.ending_date.length > 0
                     && this.amount > 0){

                    this.enable_add_project_button = true
                }                
            }
        },
    methods: {
        checkLoggedIn() {
            if (!this.$session.has("token")) {
                router.push("/login")
            }
        },
        humanize: function(x) {
                return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        fetchdata () {
            this.fetch_data_error = []

            // try local storage
            this.projects = JSON.parse(localStorage.getItem('project_list'))            
            if (this.projects){
                var array = this.projects.response
                this.foundItems = array.length 
            }

            const currentVersion = this.$store.getters.project_list_version
            var version  = localStorage.getItem('project_list_version')

            //else try the network
            if (!version || version < currentVersion) {
                this.$store.dispatch('update_isLoading', true)
                this.$http.get(this.$BASE_URL + '/api/projects/project-list/')
                .then(response => {
                   this.projects = {"response": response.data } 
                    var array = this.projects.response
                    this.foundItems = array.length

                    localStorage.setItem('project_list',JSON.stringify({"response": response.data }))                
                    localStorage.setItem('project_list_version', currentVersion) 
                    this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {
                    this.fetch_data_error.push(err)
                    this.$store.dispatch('update_isLoading', false)
                })
            }
        },
        exportData: function(){
            const FileDownload = require('js-file-download');
            //export to csv
            this.exporting_data = true
            this.$http.get(this.$BASE_URL + '/api/projects/get-project-general-stats-as-csv/' + this.csv_date +'/' )
            .then(response => {
                FileDownload(response.data,"projectsReport.csv");
               this.exporting_data = false                 
            })
            .catch((error) => {
                this.exporting_data = false
                alert('error while downloading csv')
            })
        },
        addProject: function (){ 
                this.add_project_button_text = 'adding project...'
                this.adding_project = true            
                this.$http({
                    method: 'post',
                    url: this.$BASE_URL + '/api/projects/project-list/',
                    data: {
                        name: this.project_name,
                        description: this.project_description,
                        required_amount: this.amount,
                        start: this.start_date,
                        stop: this.ending_date                                      
                    }
                }).then(response => {
                        this.adding_project = false
                        this.project_name = ''
                        this.project_description = ''
                        this.amount = ''                        
                        this.start_date = ''
                        this.ending_date = ''                      
                        this.add_project_button_text = '+ add project'
                        var new_version = parseInt(localStorage.getItem('project_list_version')) + 1
                        this.$store.dispatch('update_project_list_version', new_version)
                        alert("project added succesfully")                    
                    })
                    .catch((err) => {
                        this.adding_project = false
                        alert('failed, check date')
                    })                        
            }
    }

}
</script>


<style >
</style>
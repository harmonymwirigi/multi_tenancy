<!-- Parent.vue -->
<template>
        <div>              
            <!-- TITHES CONTENT -->
            <div v-if="! hide_content">
                <!-- tithe stats -->
                <content class="text-muted">
                    <div class="d-flex justify-content-center">
                        <div class="d-none d-lg-block stat-item mr-2 text-muted">
                                This month  <span class="text-secondary font-weight-bold">
                                    Ksh {{humanize(tithe_stats.response.total_in_tithe_this_month)}} </span>
                        </div>
                        <div class="stat-item d-none d-lg-block mr-2">
                                This year  <span class="text-secondary font-weight-bold">
                                Ksh   {{humanize(tithe_stats.response.total_in_tithe_this_year)}} </span>                                        
                        </div>
                        <a class="ml-2 btn btn-outline-secondary dropdown-toggle" data-toggle="collapse" href="#statsTab" role="button" aria-expanded="false" aria-controls="statsTab">
                                more stats
                        </a>
                        <!-- when on a small device show this button --> 
                        <div class="ml-3 d-sm-block d-md-none btn-group">
                            <button class="btn btn-success" data-toggle="modal" data-target="#addTithe">                            
                                    <b>+</b> add tithe                                           
                            </button>                      
                        </div>        
                    </div> 
                    <p>                                                    
                    </p>
                    <div class="collapse " id="statsTab">
                        <div class="card card-body outline-0 ">                            
                            <tithestats msg="tithe stats"/>
                        </div>
                    </div>
                </content>                    
                <!-- main content-->
                <content>          
                    <span class="mt-4">
                        <p><span class="mt-4 badge badge-pill badge-secondary">{{foundTithes}}</span> entries</p>
                    </span>                                                               
                    <table class="mt-5 table table-responsive-sm table-borderless">
                        <thead>
                            <tr>
                                <th>                                     
                                    <label class="anvil-checkbox">All
                                        <input type="checkbox" :value=true v-model="all_members">
                                        <span class="anvil-checkmark"></span>
                                    </label>
                                </th>
                                <th></th>
                                <th>
                                    <div class="dropdown">
                                    <a class="p-0 font-weight-bold btn btn-whte border-0 dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        Date
                                    </a>
                                    
                                    <div class="p-2 dropdown-menu border-0 shadow">
                                            <div class="p-2 form-group d-flex justify-content-between">
                                                <label class="mr-2">From</label>
                                                <input type="date" name="bday" max="3000-12-31" 
                                                min="1000-01-01" class="col-9 form-control" v-model="from_date"> 
                                            </div> 
                                            <div class="p-2 form-group d-flex justify-content-between">
                                                <label class="mr-2">To</label>
                                                <input type="date" name="bday" max="3000-12-31" 
                                                min="1000-01-01" class="col-9 form-control" v-model="to_date"> 
                                            </div> 
                                            <div class="p-2 d-flex justify-content-end">
                                                <button class="btn btn-sm btn-success"
                                                    :disabled = "!(from_date && to_date)"
                                                    @click="filterTithes()">
                                                    Filter
                                                </button>
                                            </div>
                                    </div>
                                    </div>
                                </th>
                                <th>Name</th>
                                <th>Amount</th>                                
                                <th>Method</th>                                    
                            </tr>                                  
                        </thead>                                                       
                        <tbody >
                            <tr v-for = "data in tithes.response">                                
                                <td>                                          
                                    <label class="anvil-checkbox">
                                            <input multiple type="checkbox" :value=data.id v-model="member_ids">
                                            <span class="anvil-checkmark"></span>
                                    </label>
                                </td>                             
                                <td>
                                    <h6>
                                        <span class="badge badge-danger" style="height: 5px; width: 5px" v-if="! data.notified"
                                            data-toggle="tooltip" data-placement="top" title="member has not been notified">
                                            <span style="visibility: hidden">.</span>
                                        </span>
                                        <span class="badge badge-success" style="height: 5px; width: 5px" v-if="data.notified"
                                            data-toggle="tooltip" data-placement="top" title="member has been notified">
                                            <span style="visibility: hidden">.</span>
                                        </span>
                                    </h6>
                                </td>
                                <td>{{$humanizeDate(data.date)}}</td>
                                <td v-if = "data.member != null">
                                    <router-link :to="`/memberDetail/`+ data.user_id">
                                            <span class = "text-secondary">{{data.member_full_name}}</span>
                                    </router-link>
                                </td>
                                <td v-if="data.service">{{data.service_type_name}} ({{data.service_date}})</td>
                                <td v-if="data.group">
                                    <router-link  :to="`/groupDetail/`+ data.group_id" class="text-muted">                                    
                                        <div>                                             
                                            {{data.group_name}}
                                        </div>                                                                                                                                
                                    </router-link>
                                </td>
                                <td v-if="! data.group && ! data.service && ! data.member && data.name_if_not_member">
                                    {{data.name_if_not_member}} <small>({{data.phone_if_not_member}})</small>
                                </td>
                                <td><p class="text-secondary">{{humanize(data.amount)}}</p></td>                                
                                <td>{{data.mode_of_payment_name}}</td>                                                                                             
                            </tr>
                        </tbody>
                    </table>
                </content>
            </div>
            <!-- add tithe modal -->
            <div class="modal fade" id="addTithe" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalCenterTitle">Add Tithe</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        </div>
                        <div class="modal-body">                                 
                                <customselect :fields="['member','group','service']"
                                              v-on:inputChanged="onInputChanged" 
                                              v-on:memberSelected="onMemberSelected"
                                              v-on:groupSelected="onGroupSelected"
                                              v-on:serviceFound="onServiceFound"/>                                                                                                                        
                                <div v-if="add_tithe_errors.length > 0">
                                    <ul>
                                            <small>
                                                <li v-for="error in add_tithe_errors">
                                                    <p class="text-danger">{{ error }}</p>
                                                </li>
                                            </small>
                                    </ul>
                                </div>                                    
                                <form>                                                                                                                           
                                                                              
                                        <hr/>
                                        <div class="row form-group">
                                                <label class="col-3"><b>amount:</b></label>
                                                <input type="number" class=" col-3 form-control" placeholder="amount" v-model="tithe_amount">
                                                <div class="col-6 text-success" v-if ="tithe_amount > 0"><h3>KSh {{humanize(tithe_amount)}}</h3></div>                                                                               
                                        </div>  
                                        <div v-if="tithe_amount_error.length > 0">
                                            <ul>
                                                <small>
                                                    <li v-for="error in tithe_amount_error">
                                                        <p class="text-danger">{{ error }}</p>
                                                    </li>
                                                </small>
                                            </ul>
                                        </div> 
                                        <hr/>                                                                                
                                        <div class="row">                                                        
                                                <label class="col-3 "><b>payment method</b></label>
                                            <select class="col-5 form-control custom-select"
                                                    v-model = "payment_method">
                                                    <option v-for= "method in payment_methods"
                                                         :value="method.id" >
                                                         {{method.name}}
                                                    </option>                                                    
                                            </select>                                                                                                                                                       
                                        </div>
                                        <hr>
                                        <div class="row">                                                        
                                            <label class="col-3 "><b>date</b></label>
                                            <div class="input-group form-group col-5" style="padding: 0px" >
                                                <input type="date" name="bday" max="3000-12-31" 
                                                    min="1000-01-01" class="form-control" v-model="tithe_date">                                                                                                                      
                                            </div>                                                                                                        
                                        </div>
                                        <hr>
                                        <div class="row form-group">
                                                <label class="col-3"><b>narration:</b></label>
                                                <textarea type="text" class="col-8 form-control" rows='3' v-model="tithe_narration"></textarea>                                                   
                                        </div>                                                                                                                        
                                </form>
                        </div>
                        <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-success" disabled v-if= "! enable_add_tithe_button && add_tithe_button_text != 'adding tithe...'">{{add_tithe_button_text}}</button>
                        <button type="button" class="btn btn-success" v-on:click="addTithe()">
                            add tithe
                            <span v-if="adding_tithe"
                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                            </span>
                        </button>
                        </div>
                    </div>
                    </div>
            </div>   
            <!-- export to csv format -->
            <div class="modal fade" id="exportTithesToCSV" tabindex="-1" role="dialog" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalCenterTitle">export tithe data to CSV</h5>
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
      </template>
      <script>
      import tithestats from '@/subcomponents/statistics/tithestats.vue'
      import customselect from '@/subcomponents/finances/select.vue'      
      export default {
        name: 'about',
        components: { tithestats,customselect },
        created () {
            this.getTithes()
        },
        props:{
            payment_methods:null,
            reload_data:null,
            hide_content:null
        },
        data () {
          return {
            reload_data: null,
            access_level: this.$session.get('access_level'),
            foundTithes: null,
            //fetch data
            from_date: null,
            to_date: null,
            tithe_stats: null,    
            tithes: null,
            non_member: false,
            group: false,
            fetch_data_error: [],
            // This value is set to the value emitted by the child
            selectedMember: null, 
            //add_tithe
            adding_tithe:false,
            add_tithe_button_text: '+ add tithe',
            enable_add_tithe_button: true,
            tithe_amount: null,
            tithe_date:null,
            payment_method:null,
            tithe_narration: '',
            tithe_amount_error: [], tithe_member_error: [],
            added_tithe: [],add_tithe_errors: [],
            // exporting data
            csv_date: '',
            exporting_data:false,
            //member ids
            all_members: false,
            member_ids: [],
            all_member_ids: [],
            //sending message                     
            sms_status: [],
            sending_message: false,
            //add
            not_member:false,
            group:null,
            service:null
          }
        },
        watch: {
            reload_data: function(){                
                if (this.reload_data == true){  
                    localStorage.removeItem('tithe_list_version')                  
                    this.getTithes()
                }                
            },
            all_members: function(){
                if (this.all_members != true){
                    this.member_ids = []
                }
                else{
                    this.member_ids = this.all_member_ids
                }
            },
            member_ids: function(){
                this.emitToParent()
            }
        },
        methods: {
            emitToParent (event) {                               
                this.$emit('membersSelected', this.member_ids)
            },
            humanize: function(x) {return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");},
            // Triggered when `memberSelected` event is emitted by the child.
            onMemberSelected (value) {             
                this.selectedMember = value
            },
            onInputChanged (value){
                this.selectedMember = null
                this.group = null
                this.service = null
            },
            onServiceFound (found_service){                                                                 
                this.service = found_service[0].type.id
            },
            onGroupSelected (group){                
                this.group = group
            },
            filterTithes: function(){
                localStorage.removeItem('tithe_list_version')
                this.getTithes()
            },
            getTithes: function(){                
                this.fetch_data_error = []
                this.$store.dispatch('update_isLoading', true)
                // try local storage for tithes
                this.tithes = JSON.parse(localStorage.getItem('tithe_list'))                
                if (this.tithes){                    
                    var array = this.tithes.response
                    this.foundTithes = array.length
                    for (var tithe in array){                        
                        this.all_member_ids.push(array[tithe].id)                                                                                                     
                    } 
                    this.emitToParent()
                    this.$store.dispatch('update_isLoading', false)
                }            
                this.tithe_stats = JSON.parse(localStorage.getItem('tithe_stats'))

                const currentVersion = this.$store.getters.tithe_list_version
                var version  = localStorage.getItem('tithe_list_version')

                //else try network for tithes                
                if (!version || version < currentVersion) {
                    this.all_members = false
                    this.member_ids = []
                    this.all_member_ids = []
                    var params
                    if (this.from_date && this.to_date){
                        params = {from_date : this.from_date, to_date : this.to_date}
                    }
                    this.$store.dispatch('update_isLoading', true)
                    this.$http({
                        method: 'get',
                        url : this.$BASE_URL + '/api/finance/tithes-by-members/',
                        params : params
                    }).then(response => {
                        this.tithes = {"response": response.data }   
                        var array = this.tithes.response
                        for (var tithe in array){                                   
                            this.all_member_ids.push(array[tithe].id)                             
                        }   
                        this.emitToParent()
                        this.foundTithes = array.length                  
                        
                        localStorage.setItem('tithe_list',JSON.stringify({"response": response.data }))                
                        localStorage.setItem('tithe_list_version', currentVersion) 
                        this.$store.dispatch('update_isLoading', false)
                    }).catch((err) => {
                        this.fetch_data_error.push(err)
                        this.$store.dispatch('update_isLoading', false)
                    })

                }
                this.getTitheStats()
            },
            // get tithe stats 
            getTitheStats: function(){                                    
                    this.$http.get(this.$BASE_URL + '/api/finance/tithe-stats/')
                    .then(response => {
                        this.tithe_stats = {"response": response.data } 

                        localStorage.setItem('tithe_stats',JSON.stringify({"response": response.data }))                                                  
                    })
                    .catch((err) => {
                        this.fetch_data_error.push(err)                       
                    })
            },
            //check that add tithe form is okay
            addTitheFormOK: function(){
                this.added_tithe = []
                this.tithe_member_error = []
                this.tithe_amount_error = []
                if (this.tithe_narration.length < 1){                    
                        this.tithe_narration = "none given"
                }   
                if (this.tithe_date == '' || this.tithe_date == null){
                    alert('date is required')
                    return false
                }
                if (this.tithe_amount < 1){
                    alert(" enter an amount")
                    return false
                }
                return true
            },
            //add tithe
            addTithe: function(){
                if (this.addTitheFormOK()){
                    this.enable_add_tithe_button = false
                    this.add_tithe_button_text = 'adding tithe...'  
                    this.adding_tithe = true              
                    this.$http({
                        method: 'post',
                        url: this.$BASE_URL + '/api/finance/add-tithe-for-member/',
                        data: {
                            member: this.selectedMember,
                            narration: this.tithe_narration,
                            recorded_by: this.$session.get('member_id'),                             
                            amount: this.tithe_amount,
                            date: this.tithe_date,
                            mode_of_payment: this.payment_method,
                            service:this.service,
                            group:this.group ,                                                                
                        }
                        }).then(response => {                            
                            this.adding_tithe = false                                                                                                                                                            
                            this.selectedMember = null,
                            this.tithe_narration = '',
                            this.tithe_amount = ''    
                            this.tithe_date = null           
                            this.payment_method = null                                                             
                            
                            var new_version = parseInt(localStorage.getItem('tithe_list_version')) + 1
                            this.$store.dispatch('update_tithe_list_version', new_version)                                    
                            this.getTithes()

                            alert("tithe of succesfully added, amount: " + response.data.amount )                     
                            this.can_send_message = true
                        })
                        .catch((err) => {
                            this.adding_tithe = false
                            alert(err)
                                                            
                        })
                }
            },
            //export data to csv
            exportData: function(){            
            //export to csv
            this.exporting_data = true
            this.$http.get(this.$BASE_URL + '/api/finance/get-tithes-as-csv/' + this.csv_date +'/' )
            .then(response => {                
                this.$fileDownload(response.data,"tithes_" + this.csv_date + ".csv");
                this.exporting_data = false                 
                alert("download successful")
            })
            .catch((error) => {
                this.exporting_data = false
                alert(err)
            })
        },
        }
      }
      </script>
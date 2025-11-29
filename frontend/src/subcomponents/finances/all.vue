<!-- Parent.vue -->
<template>
    <div>              
        <!-- TITHES CONTENT -->
        <div v-if="! hide_content">                            
            <!-- main content-->
            <content>          
                <span class="mt-4">
                    <p><span class="mt-4 badge badge-pill badge-secondary">{{foundTithesAndOfferings}}</span> entries</p>
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
                                                @click="filterTithesAndOfferings()">
                                                Filter
                                            </button>
                                        </div>
                                </div>
                                </div>
                            </th>
                            <th>Name</th>                        
                            <th>Amount</th>                                
                            <th>Type</th>
                            <th>Method</th>                                    
                        </tr>                                  
                    </thead>                                                       
                    <tbody >
                        <tr v-for = "data in tithes_and_offerings.response">                                
                            <td>                                          
                                <label class="anvil-checkbox">
                                    <input multiple type="checkbox" 
                                        :value="{'type': data.type_name,'id': data.id }"
                                        v-model="envelope_ids">
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
                            <td>{{data.type_name}}</td>                               
                            <td>{{data.mode_of_payment_name}}</td>                                                                                             
                        </tr>
                    </tbody>
                </table>
            </content>
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
        this.getTitheAndOfferings()
    },
    props:{
        payment_methods:null,
        reload_data:null,
        hide_content:null
    },
    data () {
      return {
        reload_data:null,
        access_level: this.$session.get('access_level'),
        foundTithesAndOfferings: null,
        //fetch data
        from_date: null,
        to_date: null,
        tithe_stats: null,    
        tithes_and_offerings: null,
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
        envelope_ids: [],
        all_envelope_ids: [],
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
                this.getTitheAndOfferings()
            }                
        },
        all_members: function(){
            if (this.all_members != true){
                this.envelope_ids = []
            }
            else{
                this.envelope_ids = this.all_envelope_ids
            }
        },
        envelope_ids: function(){
            this.emitToParent()
        }
    },
    methods: {
        emitToParent (event) {                               
            this.$emit('membersSelected', this.envelope_ids)
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
        filterTithesAndOfferings: function(){        
            this.getTitheAndOfferings()
        },
        getTitheAndOfferings: function(){
            this.all_members = false
            this.envelope_ids = []
            this.all_envelope_ids = []
            this.fetch_data_error = []
            this.$store.dispatch('update_isLoading', true)                      
            
            var params
            if (this.from_date && this.to_date){
                params = {from_date : this.from_date, to_date : this.to_date}
            }
            this.$store.dispatch('update_isLoading', true)
            this.$http({
                method: 'get',
                url : this.$BASE_URL + '/api/finance/tithes-and-offerings/',
                params : params
            }).then(response => {
                this.tithes_and_offerings = {"response": response.data }   
                var array = this.tithes_and_offerings.response
                for (var item in array){                    
                    this.all_envelope_ids.push({
                        "type": array[item].type_name,
                        "id" : array[item].id
                    })
                }   
                this.emitToParent()
                this.foundTithesAndOfferings = array.length                  
                                
                this.$store.dispatch('update_isLoading', false)
            }).catch((err) => {
                this.fetch_data_error.push(err)
                this.$store.dispatch('update_isLoading', false)
            })                
        }
    }
  }
  </script>
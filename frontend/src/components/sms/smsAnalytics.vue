<template>
    <div>
        <nav aria-label="breadcrumb" class="continer">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li> 
                    <li class="breadcrumb-item active" aria-current="page">SMS outbox</li>
                </ol>
        </nav>
        <div class="continer">
                <h3 class="font-weight-bold">SMS outbox</h3>
                <hr>
                <section class="row">
                        <div class="d-flex flex-column flex-nowrap mb-2 ml-3 text-center text-muted border border-secondary rounded">
                                <h1 class="font-weight-bold" v-if="sms_credit_balance">
                                    {{sms_credit_balance}} 
                                </h1>
                                <h1 v-else>
                                    <span
                                        class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                    </span>
                                </h1>                        
                                SMS credit balance
                        </div> 
                        <div class="mb-2 ml-3 text-center text-muted col-lg-2 col-sm-12 border border-secondary rounded">
                                <h1 class="font-weight-bold" v-if="client_details">{{client_details[0].number_of_sms}}</h1>
                                sms delivered this month
                        </div>
                </section>
                <table class="table table-responsive-sm">
                        <thead>
                          <tr>     
                            <th scope="col">date</th>                       
                            <th scope="col">message</th>
                            <th scope="col">receiver</th>
                            <th scope="col">status</th>
                            <th> cost</th>
                          </tr>
                        </thead>
                        <tbody class="text-muted">
                          <tr v-for= "message in sms_this_month" >  
                            <td>{{$humanizeDate(message.sms.date)}}</td>                                                     
                            <td><p>{{message.sms.message}}</p></td>
                            <td>
                                {{message.receipient.member.first_name}} {{message.receipient.member.last_name}}                        
                            </td>
                            <td>
                                <h5>
                                    <span v-if="message.status == 'Success'" class="badge badge-success">{{message.status}}</span>
                                    <span v-else class="badge badge-primary">{{message.status}}</span>
                                </h5>
                            </td>
                            <td>{{message.cost}}</td>                            
                          </tr>
                        </tbody>
                      </table>            
        </div>
    </div>
</template>

<script>
export default {
    name: 'smsAnalytics',
    data () {
        return{
           church_id: localStorage.getItem('church_id'),
           sms_this_month: null,
           sms_credit_balance: null,
           client_details:null,
        }
    },
    created () {
       this.fetchData() 
       this.getSMSCreditBalance()
       this.getClientDetail()
    },
    methods: {
        fetchData () {  
            this.$store.dispatch('update_isLoading', true)          
            this.$http.get(this.$BASE_URL + '/api/sms/sms-this-month/')
                .then(response => {
                this.sms_this_month =  response.data 
                this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {
                    this.$store.dispatch('update_isLoading', false)
                    alert("error occured while fetching data")
                })
        },
        //church sms balance
        getSMSCreditBalance: function(){
            this.$http.get(this.$BASE_URL + '/api/sms/sms-credit-balance')
            .then((response)=>{            
                this.sms_credit_balance =  response.data.UserData.balance
            })
        },
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
    }
}
</script>


<style >
</style>
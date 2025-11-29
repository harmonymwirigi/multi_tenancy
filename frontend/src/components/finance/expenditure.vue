<template>
    <div>
        <nav aria-label="breadcrumb" class="continer">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li>
                        <li class="breadcrumb-item"><span class="backButton"><a href=# style="text-decoration: none" v-on:click="goBack()" >finances</a></span></li>
                    <li class="breadcrumb-item active" aria-current="page">
                        <span v-for="data in expenditure_type.response">{{data.type_name}}</span>
                    </li>
                </ol>
        </nav>
        <div class = "continer">
            <div class="row">
                    <div class="filters col-sm-8 col-md-8 col-lg-2" style="padding: 3px 3px 3px 3px">
                        </div>
                        <div class="col-sm-12 col-lg-9">
                                <div class="d-flex justify-content-between">
                                        <h3>
                                            <span v-for="data in expenditure_type.response">{{data.type_name}}</span>
                                        </h3>
                                        <button class="btn btn-success"
                                                data-toggle="modal" data-target="#addExpenditure">
                                            + add expenditure
                                        </button>
                                </div>
                                <div class="mt-5">

                                        <div class="mb-4  text-muted" v-for="data in expenditure_type.response">
                                                <div class="d-flex justify-content-start">
													<div class="stat-item mr-2 text-muted">
                                                            Total allocated : <span class="text-secondary font-weight-bold">
                                                                Ksh {{humanize(data.total_available)}} </span>
                                                    </div>
													<div class="stat-item mr-2 text-muted">
                                                            Total spent : <span class="text-secondary font-weight-bold">
                                                                Ksh {{humanize(data.total.total)}} </span>
                                                    </div>
													<div class="stat-item mr-2 text-muted">
                                                            %age spent : <span class="text-secondary font-weight-bold">
                                                                {{humanize(data.total.percentage_used)}} %</span>
                                                    </div>
                                                    <div class="stat-item mr-2 text-muted">
                                                            spent this month : <span class="text-secondary font-weight-bold">
                                                                Ksh {{humanize(data.total_this_month)}} </span>
                                                    </div>
                                                    <div class="stat-item mr-2">
                                                            spent this year : <span class="text-secondary font-weight-bold">
                                                            Ksh {{humanize(data.total_this_year)}}</span>
                                                    </div>
                                                </div>
                                        </div>
                                    </div>
								<span class="mt-5 badge badge-pill badge-secondary">{{foundItems}}</span> entries found
                                <table class="mt-5 table table-responsive-sm table-borderless">
                                    <thead>
                                        <tr>
                                            <th>amount</th>
                                            <th>date</th>
                                            <th>narration</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for = "data in expenditures.response">
                                            <td>
                                                <router-link class="text-secondary" style="text-decoration: none;"  :to="`/income/`+ data.id + `/`">
                                                    {{humanize(data.amount)}}
                                                </router-link>
                                            </td>
                                            <td><p class="text-info">{{$humanizeDate(data.date)}}</p></td>
                                            <td><p class="text-secondary">{{data.narration}}</p></td>
                                        </tr>
                                    </tbody>
                                </table>
                      </div>
            <!-- add expenditure modal -->
            <div class="modal fade" id="addExpenditure" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalCenterTitle">add expenditure</h5>
                        <button id="closeAddExpenditureModal" type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        </div>
                        <div class="modal-body">
                                <form>
                                        <div class="row form-group">
                                                <label class="col-3"><b>amount:</b></label>
                                                <input type="number" class=" col-3 form-control" placeholder="amount" v-model="expenditure_amount">
                                                <div class="col-6 text-success" v-if ="expenditure_amount > 0"><h3>KSh {{humanize(expenditure_amount)}}</h3></div>
                                                <p v-if="expenditure_amount_errors.length">
                                                    <ul>
                                                            <small><li v-for="error in expenditure_amount_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                    </ul>
                                                </p>
                                        </div>
                                        <hr/>
                                        <div class="row form-group">
                                            <label class="col-3"><b>narration:</b></label>
                                            <textarea type="text" class="col-8 form-control" rows='3' v-model="expenditure_narration"></textarea>
                                        </div>
                                </form>
                        </div>
                        <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-success" v-on:click="addExpenditure()">
                            <b>+</b> add expenditure
                            <span v-if="adding_expenditure"
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
export default {
    name: 'expenditure',
    data () {
        return{
        //get data
            fetch_data_error: [],
            foundItems: 0,
            expenditure_type: null,
            expenditures: null,
        //add expenditure
            expenditure_narration: null,
            expenditure_amount: null,
            expenditure_amount_errors: [],
            adding_expenditure: false
        }
    },
    created () {
        this.checkLoggedIn()
        this.fetchdata()
    },
    watch: {
        '$route': 'fetchdata',
    },
    methods: {
        //check if member is logged in
        checkLoggedIn() {
            if (!this.$session.has("token")) {
                router.push("/login")
            }
        },
        humanize: function(x) {
                return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        //go back to previous window
        goBack: function() {
            window.history.back();
        },
        //fetch data
        fetchdata () {
            this.fetch_data_error = []
            this.$store.dispatch('update_isLoading', true)
            this.$http.get(this.$BASE_URL + '/api/finance/expenditure-type/' + this.$route.params.id + "/")
                .then(response => {
                this.expenditure_type = {"response": response.data }
                this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {
                    this.fetch_data_error.push(err)
                    this.$store.dispatch('update_isLoading', false)
                })

            this.$store.dispatch('update_isLoading', true)
            this.$http.get(this.$BASE_URL + '/api/finance/expenditures-of-type/' + this.$route.params.id + "/")
                .then(response => {
                this.expenditures = {"response": response.data }
                var array = this.expenditures.response
                this.foundItems = array.length
                this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {
                    this.fetch_data_error.push(err)
                    this.$store.dispatch('update_isLoading', false)
                })
        },
        expenditureFormOkay: function(){
        this.added_income = []
        this.expenditure_amount_errors = []
        this.income_type_errors = []

        if (this.expenditure_type != null
            && this.expenditure_amount != null){
                return true
            }
        if (this.expenditure_type == null){
                this.income_type_errors.push("select an income type or add one ")
                return false
            }
        if (! this.expenditure_amount > 0
            || this.expenditure_amount == null){
            this.expenditure_amount_errors.push("enter an amount")
            return false
        }
    },
        addExpenditure: function(){
        if (this.expenditureFormOkay()){
            this.adding_expenditure = true
            this.$http({
                    method: 'post',
                    url: this.$BASE_URL + '/api/finance/add-expenditure/',
                    data: {
                            recording_member_id: this.$session.get('member_id'),
                            expenditure_type_id: this.$route.params.id,
                            narration: this.expenditure_narration,
                            amount: this.expenditure_amount
                    }
                    }).then(response => {
                        this.added_income.push(response.data)
                        this.expenditure_amount = null,
                        this.expenditure_narration = ''
                        this.adding_expenditure = false
                        var new_version = parseInt(localStorage.getItem('expenditure_list_version')) + 1
                        this.$store.dispatch('update_expenditure_list_version', new_version)
                        document.getElementById('closeAddExpenditureModal').click()
                        this.fetchdata()
                    })
                    .catch((err) => {
                        alert("error while adding expenditure, check your connection and try again")
                        this.adding_expenditure = false
                    })
        }
    }

    },

}
</script>


<style >
</style>

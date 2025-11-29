<template>
	<div>
		<!-- EXPENDITURE CONTENTS -->
		<div>
			<h3 class="font-weight-bold">Expenditure</h3>
			<br>
			<div class="mt-5 text-muted" v-if="expenditure_stats">
					<div class="d-flex d-flex-row justify-content-start">
							<div class="d-none d-lg-block stat-item mr-2 text-muted">
									This month  <span class="text-secondary font-weight-bold">
									 Ksh {{humanize(expenditure_stats.total_this_month)}}</span>
							</div>
							<div class="d-none d-lg-block stat-item mr-2">
									This year  <span class="text-secondary font-weight-bold">
									Ksh   {{humanize(expenditure_stats.total_this_year)}}</span>
							</div>
							<a class="ml-2 btn btn-sm btn-outline-secondary dropdown-toggle" data-toggle="collapse" href="#statsTab" role="button" aria-expanded="false" aria-controls="statsTab">
									more stats
							</a>
							 <!-- when on a small device show this button -->
							 <div class="ml-3 d-sm-block d-md-none btn-group">
									<button class="btn btn-success" data-toggle="modal" data-target="#addOffering">
											Add expenditure type
									</button>
							</div>
					</div>
					<div class="collapse" id="statsTab">
							<div class="card card-body outline-0">
								<expenditurestats  msg="expenditure stats"/>
							</div>
					</div>
				</div>
			<table class="mt-5 table table-responsive-sm table-borderless">
				<thead>
					<tr>
						<th>type</th>
						<th>created</th>
						<th>this month</th>
						<th>this year</th>
					</tr>
				</thead>
				<p class="mt-4 col-8">
					<span class="badge badge-pill badge-secondary">{{found_expenditure_types}}</span> entries found
				</p>
				<tbody>
					<tr v-for = "data in expenditure_types.response">
						<td>
							<router-link class="text-muted"  :to="`/expenditure/`+ data.id + `/`">
								{{data.type_name}}
							</router-link>
						</td>
						<td>{{$humanizeDate(data.created)}}</td>
						<td><p class="text-secondary">{{humanize(data.total_this_month)}}</p></td>
						<td><p>{{humanize(data.total_this_year)}}</p></td>
						<td>
							<router-link class="text-muted" style="text-decoration: none;"  :to="`/expenditure/`+ data.id + `/`">
								<img style="width: 20px ;height: auto" src="@/assets/icons/icons8-right-arrow-50.png">
							</router-link>
						</td>
					</tr>
				</tbody>
			</table>
		</div>


		<!-- add expenditure type modal -->
		<div class="modal fade" id="addExpenditureType" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
				<div class="modal-dialog modal-dialog-centered" role="document">
				<div class="modal-content">
					<div class="modal-header">
					<h5 class="modal-title">add expenditure type</h5>
					<button id="closeAddExpenditureTypeModalButton" type="button" class="close" data-dismiss="modal" aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
					</div>
					<div class="modal-body">
							<form>
									<div class="row form-group">
											<label class="col-3"><b>name:</b></label>
											<input type="text" class=" col-8 form-control" placeholder="give a name" v-model="expenditure_type_name">
											<p v-if="expenditure_type_name_errors.length">
												<ul>
														<small><li v-for="error in expenditure_type_name_errors"><p class="text-danger">{{ error }}</p></li></small>
												</ul>
											</p>
									</div>
									<div class="row form-group">
											<label class="col-3"><b>total allocation:</b></label>
											<input type="number" class=" col-8 form-control" v-model="expenditure_allocation">
									</div>
									<div class="row form-group">
										<label class="col-3"><b>describe:</b></label>
										<textarea type="text" class="col-8 form-control" rows='3' v-model="expenditure_type_description"></textarea>
									</div>
							</form>
					</div>
					<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					<button type="button" class="btn btn-success" v-on:click="addExpenditureType()">
						<b>+</b> add expenditure type
						<span v-if="adding_expenditure"
							class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
						</span>
					</button>
					</div>
				</div>
				</div>
		</div>
		 <!-- export to csv format -->
		 <div class="modal fade" id="exportEpenditureToCSV" tabindex="-1" role="dialog" aria-hidden="true">
				<div class="modal-dialog modal-dialog-centered" role="document">
				<div class="modal-content">
					<div class="modal-header">
					<h5 class="modal-title" id="exampleModalCenterTitle">export expenditure data to CSV</h5>
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
import expenditurestats from '@/subcomponents/statistics/expenditurestats.vue'
export default {
	name: 'expenditures',
	components: { expenditurestats },
	props: {
		msg: String
	},
	created(){
		this.getExpenditures()
	},
	data(){
		return{
			fetch_data_error: [],
			adding_expenditure: false,
			//get expenditure
			found_expenditure_types: 0,
			expenditure_types: null,
			expenditure_stats: null,
			//add expenditure
			expenditure_type_name: '',
			expenditure_allocation:0.00,
			expenditure_type_description: '',
			expenditure_type_name_errors: [],
			// exporting data
			csv_date: '',
			exporting_data:false
		}
	},

	methods:{
		humanize: function(x) {return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")},
		getExpenditures: function(){
			//try local storage
			this.expenditure_stats = JSON.parse(localStorage.getItem('expenditure_stats'))
			this.expenditure_types = JSON.parse(localStorage.getItem('expenditure_type_list'))
			if (this.expenditure_types){
				var array = this.expenditure_types.response
				this.found_expenditure_types = array.length
			}

			// else try the network
			// expenditure stats
			const currentVersion = this.$store.getters.expenditure_list_version
			var version  = localStorage.getItem('expenditure_list_version')
			var test = true
			if (test) {
				this.$store.dispatch('update_isLoading', true)
				this.$http.get(this.$BASE_URL + '/api/finance/expenditure-stats/')
				.then(response => {
					this.expenditure_stats =  response.data
					localStorage.setItem('expenditure_stats',JSON.stringify(response.data) )
					this.$store.dispatch('update_isLoading', false)
				})
				.catch((err) => {
					this.fetch_data_error.push(err)
					this.$store.dispatch('update_isLoading', false)
				})

				// expenditure type list
				this.$store.dispatch('update_isLoading', true)
				this.$http.get(this.$BASE_URL + '/api/finance/expenditure-type-list/')
				.then(response => {
					this.expenditure_types = {"response": response.data }
					localStorage.setItem('expenditure_type_list',JSON.stringify({"response": response.data } ))
					localStorage.setItem('expenditure_list_version', currentVersion)

					var array = this.expenditure_types.response
					this.found_expenditure_types = array.length
					this.$store.dispatch('update_isLoading', false)
				})
				.catch((err) => {
					this.fetch_data_error.push(err)
					this.$store.dispatch('update_isLoading', false)
				})
			}
		},

		// ADD EXPENDITURE TYPE
		expenditureTypeFormOK: function(){
			//check if form is okay
			this.expenditure_type_name_errors = []

			if (this.expenditure_type_description.length < 1){
				this.expenditure_type_description = "none given"
			}
			if (this.expenditure_type_name.length > 0){
				return true
			}
			if (this.expenditure_type_name.length < 1){
				this.expenditure_type_name_errors.push("name required")
				return false
			}
		},
		addExpenditureType: function(){
			if (this.expenditureTypeFormOK()){
				this.adding_expenditure = true
				this.$http({
					method: 'post',
					url: this.$BASE_URL + '/api/finance/expenditure-type-list/',
					data: {
						type_name: this.expenditure_type_name,
						total_available: this.expenditure_allocation,
						description: this.description_type_description
					}
				})
				.then(response => {
					this.adding_expenditure = false
					this.expenditure_type_name = '',
					this.expenditure_type_description = ''
					var new_version = parseInt(localStorage.getItem('expenditure_list_version')) + 1
					this.$store.dispatch('update_expenditure_list_version', new_version)
					document.getElementById('closeAddExpenditureTypeModalButton').click()
					this.getExpenditures()
				})
				.catch((err) => {
					this.adding_expenditure = false
					alert("an error occured, try again later")
				})
			}
		},
		//export data to csv
		exportData: function(){
			//export to csv
			this.exporting_data = true
			this.$http.get(this.$BASE_URL + '/api/finance/get-expenditure-csv/' + this.csv_date +'/' )
			.then(response => {
				this.$fileDownload(response.data,"expenditures_" + this.csv_date + ".csv");
				this.exporting_data = false
				alert("download successful")
			})
			.catch((error) => {
				this.exporting_data = false
				alert('error while downloading expenditure csv')
			})
		},



	},

}
</script>

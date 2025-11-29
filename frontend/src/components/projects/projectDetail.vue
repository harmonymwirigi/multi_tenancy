<template>
	<div v-if="context && contributions">
		<!-- this compnent requires text message modal -->	
		<nav aria-label="breadcrumb" class="continer">
				<ol class="breadcrumb">
					<li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li>
					<li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'generalFinance'}">finances</router-link></span></li>
					<li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'projectList'}">projects</router-link></span></li>
					<li class="breadcrumb-item active" aria-current="page">
							<span v-if="context" v-for = "data in context.response">{{data.name}}</span>
					</li>
				</ol>
		</nav>
		<div class="continer">
			<div class="row">
				<div class="col-12 col-sm-10 col-md-8 col-lg-2 border rounded">
						<div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
							<!-- <a class="action-list list-group-item list-group-item-action border-0" id="v-pills-contributions-tab" data-toggle="pill" href="#v-pills-contributions" role="tab" aria-controls="v-pills-contributions" aria-selected="true" v-on:click="getContributionsTab()">
									<span class="">
											<i class="fas fa-donate"></i>
											Contributions
									</span>
							</a> -->
							<a class="action-list list-group-item list-group-item-action active border-0" id="v-pills-pledges-tab" data-toggle="pill" href="#v-pills-pledges" role="tab" aria-controls="v-pills-pledges" aria-selected="false" v-on:click="getPledgesTab()">
									<span class="">
											<i class="fas fa-bullseye"></i>
											pledges
									</span>
							</a>
							<a class="action-list list-group-item list-group-item-action  border-0" id="v-pills-pledgepayment-tab" data-toggle="pill" href="#v-pills-pledgepayment" role="tab" aria-controls="v-pills-pledgepayment" aria-selected="false" v-on:click="getPledgePaymentsTab()">
									<span class="text-nowrap">
											<i class="fas fa-donate"></i>
											Pledge Payments
									</span>
							</a>

						</div>
				</div>
				<div class="col">
						<div class="tab-content" id="v-pills-tabContent">
								<!-- contributions tab -->
								<div class="tab-pane fade" id="v-pills-contributions" role="tabpanel" aria-labelledby="v-pills-contributions-tab">
									<h3 class="font-weight-bold">
											<span v-if="context" v-for = "data in context.response">{{data.name}} /</span> contributions
									</h3>
									<hr>
									<!-- what to show on small devices -->
									<div class="d-sm-block d-md-none btn-group" style="padding: 0px 0px 25px 10px" v-if=" tab == 'contributions'">
											<a href="#" data-toggle="modal" data-target="#addContribution" style="text-decoration: none">
													<div class="add-button" >
													<b>+</b> add contribution
													</div>
											</a>
											<button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
													<span class="sr-only">Toggle Dropdown</span>
											</button>
											<div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">
													<a class="dropdown-item" href="#" data-toggle="modal" data-target="#addPledge"><b>+</b> add pledge</a>
													<a class="dropdown-item" href="#" data-toggle="modal" data-target="#settlePledge"><b>+</b> settle pledge</a>
											</div>
									</div>									
									<div class=" text-muted" v-if="context" v-for = "data in context.response ">
											<div class="mt-4 d-flex d-flex-row justify-content-center">												
													<div class="d-none d-lg-block stat-item mr-2 text-muted">
															Required  <span class="text-secondary font-weight-bold">
																	Ksh {{humanize(data.required_amount)}}</span>
													</div>
													<div class="d-none d-lg-block stat-item mr-2">
															Raised  <span class="text-secondary font-weight-bold">
															Ksh   {{humanize(data.raised_amount)}}</span>
													</div>
													<div class=" d-none d-lg-block stat-item mr-2">
															Funded  <span class="text-secondary font-weight-bold">
															{{data.percentage_funded}} %</span>
													</div>
											</div>
									</div>
									<div class="row">
									<p class="col-8">
											Found <span class="mt-5 badge badge-pill badge-secondary">{{foundItems}}</span>
									</p>
									</div>
									<table class="table table-responsive-sm table-borderless">
										<thead>
											<tr>
												<th>
													<label class="anvil-checkbox">all
														<input type="checkbox" :value=true v-model="all_pledge_ids_selected">
														<span class="anvil-checkmark"></span>
													</label>
												</th>
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
												<th>name</th>
												<th>amount</th>
											</tr>
										</thead>
										<tbody>
											<tr v-if="contributions" v-for = "data in contributions.response">
												<td v-if = "data.member != null">
												   <label class="anvil-checkbox">
														<input multiple type="checkbox" :value=data.member.member.id v-model="pledge_ids">
														<span class="anvil-checkmark"></span>
												   </label>
												</td>
												<td v-else></td>
												<td v-if = "data.member != null">
														<router-link :to="`/memberDetail/`+ data.member.member.id">
																<span class = "text-secondary">{{data.member.member.first_name}} {{data.member.member.last_name}}</span>
														</router-link>
												</td>
												<td>{{$humanizeDate(data.recorded_at)}}</td>
												<td v-if = "data.names != ''"> {{data.names}}</td>
												<td><p class="text-muted">{{humanize(data.amount)}}</p></td>
											</tr>
										</tbody>
									</table>
								</div>
								<!-- pledges tab -->
								<div class="tab-pane fade show active" id="v-pills-pledges" role="tabpanel" aria-labelledby="v-pills-pledges-tab">
									<div v-if = "pledges_selected">
										<h3 class="font-weight-bold">
												<span v-for = "data in context.response">{{data.name}} /</span> pledges
										</h3>
										<hr>
										<!-- what to show on small devices -->
										<div class="d-sm-block d-md-none btn-group" style="padding: 0px 0px 25px 10px" v-if=" tab == 'pledges'">
												<a href="#" data-toggle="modal" data-target="#addPledge" style="text-decoration: none">
														<div class="add-button" >
														<b>+</b> add pledge
														</div>
												</a>
												<button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
														<span class="sr-only">Toggle Dropdown</span>
												</button>
												<div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">
														<a class="dropdown-item" href="#" data-toggle="modal" data-target="#settlePledge"><b>+</b> settle pledge</a>
														<div class="dropdown-divider"></div>
														<a class="dropdown-item" href="#" data-toggle="modal" data-target="#addContribution"><b>+</b> add contribution</a>
														<a class="dropdown-item"><router-link style="text-decoration: none" :to="{name: 'ImportPledgesFromCSV'}">Import from CSV</router-link></a>
												</div>
										</div>
										<!-- pledges -->
										<div class="text-muted" v-for = "data in context.response ">
												<div class="mt-4 d-flex d-flex-row justify-content-center">
														<div class="d-none d-lg-block stat-item mr-2 text-muted">
																Pledges  <span class="text-text-secondary font-weight-bold">
																		Ksh {{humanize(data.total_in_pledges)}}</span>
														</div>
														<div class=" d-none d-lg-block stat-item mr-2">
																Settled  <span class="text-text-secondary font-weight-bold">
																Ksh   {{humanize(data.total_in_settled_pledges)}}</span>
														</div>
														<div class="d-none d-lg-block stat-item mr-2">
																Percentage settled  <span class="text-secondary font-weight-bold">
																Ksh   {{data.percentage_of_pledge_settled}}%</span>
														</div>
												</div>
										</div>
										   <div class="mt-5 d-flex justify-content-between">
												<p class="col-6">
														showing <span class="mt-4 badge badge-pill badge-secondary">{{humanize(pledges_count)}}</span>
												</p>
												<div class="d-flex justify-content-end">
													<button class="btn" @click="prevPage"
														:disabled="pageNumber == 1">
														<i class="arrow left"></i>
													</button>
													<span class="p-3">{{pageNumber}} / {{pageCount}}</span>
													<button class="btn" @click="nextPage"
														:disabled="pageNumber == pageCount">
														<i class="arrow right"></i>
													</button>
												</div>
											</div>
										<table class="table table-responsive-sm table-borderless">
												<thead>
													<tr>
														<th>
														<label class="anvil-checkbox">all
																<input type="checkbox" :value=true v-model="all_pledge_ids_selected">
																<span class="anvil-checkmark"></span>
														</label>
														</th>
														<th>name</th>
														<th>pledged</th>
														<th>raised</th>
														<th>remaining</th>
														<th>funded</th>
													</tr>
												</thead>
												<tbody>
													<tr v-for = "data in pledges.response" :key=data.id v-if="selectedMember == '' || selectedMember == null || memberSearch == ''">														
														<td>
															<label class="anvil-checkbox">
																	<input multiple type="checkbox" :value=data.id v-model="pledge_ids">
																	<span class="anvil-checkmark"></span>
															</label>
														</td>
														<td v-if = "data.member != null">
																<router-link :to="`/memberDetail/`+ data.member.member.id">
																		<span class = "text-secondary">{{data.member.member.first_name}} {{data.member.member.last_name}}</span>
																</router-link>
														</td>
														<td v-else = "data.member != null">
															<span class = "text-secondary">{{data.names}}</span>
														</td>

														<td>{{humanize(data.amount)}}</td>
														<td><p class="text-secondary">{{humanize(data.amount_so_far)}}</p></td>
														<td><p class="text-danger">{{humanize(data.remaining_amount)}}</p></td>
														<td>{{data.percentage_funded}}</td>

													</tr>
												</tbody>
										</table>
										<div class="mt-3 d-flex justify-content-end">
											<div class="d-flex justify-content-end">
												<button class="btn" @click="prevPage"
													:disabled="pageNumber == 1">
													<i class="arrow left"></i>
												</button>
												<span class="p-3">{{pageNumber}} / {{pageCount}}</span>
												<button class="btn" @click="nextPage"
													:disabled="(pageNumber) == pageCount">
													<i class="arrow right"></i>
												</button>
											</div>
										</div>
									</div>
								</div>
								<!-- pledge payments tab -->
								<div class="tab-pane fade" id="v-pills-pledgepayment" role="tabpanel" aria-labelledby="v-pills-pledgepayment-tab">
									<div v-if="pledge_payment_selected">
										<h3 class="font-weight-bold">
											Pledges
										</h3>
										<div class="">
											<div class="p-3">
												<span class="badge badge-pill badge-secondary">{{payment_ids.length}}</span> selected
											</div>
											<table class="table table-responsive-sm table-borderless">
												<thead>
													<tr>
														<th>
															<label class="anvil-checkbox">all
																<input type="checkbox" :value=true v-model="all_payments">
																<span class="anvil-checkmark"></span>
															</label>
														</th>
														<th></th>
														<th>name</th>
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
																			@click="getPledgePayments()">
																			Filter
																		</button>
																	</div>
															</div>
															</div>
														</th>
														<th>this payment</th>
														<th>target</th>
														<th>remaining</th>
													</tr>
												</thead>
												<tbody>
													<tr v-for = "data in pledge_payments.response">
														<td>
														   <label class="anvil-checkbox">
																<input multiple type="checkbox" :value=data.id v-model="payment_ids">
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
														<td v-if = "data.pledge.member != null">
																<router-link :to="`/memberDetail/`+ data.pledge.member.member.id">
																		<span class = "text-secondary">{{data.pledge.member.member.first_name}} {{data.pledge.member.member.last_name}}</span>
																</router-link>
														</td>
														<td v-else>
															{{data.pledge.names}}
														</td>
														<td>{{$humanizeDate(data.payment_recorded_on)}}</td>
														<td><p class="text-muted">{{humanize(data.payment_amount)}}</p></td>
														<td><p class="text-muted">{{humanize(data.pledge.amount)}}</p></td>
														<td><p class="text-muted">{{humanize(data.remaining_amount)}}</p></td>

													</tr>
												</tbody>
											</table>
										</div>
									</div>
								</div>

						</div>
				</div>
				<!-- ACTIONS ON THE RIGHT -->
				<div class="col-12 col-sm-10 col-md-8 col-lg-3">
						<!-- add contribution button when tab is contributions -->
						<div class="btn-group" style="padding: 0px 0px 25px 10px" v-if=" tab == 'contributions'">
								<a href="#" data-toggle="modal" data-target="#addContribution" style="text-decoration: none">
									<div class="add-button" >
										<b>+</b> add contribution
									</div>
								</a>
								<button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
										<span class="sr-only">Toggle Dropdown</span>
								</button>
								<div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">
										<a class="dropdown-item" href="#" data-toggle="modal" data-target="#addPledge"><b>+</b> add pledge</a>
										<a class="dropdown-item" href="#" data-toggle="modal" data-target="#settlePledge"><b>+</b> settle pledge</a>
								</div>
						</div>
						<!-- add pledge button when tab is pladges -->
						<div class="btn-group" style="padding: 0px 0px 25px 10px" v-if="tab == 'pledges' || tab == 'pledge_payments' ">
								<a href="#" data-toggle="modal" data-target="#addPledge" style="text-decoration: none">
									<div class="add-button" >
										<b>+</b> add pledge
									</div>
								</a>
								<button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
										<span class="sr-only">Toggle Dropdown</span>
								</button>
								<div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">
										<a class="dropdown-item" href="#" data-toggle="modal" data-target="#settlePledge"><b>+</b> settle pledge</a>
										<div class="dropdown-divider"></div>
										<a class="dropdown-item" href="#" data-toggle="modal" data-target="#addContribution"><b>+</b> add contribution</a>
										<div class="dropdown-item"><router-link style="text-decoration: none" :to="{name: 'importPledgesFromCSV'}">+ Import from CSV</router-link></div>
								</div>
						</div>

						<!-- more actions -->
						<div class="list-group font-weight-bold">
								<button v-if="tab == 'contributions'" type="button" class="d-flex justify-content-about font-weight-bold text-muted list-group-item list-group-item-action border-0"
										data-toggle="modal"
										data-target="#textModalCenter">
										<span>
											<i class="fas fa-comment"></i>
											Text People
										</span>
								</button>
								<button v-if="tab == 'pledge_payments'" type="button" class="d-flex justify-content-about font-weight-bold text-muted list-group-item list-group-item-action border-0"
										data-toggle="modal"
										data-target="#paymentstextModal">
										<span>
											<i class="fas fa-comment"></i>
											Text People
										</span>
								</button>
								<button type="button" class=" d-flex justify-content-about font-weight-bold text-muted action-list list-group-item list-group-item-action border-0"
										data-toggle="modal" data-target="#exportToCSV" >
										<span>
											<i class="fas fa-file-export"></i>
											Export to CSV
										</span>
								</button>
								<button v-if="tab == 'pledges'" type="button" class="d-flex justify-content-about font-weight-bold text-muted list-group-item list-group-item-action border-0"
										data-toggle="modal"
										data-target="#deletePledgesModal">
									<span class="text-danger">
										<span><i class="fas fa-trash-alt"></i> Delete pledges</span>
									</span>
								</button>
								<button v-if="tab == 'pledge_payments'" type="button" class="d-flex justify-content-about font-weight-bold text-muted list-group-item list-group-item-action border-0"
									v-on:click="deleteEnvelopes()">
									<span class="text-danger">
										<span><i class="fas fa-trash-alt"></i> Delete</span>
									</span>
								</button>
						</div>
				</div>
				<!-- export to csv modal -->
				<div class="modal fade" id="exportToCSV" tabindex="-1" role="dialog" aria-hidden="true">
						<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							<div class="modal-header">
							<h5 class="modal-title" id="exampleModalCenterTitle">export data to CSV</h5>
							<button type="button" class="close" data-dismiss="modal" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
							</div>
							<div class="modal-body">
									<form>
											<div class="form-group">
													<div class="row">
															<label class="col-3 "><b></b></label>
															<div class="input-group form-group col-5" style="padding: 0px" >
																	<small>2 files will be downloaded, one for contributions,another for pledge settlements</small>
															</div>

													</div>
											</div>

									</form>
							</div>
							<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
							<button type="button" class="btn btn-success" v-on:click="exportData()">
								download CSVs
								<span v-if="exporting_data"
									class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
								</span>
							</button>
							</div>
						</div>
						</div>
				</div>
				<!-- add contribution Modal -->
				<div class="modal fade" id="addContribution" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
						<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							<div class="modal-header">
							<h5 class="modal-title" id="exampleModalCenterTitle">add contribution</h5>
							<button type="button" class="close" data-dismiss="modal" aria-label="Close" v-on:click="fetchdata()">
								<span aria-hidden="true">&times;</span>
							</button>
							</div>
							<div class="modal-body">
									<form>
											<div class=" row form-group" v-if="! non_member">
											  <label class="col-3"><b>member:</b></label>
											  <div class="col-8">
														<searchmember v-on:memberSelected="onMemberSelected" />
											  </div>

											</div>

											<div class=" row form-group" v-if="non_member">
													<label class="col-3"><b>names:</b></label>
													<input type="text" class="col-8 form-control" placeholder="enter name of contributor" v-model = "name_if_not_member">
											</div>
											<div class=" row form-group" v-if="non_member">
													<label class="col-3"><b>phone:</b></label>
													<div class="col-8">
															<div class="row">
																	<span class="col-4">
																			<label><b>code :</b></label>
																			<input class="form-control" type="text" placeholder="+254" v-model = "country_code">
																	</span>
																	<span class="col-8">
																			<label><b>number :</b></label>
																			<input type="text" class="form-control"  placeholder="712345678" v-model = "phone_number">
																	</span>
																	<div style="padding: 5px">
																	<p v-if="phone_number_errors.length">
																		<ul>
																				<small><li v-for="error in phone_number_errors"><p class="text-danger">{{ error }}</p></li></small>
																		</ul>
																		</p>
																   <p v-if="phone_number_OK.length">
																		<ul>
																				<small><li v-for="error in phone_number_OK"><p class="text-success">{{ error }}</p></li></small>
																		</ul>
																	</p>
																	</div>
															</div>
													</div>
											</div>
											<hr/>
											<div class="row form-group">
													<label class="col-3"><b>amount:</b></label>
													<input type="number" class=" col-3 form-control" placeholder="amount" v-model="contribution_amount">
													<div class="col-6 text-success" v-if ="contribution_amount > 0"><h3>KSh {{humanize(contribution_amount)}}</h3></div>
											</div>
									</form>
							</div>
							<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal" v-on:click="fetchdata()">Close</button>
							<button type="button" class="btn btn-success" disabled v-if="! enable_add_button">
									+ add contribution
									<span v-if="adding_to_project"
										 class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
								   </span>
							</button>
							<button type="button" class="btn btn-success" v-if="enable_add_button" v-on:click="addContribution()">
									{{add_contribution_button_text}}
									<span v-if="adding_to_project"
										 class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
								   </span>
							</button>
							</div>
						</div>
						</div>
				</div>
				<!-- add pledge Modal -->
				<div class="modal fade" id="addPledge" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
						<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							<div class="modal-header">
							<h5 class="modal-title" id="exampleModalCenterTitle">add pledge</h5>
							<button type="button" class="close" data-dismiss="modal" aria-label="Close" v-on:click="getPledges()">
								<span aria-hidden="true">&times;</span>
							</button>
							</div>
							<div class="modal-body">
									<form>
											<div class=" row form-group" v-if="! non_member">
											  <label class="col-3"><b>member:</b></label>
											  <div class="col-8">
														<searchmember v-on:memberSelected="onMemberSelected" />
														<p v-if="selected_member_errors.length">
																<ul>
																		<small><li v-for="error in selected_member_errors"><p class="text-danger">{{ error }}</p></li></small>
																</ul>
														</p>
											  </div>

											</div>

											<div class=" row form-group" v-if="non_member">
													<label class="col-3"><b>names:</b></label>
													<input type="text" class="col-8 form-control" placeholder="enter name of person pledging" v-model="name_if_not_member">
													<div style="padding: 5px; text-align: center">
													<p v-if="name_if_not_member_errors.length">
														<ul>
																<small><li v-for="error in name_if_not_member_errors"><p class="text-danger">{{ error }}</p></li></small>
														</ul>
													</p>
													</div>
											</div>

											<div class=" row form-group" v-if="non_member">
													<label class="col-3"><b>phone:</b></label>
													<div class="col-8">
															<div class="row">
																	<span class="col-4">
																			<label><b>code :</b></label>
																			<input class="form-control" type="text" placeholder="+254" v-model = "country_code">
																	</span>
																	<span class="col-8">
																			<label><b>number :</b></label>
																			<input type="text" class="form-control"  placeholder="712345678" v-model = "phone_number">
																	</span>
															</div>
															<div style="padding: 5px">
																<p v-if="phone_number_errors.length">
																	<ul>
																			<small><li v-for="error in phone_number_errors"><p class="text-danger">{{ error }}</p></li></small>
																	</ul>
																	</p>
															   <p v-if="phone_number_OK.length">
																	<ul>
																			<small><li v-for="error in phone_number_OK"><p class="text-success">{{ error }}</p></li></small>
																	</ul>
																</p>
														   </div>
													</div>
											</div>
											<hr/>
											<div class="row">
														<label class="col-3 "><b>due date</b></label>
														<div class="col-8">
															<div class="row">
																<div class="input-group form-group col-8" style="padding: 0px" >
																		<input type="date" name="bday" max="3000-12-31"
																			   min="1000-01-01" class="form-control" v-model="pledge_due_date">
																</div>
															</div>
															<p v-if="pledge_date_errors.length">
																<ul>
																		<small><li v-for="error in pledge_date_errors"><p class="text-danger">{{ error }}</p></li></small>
																</ul>
															</p>
														</div>
												</div>
											<hr/>
											<div class="row form-group">
													<label class="col-3"><b>amount:</b></label>
													<input type="number" class=" col-3 form-control" placeholder="amount" v-model="pledge_amount">
													<div class="col-6 text-success" v-if ="pledge_amount > 0"><h3>KSh {{humanize(pledge_amount)}}</h3></div>
													<p v-if="pledge_amount_errors.length">
														<ul>
																<small><li v-for="error in pledge_amount_errors"><p class="text-danger">{{ error }}</p></li></small>
														</ul>
													</p>
											</div>
									</form>
							</div>
							<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal" v-on:click="getPledges()">Close</button>
							<button type="button" class="btn btn-success" disabled v-if="! enable_add_pledge_button">
									<b>+</b> add pledge
									<span v-if="adding_to_project"
										 class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
								   </span>
							</button>
							<button type="button" class="btn btn-success" v-if="enable_add_pledge_button" v-on:click="addPledge()">
									{{add_pledge_button_text}}
									<span v-if="adding_to_project"
										class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
									</span>
							</button>
							</div>
						</div>
						</div>
				</div>
				<!-- settle pledge Modal -->
				<div class="modal fade" id="settlePledge" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
						<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							<div class="modal-header">
							<h5 class="modal-title" id="exampleModalCenterTitle">settle pledge</h5>
							<button type="button" class="close" data-dismiss="modal" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
							</div>
							<div class="modal-body">
									<form>
											<div class="row checkbox">
													<div class="col-3"></div>
													<div class="col-8">
															<label><input type="checkbox" :value= true v-model = "non_member"> settle for non-member </label>
													</div>
											</div>
											<hr/>

											<div class=" row form-group" v-if="! non_member">
												<label class="col-3"><b>member:</b></label>
												<div class="col-8">
														<searchmember v-on:memberSelected="onMemberSelected" />
														<p v-if="selected_member_errors.length">
																<ul>
																		<small><li v-for="error in selected_member_errors"><p class="text-danger">{{ error }}</p></li></small>
																</ul>
														</p>
												</div>

											</div>

											<div class=" row form-group" v-if="non_member">
													<label class="col-3"><b>names:</b></label>
													<input type="text" class="col-8 form-control" placeholder="enter name of person pledging" autofocus>
											</div>
											<div class=" row form-group" v-if="non_member">
													<label class="col-3"><b>phone:</b></label>
													<div class="col-8">
															<div class="row">
																	<span class="col-4">
																			<label><b>code :</b></label>
																			<input class="form-control" type="text" placeholder="+254" v-model = "country_code">
																	</span>
																	<span class="col-8">
																			<label><b>number :</b></label>
																			<input type="text" class="form-control"  placeholder="712345678" v-model = "phone_number">
																	</span>
															</div>
													</div>
													<div style="padding: 5px">
																<p v-if="phone_number_errors.length">
																	<ul>
																			<small><li v-for="error in phone_number_errors"><p class="text-danger">{{ error }}</p></li></small>
																	</ul>
																	</p>
															   <p v-if="phone_number_OK.length">
																	<ul>
																			<small><li v-for="error in phone_number_OK"><p class="text-success">{{ error }}</p></li></small>
																	</ul>
																</p>
													 </div>
											</div>
											<hr/>
											<div class="row form-group">
														<label class="col-3"><b>amount:</b></label>
														<input type="number" class=" col-3 form-control" placeholder="amount" v-model="pledge_amount">
														<div class="col-6 text-success" v-if ="pledge_amount > 0"><h3>KSh {{humanize(pledge_amount)}}</h3></div>
														<p v-if="pledge_amount_errors.length">
															<ul>
																	<small><li v-for="error in pledge_amount_errors"><p class="text-danger">{{ error }}</p></li></small>
															</ul>
														</p>
												</div>
									</form>
							</div>
							<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal" v-on:click="fetchdata();getPledges()">Close</button>
							<button type="button" class="btn btn-success" v-on:click="settlePledge()">
								settle pledge
								<span v-if="adding_to_project"
										class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
								</span>
							</button>
							</div>
						</div>
						</div>
				</div>
				<!-- export to csv modal -->
				<div class="modal fade" id="paymentstextModal" tabindex="-1" role="dialog" aria-hidden="true">
						<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							<div class="modal-header">
								<h5 class="modal-title" id="exampleModalCenterTitle">send Message</h5>
							</div>
							<div class="modal-body">
								<label for="">Message ({{payment_ids.length}} payments selected)</label>
								<br>
								<small v-if="sms_credit_balance">sms credit balance - {{sms_credit_balance}} </small>
								<textarea rows="5" class="form-control" placeholder="Text message" v-model="payments_text_message">
								</textarea>
								<p class="mt-2 ml-2 small text-muted"><span class="font-weight-bold">{{parseInt((payments_text_message.length)/160)}}</span> messages | a message is 160 characters long</p> 
								<small class="mt-2 small text-muted">
									[name] ---- will be replaced by the member's name.<br/>
									[pledged_amount] ---- the amount pledged.<br/>
									[payed_amount] ---- the amount payed.<br/>
									[date] ---- the date <br>
									[remaining_amount] ---- the amount remaining
								</small>
							</div>
							<div class="modal-footer">
							<button type="button" id="closeTextModal" class="btn btn-secondary" data-dismiss="modal">Close</button>
							<button v-if="payment_ids.length > 0" type="button" class="btn btn-success" v-on:click="sendPaymentsReceivedMessage()">
								send Message
								<span v-if="sending_message"
									class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
								</span>
							</button>
							<button disabled v-if="payment_ids.length == 0" type="button" class="btn btn-outline-secondary"
								data-toggle="tooltip" data-placement="top" title="No members selected. Select members to send message.">
								Nothing selected
							</button>
							</div>
						</div>
						</div>
				</div>

				<!-- Delete pledges -->
				<div class="modal fade" id="deletePledgesModal" tabindex="-1" role="dialog" aria-hidden="true">
						<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							<div class="modal-header">
								<h5 class="modal-title" id="exampleModalCenterTitle">Delete pledges</h5>
							</div>
							<div class="modal-body">
								<label for="">{{pledge_ids.length}} pledges will be deleted</label>							
							</div>
							<div class="modal-footer">
							<button type="button" id="closeDeletePledgesModal" class="btn btn-secondary" data-dismiss="modal">Close</button>
							<button v-if="pledge_ids.length > 0" type="button" class="btn btn-success" v-on:click="deletePledges()">
								Delete pledges
								<span v-if="deleting_pledges"
									class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
								</span>
							</button>
							<button disabled v-if="pledge_ids.length == 0" type="button" class="btn btn-outline-secondary"
								data-toggle="tooltip" data-placement="top" title="No pledges selected">
								Nothing selected
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
import searchmember from '@/subcomponents/searchmember.vue'
import textmessage from '@/subcomponents/textmessage.vue'
export default {
	name : 'projectDetail',
	components: { searchmember,textmessage },
	data () {
		return {
		from_date:null,
		to_date:null,
		//get data
		foundItems: 0,
		pledges_count: 0,
		logged_in_member_id: null,
		context: null,
		tab: 'pledges',
		contributions: null,
		pledges: null,
		pledge_payments:[],
		pledge_payment_selected:false,
		pledges_selected: false,
		foundItems: null,
		fetch_data_error: [],
		deleting_pledges:false,
		//search for member
		// This value is set to the value emitted by the child
		selectedMember: null,
		pledge_ids: [],
		all_payments:false,
		payment_ids:[],
		all_payment_ids:[],
		payments_text_message:null,
		sending_message:false,
		//add contribution
		adding_to_project: false,
		non_member: false,
		add_contribution_button_text: '+ add contribution',
		contribution_amount: null,
		name_if_not_member: '',
		phone_number: '',
		country_code: '+254',
		enable_add_button: false,
		phone_number_errors: [], phone_number_OK: [],
		added_contribution: [],
		//add pledge
		add_pledge_button_text: '+ add pledge',
		enable_add_pledge_button: true,
		pledge_amount: null,
		pledge_due_date: '',
		pledge_amount_errors: [],
		selected_member_errors: [],name_if_not_member_errors: [],
		pledge_date_errors: [],
		//download csv
		exporting_data:false,
		//member ids
		all_pledge_ids_selected: false,
		pledge_ids: [],
		all_pledge_ids: [],
		//sending message
		sms_context:'Contribution',
		can_send_message:false,
		message: " ",
		sms_status: [],
		//pagination
		pageNumber: 1,
		pageCount:1,
		sms_credit_balance : null
		}
	},
	created () {
		this.fetchdata()
		this.getSMSCreditBalance()
	},
	watch: {
		'$route': 'fetchdata',
		all_pledge_ids_selected: function(){
			if (this.all_pledge_ids_selected != true){
				this.pledge_ids = []
			}
			else{								
				this.pledge_ids = this.all_pledge_ids
			}
		},
		all_payments:function(){
			if (this.all_payments != true){
				this.payment_ids = []
			}
			else{
				this.payment_ids = this.all_payment_ids
			}
		},
	//add contribution
		name_if_not_member: function(){
			if (this.name_if_not_member.length > 0
				&& this.non_member
				&& this.contribution_amount > 0){
					this.added_contribution = []
					this.enable_add_button = true
			}
		},
		contribution_amount: function(){
			this.add_contribution_button_text = '+ add contribution'
			if (this.contribution_amount > 0
				&& this.selectedMember > 0
				|| this.name_if_not_member.length > 0){
					this.added_contribution = []
					this.enable_add_button = true
			}
		},
		phone_number: function(){
			if (this.phone_number.isNaN){
					this.phone_number_errors = []
					this.phone_number_errors.push(" phone number should be numbers only")
			}
			if (this.phone_number.length > 9){
					this.phone_number_OK = []
					this.phone_number_errors = []
					this.phone_number_errors.push("number too long")
			}
			if (this.phone_number.length < 9){
					this.phone_number_OK = []
					this.phone_number_errors = []
					this.phone_number_errors.push("number too short")
			}
			if (this.phone_number.length == 9){
					this.phone_number_errors = []
					this.phone_number_OK.push(" number OK")
			}
		},
		pageNumber: function(){
			this.getPledges()
		}

	 },
	methods: {
		nextPage(){
			this.pageNumber++
		},
		prevPage(){
			this.pageNumber--
		},
		onMemberSelected (value) {
			this.selectedMember = value
			this.pledge_amount = 0
			this.contribution_amount = 0
		  },
		humanize: function(x) {
				return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		},
		getSMSCreditBalance: function(){
			this.$http.get(this.$BASE_URL + '/api/sms/sms-credit-balance')
			.then((response)=>{            
				this.sms_credit_balance =  response.data.UserData.balance
			})
		},
		exportData: function(){
			const FileDownload = require('js-file-download');
			//export contributions to csv
			this.exporting_data = true
			var project_name = this.context.response[0].name.split(" ").join("")
			this.$http.get(this.$BASE_URL + '/api/projects/get-project-contributions-as-csv/' + this.$route.params.id +'/' )
			.then(response => {
				FileDownload(response.data, project_name + "_contributions.csv");
			   this.exporting_data = false
			})
			.catch((error) => {
				this.exporting_data = false
				alert('error while downloading csv')
			})

			//export pledge settlements to csv
			this.exporting_data = true
			var project_name = this.context.response[0].name.split(" ").join("")
			this.$http.get(this.$BASE_URL + '/api/projects/get-pledge-payments-as-csv/' + this.$route.params.id +'/' )
			.then(response => {
				FileDownload(response.data, project_name + "_pledges.csv");
			   this.exporting_data = false
			})
			.catch((error) => {
				this.exporting_data = false
				alert('error while downloading csv')
			})
		},
		fetchdata: function() {			
			this.fetch_data_error = []
			//get project with id
			this.$store.dispatch('update_isLoading', true)
			this.$http.get(this.$BASE_URL +'/api/projects/project-with-id/' + this.$route.params.id + '/')
				.then(response => {
				this.context = {"response": response.data }
				this.payments_text_message = `Dear [name], Thank you for your generous support towards ${this.context.response[0].name} project  with a pledge of  Kshs  [pledged_amount]  . Total amount paid so far is Kshs [payed_amount]. Balance is kshs. [remaining_amount] .`
				this.$store.dispatch('update_isLoading', false)
				})
				.catch((err) => {
					this.fetch_data_error.push(err)
					this.$store.dispatch('update_isLoading', false)
				})


		   // contributions  towards a project
			this.$store.dispatch('update_isLoading', true)
			this.$http.get(this.$BASE_URL +'/api/projects/contribution-for-project/'+ this.$route.params.id + '/')
				.then(response => {
				this.contributions = {"response": response.data }
				var array = this.contributions.response
				//set up selected members
				for (var contribution in array){
						this.all_pledge_ids.push(array[contribution].member.member.id)
				}
				this.foundItems = array.length
				this.$store.dispatch('update_isLoading', false)
				})
				.catch((err) => {
				this.$store.dispatch('update_isLoading', false)
				})

		  this.getPledges()

		},
		getPledges: function(){
			this.memberSearch = ''
			this.pledges_selected = true
			this.$store.dispatch('update_isLoading', true)
			this.$http.get(this.$BASE_URL +'/api/projects/pledges-for-project/'+ this.$route.params.id + '/',
				{ params: { p: this.pageNumber } }
				).then(response => {						
						this.pledges = {"response": response.data.data }
						var array = this.pledges.response
						this.all_pledge_ids = []
						// set up member ids for selection
						for (var pledge in array){														
							this.all_pledge_ids.push(array[pledge].id)
						}						
						this.pledges_count = array.length
						this.pageCount = response.data.page_count
						this.$store.dispatch('update_isLoading', false)
					})
					.catch((err) => {
						this.$store.dispatch('update_isLoading', false)
			})
		},
		getPledgePayments: function(){
			this.payment_ids = []
			this.memberSearch = ''
			this.pledge_payment_selected = true
			this.$store.dispatch('update_isLoading', true)
			var params
			if (this.from_date && this.to_date){
				params = {from_date : this.from_date, to_date : this.to_date}
			}
			this.$http({
				method: 'get',
				url : `${this.$BASE_URL}/api/projects/pledge-payment-for-project/${this.$route.params.id}/`,
				params: params
			}).then((response) => {
				this.all_payment_ids = []
				this.pledge_payments = {"response": response.data }
				var array = this.pledge_payments.response
				// set up member ids for selection
				for (var pledge of array){
					this.all_payment_ids.push(pledge.id)
				}
				this.$store.dispatch('update_isLoading', false)
			}).catch((err) => {
					this.$store.dispatch('update_isLoading', false)
			})
		},
		getContributionsTab: function(){
			this.tab = 'contributions'
			this.sms_context = "Contribution"			
		},
		getPledgesTab: function(){
			this.sms_context = "Pledge"
			this.tab='pledges'			
		},
		getPledgePaymentsTab: function(){
			this.getPledgePayments()
			this.sms_context = "PledgePayments"
			this.tab='pledge_payments'			
		},
		//add contribution
		addContribution: function(){
			if (this.non_member){
				this.enable_add_project_button = false
				this.adding_to_project = true
				this.add_contribution_button_text = '+ adding contribution...'
				this.$http({
				method: 'post',
				url: this.$BASE_URL + '/api/projects/add-non-member-contribution-to-project/',
				data: {
					project_id: this.$route.params.id,
					names: this.name_if_not_member,
					recording_member_id: this.$session.get('member_id'),
					phone: this.country_code.toString() + this.phone_number.toString(),
					anonymous: true,
					amount: this.contribution_amount
				}
				}).then(response => {
					alert("contribution succesfully added")
					if (this.auto_message ){
						this.can_send_message = true
					}
					this.adding_to_project = false
					this.enable_add_project_button = true
					this.name_if_not_member = ''
					this.phone_number = ''
					this.contribution_amount = null
					this.add_contribution_button_text = '+ add contribution'
				})
				.catch((err) => {
					this.adding_to_project = false
					this.enable_add_project_button = true
					this.add_contribution_button_text = '+ add contribution'
					alert("an error has occured, try again later")
				})
				}
				if (! this.non_member){
					this.enable_add_project_button = false
					this.adding_to_project = true
					this.add_contribution_button_text = 'adding contribution...'
					this.$http({
					method: 'post',
					url: this.$BASE_URL + '/api/projects/add-contribution-to-project/',
					data: {
						project_id: this.$route.params.id,
						member_id: this.selectedMember,
						recording_member_id: this.$session.get('member_id'),
						anonymous: false,
						amount: this.contribution_amount
					}
					}).then(response => {
						this.adding_to_project = false
						this.memberSearch = ''
						this.contribution_amount = null
						this.added_contribution.push(response.data)
						this.add_contribution_button_text = '+ add contribution'
						this.enable_add_button = true
						alert("contribution succesfully added")
					})
					.catch((err) => {
						this.adding_to_project = false
						this.enable_add_project_button = true
						this.add_contribution_button_text = '+ add contribution'
						alert("an error has occured, try agin later")
					})
				}
		},
		pledgeFormOkay: function(){

			this.pledge_amount_errrors = []
			this.selected_member_errors = []
			this.pledge_date_errors = []
			this.pledge_amount_errors = []
			this.name_if_not_member_errors = []

			if (     !  this.non_member
					&& (this.pledge_amount != null
					|| this.pledge_amount > 0)
					&& (this.selectedMember != null
					|| this.selectedMember != 0)
					&& this.pledge_due_date.length == 10){
							return true
					}
			if (    this.non_member
					&& (this.pledge_amount != null
					|| this.pledge_amount > 0)
					&& (this.name_if_not_member != null
					|| this.name_if_not_member != '')
					&& this.pledge_due_date.length == 10){
							return true
					}
			if (    ! this.non_member
					&&  (this.selectedMember == null
					|| this.selectedMember == 0)){
							this.selected_member_errors.push("select a member")
							return false
			}
			if (    this.non_member
					&& (this.name_if_not_member.length < 1
					|| this.name_if_not_member == null)){
							this.name_if_not_member_errors.push("enter name of the contributor")
							return false
			}
			if (this.pledge_due_date.length == 0){
					this.pledge_date_errors.push("date input required")
					return false
			}
			if (this.pledge_due_date.length != 10){
					this.pledge_date_errors.push("incorrect date use YYYY-MM-DD format")
					return false
			}
			if (this.pledge_amount < 1
					|| this.pledge_amount == null){
							this.pledge_amount_errors.push("pledge amount required")
							return false
			}
		},
		addPledge: function(){
			if (this.pledgeFormOkay()){
				if (! this.non_member){
					this.adding_to_project = true
					this.$http({
							method: 'post',
							url: this.$BASE_URL + '/api/projects/add-pledge-to-project/',
							data: {
								project_id: this.$route.params.id,
								member_id: this.selectedMember,
								recording_member_id: this.$session.get('member_id'),
								amount: this.pledge_amount,
								date: this.pledge_due_date
							}
							}).then(response => {
								this.selectedMember = null
								this.pledge_amount = null
								this.adding_to_project = false
								this.enable_add_pledge_button = true
								this.memberSearch = ''
								alert("pledge of amount " + response.data.amount + "\n" + "added for " + response.data.member.member.first_name)
							})
							.catch((err) => {
								this.adding_to_project = false
								alert("an error occured while attempting to add pledge. \n"
										+ "check your connection and try again")

							})
				}
				if (this.non_member){
					this.adding_to_project = true
					this.$http({
						method: 'post',
						url: this.$BASE_URL + '/api/projects/add-anonymous-pledge-to-project/',
						data: {
							project_id: this.$route.params.id,
							recording_member_id: this.$session.get('member_id'),
							phone: this.country_code + this.phone_number,
							names: this.name_if_not_member,
							amount: this.pledge_amount,
							date: this.pledge_due_date
						}
						}).then(response => {
							this.adding_to_project = false
							this.selectedMember = null
							this.name_if_not_member = null
							this.phone_number = null
							this.phone_number_errors = []
							this.pledge_amount = null
							this.enable_add_pledge_button = true
							this.memberSearch = ''
							alert("pledge of amount " + response.data.amount + "\n"
									+ "added for " + response.data.names)
						})
						.catch((err) => {
							this.adding_to_project = false
							alert("an error occured while attempting to add pledge. \n"
									+ "check your connection and try again")
						})
					}
			}
		},
		settlePledgeFormOkay: function(){

				this.pledge_amount_errrors = []
				this.selected_member_errors = []
				this.pledge_amount_errors = []
				this.name_if_not_member_errors = []

				if (     !  this.non_member
						&& (this.pledge_amount != null
						|| this.pledge_amount > 0
						|| this.pledge_amount.length != 0)
						&& (this.selectedMember != null
						|| this.selectedMember != 0)){
								return true
						}
				if (    this.non_member
						&& (this.pledge_amount != null
						|| this.pledge_amount > 0)
						&& (this.name_if_not_member != null
						|| this.name_if_not_member != '')){
								return true
						}
				if (    ! this.non_member
						&&  (this.selectedMember == null
						|| this.selectedMember == 0)){
								this.selected_member_errors.push("select a member")
								return false
				}
				if (    this.non_member
						&& (this.name_if_not_member.length < 1
						|| this.name_if_not_member == null)){
								this.name_if_not_member_errors.push("enter name of the person who pledged")
								return false
				}
				if (this.pledge_amount < 1
						|| this.pledge_amount == null
						|| this.pledge_amount.length == 0){
								this.pledge_amount_errors.push("pledge amount required")
								return false
				}
				},
		settlePledge: function(){
			if (this.settlePledgeFormOkay()){
				if (! this.non_member){
					this.adding_to_project = true
					this.$http({
						method: 'post',
						url: this.$BASE_URL + '/api/projects/service-pledge/',
						data: {
							project_id: this.$route.params.id,
							member_id: this.selectedMember,
							recording_member_id: this.$session.get('member_id'),
							amount: this.pledge_amount
						}
						}).then(response => {
							this.selectedMember = null
							this.pledge_amount = null
							this.adding_to_project = false
							this.enable_add_pledge_button = true
							this.memberSearch = ''
							alert("amount " + response.data.payment_amount+ " "
								+ "settled for pledge by " + response.data.pledge.member.member.first_name
								+ "\n remaining amount is " + response.data.pledge.remaining_amount
								+ "\n percentage settled is "
								+ response.data.pledge.percentage_funded )
						})
						.catch((err) => {
							this.adding_to_project = false
							alert("error, this may be because the member you selected has not pledged for this project")
						})
				}
			}
		},
		sendPaymentsReceivedMessage: function(){
			this.sending_message = true
			this.$http({
				method: 'post',
				url: this.$BASE_URL + '/api/projects/send-pledge-payment-received-message/',
				data: {
					payment_ids: this.payment_ids,
					message: this.payments_text_message,
				}
				}).then(response => {
					document.getElementById('closeTextModal').click()					
					localStorage.setItem('pledge_message',this.payments_text_message)
					console.log(localStorage.getItem('pledge_message'))
					this.getPledgePayments()
					this.sending_message = false
				})
				.catch((err) => {
					this.sending_message = false
					alert("an error occured")
				})
		},
		// delete payments
		deleteEnvelopes: function (){
			if (confirm(`Delete ${this.payment_ids.length} Pledge payments. This cannot be reversed`)){
				this.$store.dispatch('update_isLoading', true)
				this.$http({
					method: 'delete',
					url: this.$BASE_URL + '/api/projects/delete-pledge-payments/',
					data: {
						ids: this.payment_ids,
					}
					}).then(() => {
						this.$store.dispatch('update_isLoading', false)
						this.getPledgePayments()
					})
					.catch((err) => {
						this.$store.dispatch('update_isLoading', false)
						this.getPledgePayments()
					})
				}
		},
		deletePledges: function(){
			this.$store.dispatch('update_isLoading', true)
			this.deleting_pledges = true
			this.$http({
				method: 'delete',
				url: this.$BASE_URL + '/api/projects/delete-pledges/',
				data: {
					ids: this.pledge_ids,
				}
				}).then(() => {
					document.getElementById('closeDeletePledgesModal').click()
					this.deleting_pledges = false
					this.$store.dispatch('update_isLoading', false)
					this.pledge_ids = []
					this.getPledges()					
				})
				.catch((err) => {
					this.deleting_pledges = false
					this.$store.dispatch('update_isLoading', false)					
				})
		}		
	}

}
</script>
<style >
</style>

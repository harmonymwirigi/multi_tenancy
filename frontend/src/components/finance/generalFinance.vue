<template>
    <div>
        <!-- this component requires text message modal -->
        <textmessage :memberIds="member_ids" :context="context"/>
        <!-- the modal used to import finace data from csv -->
        <importFromCSV v-on:dataExtracted="csvDataExtracted"/>

        <nav aria-label="breadcrumb" class="continer">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li>
                <li class="breadcrumb-item active" aria-current="page">finances</li>
            </ol>
        </nav>
        <div class = "continer">
            <div class = "row">
                <!-- NAVIGATIONS -->
                <div class="filters col-sm-12 col-md-8 col-lg-2 border rounded" >
                        <div class="mt-3 nav success flex-column nav-pills" style="height:100vh" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                                <a class="action-list list-group-item list-group-item-action border-0 active" id="v-pills-envelopes-tab" data-toggle="pill" href="#v-pills-envelopes" role="tab" aria-controls="v-pills-envelopes" aria-selected="true"
                                    v-on:click=" hide_content = true">
                                    <span class="" style="white-space:nowrap">
										<i class="text-dark far fa-clock"></i>
										Quick links
                                    </span>
                                </a>

                                <a class="action-list list-group-item list-group-item-action border-0" id="v-pills-envelopes-tab" data-toggle="pill" href="#v-pills-envelopes" role="tab" aria-controls="v-pills-envelopes" aria-selected="true"
                                    v-on:click="getAll(); hide_content=false">
                                    <span >
										<i class="text-dark far fa-envelope"></i>
										Envelopes
                                    </span>
                                </a>
                                <a     class="action-list list-group-item list-group-item-action border-0"
                                        id="v-pills-income-tab" data-toggle="pill" href="#v-pills-income"
                                        role="tab" aria-controls="v-pills-income"
                                        v-on:click="tithes_selected = true; expenditures_selected=false; getIncome()">

                                    <span>
                                        <i class="text-dark fas fa-coins"></i>
                                        Income
                                    </span>
                                </a>
                                <a class="action-list list-group-item list-group-item-action border-0" id="v-pills-expenditure-tab" data-toggle="pill" href="#v-pills-expenditure" role="tab" aria-controls="v-pills-expenditure" aria-selected="false" v-on:click="getExpenditures()">
                                    <span>
                                        <i class="text-dark far fa-share-square"></i>
                                        Expenditure
                                    </span>
                                </a>
                                <router-link class="action-list list-group-item list-group-item-action border-0" id="v-pills-expenditure-tab" :to="{name: 'projectList'}">
                                    <span>
                                        <i class="text-dark fas fa-tasks"></i>
                                        Projects
                                    </span>
                                </router-link>
                            </div>
                </div>
                <!-- CONTENT -->
                <div class = "col-lg-7 col-sm-12">
                    <div class="tab-content" id="v-pills-tabContent">
                       <!-- ENVELOPES -->
                        <div class="tab-pane fade show active" id="v-pills-envelopes" role="tabpanel" aria-labelledby="v-pills-envelopes-tab">
                            <!-- on hide content -->
                            <div class="mt-5 mb-5 d-flex flex-wrap justify-content-center"
                                v-if="hide_content">
                                <a class="p-4 d-flex justify-content-center"
                                    href="#" data-toggle="modal"
                                    data-target="#importFromCSV">
									<span><i class="text-dark fas fa-file-import"></i> Import from CSV &rarr;</span>
                                </a>
                            </div>
                            <!-- when content is to be shown -->
                            <div  class="continer" :class="{'d-none': hide_content}">
                                <div class="d-flex justify-content-center">
                                    <!-- nav pills for offerings,tithes and others -->
                                    <div class="col-sm-12 col-lg-10" >
                                        <hr class="d-sm-block d-lg-none">
                                        <div class="d-flex flex-nowrap">
                                            <a href="#" class="p-2" @click=scrollRight()>
                                                <i class="arrow left"></i>
                                            </a>
                                            <ul class="mb-2 d-flex flex-nowrap nav nav-pills scrollbar-none"
                                                id="pills-tab" role="tablist"
                                                style="overflow-x: scroll;white-space: nowrap">
                                                    <li class="nav-item">
                                                        <a class="nav-link active"
                                                            id="pills-all-tab"
                                                            data-toggle="pill"
                                                            href="#pills-all" role="tab"
                                                            aria-controls="pills-all"
                                                            Tithe="true"
                                                            v-on:click = "getAll(); scrollToElement('pills-tithe-tab')">
                                                            All
                                                        </a>
                                                    </li>
                                                    <li class="nav-item">
                                                        <a class="nav-link"
                                                            id="pills-tithe-tab"
                                                            data-toggle="pill"
                                                            href="#pills-home" role="tab"
                                                            aria-controls="pills-home"
                                                            Tithe="true"
                                                            v-on:click = "getTithes(); scrollToElement('pills-tithe-tab')">
                                                            Tithes
                                                        </a>
                                                    </li>
                                                    <li class="nav-item" v-for="type in offering_types">
                                                        <a class="nav-link text-capitalize" :id="`type-${type.id}`"
                                                            data-toggle="pill" :href="`#pills-${type.id}`" role="tab"
                                                            :aria-controls="`pills-${type.id}`"
                                                            aria-selected="false"
                                                            @click="offering_type = type;scrollToElement(`type-${type.id}`);getOfferings()">
                                                            <span v-if="type.name != 'general offering'">{{type.name}}</span>
                                                            <span v-else>Offering</span>
                                                        </a>
                                                    </li>
                                            </ul>
                                            <a href="#" class="p-2" @click=scrollLeft()>
                                                <i class="arrow right"></i>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- ENVELOP TABS CONTENT -->
                            <div class="tab-content" id="pills-tabContent">
                                <!-- tithes -->
                                <div class="tab-pane fade show active" id="pills-all" role="tabpanel" aria-labelledby="pills-all-tab">
                                    <h3 v-if="! hide_content" class="font-weight-bold">All</h3>
                                    <hr>
                                    <all
                                        v-on:membersSelected="setMemberIds"
                                        :payment_methods = "payment_methods"
                                        :reload_data = "reload_data"
                                        :hide_content = "hide_content"
                                    />
                                </div>
                                <!-- tithes -->
                                <div class="tab-pane" id="pills-home" role="tabpanel" aria-labelledby="pills-home-tab">
                                        <h3 v-if="! hide_content" class="font-weight-bold">Tithes </h3>
                                        <hr>
                                        <tithes
                                            v-on:membersSelected="setMemberIds"
                                            :payment_methods = "payment_methods"
                                            :reload_data = "reload_data"
                                            :hide_content = "hide_content"
                                      />
                                </div>
                                <!-- Offerings-->
                                <div v-for="type in offering_types"
                                    class="tab-pane fade"
                                    :id="`pills-${type.id}`" role="tabpanel">
                                    <div>
                                        <!-- offerings -->
                                        <div v-if="! hide_content">
                                            <h3 class="font-weight-bold text-capitalize"
                                            v-if="type.name != 'general offering'">{{type.name}}</h3>
                                            <h3 class="font-weight-bold" v-else>Offering</h3>
                                        </div>
                                        <hr>
                                        <offerings
                                            :offering_type="type"
                                            :payment_methods = "payment_methods"
                                            :reload_data = "reload_data"
                                            v-on:membersSelected="setMemberIds"
                                            :hide_content = "hide_content"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- INCOME -->
                        <div class="tab-pane fade show" id="v-pills-income" role="tabpanel" aria-labelledby="v-pills-expenditure-tab">
                            <div>
                                <div v-if="any_other_selected">
                                    <hr class="d-sm-block d-lg-none">
                                    <h3 class="font-weight-bold">Other incomes</h3>
                                    <hr>
                                    <div class="text-muted" v-if="any_other_selected">
                                            <div class="d-flex d-flex-row justify-content-center">
                                                <div class="d-none d-lg-block stat-item mr-2 text-muted">
                                                    This month  <span class="text-secondary font-weight-bold">
                                                    Ksh {{humanize(income_stats.response.total_this_month)}} </span>
                                                </div>
                                                <div class="d-none d-lg-block stat-item mr-2">
                                                    This year  <span class="text-secondary font-weight-bold">
                                                    Ksh   {{humanize(income_stats.response.total_this_year)}}</span>
                                                </div>
                                                <a class="ml-2 btn btn-outline-secondary dropdown-toggle" data-toggle="collapse" href="#statsTab" role="button" aria-expanded="false" aria-controls="statsTab">
                                                    more stats
                                                </a>

                                                <!-- what to show on small devices -->
                                                <div class="ml-2 d-sm-block d-md-none d-lg-none btn-group">
                                                        <a href="#" data-toggle="modal" data-target="#addIncomeType" style="text-decoration: none">
                                                            <div class="add-button">
                                                                add income type
                                                            </div>
                                                        </a>
                                                        <button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
                                                                <span class="sr-only">Toggle Dropdown</span>
                                                        </button>
                                                        <div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">
                                                            <a class="dropdown-item" href="#" data-toggle="modal" data-target="#addIncome"><b>+</b> add income</a>
                                                        </div>
                                                </div>
                                            </div>
                                            
                                            <div class="collapse" id="statsTab">
                                                <div class="card card-body outline-0">
                                                    <incomestats msg="income stats"/>
                                                </div>
                                            </div>
                                    </div>

                                    <table class="mt-4 table table-responsive-sm table-borderless">
                                        <thead>
                                            <tr>
                                                <th>Type</th>
                                                <th>This month</th>
                                                <th>This year</th>
                                                <th></th>
                                            </tr>
                                        </thead>
                                        <p class="mt-4 col-8">
                                            <span class="badge badge-pill badge-secondary">{{foundIncomes}}</span> types found
                                        </p>
                                        <tbody>
                                            <tr v-for = "data in incomes.response">
                                                <td>
                                                    <router-link class="text-secondary"  :to="`/income/`+ data.id + `/`">
                                                        {{data.type_name}}
                                                    </router-link>
                                                </td>
                                                <td><p>{{humanize(data.total_this_month)}}</p></td>
                                                <td><p class="text-secondary">{{humanize(data.total_this_year)}}</p></td>
                                                <td>
                                                    <router-link class="text-muted" :to="`/income/`+ data.id + `/`">
                                                        <img style="width: 20px ;height: auto" src="@/assets/icons/icons8-right-arrow-50.png">
                                                    </router-link>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        <!-- EXPENDITURE -->
                        <div class="tab-pane fade show " id="v-pills-expenditure" role="tabpanel" aria-labelledby="v-pills-expenditure-tab">
                            <div v-if = "expenditures_selected">
                                <hr class="d-sm-block d-lg-none">
                                <expenditures/>
                            </div>
                        </div>
                        <!-- TEST-->
                        <div class="tab-pane fade show " id="v-pills-test" role="tabpanel" aria-labelledby="v-pills-test-tab">
                           test
                        </div>
                    </div>
                </div>
                <!-- ACTION BUTTONS -->
                <div class = "col-12 col-sm-10 col-md-8 col-lg-3">
                    <!-- add for tithes -->
                    <div class="btn-group" style="padding: 0px 0px 25px 10px"
                         v-if = "(tithes_selected || offerings_selected)">
                            <a href="#" id="dropdownMenuReference" data-toggle="dropdown"
                                aria-haspopup="true" aria-expanded="false" data-reference="parent"
                                style="text-decoration: none">
                                <div class="add-button">
                                    <b>+</b> New Envelope
                                </div>
                            </a>
                            <a href="#" id="tithe-modal-button" data-toggle="modal" data-target="#addTithe">
                                <div class="add-button d-none" style="text-align: center">
                                    <b>+</b> Add Tithe
                                </div>
                            </a>
                            <button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split"
                                    id="dropdownMenuReference" data-toggle="dropdown"
                                    aria-haspopup="true" aria-expanded="false" data-reference="parent"
                            >
                                <span class="sr-only">Toggle Dropdown</span>
                            </button>
                            <div class="dropdown-menu border-success text-capitalize"
                                aria-labelledby="dropdownMenuReference"
                                style="z-index:99999">
                                <a class="dropdown-item"
                                    href="#" @click=openTitheTab()>
                                    Tithe
                                </a>
                                <a class="dropdown-item d-flex justify-content-between"
                                    v-for="type in offering_types"
                                    href="#" data-toggle="modal"
                                    data-target="#addOffering"
                                    @click="openTab(type.id)">
                                    <span v-if="type.name != 'general offering'">{{type.name}}</span>
                                    <span v-else>Offering</span>
                                    <span class="hidden p-1 font-weight-bold text-muted">&times;</span>
                                </a>
                                <hr>
                                <a class="dropdown-item"
                                    href="#" data-toggle="modal"
                                    data-target="#importFromCSV">
                                    <b>+</b> Import from CSV
                                </a>
                                <hr>
                                <a class="dropdown-item"
                                    href="#" data-toggle="modal"
                                    data-target="#addOfferingType">
                                    <b>+</b> Add Envelope Type
                                </a>
                                <a class="dropdown-item"
                                    href="#" data-toggle="modal"
                                    data-target="#addPaymentMethod">
                                    <b>+</b> Add Payment Method
                                </a>
                            </div>
                    </div>
                    <!-- add for offerings -->
                    <div class="btn-group d-none">
                            <a href="#" data-toggle="modal"
                                id = "add-offering-button"
                                :data-target="`#addOffering-${offering_type.id}`"
                                style="text-decoration: none">
                                <div class="add-button">
                                    <b>+</b> add offering
                                </div>
                            </a>
                            <button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
                                    <span class="sr-only">Toggle Dropdown</span>
                            </button>
                            <div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">
                                <a class="dropdown-item" href="#" data-toggle="modal" data-target="#addOfferingType"><b>+</b> add offering type</a>
                            </div>
                    </div>
                    <!-- add for incomes  -->
                    <div class="btn-group" style="padding: 0px 0px 25px 10px" v-if = "any_other_selected">
                            <a href="#" data-toggle="modal" data-target="#addIncomeType" style="text-decoration: none">
                                <div class="add-button">
                                    <b>+</b> add income type
                                </div>
                            </a>
                            <button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">
                                    <span class="sr-only">Toggle Dropdown</span>
                            </button>
                            <div class="dropdown-menu border-success" aria-labelledby="dropdownMenuReference">
                                <a class="dropdown-item" href="#" data-toggle="modal" data-target="#addIncome"><b>+</b> add income</a>
                            </div>
                    </div>
                    <div class="btn-group" style="padding: 0px 0px 25px 10px" v-if = "expenditures_selected">
                        <a href="#" data-toggle="modal" data-target="#addExpenditureType" style="text-decoration: none">
                            <div class="btn btn-success">
                                <b>+</b> add expenditure type
                            </div>
                        </a>
                    </div>

                    <!-- actions on list  -->
					<div class="border rounded">
						<div class="list-group font-weight-bold"  v-if = "expenditures_selected">
								<button type="button" class="d-flex justify-content-about font-weight-bold text-muted action-list list-group-item list-group-item-action border-0" data-toggle="modal" data-target="#exportEpenditureToCSV" >
								  <span><i class="fas fa-file-export"></i> Export To CSV</span>
								</button>
						</div>
						<div class="list-group font-weight-bold"  v-if = "tithes_selected">
								<button type="button" class="d-flex justify-content-about font-weight-bold text-muted list-group-item list-group-item-action border-0"
									 data-toggle="modal" data-target="#textModalCenter">
									<span><i class="far fa-comment"></i> Text people</span>
								</button>
								<button type="button" class="d-flex justify-content-about font-weight-bold text-muted action-list list-group-item list-group-item-action border-0"
									 data-toggle="modal" data-target="#exportTithesToCSV" >
									<span><i class="fas fa-file-export"></i> Export To CSV</span>
								</button>
						</div>
						<div class="list-group "  v-if = "offerings_selected">
								<button type="button" class="d-flex justify-content-about font-weight-bold text-muted list-group-item list-group-item-action border-0"
										data-toggle="modal" data-target="#textModalCenter">
										<span><i class="far fa-comment"></i> Text people</span>
								</button>
								<button type="button" class="d-flex justify-content-about font-weight-bold text-muted action-list list-group-item list-group-item-action border-0"
										data-toggle="modal" :data-target="`#exportOfferingsToCSV-${offering_type.id}`" >
										<span><i class="fas fa-file-export"></i> Export To CSV</span>
								</button>
						</div>
						<div class="list-group font-weight-bold"  v-if = "any_other_selected">
								<button type="button" class="d-flex justify-content-about font-weight-bold text-muted action-list list-group-item list-group-item-action border-0"
									 data-toggle="modal" data-target="#exportIncomeToCSV" >
									<span><i class="fas fa-file-export"></i> Export To CSV</span>
								</button>
						</div>
						<div class="list-group font-weight-bold" v-if = "tithes_selected || offerings_selected">
								<button type="button" class="d-flex justify-content-about font-weight-bold text-muted action-list list-group-item list-group-item-action border-0"
									data-toggle="modal" data-target="#deleteEnvelopes" >
									<span><i class="fas fa-trash-alt"></i> Delete envelopes</span>
								</button>
						</div>
					</div>
                </div>
            </div>
                <!-- add income modal -->
                <div class="modal fade" id="addIncome" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h5 class="modal-title font-weight-bold text-capitalize" id="exampleModalCenterTitle">add income type</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        </div>
                        <div class="modal-body">
                                <form>
                                        <div class=" row form-group">
                                            <label class="col-3"><b>type:</b></label>
                                            <select class="col-8 form-control" v-model="income_type" >
                                                <option v-for="data in income_types.response" :value="data.id" >{{data.type_name}}</option>
                                            </select>
                                            <p v-if="income_type_errors.length">
                                                <ul>
                                                        <small><li v-for="error in income_type_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                </ul>
                                            </p>
                                        </div>
                                        <hr/>
                                        <div class="row form-group">
                                                <label class="col-3"><b>amount:</b></label>
                                                <input type="number" class=" col-3 form-control" placeholder="amount" v-model="income_amount">
                                                <div class="col-6 text-success" v-if ="income_amount > 0"><h3>KSh {{humanize(income_amount)}}</h3></div>
                                                <p v-if="income_amount_errors.length">
                                                    <ul>
                                                            <small><li v-for="error in income_amount_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                    </ul>
                                                </p>
                                        </div>
                                        <hr/>
                                        <div class="row form-group">
                                            <label class="col-3"><b>narration:</b></label>
                                            <textarea type="text" class="col-8 form-control" rows='3' v-model="income_narration"></textarea>
                                        </div>
                                </form>
                        </div>
                        <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-success" v-on:click="addIncome()">
                            <b>+</b> add income
                            <span v-if="adding_to_finance"
                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                            </span>
                        </button>
                        </div>
                    </div>
                    </div>
                </div>
                <!-- add income type modal -->
                <div class="modal fade" id="addIncomeType" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalCenterTitle">add income type</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    </div>
                    <div class="modal-body">
                            <form>
                                    <div class="row form-group">
                                            <label class="col-3"><b>name:</b></label>
                                            <input type="text" class=" col-8 form-control" placeholder="give the type a name" v-model="income_type_name">
                                            <p v-if="income_type_name_errors.length">
                                                <ul>
                                                        <small><li v-for="error in income_type_name_errors"><p class="text-danger">{{ error }}</p></li></small>
                                                </ul>
                                            </p>
                                    </div>
                                    <hr/>
                                    <div class="row form-group">
                                        <label class="col-3"><b>describe:</b></label>
                                        <textarea type="text" class="col-8 form-control" rows='3' v-model="income_type_description"></textarea>
                                    </div>
                            </form>
                    </div>
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" v-on:click="getIncome()" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success" v-on:click="addIncomeType()">
                        <b>+</b> add income type
                        <span v-if="adding_to_finance"
                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                        </span>
                    </button>
                    </div>
                </div>
                </div>
                </div>
                <!-- add offering type-->
                <div   class="modal fade" id="addOfferingType" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalCenterTitle">Add Envelope Type</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                            </div>
                            <div class="modal-body">
                            <form>
                            <div class="row form-group">
                                <label class="col-3"><b>name:</b></label>
                                <input type="text" class="col-8 form-control" rows='3' maxlength="50" v-model="offering_type_name"/>
                            </div>
                                <hr/>
                                <div class="row form-group">
                                <label class="col-3"><b>description:</b></label>
                                <textarea type="text" class="col-8 form-control" rows='3' v-model="offering_type_description"></textarea>
                                </div>
                            </form>
                            </div>
                            <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-success" v-on:click="addOfferingType()">
                                <b>+</b> add envelope type
                                <span v-if="adding_offering"
                                    class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                </span>
                            </button>
                            </div>
                        </div>
                        </div>
                </div>
                <!-- add payment method-->
                <div   class="modal fade" id="addPaymentMethod" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalCenterTitle">Add Payment Method</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                            </div>
                            <div class="modal-body">
                            <form>
                            <div class="row form-group">
                                <label class="col-3"><b>name:</b></label>
                                <input type="text" class="col-8 form-control" rows='3' maxlength="50" v-model="payment_method_name"/>
                            </div>
                            </form>
                            </div>
                            <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-success" v-on:click="addPaymentMethod()">
                                <b>+</b> add payment method
                                <span v-if="adding_offering"
                                    class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                                </span>
                            </button>
                            </div>
                        </div>
                        </div>
                </div>
                <!-- export to csv format -->
                <div class="modal fade" id="exportIncomeToCSV" tabindex="-1" role="dialog" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalCenterTitle">export income data to CSV</h5>
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
                <!-- delete envelopes-->
                <div class="modal fade" id="deleteEnvelopes" tabindex="-1" role="dialog" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalCenterTitle">Delete Envelopes</h5>
                        <button type="button" id="closeDeleteEnvelopesButton" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        </div>
                        <div class="modal-body">
                            <div class="continer mt-5 mb-5">
                                <span class="d-flex fex-row"><h2 class="text-muted font-weight-bold">{{member_ids.length}} </h2>envelopes</span>
                                <h4 class="text-danger">These envelopes will be deleted</h4>
                                <i>this action is irreversible, are you sure that this is what you want??</i>
                            </div>
                        </div>
                        <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-success" v-on:click="deleteEnvelopes()">
                            delete envelope
                            <span v-if="adding_offering"
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
import router from "../../router";
import incomestats from '@/subcomponents/statistics/incomestats.vue'

import expenditures from '@/subcomponents/finances/expenditure.vue'
import all from '@/subcomponents/finances/all.vue'
import tithes from '@/subcomponents/finances/tithes.vue'
import offerings from '@/subcomponents/finances/offerings.vue'
import importFromCSV from '@/subcomponents/finances/importFromCSV.vue'
import textmessage from '@/subcomponents/textmessage.vue'
export default {
    name: 'generalFinance',
    components: {
        incomestats,
        expenditures,
        all,
        tithes,
        offerings,
        importFromCSV,
        textmessage
    } ,

    data () {
        return{
        //hide content.
        hide_content: true,
        //reloadind
        reload_data: false,
        //offering types
        offering_type: {'id':0},
        offering_types:null,
        //get data
        fetch_data_error: [],
        income_types: null,
        foundIncomes: 0,
        foundOfferings: 0,
        foundTithes: 0,
        found_expenditure_types: 0,
        //select tabs
        tithes_selected: false,
        offerings_selected: false,
        any_other_selected: false,
        expenditures_selected: false,
        //get stats data
        offering_stats: null,
        offerings: null,
        income_stats: null,
        incomes: null,
        //adding.
        adding_to_finance: false,
        //add income type
        income_type_name: '',
        income_type_description: '',
        income_type_name_errors: [],
        added_income_type: [],
        //add income
        income_type: null,
        income_narration: null,
        income_type_errors: [],
        income_amount: null,
        income_amount_errors: [],
        added_income: [],
        // add offerng type
        adding_offering: false,
        offering_type_name:null,
        offering_type_description:null,
        //payment methods
        payment_methods: null,
        //add payment method
        payment_method_name:null,
        // exporting data
        csv_date: '',
        exporting_data:false,
        //select members
        member_ids:[],
        envelope_ids:[],
        //context.
        context:{'name':'All','type':null},
        }
    },
    created () {
        this.checkLoggedIn()
        this.fetchdata()
        this.getOfferingTypes()
        this.getAll()
    },
    watch: {
        //watch for phone number input
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
        // watch for service date and type to determine if there exists a service for that day
     },
    methods: {
        csvDataExtracted:function(){
            this.reload_data = true
            setTimeout(()=>{
                this.reload_data = false
            },1000)
        },
        scrollToElement: function(element){
            document.getElementById(element).scrollIntoView({
                behavior: 'auto',
                block: 'center',
                inline: 'center'
            });
        },
        scrollLeft:function(){
            document.getElementById('pills-tab').scrollLeft += 50
        },
        scrollRight:function(){
            document.getElementById('pills-tab').scrollLeft -= 50
        },
        openTab: function(type){
            var nav_pill =  document.getElementById(`type-${type}`)
            nav_pill.click()
            var modal_button = document.getElementById(`add-offering-button`)
            //wait for DOM to be ready before clicking
            setTimeout(()=>{
                modal_button.click()
            },500)
        },
        openTitheTab: function(){
            var nav_pill = document.getElementById('pills-tithe-tab')
            nav_pill.click()
            var tithe_modal_button = document.getElementById('tithe-modal-button')
            //wait for DOM to be ready before clicking
            setTimeout(()=>{
                tithe_modal_button.click()
            },500)

        },
        //check if member is logged in
        checkLoggedIn() {
            if (!this.$session.has("token")) {
                router.push("/login")
            }
        },
        humanize: function(x) {
                return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        setMemberIds (value){
            this.member_ids = value
        },
        //fetch data
        fetchdata () {
            this.tithes_selected = true
            this.getIncomeTypeList()
            this.getPaymentMethods()
        },
        //get payment methods.
        getPaymentMethods: function(){
            this.$http({
                method: 'get',
                url: this.$BASE_URL + '/api/finance/modes-of-payment/'
            }).then((response)=>{
                this.payment_methods = response.data
            }).catch((err)=>{
                alert(err)
            })
        },
        //get offering types
        getOfferingTypes: function(){
            this.$http.get(this.$BASE_URL + '/api/finance/offering-types/')
            .then((response)=>{
                this.offering_types = response.data
            })
        },
        deleteOfferingType:function(id){
            this.$http.delete(
                this.$BASE_URL + '/api/finance/offering-types/' + id + '/'
            ).then(response => {
                alert("deleted")
                this.getOfferingTypes()
            }).catch((err) => {
                alert(err)
            })
        },
        //get the list of income types
        getIncomeTypeList: function(){
            //try local storage
            this.income_types = JSON.parse(localStorage.getItem('income_type_list'))
            if (this.income_types){
                var array = this.income_types.response
                this.foundIncomes = array.length
            }
            this.income_stats = JSON.parse(localStorage.getItem('income_stats'))

            const currentVersion = this.$store.getters.income_type_list_version
            var version  = localStorage.getItem('income_type_list_version')

            // else try the network
            if (!version || version < currentVersion) {
                this.$store.dispatch('update_isLoading', true)
                this.$http.get(this.$BASE_URL + '/api/finance/income-stats/')
                .then(response => {
                   this.income_stats = {"response": response.data }

                   localStorage.setItem('income_stats',JSON.stringify({"response": response.data }) )
                   this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {
                    this.fetch_data_error.push(err)
                    this.$store.dispatch('update_isLoading', false)
                })

                this.$store.dispatch('update_isLoading', true)
                this.$http.get(this.$BASE_URL + '/api/finance/income-type-list/')
                .then(response => {
                    this.income_types = {"response": response.data }

                    localStorage.setItem('income_type_list',JSON.stringify({"response": response.data }))
                    localStorage.setItem('income_type_list_version', currentVersion)
                    this.$store.dispatch('update_isLoading', false)
                })
                .catch((err) => {
                    this.fetch_data_error.push(err)
                    this.$store.dispatch('update_isLoading', false)
                })
            }
        },
        getAll: function(){
            this.offerings_selected = false
            this.any_other_selected = false
            this.expenditures_selected = false
            this.tithes_selected = true
            this.context={'name':'All','type':null}
        },
        getTithes: function(){
            this.offerings_selected = false
            this.any_other_selected = false
            this.expenditures_selected = false
            this.tithes_selected = true
            this.context={'name':'Tithe','type':null}
        },
        getOfferings: function(){
            this.tithes_selected = false
            this.any_other_selected = false
            this.expenditures_selected = false
            this.offerings_selected = true
            this.context={'name':'Offering','type':this.offering_type}
        },
        getIncome: function(){
            this.tithes_selected = false
            this.offerings_selected = false
            this.expenditures_selected = false
            this.any_other_selected = true

            const currentVersion = this.$store.getters.income_type_list_version
            var version  = localStorage.getItem('income_type_list_version')

            //try local storage
            this.incomes = JSON.parse(localStorage.getItem('income_type_list'))
            if (this.incomes){
                var array = this.incomes.response
                this.foundIncomes = array.length
            }
            else{
                if (!version || version < currentVersion) {
                    this.$store.dispatch('update_isLoading', true)
                    this.$http.get(this.$BASE_URL + '/api/finance/income-type-list/')
                    .then(response => {
                        this.incomes = {"response": response.data }
                        var array = this.incomes.response
                        this.foundIncomes = array.length

                        localStorage.setItem('income_type_list',JSON.stringify({"response": response.data }))
                        localStorage.setItem('income_type_list_version', currentVersion)
                        this.$store.dispatch('update_isLoading', false)
                    })
                    .catch((err) => {
                        this.fetch_data_error.push(err)
                        this.$store.dispatch('update_isLoading', false)
                    })
                }
            }
            this.income_stats = JSON.parse(localStorage.getItem('income_stats'))
            if (this.income_stats){

            }
            else{
                if (!version || version < currentVersion) {
                    this.$store.dispatch('update_isLoading', true)
                    this.$http.get(this.$BASE_URL + '/api/finance/income-stats/')
                    .then(response => {
                        this.income_stats = {"response": response.data }
                        localStorage.setItem('income_stats',JSON.stringify({"response": response.data }) )
                        this.$store.dispatch('update_isLoading', false)
                    })
                    .catch((err) => {
                        this.fetch_data_error.push(err)
                        this.$store.dispatch('update_isLoading', false)
                    })
                }
            }

        },
        getExpenditures: function(){
            this.tithes_selected = false
            this.offerings_selected = false
            this.any_other_selected = false
            this.expenditures_selected = true
        },
        incomeTypeFormOK: function(){
            this.income_type_name_errors = []

            if (this.income_type_description.length < 1){
                this.income_type_description = "none given"
            }
            if (this.income_type_name.length > 0){
                return true
            }
            if (this.income_type_name.length < 1){
                this.income_type_name_errors.push("name required")
                return false
            }
        },
        addIncomeType: function(){
            if (this.incomeTypeFormOK()){
                this.adding_to_finance = true
                this.$http({
                    method: 'post',
                    url: this.$BASE_URL + '/api/finance/income-type-list/',
                    data: {
                        type_name: this.income_type_name,
                        description: this.income_type_description
                    }
                    }).then(response => {
                        this.adding_to_finance = false
                        this.income_type_name = '',
                        this.income_type_description = ''
                        var new_version = parseInt(localStorage.getItem('income_type_list_version')) + 1
                        this.$store.dispatch('update_income_type_list_version', new_version)
                        this.getIncomeTypeList()
                        alert("income type succesfully added")
                    })
                    .catch((err) => {
                        this.adding_to_finance = false
                        alert("an error occured, try again later")
                    })
            }
        },
        incomeFormOK: function(){
            this.added_income = []
            this.income_amount_errors = []
            this.income_type_errors = []

            if (this.income_type != null
                && this.income_amount != null){
                    return true
                }
            if (this.income_type == null){
                    this.income_type_errors.push("select an income type or add one ")
                    return false
                }
            if (! this.income_amount > 0
                || this.income_amount == null){
                this.income_amount_errors.push("enter an amount")
                return false
            }
        },
        addIncome: function(){
            if (this.incomeFormOK()){
                this.adding_to_finance = true
                this.$http({
                        method: 'post',
                        url: this.$BASE_URL + '/api/finance/add-income/',
                        data: {
                                recording_member_id: this.$session.get('member_id'),
                                income_type_id: this.income_type,
                                narration: this.income_narration,
                                amount: this.income_amount
                        }
                        }).then(response => {
                            this.adding_to_finance = false
                            this.added_income.push(response.data)
                            this.income_type = null,
                            this.income_amount = null,
                            this.income_narration = ''
                            alert("income successfully added")
                        })
                        .catch((err) => {
                            this.adding_to_finance = false
                            alert("an error occured, try again later")
                        })
            }
        },
        //export data to csv
        exportData: function(){
            //export to csv
            this.exporting_data = true
            this.$http.get(this.$BASE_URL + '/api/finance/get-income-csv/' + this.csv_date +'/' )
            .then(response => {
                this.$fileDownload(response.data,"income_" + this.csv_date + ".csv");
                this.exporting_data = false
                alert("download successful")
            })
            .catch((error) => {
                this.exporting_data = false
                alert('error while downloading income csv')
            })
        },
        //add offerring type
        addOfferingType: function(){
            this.adding_offering = true
            this.$http({
                method: 'post',
                url: this.$BASE_URL + '/api/finance/offering-types/',
                data: {
                    name:this.offering_type_name,
                    description:this.offering_type_description
                }
                }).then(response => {
                    this.adding_offering = false
                    this.offering_type_name = null
                    this.offering_type_description=null
                    this.getOfferingTypes()
                    alert("offering type succesfully added ")
                })
                .catch((err) => {
                    this.adding_offering = false
                    alert("an error occured, please try again later")
                })
        },
        //add payment method.
        addPaymentMethod: function(){
            this.adding_offering = true
            this.$http({
                method: 'post',
                url: this.$BASE_URL + '/api/finance/modes-of-payment/',
                data:{
                    name: this.payment_method_name
                }
            }).then(()=>{
                alert('payment method added successfully')
                this.adding_offering = false
                this.payment_method_name = null
                this.getPaymentMethods()
            }).catch((err)=>{
                alert(err)
                this.adding_offering = false
            })
        },
        //delete envelopes.
        deleteEnvelopes: function (){
            var context = null
            if (this.context){
                if (! this.context.type){
                    context = this.context.name
                }
                else{
                    context = "Offering"
                }
            }
            this.adding_offering = true
            this.$http({
                method: 'delete',
                url: this.$BASE_URL + '/api/finance/delete-envelopes/',
                data: {
                    envelope_ids: this.member_ids,
                    context:context
                }
                }).then(() => {
                    this.adding_offering = false
                    this.reload_data = true
                    document.getElementById('closeDeleteEnvelopesButton').click()
                    setTimeout(()=>{
                        this.reload_data = false
                    },1000)
                })
                .catch((err) => {
                    this.adding_offering = false
                    alert(err)
                })
            },
        },

}
</script>


<style scoped lang="scss">
.hidden {
  visibility: hidden;
}

.hidden:hover {
  font-size: 20px;
  visibility: visible !important;
  color: red !important;
}
</style>


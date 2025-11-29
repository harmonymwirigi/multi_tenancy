<!-- Parent.vue -->
<template>
<div>
    <!-- Modal import CSV -->
    <div>
			<nav class="container">
				<a href="#" @click="goBack()">&larr; Back</a>
			</nav>
            <div class="container" role="document">
                <div class="modal-content border-0">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalCenterTitle">import from CSV</h5>
                </div>
                <div class="modal-body">
                    <h3 class="text-muted">demo</h3>
                    <div class="continer">
                        <table class="table table-borderless text-capitalize">
                            <thead>
                                <tr>
	                                <th scope="col">names</th>
	                                <th scope="col">phone number</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Daniel Jones</td>
                                    <td>07********</td>
                                </tr>
                                <tr>
                                    <td>Martha Mercy</td>
                                    <td>07********</td>
								</tr>
                            </tbody>
                            </table>
                        <hr/>
                        <h3 class="text-muted">your csv :</h3>
                        <h3 class="text-muted">{{get_data_status}}</h3>

                        <div v-if="csv_data.length" style="height: 40vh; overflow-y: scroll">
                            <table class="table table-borderless">
                                <thead>
                                <tr v-for="data in csv_data.slice(0,1)">
                                    <th scope="col" v-for="(value,key) in data">
                                        {{key}}
                                        <select class="form-control"  v-model='csv_columns[key]'>
                                            <option selected>import as ...</option>
                                            <option>names</option>
                                            <option>phone number</option>
										</select>
                                    </th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="data in csv_data">
                                    <td v-for="(value,key) in data">{{value}}</td>
                                </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="mt-3 large-12 medium-12 small-12 cell">
                            <label><b>file: </b>
                            <button class="mr-2 btn btn-success" v-on:click="reset()">
                                Choose file
                            </button>
                            {{file_name}}
                            <input class="d-none" type="file" accept=".csv" id="file" ref="file"
                                v-on:change="handleFileUpload()"/>
                            </label>
                        </div>
                        <p v-if="test_csv_errors.length">
                            <ul>
                                <small><li v-for="error in test_csv_errors"><p class="text-danger">{{error}}</p></li></small>
                            </ul>
                        </p>
						<div class=""  v-if="file_format_okay">
							<p class="text-success">file okay, proceed to import</p>
							<label for="">Your message</label>
                            <br>
                            <small v-if="sms_credit_balance">sms credit balance - {{sms_credit_balance}} </small>
							<textarea class="form-control" id="exampleFormControlTextarea1" rows="5" v-model="message"></textarea>
						</div>
                        <p v-if="error_500.length">
                            <ul>
                                <small><li v-for="error in error_500">
                                    <p class="text-danger">unexpected data format in your file, make sure your CSV or EXCEL file matches the demo</p>
                                    <p class="text-danger">select how you want to import your csv above</p>
                                </li></small>
                            </ul>
                        </p>
                        </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success"
                            v-on:click="submitFile()"
                            v-if="file">
                            submit file
                            <span v-if="submitting_file"
                                class="spinner-border spinner-border-sm"
                                role="status"
                                aria-hidden="true">
                            </span>
                    </button>
                    <button type="button" class="btn btn-success"
                            v-if="uploaded_file.length != 0"
                            v-on:click="checkCSV()">
                            check CSV file
                            <span v-if = "checking_csv"
                                class="spinner-border spinner-border-sm"
                                role="status"
                                aria-hidden="true"></span>
                    </button>
                    <button type="button" class="btn btn-success"
                            v-if="file_format_okay"
                            v-on:click="extractData()">
                            extract Data and send message
                            <span v-if = "extracting_data"
                                class="spinner-border spinner-border-sm"
                                role="status"
                                aria-hidden="true"></span>
                    </button>
                </div>
                </div>
            </div>
    </div>
</div>
</template>
<script>
export default {
name: 'randomMessage',
data () {
    return {
        file_name: "No file chosen",
        // csv file upload
        submitting_file: false,
        checking_csv: false,
        extracting_data: false,
        extract_data_button_text: "import data",
        file: null,
        error_500: [],
        test_csv_errors: [],
        uploaded_file: '',
        uploaded_file_id: null,
        csv_data: [],get_data_status: '',
        file_format_okay: false,
        csv_columns: {},
		message:'',
        sms_credit_balance : null

    }
},

methods: {
    emitToParent (event) {
        this.$emit('dataExtracted')
    },
	goBack(){
		history.back()
	},
    getSMSCreditBalance: function(){
        this.$http.get(this.$BASE_URL + '/api/sms/sms-credit-balance')
        .then((response)=>{            
            this.sms_credit_balance =  response.data.UserData.balance
        })
    },
    //Submits the file to the server
    submitFile: function(){
        this.file_format_okay = false
        this.error_500 = []
        this.test_csv_errors = []
        let formData = new FormData();
        formData.append('csv', this.file);

        this.submitting_file = true
        this.$http.post( this.$BASE_URL + '/api/groups/upload-csv/',
            formData,
            {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response =>{
            var data = response.data
            //if data is not array there are no errors
            if (! data.length){                
                this.uploaded_file = data.csv                
                this.uploaded_file_id = data.id
                alert("file uploaded")
                this.previewCSV()
                this.submitting_file = false
            }
        })
        .catch((err) =>{
            this.error_500.push(err)
            this.submitting_file = false
        });
    },
    // handle the case that the file changes
    handleFileUpload: function(){
        this.file = this.$refs.file.files[0];
        this.file_name = this.file.name
        this.uploaded_file = ''
        this.file_format_okay = false
        this.$refs.file.value = null
    },
    //preview the csv file
    previewCSV: function(){
        this.get_data_status = 'setting up preview ...'       
        this.$http.get(this.$BASE_URL + '/api/groups/preview-csv/'+ this.uploaded_file_id + '/')
        .then(response => {
            this.csv_data = response.data
            this.get_data_status = ''
        })
        .catch((err) => {
            this.get_data_status = ''
        })
    },
    // check that the csv file is of the required format
    checkCSV: function(){
        this.error_500 = []
        this.test_csv_errors = []
        this.file_format_okay = false       

        this.checking_csv = true
        this.$http({
            method: 'post',
            url: this.$BASE_URL + '/api/groups/check-csv/',
            data: {
                file_id: this.uploaded_file_id,
                column_config: this.csv_columns
            },
        }).then(response => {
                var data = response.data
                //if data is not array there are no errors
                if (! data.length){
                    this.file_format_okay = true
                }
                else{
                    this.test_csv_errors = data
                }
                this.checking_csv = false
                this.getSMSCreditBalance()
        }).catch((err) => {
            this.error_500.push(err)
            this.checking_csv = false
        })
    },
    // extract data from the csv file
    extractData: function(){
        this.extract_data_button_text = "extracting..."
        this.extracting_data = true
        this.$http({
            method: 'post',
            url: this.$BASE_URL + '/api/groups/send-message-to-data-from-csv/',
            data: {
                file_id: this.uploaded_file_id,
                column_config: this.csv_columns,
				message:this.message
            }
        }).then(response => {
            alert("data extracted succesfully, Your messages have been queued.")
			this.reset()
        }).catch((err) => {
            alert("an error occured, check CSV and try again")
			this.reset()
        })
    },
    reset: function(){
        // csv file upload
        this.submitting_file = false
        this.checking_csv = false
        this.extracting_data = false
        this.extract_data_button_text = "import data"
        this.error_500 = []
        this.test_csv_errors = []
        this.uploaded_file = ''
        this.csv_data = []
        this.get_data_status = ''
        this.file_format_okay = false
        this.csv_columns =  {}
        this.file = null
        this.file_name = "No file chosen"
        document.getElementById('file').click()
    }

}
}
</script>

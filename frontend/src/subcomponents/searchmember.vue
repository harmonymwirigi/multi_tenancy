<!-- Child.vue -->
<template>
    <div class="child">
        <div class="anvil-select row form-group">
            <select class="ml-3 custom-select border-0 shadow-0 text-muted "
                v-model = "selected_input"
                style="outline: none;
                       box-shadow:none !important;">
                <option value="existing_member" selected>existing member</option>
                <option value="new_member">new member</option>
            </select> 
        </div>

        <div v-if="selected_input == 'existing_member'">
            <!-- search for member -->
            <input type="text" class=" form-control" placeholder="type to search member" v-model="memberSearch" autofocus>                  
            <div class="pre-scrollable searchedItemsDiv border " 
                style="min-width: 300px; 
                        max-height: 185px;
                        overflow-y: scroll;
                            position: absolute;
                            z-index: 1;
                            background-color: white"
                v-if="showMemberInput">

                <div style="padding: 10px 10px 10px 10px" class="text-info" >{{memberSearch_status}}</div> 

                <table class="table border-0" >
                    <tbody>
                    <tr class="searchedItem border-0" v-for="data in found_members.response">
                        <a href="#" style="text-decoration: none" v-on:click="selectMember(data.member.id,data.member.first_name,data.member.last_name)"> 
                        <td class="border-0">
                        
                            <img v-if = "data.gender == 'M'" style = "height: 32px "src="@/assets/avatars/icons8-user-male-skin-type-4-40.png">
                            <img v-if = "data.gender == 'F'" style = "height: 32px "src="@/assets/avatars/icons8-user-female-skin-type-4-40.png">
                            <img v-if = "data.gender == 'R'" style = "height: 32px "src="@/assets/avatars/icons8-contacts-96.png">
                            
                            <span class = "text-secondary text-capitalize">
                                {{data.member.first_name}} {{data.member.last_name}} 
                                <small>( {{data.phone_number}} )</small>
                           </span>                                                                      
                        </td>
                        </a>                                                                                                                                  
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <!-- add new member -->
        <div v-if="selected_input == 'new_member'">
                <div>
                        <div>
                        <div class="form-group">
                                <label><b>first name :</b></label>
                                <input type="text" class="form-control"  placeholder="first name" v-model="first_name" autofocus>
                                <p v-if="first_name_errors.length">
                                        <ul>
                                                <small><li v-for="error in first_name_errors"><p class="text-danger">{{ error }}</p></li></small>
                                        </ul>
                                </p>
                        </div>
                        <div class="form-group">
                                <label><b>last name :</b></label>
                                <input type="text" class="form-control"  placeholder="last name" v-model="last_name" >
                                <p v-if="last_name_errors.length">
                                        <ul>
                                                <small><li v-for="error in last_name_errors"><p class="text-danger">{{ error }}</p></li></small>
                                        </ul>
                                </p>
                        </div>
                        <hr>
                        <div class="checkbox">
                                <div class="radio">
                                        <label><input type="radio" value = "M" v-model = "gender" > male</label>
                                </div>
                                <div class="radio">
                                         <label><input type="radio" value = "F" v-model = "gender"> female</label>
                                </div>
                                <p v-if="gender_errors.length">
                                <ul>
                                        <small><li v-for="error in gender_errors"><p class="text-danger">{{ error }}</p></li></small>
                                </ul>
                                </p>
                        </div>
                        <hr>
                        <div>
                                <span class="col-4">
                                        <label><b>code :</b></label>
                                        <input class="form-control" type="text" placeholder="+254" v-model = "country_code">
                                </span>
                                <span class="col-8">
                                        <label><b>phone number :</b></label>
                                        <input type="text" class="form-control"  placeholder="712345678" v-model = "phone_number">
                                </span>
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
                        <div style="padding: 0px 0px 25px 0px">
                                <a href="#add-member" v-on:click = "addMember()" style="text-decoration: none" >
                                    <div class="add-button">                                       
                                        add new member
                                        <span v-if="adding_member"
                                              class="spinner-border spinner-border-sm" 
                                              role="status" 
                                              aria-hidden="true"></span>
                                    </div>
                                </a>
                        </div>
                        </div>
                </div>
        </div>
    </div>
</template>
<script>
export default {
name: 'searchmember',
created () {        
    this.debouncedGetAnswer = _.debounce(this.getAnswer, 1000)
},
data() {
    return {
        childMessage: '',
        selected_input: "existing_member",
        //member search
        memberSearch: '',found_members:[],
        memberSearch_status: '',
        selectedMember: null,
        showMemberInput: false,  

        country_code: '+254',
        contact: ' ',postal_address: '',
        phone_number: '',phone_number_errors: [],phone_number_OK: [],
        //names and gender
        first_name: '',first_name_errors: [],
        last_name: '',last_name_errors: [],
        gender: '',gender_errors: [],
        added_member: [],add_member_button_text: "+ add member",
        add_member_error: [],
        added_member_id: null,
        //adding member
        adding_member: false
    }
},
watch:{
    memberSearch: function () {
        var array = this.memberSearch.split(" ")
        if (this.memberSearch.length > 0 && array.length == 1){
            this.showMemberInput = true        
            this.debouncedGetAnswer()
        }else{
            this.memberSearch_status = ''
            this.found_members = []
            this.showMemberInput = false                
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

},
methods: {
    // Define the method that emits data to the parent as the first parameter to `$emit()`.
    // This is referenced in the <template> call in the parent. The second parameter is the payload.
    emitToParent (event) {
        this.$emit('memberSelected', this.selectedMember)
    },
    //search for member
    getAnswer: function () {
        var vm = this
        if (this.memberSearch.length > 0){
            this.found_members = []
            this.memberSearch_status = 'searching...'
            this.$http.get(this.$BASE_URL + '/api/members/filter-by-first_name/' + this.memberSearch +'/')
            .then(function (response) {
                vm.found_members = {"response": response.data } 
                vm.memberSearch_status = ''                
            })
            .catch(function (error) {
                vm.memberSearch_status = ''  
                vm.showMemberInput = false
            })
        }
    },
    selectMember: function(id,first_name,last_name) {
        this.selectedMember = id          
        this.memberSearch =  first_name + ' ' + last_name 
        this.memberSearch_status = ''
        this.showMemberInput = false
        this.emitToParent(this.selectedMember) 
    },
    addMember: function(){
        this.first_name_errors = []
        this.last_name_errors = []
        this.gender_errors = []

        if (! this.first_name){
                this.first_name_errors.push('you must enter the first name')
                return false;
        }
        if (this.first_name.split(' ').length > 1){
                this.first_name_errors.push('first name must be one word only, remove any spaces')
                return false;
        }
        if(! this.last_name){
                this.last_name_errors.push('you must enter a last name')
                return false;
        }
        if (this.last_name.split(' ').length > 1){
                this.last_name_errors.push('last name must be one word only, remove spaces')
                return false;
        }
        if (! this.gender ){
                this.gender_errors.push('select gender')
                return false;
        }
        this.adding_member = true
        this.$http({
                method: 'post',
                url: this.$BASE_URL + '/api/members/add-member/',
                data: {
                  first_name: this.first_name,
                  last_name: this.last_name,
                  gender: this.gender,
                  email: ''         
                }
              }).then(response => {                
                    var added_member = []
                    added_member.push(response.data )                  
                    this.gender_male = false
                    this.gender_female = false
                    this.last_name = ''
                    this.first_name = ''                                                            
                    this.adding_member = false
                    
                    var added_member_id = added_member[0].member.id
                    var added_member_firstname = added_member[0].member.first_name
                    var added_member_lastname = added_member[0].member.last_name

                    this.selected_input =  "existing_member"                    
                    this.selectMember(added_member_id,added_member_firstname,added_member_lastname)                    
                    
                    this.addContact(added_member_id)
                    var new_version = parseInt(localStorage.getItem('member_list_version')) + 1
                    this.$store.dispatch('update_member_list_version', new_version)  
                    alert("member added succesfully")   
                })
                .catch((err) => {
                    this.add_member_error.push(err)
                })
        
    },
    addContact: function(added_member_id){
        this.$http({
                method:'post',
                url: this.$BASE_URL + '/api/members/add-member-contact/',
                data: {
                        member_id: added_member_id,
                        postal_address: this.postal_address,
                        phone: this.country_code + this.phone_number,
                        contact: this.contact
                }
        })            
    },
}
}
</script>
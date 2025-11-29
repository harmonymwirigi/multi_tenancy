<template>
    <div>
        <div class="continer">                        
            <div class="d-flex justify-content-center">
                <div class="card w-400 border-0"
                     style="background-color: ghostwhite; height: 80vh; min-width: 300px;">
                <div class="card-header text-center border-0">
                    <img class="mr-0 " style="width: 50px ;height: auto" src="@/assets/app_logo1.png"
                        v-if="$host_name == 'my-domain' || $host_name == 'anvilchurch'">
                    <img class="ml-4 " style="width: 100px ;height: auto ;border-radius: 5px" src="@/assets/methodist_logo.jpeg" alt="logo not found"
                        v-if="$host_name == 'methodistkenya' " >  
                    <small class="d-flex justify-content-center">change credentials for</small>               
                    <p>                        
                        {{username}}
                    </p>
                </div>
                <div class="card-body">
                    <div class="d-flex justify-content-center text-muted">
                        <small  id="change_password_button"
                                @click="changing_password = true"
                                class="" 
                                style="cursor:pointer">
                            change password
                        </small>
                        <span class="ml-2 mr-2">|</span>
                        <small  id = change_username_button
                                @click="changing_password = false"
                                class="text-primary"
                                style="cursor:pointer">                                
                            change username
                        </small>
                    </div>
                    <!-- if changing password -->
                    <form v-if="changing_password">                            
                        <div class="mt-4 mb-5 form-group">
                            <label for="exampleInputPassword1">Old password</label>
                            <input 
                                    type="password" class="form-control"
                                    placeholder="your old password"
                                    v-model="password">
                        </div>                                                                                 
                        <div class="form-group">
                            <label for="exampleInputPassword1">New password</label>
                            <input 
                                    type="password" class="form-control"
                                    placeholder="your new password"
                                    v-model="new_password">
                            <!-- username errors-->
                            <ul v-if="password_errors.length">
                                <li v-for="error in password_errors" class="text-danger">
                                    <small>{{ error }}</small>
                                </li>
                            </ul>
                        </div>  
                        <div class="form-group">
                            <label for="exampleInputPassword1">Confirm new password</label>
                            <input 
                                    type="password" class="form-control"
                                    placeholder="confirm new password"
                                    v-model="new_password_confirmation">
                        </div>        
                            
                        <button v-if="username_errors.length == 0  
                                && password != null
                                && new_password != null
                                && new_password_confirmation != null
                                && new_password == new_password_confirmation"
                                class="mt-5 btn btn-block btn-success"
                                @click=changePassword()>
                            change password
                        </button>
                        <button v-else
                                class="mt-5 btn btn-block btn-success"
                                disabled>
                            change password
                        </button> 
                    </form>
                    <!-- if changing username -->
                    <form v-if="! changing_password">    
                        <div class="mt-4 mb-5 form-group">
                            <label for="exampleInputPassword1">Password</label>
                            <input 
                                    type="password" class="form-control"
                                    id="exampleInputPassword1" placeholder="your password"
                                    v-model="password">
                        </div>          

                        <div class="form-group">
                            <label >New username</label>
                            <input 
                                    type="text" class="form-control"
                                    placeholder="your new username"
                                    v-model="new_username">
                            <!-- username errors-->
                            <ul v-if="username_errors.length">
                                <li v-for="error in username_errors" class="text-danger">
                                    <small>{{ error }}</small>
                                </li>
                            </ul>
                        </div>  
                        <div class="form-group">
                            <label >Confirm new username</label>
                            <input 
                                    type="text" class="form-control"
                                    placeholder="confirm your new username"
                                    v-model="new_username_confirmation">
                        </div>                                
                        <button v-if="username_errors.length == 0  
                                      && password != null
                                      && new_username != null
                                      && new_username_confirmation != null
                                      && new_username == new_username_confirmation"
                                class="mt-5 btn btn-block btn-success"
                                @click=changeUsername()>
                            change username
                        </button>
                        <button v-else
                                class="mt-5 btn btn-block btn-success"
                                disabled>
                            change username
                        </button> 
                    </form>
                </div>
                </div>
            </div>            
        </div>
    </div>
</template>

<script>
import router from "../../router";
export default {
    name: 'credentialsReset',
    data() {
    return {                
        username:this.$session.get("username") ,
        changing_password:true,
        //changing password
        old_password:null,
        new_password:null,
        new_password_confirmation:null,
        password_errors:[],
        //changing username
        debouncing_timeout:null,
        password:null,        
        new_username:null,
        new_username_confirmation:null,
        username_errors:[]
    }
    },
    created(){

    },
    watch: {
        changing_password: function(){
            //if change password has been selected
            if (this.changing_password){
                document.getElementById('change_username_button').classList.add('text-primary')
                document.getElementById('change_password_button').classList.remove('text-primary')
            }else{            
                document.getElementById('change_password_button').classList.add('text-primary')
                document.getElementById('change_username_button').classList.remove('text-primary')
            }
        },
        new_username: function(){
            clearTimeout(this.debouncing_timeout);
            this.debouncing_timeout = setTimeout(() => {
                this.username_errors = []
                //clear
                if(this.new_username.length == 0){
                    this.new_username = null
                    return
                }
                //too short
                if (this.new_username.length < 5){
                    this.username_errors.push('too short')
                }   
                //remove spaces 
                if (this.new_username.split(' ').length != 1){                  
                    this.username_errors.push('remove spaces')
                }     
                //taken 
                if (this.new_username.length >= 5 
                    && this.new_username.split(' ').length == 1){
                        this.checkIfUsernameIsAvailable()
                    }       
            }, 500);
        },
        new_username_confirmation: function(){
            clearTimeout(this.debouncing_timeout);                              
            this.debouncing_timeout = setTimeout(() => {  
                //clear 
                this.username_errors = []         
                if (this.username_errors.length == 0){
                    //confirmatin did not match username
                    if (this.new_username != this.new_username_confirmation){
                        this.username_errors.push('confirmation did not match username')
                    }
                }
            },500)                                            
        },
        //password
        new_password: function(){
            clearTimeout(this.debouncing_timeout);
            this.debouncing_timeout = setTimeout(() => {
                this.password_errors = []
                //clear
                if(this.new_password.length == 0){
                    this.new_password = null
                    return
                }
                //too short
                if (this.new_password.length < 5){
                    this.password_errors.push('too short')
                }   
                //remove spaces 
                if (this.new_password.split(' ').length != 1){                  
                    this.password_errors.push('remove spaces')
                }                        
            }, 500);
        },
        new_password_confirmation: function(){
            clearTimeout(this.debouncing_timeout);                              
            this.debouncing_timeout = setTimeout(() => {  
                //clear 
                this.password_errors = []         
                if (this.password_errors.length == 0){
                    //confirmatin did not match username
                    if (this.new_password != this.new_password_confirmation){
                        this.password_errors.push('confirmation did not match password')
                    }
                }
            },500)                                            
        },
    },
    methods: {
        //check if username is taken
        checkIfUsernameIsAvailable:function(){
            this.$http({
                method:'post',
                url: this.$BASE_URL + `/api/members/check-if-username-is-taken/`,
                data:{
                    username:this.new_username
                }
            }).then(()=>{
                this.username_errors = []
            }).catch((err)=>{
                this.username_errors.push('username taken')
            })
        },
        //change username
        changeUsername: function(){
            this.$http({
                method:'post',
                url: this.$BASE_URL + `/api/members/change-credentials/`,
                data:{
                    old_password: this.password,
                    new_password: null,
                    old_username:this.username,
                    new_username:this.new_username                    
                }
            }).then(()=>{
                alert('username changed successfully')
                router.push('/login') 
            }).catch((err)=>{                
                alert('could not verify you. enter correct password')
            })
        },
        //change password.
        changePassword: function(){
            this.$http({
                method:'post',
                url: this.$BASE_URL + `/api/members/change-credentials/`,
                data:{
                    old_password: this.password,
                    new_password: this.new_password,
                    old_username:this.username,
                    new_username:null
                }
            }).then(()=>{
                alert('password changed successfully')
                router.push('/login') 
            }).catch((err)=>{                
                alert('could not verify you. your old password was incorrect')
            })
        },



    }
}
</script>


<style>
</style>
      
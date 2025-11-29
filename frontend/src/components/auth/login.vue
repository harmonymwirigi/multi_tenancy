<!-- <template>
  <div>
    <div class="continer">
        <div class="d-flex justify-content-center">
          <div  class="card w-400 border-0"
                style="background-color: ghostwhite; height: 80vh; min-width: 300px;">

            <div class="card-header text-center border-0">
              <img class="mr-0 " style="width: 50px ;height: auto" src="@/assets/app_logo1.png"
                  v-if="$host_name == 'my-domain' || $host_name == 'anvilchurch'">
              <img class="ml-4 " style="width: 60px ;height: auto ;border-radius: 5px" src="@/assets/methodist_logo.jpeg" alt="logo not found"
                    v-if="$host_name == 'methodistkenya' " >
              <p>admin login</p>
            </div>
            <div class="card-body">

              <form>
                <div>
                  <ul v-if="login_error.length">

                    <li v-for="error in login_error">
                      <small class="text-danger">{{ error }}</small>
                    </li>
                  </ul>

                  <ul v-if="login_info.length">
                    <li v-for="error in login_info" class="text-info">
                      <small>{{ error }}</small>
                    </li>
                  </ul>

                </div>
                <div class="form-group">
                  <label for="exampleInputEmail1">church code</label>
                  <input @keyup.enter="getToken()"
                         type="number" class="form-control"
                         placeholder="000" v-model="church_code">
                </div>
                <div class="form-group">
                  <label for="exampleInputEmail1">username</label>
                  <input @keyup.enter="getToken()"
                         type="text" class="form-control"
                         id="exampleInputEmail1" aria-describedby="emailHelp"
                         placeholder="Enter username" v-model="username">
                </div>
                <div class="form-group">
                  <label for="exampleInputPassword1">Password</label>
                  <input @keyup.enter="getToken()"
                         type="password" class="form-control"
                         id="exampleInputPassword1" placeholder="Password"
                         v-model="password">
                </div>
                <a  href=#
                    v-on:click="getToken()"
                    style="text-decoration: none">
                  <div class="mt-5 add-button">
                    <span>login</span>
                  </div>
                </a>
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
    name: 'login',
    data() {
      return {
        church_code: null,
        church_code_set : false,
        username: null,
        password: null,
        login_error: [],
        login_info: []

      }
    },
    created(){
      this.church_code =  localStorage.getItem('church_id')
      this.church_code = this.church_code.padStart(3, '0')
      if (this.church_code != 'null'){
        this.church_code_set = true
      }
    },
    watch: {
      church_code:function(){
        this.login_info = []
        this.login_error = []
        if (this.church_code.toString().length == 3){
          var church_id = parseInt(this.church_code)
          this.$http.get(this.$DOMAIN.value + '/api/clients/client/' + church_id + '/')
            .then(response => {
              var data = response.data
              this.$BASE_URL.value = "https://"+ data[0].domain_url //+ ":8000"
              localStorage.setItem('base_url_value',this.$BASE_URL.value)
              localStorage.setItem('church_id', church_id )
              localStorage.setItem('church_details',JSON.stringify(response.data))
            })
            .catch((err) => {
              this.login_error.push("church code not set or invalid")
            })
        }
      }
    },
    methods: {
      //get access token
      getToken: function () {
        this.login_info = []
        this.login_error = []
        this.login_info.push("authenticating...")
        this.$http({
          method: 'post',
          url: this.$BASE_URL + '/api/token/',
          data: {
            username: this.username,
            password: this.password
          }
        }).then(response => {
            this.login_info = []
            this.login_error = []
            this.$session.start();
            this.$session.set('token', response.data.access)
            this.$session.set('username', this.username)
            //get logged in member data
            this.getLoggedInMemberData()
            router.push('/')

        }).catch((err) => {
            this.login_info = []
            this.login_error = []
            if(! err.response){
              this.login_error.push(err)
            }
            else{
              this.login_error.push("invalid credentials")
            }

        })
      },
      //get logged in member info
      getLoggedInMemberData: function(){
        this.$http({
          method:'get',
          url:this.$BASE_URL + `/api/members/member/${this.$session.get('username')}/`
        }).then(response => {
            this.$session.set('member_id', response.data[0].member.id)
            this.getPermisionLevel(response.data[0].member.id)
        }).catch((err) => {
            this.fetch_data_error.push(err)
        })
      },
      //get logged in member permision level
      getPermisionLevel: function(member_id){
        this.$http({
          method:'get',
          url: this.$BASE_URL + `/api/members/get-permision-level/${member_id}/`
        }).then((response)=>{
            var response_data = response.data
            this.$session.set('access_level',response_data.level)
        }).catch((err)=>{
            alert(err)
        })
      }
    }
  }
</script> -->




<template>
  <div>
    <div class="continer">
        <div class="d-flex justify-content-center">
          <div  class="card w-400 border-0"
                style="background-color: ghostwhite; height: 80vh; min-width: 300px;">

            <div class="card-header text-center border-0">
              <img class="mr-0 " style="width: 50px ;height: auto" src="@/assets/app_logo1.png"
                  v-if="$host_name == 'my-domain' || $host_name == 'anvilchurch'">
              <img class="ml-4 " style="width: 60px ;height: auto ;border-radius: 5px" src="@/assets/methodist_logo.jpeg" alt="logo not found"
                    v-if="$host_name == 'methodistkenya' " >
              <p>admin login</p>
            </div>
            <div class="card-body">

              <form>
                <div>
                  <ul v-if="login_error.length">
                    <li v-for="error in login_error" :key="error">
                      <small class="text-danger">{{ error }}</small>
                    </li>
                  </ul>

                  <ul v-if="login_info.length">
                    <li v-for="error in login_info" :key="error" class="text-info">
                      <small>{{ error }}</small>
                    </li>
                  </ul>

                </div>
                <div class="form-group">
                  <label for="exampleInputEmail1">church code</label>
                  <input @keyup.enter="getToken()"
                         type="number" class="form-control"
                         placeholder="000" v-model="church_code">
                </div>
                <div class="form-group">
                  <label for="exampleInputEmail1">username</label>
                  <input @keyup.enter="getToken()"
                         type="text" class="form-control"
                         id="exampleInputEmail1" aria-describedby="emailHelp"
                         placeholder="Enter username" v-model="username">
                </div>
                <div class="form-group">
                  <label for="exampleInputPassword1">Password</label>
                  <input @keyup.enter="getToken()"
                         type="password" class="form-control"
                         id="exampleInputPassword1" placeholder="Password"
                         v-model="password">
                </div>
                <a  href=#
                    v-on:click="getToken()"
                    style="text-decoration: none">
                  <div class="mt-5 add-button">
                    <span>login</span>
                  </div>
                </a>
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
    name: 'login',
    data() {
      return {
        church_code: null,
        church_code_set : false,
        username: null,
        password: null,
        login_error: [],
        login_info: []
      }
    },
    created(){
      this.church_code = localStorage.getItem('church_id') || '000'
      this.church_code = this.church_code.padStart(3, '0')
      if (this.church_code != 'null'){
        this.church_code_set = true
      }

      // For local development, set the base URL directly
      if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        this.$BASE_URL.value = 'http://ruaraka.localhost:8000'
        localStorage.setItem('base_url_value', this.$BASE_URL.value)
        console.log('Local development mode - Base URL set to:', this.$BASE_URL.value)
      }
    },
    watch: {
      church_code:function(){
        this.login_info = []
        this.login_error = []
        if (this.church_code && this.church_code.toString().length == 3){
          var church_id = parseInt(this.church_code)

          // Check if we're in local development mode
          const isLocalDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'

          if (isLocalDev) {
            // For local development, skip the church lookup and use direct URL
            this.$BASE_URL.value = 'http://ruaraka.localhost:8000'
            localStorage.setItem('base_url_value', this.$BASE_URL.value)
            localStorage.setItem('church_id', church_id)
            console.log('Local dev: Church code set, base URL:', this.$BASE_URL.value)
          } else {
            // Production mode - fetch church details
            this.$http.get(this.$DOMAIN.value + '/api/clients/client/' + church_id + '/')
              .then(response => {
                var data = response.data
                this.$BASE_URL.value = "https://"+ data[0].domain_url
                localStorage.setItem('base_url_value',this.$BASE_URL.value)
                localStorage.setItem('church_id', church_id )
                localStorage.setItem('church_details',JSON.stringify(response.data))
              })
              .catch((err) => {
                console.error('Church lookup error:', err)
                this.login_error.push("church code not set or invalid")
              })
          }
        }
      }
    },
    methods: {
      //get access token
      getToken: function () {
        this.login_info = []
        this.login_error = []
        this.login_info.push("authenticating...")

        console.log('Attempting login to:', this.$BASE_URL.value)
        console.log('Login data:', { username: this.username, church_code: this.church_code })

        this.$http({
          method: 'post',
          url: this.$BASE_URL.value + '/api/token/',
          data: {
            username: this.username,
            password: this.password
          },
          headers: {
            'Content-Type': 'application/json'
          },
          withCredentials: true
        }).then(response => {
            console.log('Login successful:', response.data)
            this.login_info = []
            this.login_error = []
            this.$session.start();
            this.$session.set('token', response.data.access)
            this.$session.set('username', this.username)
            //get logged in member data
            this.getLoggedInMemberData()
            router.push('/')

        }).catch((err) => {
            console.error('Login error:', err)
            this.login_info = []
            this.login_error = []
            if(! err.response){
              this.login_error.push(`Connection error: ${err.message}`)
            }
            else{
              console.log('Error response:', err.response.data)
              this.login_error.push("invalid credentials")
            }
        })
      },
      //get logged in member info
      getLoggedInMemberData: function(){
        this.$http({
          method:'get',
          url:this.$BASE_URL.value + `/api/members/member/${this.$session.get('username')}/`,
          headers: {
            'Authorization': `Bearer ${this.$session.get('token')}`
          },
          withCredentials: true
        }).then(response => {
            this.$session.set('member_id', response.data[0].member.id)
            this.getPermisionLevel(response.data[0].member.id)
        }).catch((err) => {
            console.error('Member data error:', err)
        })
      },
      //get logged in member permision level
      getPermisionLevel: function(member_id){
        this.$http({
          method:'get',
          url: this.$BASE_URL.value + `/api/members/get-permision-level/${member_id}/`,
          headers: {
            'Authorization': `Bearer ${this.$session.get('token')}`
          },
          withCredentials: true
        }).then((response)=>{
            var response_data = response.data
            this.$session.set('access_level',response_data.level)
        }).catch((err)=>{
            console.error('Permission level error:', err)
        })
      }
    }
  }
</script>


<style>
</style>

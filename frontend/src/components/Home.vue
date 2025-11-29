<template>
    <div class="Home">
        <div class="continer">
            <div class="church-is-home row" style="position:absolute;left:50%;top:50%; transform: translate(-50%, -50%);">
              <div class="col-sm mb-3 ">
                  <router-link :to="{name: 'memberList'}">
                      <div class="home-menu-item">
						   <i class="text-dark mb-4 far fa-user fa-3x"></i>
                          	<p class="font-weight-bold">Members &rarr;</p>
                      </div>
                  </router-link>
                <div>
                    <ul class="list-group list-group-flush">

                      </ul>
                </div>
              </div>
              <div class="col-sm mb-3">
                  <router-link :to="{name: 'groupsLanding'}">
                      <div class="home-menu-item">
                        <i class="text-dark mb-4  fas fa-users fa-3x"></i>
                        <p class="font-weight-bold">Groups &rarr;</p>
                      </div>
                  </router-link>
                  <div>
                      <ul class="list-group list-group-flush">

                        </ul>
                  </div>
                </div>
                <div class="col-sm mb-3">
                    <router-link :to="{name: 'generalFinance'}">
                        <div class="home-menu-item">
                            <i class="text-dark mb-4 fas fa-money-bill-alt fa-3x"></i>
                          <p class="font-weight-bold">Finances &rarr;</p>
                        </div>
                    </router-link>
                    <!-- notifications -->
                    <div>
                      <div class="list-group list-group-flush">
                        <hr/>

                        <h3 v-if="pending_confirmations.length" class="text-primary">General</h3>

                        <div class="list-group-item flex-column align-items-start" v-for="data in pending_confirmations">
                          <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1 font-weight-bold" v-if="data.type == 'O'">pending Offering</h5>
                            <h5 class="mb-1 font-weight-bold" v-else>pending Tithe</h5>
                            <small class="text-muted">{{data.date}}</small>
                          </div>
                          <p class="mb-1 text-muted">{{data.confirmation_message}}</p>
                          <p>amount: <span>{{data.amount}}</span></p>
                          <small>by <span>{{data.confirming_for.member.first_name}} {{data.confirming_for.member.last_name}}</span></small>
                          <div class="row">
                            <div class="col-2"></div>
                            <div class="col-10 text-right">
                              <button class="btn btn-sm btn-outline-success" @click="confirmPending(data.id)" :id="data.id + `_button`">confirm</button>
                            </div>
                          </div>
                        </div>

                        <h3 v-if="pending_confirmations_projects.length" class="text-primary">Projects</h3>
                        <div class="list-group-item flex-column align-items-start" v-for="data in pending_confirmations_projects">
                            <div class="d-flex w-100 justify-content-between">
                              <h5 class="mb-1 font-weight-bold" v-if="data.type == 'C'">pending Contribution</h5>
                              <h5 class="mb-1 font-weight-bold" v-else>pending Pledge Settlement</h5>
                              <small class="text-muted">{{data.date}}</small>
                            </div>
                            <p class="mb-1 text-muted">{{data.confirmation_message}}</p>
                            <p>amount: <span>{{data.amount}}</span></p>
                            <small>by <span>{{data.confirming_for.member.first_name}} {{data.confirming_for.member.last_name}}</span></small>
                            <div class="row">
                              <div class="col-2"></div>
                              <div class="col-10 text-right">
                                <button class="btn btn-sm btn-outline-success" @click="confirmPendingProject(data.id)" :id="data.id + `_Pbutton`">confirm</button>
                              </div>
                            </div>
                          </div>
                      </div>
                    </div>
                  </div>
            </div>
          </div>
    </div>
  </template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      pending_confirmations: [],
      pending_confirmations_projects: []
    }
  },
  mounted() {
    this.fetchData()
  },
  destroyed(){
    document.getElementById("anvil-side-nav").style.width = "0";
    document.getElementById("main-app").style.marginLeft = "0";
  },
  methods: {
    fetchData: function(){
      this.$http.get(this.$BASE_URL + '/api/finance/pending-confirmations/')
      .then( response =>{
        this.pending_confirmations = response.data
      })

      //get pending for projects
      this.$http.get(this.$BASE_URL+'/api/projects/pending-confirmations')
      .then( response =>{
        this.pending_confirmations_projects = response.data
      })
    },
    confirmPending: function(id){
      this.$http.get(this.$BASE_URL + '/api/finance/confirm-payment/'+id+'/')
      .then( response =>{
          var data = response.data
          document.getElementById(id+"_button").lastChild.data = "confirmed"
          document.getElementById(id+"_button").setAttribute("disabled",null)
          alert("the giving has been confirmed")
      })
      .catch(error =>{
        alert("not confirmed, try again later")
      })
    },
    confirmPendingProject: function(id){
      this.$http.get(this.$BASE_URL + '/api/projects/confirm-payment/'+id+'/')
      .then( response =>{
          var data = response.data
          document.getElementById(id+"_Pbutton").lastChild.data = "confirmed"
          document.getElementById(id+"_Pbutton").setAttribute("disabled",null)
          alert("the giving has been confirmed")
      })
      .catch(error =>{
        alert("not confirmed, try again later")
      })
    },

  }
}
</script>


<style >
</style>

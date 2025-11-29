<template>
        <div class="offering-stats" >                
            <!-- offering by type stats -->

            <div v-if="data.datasets.length" >
                <h3>Member Envelopes <small>(grouped by type of envelope)</small></h3>
                <barchart :data='data' :options='options'/>                        
            </div>  
            <div v-else>
                    loading data ...
            </div>

            <!-- offering from service stats -->

            <div v-if="data2.datasets.length" class="mt-4">  
                <h3>Envelopes from services <small>(grouped by service type)</small></h3>             
                <barchart :data='data2' :options='options'/>  
            </div>      
            <div v-else>
                loading data ...
            </div>
            
        </div>
        
    </template>
    
    <script>
    import barchart from '@/subcomponents/statistics/charts/bar.vue'   
    export default {
        name: 'offeringstats',
        components: { barchart },
        props: {
            msg: String
        },
        watch: {
            // offering by type statistics
            offering_by_type_stats: function(){ 
                if (this.offering_by_type_stats){
                  for (var type in this.offering_by_type_stats[0].stats){
                    var this_type = this.offering_by_type_stats[0].stats[type].type
                    var data = []
                    for (var month in this.offering_by_type_stats){
                        for (var offering_type in this.offering_by_type_stats[month].stats){

                            var type_this_month = this.offering_by_type_stats[month].stats[offering_type].type
                            var total_this_month = this.offering_by_type_stats[month].stats[offering_type].total                            

                            if (type_this_month == this_type){
                                data.push(total_this_month)
                            }                            

                        }
                    }
                    var dataset =
                    {
                        label: this_type,
                        backgroundColor: "#"+((1<<24)*Math.random()|0).toString(16),
                        data : data
                    }
                    this.data.datasets.push(dataset)
                  }
                }
            },
            //offering from service statistics
            offering_by_service_stats: function(){                                  
                if (this.offering_by_service_stats){
                  for (var type in this.offering_by_service_stats[0].stats){
                    var this_type = this.offering_by_service_stats[0].stats[type].type
                    var data = []
                    for (var month in this.offering_by_service_stats){
                        for (var service_type in this.offering_by_service_stats[month].stats){

                            var type_this_month = this.offering_by_service_stats[month].stats[service_type].type
                            var total_this_month = this.offering_by_service_stats[month].stats[service_type].total                            

                            if (type_this_month == this_type){
                                data.push(total_this_month)
                            }                            

                        }
                    }
                    var dataset =
                    {
                        label: this_type,
                        backgroundColor: "#"+((1<<24)*Math.random()|0).toString(16),
                        data : data
                    }
                    this.data2.datasets.push(dataset)
                  }
                }
            
            }
        },
    
        created(){
            this.fetchData()        
        },
        data(){
            return{
                options: {
                    scales: {
                        xAxes: [{
                            stacked: true
                        }],
                        yAxes: [{
                            stacked: true
                        }]
                    }
                },          
                offering_by_type_stats: null,
                offering_by_service_stats: null,    
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: []
                },   
                data2: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: []
                }        
            }
        },
    
        methods:{
            fetchData: function(){
                // offering by type stats
                this.$http.get(this.$BASE_URL + '/api/finance/offering-by-type-stats/')
                .then(response => {
                    this.offering_by_type_stats = response.data                
                })
                .catch((error) => {
                    console.log('error while fetching statistics for your offerings')
                })

                // offering by service type stats
                this.$http.get(this.$BASE_URL + '/api/finance/offering-from-service-stats/')
                .then(response => {
                    this.offering_by_service_stats = response.data                
                })
                .catch((error) => {
                    console.log('error while fetching statistics for your service offerings')
                })
            },
    
    
        },
    
    }
    </script>
    
<template>
        <div class="offering-stats" >                
            <!-- income stats -->

            <div v-if="data.datasets.length" >
                <h3>other incomes grouped by type</h3>
                <barchart :data='data' :options='options'/>                        
            </div>  
            <div v-else>
                    loading data ...
            </div>
            
        </div>
        
    </template>
    
    <script>
    import barchart from '@/subcomponents/statistics/charts/bar.vue'   
    export default {
        name: 'incomestats',
        components: { barchart },
        props: {
            msg: String
        },
        watch: {
            // offering by type statistics
            income_general_stats: function(){ 
                if (this.income_general_stats){
                  for (var type in this.income_general_stats[0].stats){
                    var this_type = this.income_general_stats[0].stats[type].type
                    var data = []
                    for (var month in this.income_general_stats){
                        for (var income_type in this.income_general_stats[month].stats){

                            var type_this_month = this.income_general_stats[month].stats[income_type].type
                            var total_this_month = this.income_general_stats[month].stats[income_type].total_for_type                            

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
            }  
        },
    
        created(){
            this.fetchData()        
        },
        data(){
            return{
                //options for displaying the graph
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
                // data from API call     
                income_general_stats: null,  
                //data for displaying the chart            
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: []
                }       
            }
        },
    
        methods:{
            fetchData: function(){
                // general income stats
                this.$http.get(this.$BASE_URL + '/api/finance/income-general-stats/')
                .then(response => {
                    this.income_general_stats = response.data                
                })
                .catch((error) => {
                    console.log('error while fetching statistics for your offerings')
                })
            
            },
    
    
        },
    
    }
    </script>
    
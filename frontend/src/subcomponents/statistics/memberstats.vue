<template>
        <div class="member-stats col-sm-12 col-lg-8">    
            <div v-if="data.datasets.length">
                <h3>New members </h3>
                <barchart :data='data'/>
            </div>    
            <div v-else>
                loading data ...
            </div>
            <!-- age distribution -->
            <div class = "mt-4" v-if="age_distribution_data.datasets.length">
                <h3>Age distribution</h3>                
                <div class="col-4" style="background-color: ghostwhite; border-radius: 5px">
                    <h1><span class="label label-secondary text-secondary">{{recorded_ages}}</span></h1>
                    recorded ages                        
                </div>             
                <doughnutchart :data='age_distribution_data'/>
            </div>
            
        </div>
        
    </template>
    
    <script>
    import barchart from '@/subcomponents/statistics/charts/bar.vue'
    import doughnutchart from '@/subcomponents/statistics/charts/doughnut.vue'
    export default {
        name: 'tithestats',
        components: { barchart,doughnutchart },
        props: {
            msg: String
        },
        watch: {
            age_distribution_stats: function(){
                if (this.age_distribution_stats){
                    var stats = this.age_distribution_stats[0].stats
                    this.recorded_ages = this.age_distribution_stats[0].members_with_recorded_ages
                    for (var range in stats){                        
                        this.age_distribution_data.labels.push(stats[range].range) 
                        this.age_distribution_data.datasets[0].backgroundColor.push("#"+((1<<24)*Math.random()|0).toString(16))
                        this.age_distribution_data.datasets[0].data.push(stats[range].total)
                    }
                }
            },
            new_members_stats: function(){  
                var totals = []
                // totals
                if (this.new_members_stats){                
                    for (var i in this.new_members_stats){                         
                        var stat = this.new_members_stats[i]                        
                        totals.push(stat.total)
                    }  
                    var totals = {
                        label: "new members",
                        backgroundColor: "#"+((1<<24)*Math.random()|0).toString(16),
                        data: totals
                    }                
                    this.data.datasets.push(totals)              
                }
            }
        },
    
        created(){
            this.fetchData()        
        },
        data(){
            return{
                recorded_ages: 0,
                new_members_stats: null ,
                age_distribution_stats: null,
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: []
                }, 
                age_distribution_data: {
                    labels:[],
                    datasets:[
                        {
                            data:[],
                            backgroundColor:[]
                        }                        
                    ]
                }          
            }
        },
    
        methods:{            
            fetchData: function(){
                // new_members_stats
                this.$http.get(this.$BASE_URL + '/api/members/new-member-count/')
                .then(response => {
                    this.new_members_stats = response.data                
                })
                .catch((error) => {
                    console.log('error while fetching statistics for new members')
                })

                //age distribution stats
                this.$http.get(this.$BASE_URL + '/api/members/age-distribution/')
                .then(response => {
                    this.age_distribution_stats = response.data                
                })
                .catch((error) => {
                    console.log('error while fetching statistics for age distribution')
                })
            },
    
    
        },
    
    }
    </script>
    
<template>
        <div class="project-stats" >    
            <div v-if="data2.datasets.length">
                <h3>project sizes</h3>
                <doughnutchart :data='data2'/>
            </div>                
            <div v-else>
                loading data
            </div>
            <div v-if="data.datasets.length">
                <h3>project financing stats</h3>                
                <barchart :data='data' :options='options'/>
            </div>                
            <div v-else>
                loading data ...
            </div>
            
        </div>
        
    </template>
    
    <script>
    import barchart from '@/subcomponents/statistics/charts/bar.vue'
    import doughnutchart from '@/subcomponents/statistics/charts/doughnut.vue'
    export default {
        name: 'projectstats',
        components: { barchart,doughnutchart },
        props: {
            msg: String
        },
        watch: {
            project_size_stats: function(){
                if (this.project_size_stats){                    
                    for (var project in this.project_size_stats){
                        var project_stat = this.project_size_stats[project]
                        this.data2.labels.push(project_stat.project)                           
                        this.data2.datasets[0].backgroundColor.push("#"+((1<<24)*Math.random()|0).toString(16))
                        this.data2.datasets[0].data.push(project_stat.size)
                    }
                }
            },
            project_general_stats: function(){  
                var contributions = []
                // contributions
                if (this.project_general_stats){                
                    for (var month in this.project_general_stats[0].months){                        
                        var month_stats = this.project_general_stats[0].months[month]                        
                        contributions.push(month_stats.contribution_this_month)                        
                    }
                    var contributions = {
                        label: "contributions",
                        backgroundColor: "#"+((1<<24)*Math.random()|0).toString(16),
                        data: contributions
                    }                
                    this.data.datasets.push(contributions) 

                //pledge settlements
                var settlements = []
                for (var month in this.project_general_stats[0].months){                        
                        var month_stats = this.project_general_stats[0].months[month]                        
                        settlements.push(month_stats.settled_pledges_this_month)                        
                    }
                    var settlements = {
                        label: "pledge settlements",
                        backgroundColor: "#"+((1<<24)*Math.random()|0).toString(16),
                        data: settlements
                    }                
                    this.data.datasets.push(settlements) 
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
                project_general_stats: null ,
                project_size_stats: null,
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: []
                },     
                data2: {
                    labels: [],
                    datasets: [
                        {
                            backgroundColor: [],
                            data: []
                        }
                    ]                  
                },       
            }
        },
    
        methods:{

            fetchData: function(){
                //project financing stata
                this.$http.get(this.$BASE_URL + '/api/projects/project-general-stats/')
                .then(response => {
                    this.project_general_stats = response.data                
                })
                .catch((error) => {
                    console.log('error while fetching statistics for projects')
                })

                //project size stats                
                this.$http.get(this.$BASE_URL + '/api/projects/project-size-stats/')
                .then(response => {
                    this.project_size_stats = response.data                
                })
                .catch((error) => {
                    console.log('error while fetching statistics for project sizes')
                })
            },
    
    
        },
    
    }
    </script>
    
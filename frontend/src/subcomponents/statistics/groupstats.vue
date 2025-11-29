<template>
        <div class="member-stats" >              
            <!-- age distribution -->
            <div v-if="group_data.datasets.length">
                <h3>Member distribution</h3>                                            
                <doughnutchart :data='group_data'/>
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
            group_general_stats: function(){
                if (this.group_general_stats){
                    var stats = this.group_general_stats[0].stats
                    this.members_in_groups = this.group_general_stats[0].total_members_in_groups
                    for (var group in stats){                        
                        this.group_data.labels.push(stats[group].group) 
                        this.group_data.datasets[0].backgroundColor.push("#"+((1<<24)*Math.random()|0).toString(16))
                        this.group_data.datasets[0].data.push(stats[group].members_count)
                    }
                }
            }
        },
    
        created(){
            this.fetchData()        
        },
        data(){
            return{
                members_in_groups: 0,
                new_members_stats: null ,
                group_general_stats: null,
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: []
                }, 
                group_data: {
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
                //age distribution stats
                this.$http.get(this.$BASE_URL + '/api/groups/group-general-stats/')
                .then(response => {
                    this.group_general_stats = response.data                
                })
                .catch((error) => {
                    console.log('error while fetching statistics for groups')
                })
            },
    
    
        },
    
    }
    </script>
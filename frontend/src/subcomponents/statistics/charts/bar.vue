<script>
 import { Bar } from 'vue-chartjs'
 
 export default {
   name: 'barchart',
   extends: Bar,
   props: ['data', 'options'],
   mounted () {
     this.renderChart(this.data, this.options)
   }
 }
</script>
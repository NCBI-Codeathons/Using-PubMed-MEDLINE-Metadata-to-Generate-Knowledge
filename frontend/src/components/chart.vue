<template>
  <Chart :options="options"></chart>
</template>

<script>
import {Chart} from 'highcharts-vue'
export default {
  props: [
    'categories',
    'counts'
  ],
  components: {
      Chart
  },
  data: function() {
    const data = this.msg;
    return {
      options: {
        credits: {
          enabled: false // Remove watermark.
        },
        chart: {
          type: "column",
          height: 400,
          
          backgroundColor: 0,
          animation: false,
          spacing: [10, 20, 10, 10]
        },
        title: null,
        legend:{
          enabled: false
        },
        xAxis: {
          categories: this.categories,
          title: null
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Number of publications',
                // align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        series: [{
          name: 'Test',
          data: this.counts,
          animation: false,
          color: '#24A'
        }]
      }
    }
  },
}
</script>

<style scoped>

</style>
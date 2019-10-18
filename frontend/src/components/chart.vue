<template>
  <Chart :options="options" />
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
    return {
      options: this.build()
    }
  },
  watch: {
    categories(val) {
      this.options = this.build();
    },
    counts(val) {
      this.options = this.build();
    }
  },
  methods: {
    build() {
      return {
        credits: {
          enabled: false // Remove watermark.
        },
        chart: {
          type: "column",
          height: 400,
          
          backgroundColor: 0,
          animation: false,
          spacing: [50, 20, 20, 20]
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
          color: '#1E88E5'
        }]
      }
    }
  }
}
</script>

<style scoped>

</style>
<template>
  <Chart :options="options" />
</template>

<script>
import {Chart} from 'highcharts-vue'
export default {
  props: [
    'config'
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
    config(val) {
      this.options = this.build();
    }
  },
  methods: {
    navigate(category) {
       window.open(this.config.data[category].pub_med, '_blank');
    },
    
    build() {

      const self = this;
      const counts = [];
      const categories = [];
      for (const [cat, count] of Object.entries(this.config.data)) {
        counts.push([parseInt(count.count)]);
        categories.push([cat]);
      }

      const total = counts.reduce((a, b) => a + parseInt(b), 0);
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
        title: {
          text: this.config.primary.join("; ") + "<br/><span class='caption'>" + total + " total matches</span>",
        },
        legend:{
          enabled: false
        },
        xAxis: {
          categories: categories,
          title: {
            text: this.config.refinment.join('; ')
          }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Number of publications',
            },
            labels: {
                overflow: 'justify'
            }
        },
        plotOptions: {
          series: {
              cursor: 'pointer',
              point: {
                  events: {
                      click: function () {
                          self.navigate(this.category)
                      }
                  }
              }
          }
        },
        series: [{
          name: 'Counts',
          data: counts,
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
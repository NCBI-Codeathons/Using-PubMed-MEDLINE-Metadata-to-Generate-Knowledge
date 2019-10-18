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
    build() {


      const counts = [];
      const categories = [];
      for (const [cat, count] of Object.entries(this.config.data)) {
        counts.push([parseInt(count)]);
        categories.push([cat]);
      }

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
          text: this.config.primary.join("; ")
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
                          window.open('http://stackoverflow.com', '_blank');
                          //alert('Category: ' + this.category + ', value: ' + this.y);
                      }
                  }
              }
          }
        },
        series: [{
          name: 'Test',
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
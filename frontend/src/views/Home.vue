<template>
<v-container>
  <v-overlay v-if="loading" opacity="0.8" color="white">
      <v-progress-circular :size="150" color="blue darken-1" indeterminate />
  </v-overlay>
  <v-row>
    <v-col>
      <v-card class="mx-auto">
        <v-container>
          <v-row dense>
            <v-col dense>
              <Terms v-model="primary" vocab="primary" label="Primary search terms"/>
              <Terms v-model="refinment" vocab="refinment" label="Refinment search terms" />
              <v-btn :disabled="disabled" block color="blue darken-1" light v-on:click="query">Enlighten me!</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-col>
  </v-row>
  <v-row v-if="loaded">
    <v-col>
    <v-card class="mx-auto">
      <Chart :categories="categories" :counts="counts" :primary="primary" :refinment="refinment" />
    </v-card>
    </v-col>
  </v-row>
</v-container>
</template>

<script>

import Chart from '@/components/chart'
import Terms from '@/components/terms'
import {search} from '@/plugins/api'

export default {
  name: 'home',
  components: {
    Chart,
    Terms
  },
  data: function() {
     return {
      primary: [],
      refinment: [],
      loaded: false,
      loading: false,
      categories: [],
      counts: [],
      disabled: true,
     }
  },
  watch: {
    primary(val) {
      this.disabled = !(this.checkValid(val) && this.checkValid(this.refinment));
    },
    refinment(val) {
      this.disabled = !(this.checkValid(val) && this.checkValid(this.primary));
    }
  },
  methods: {
    checkValid(val) {
      return Array.isArray(val) && ( val.length != 0 );
    },
    async query() {

      this.loading = true;
      
      const result = await search(this.primary, this.refinment);
      
      this.disabled = !(this.checkValid(this.primary) && this.checkValid(this.refinment));
      this.loading = false;

      if ('error' in result) {
        this.loaded = false;
        alert(result.error);
        return;
      }
      this.categories = result.categories;
      this.counts = result.counts;
      this.loaded = true;
    }
   }
}
</script>

<style scoped>
.head {
  width: auto !important;
  color: var(--v-secondary-lighten1);
  font-weight: bold;
}
</style>
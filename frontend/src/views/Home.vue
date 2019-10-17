<template>
<v-container>
  <v-overlay v-if="loading" opacity="0.5" color="white">
      <v-progress-circular :size="150" color="primary" indeterminate />
  </v-overlay>
  <v-row>
    <v-col>
      <v-card class="mx-auto">
     <v-simple-table>
        <tbody>
          <tr>
            <td class="head">Primary search terms</td>
            <td><Terms v-model="primary" vocab="primary" /></td>
          </tr>
          <tr>
            <td class="head">Refinment search terms</td>
            <td><Terms v-model="refinment" vocab="refinment" /></td>
          </tr>
        </tbody>
      </v-simple-table>
      </v-card>
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <v-card class="mx-auto">
            <v-card-actions>
              <v-btn :disabled="disabled" block color="blue darken-1" light v-on:click="query">Enlight me!</v-btn>
            </v-card-actions>
          </v-card>
    </v-col>
  </v-row>
  <v-row v-if="loaded">
    <v-card class="mx-auto">
      <Chart :categories="categories" :counts="counts" />
    </v-card>
  </v-row>
</v-container>
</template>

<script>
// Search

// Split categories
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
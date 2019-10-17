<template>
<v-container>
  <v-row>
    <v-col>
     <v-simple-table>
        <tbody>
          <tr>
            <td class="head">Primary search terms</td>
            <td><Terms v-model="primary" /></td>
          </tr>
          <tr>
            <td class="head">Refinment search terms</td>
            <td><Terms v-model="refinment" /></td>
          </tr>
        </tbody>
      </v-simple-table>
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <v-card class="mx-auto">
            <v-card-actions>
              <v-btn :disabled="disabled" block color="indigo" light v-on:click="query">Enlight me!</v-btn>
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
import search from '@/plugins/api'

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
      categories: [],
      counts: [],
      disabled: false,
     }
  },
   methods: {
    async query() {
      this.loaded = false;
      this.disabled = true;
      console.warn(this.primary, this.refinment);
      
      const result = await search(this.primary, this.refinment);
      console.log(result);
      this.categories = result.categories;
      this.counts = result.counts;
      this.loaded = true;
      this.disabled = false;
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
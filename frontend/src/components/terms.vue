<template>
  <v-row>
    <v-autocomplete
     dense
     chips
     small-chips
     multiple
     v-model="select"
     :loading="loading"
     :items="items"
     :search-input.sync="search"/>
  </v-row>
</template>

<script>

export default {
  components: {
  },
  props: {
    value: Array
  },
  data: function() {
     return {
      loading: false,
      items: ["Measles", "Europe", "Russia"],
      select: [],
      search: null
     }
  },
  watch: {
    select(val) {
      console.error("Updated: ", val);
      this.$emit('input', val);
    },
    search(val) {
      val && val != this.select && this.lookUp(val)
    }
  },
  methods: {
    lookUp(val) {
      this.loading = true;
      this.items = ["Measles", "Europe", "Russia"];
      this.loading = false;
    }
  }
}
</script>

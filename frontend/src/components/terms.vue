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
import {suggestions} from '@/plugins/api'

export default {
  components: {
  },
  props: {
    value: Array,
    vocab: String
  },
  async created() {
    this.items = await suggestions("", this.vocab);
  },
  data: function() {
     return {
      loading: false,
      items: [],
      select: [],
      search: null
     }
  },
  watch: {
    select(val) {
      this.$emit('input', val);
    },
    search(val) {
      val && val != this.select && this.lookUp(val)
    }
  },
  methods: {
    async lookUp(val) {
      this.loading = true;
      this.items = await suggestions(val, this.vocab);
      this.loading = false;
    }
  }
}
</script>

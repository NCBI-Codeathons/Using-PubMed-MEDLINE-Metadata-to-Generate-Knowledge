<template>
  <v-row>
    <v-autocomplete
     dense
     chips
     small-chips
     multiple
     auto-select-first
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
    console.log(this.vocab, "Created!", this.value);
    const res = await suggestions("", this.vocab);
    this.items = this.value;
    this.items = this.items.concat(res);
  },
  data: function() {
     return {
      loading: false,
      items: this.value,
      select: this.value,
      search: null
     }
  },
  watch: {
    select(val) {
      console.log(this.vocab, "Select!");
      this.$emit('input', val);
    },
    search(val) {
      console.log(this.vocab, "Search!");
      val && val != this.select && this.lookUp(val)
    }
  },
  methods: {
    async lookUp(val) {
      this.loading = true;
      const res = await suggestions(val, this.vocab);
      this.items = this.value;
      this.items = this.items.concat(res);
      this.loading = false;
      console.log(this.vocab, "Lookup end!");
    }
  }
}
</script>

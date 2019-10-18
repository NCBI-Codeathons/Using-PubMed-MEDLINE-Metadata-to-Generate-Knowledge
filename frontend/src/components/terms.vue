<template>
    <v-autocomplete
     outlined
     dense
     chips
     multiple
     deletable-chips
     auto-select-first
     v-model="select"
     :label="label"
     :loading="loading"
     :items="items"
     :search-input.sync="search"/>
</template>

<script>
import {suggestions} from '@/plugins/api'

export default {
  components: {
  },
  props: {
    value: Array,
    vocab: String,
    label: String
  },
  async created() {
    const res = await suggestions("", this.vocab);
    this.items = this.value;
    this.items = this.unique(this.items.concat(res));
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
      this.$emit('input', val);
      this.search = "";
    },
    search(val) {
      val && val != this.select && this.lookUp(val)
    }
  },
  methods: {
    unique (a) {
     return Array.from(new Set(a));
    },
    async lookUp(val) {
      this.loading = true;
      const res = await suggestions(val, this.vocab);
      this.items = this.value;
      this.items = this.unique(this.items.concat(res));
      this.loading = false;
    }
  }
}
</script>

<template>
  <v-app>
    <v-app-bar app elevation="1">
      <v-toolbar-title class="headline text-uppercase">
        <v-btn text to="/">
          <span class="font-weight-black">NLM</span>
          <span class="font-weight-regular">Pub</span>
          <span class="font-weight-light">Meta</span>
        </v-btn>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/about">
        <span class="mr-2">About</span>
      </v-btn>
    </v-app-bar>

    <v-content>
      <router-view />
    </v-content>
    <v-footer elevation="1">
      <v-container>
        <p class="text-right">NLM Internal Codethon</p>
        
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  name: "App",
  components: {
  }
};
</script>

<style scoped>
</style>
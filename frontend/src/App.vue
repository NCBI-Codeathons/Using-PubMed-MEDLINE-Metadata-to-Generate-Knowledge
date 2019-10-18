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
      <v-btn text href="https://github.com/NCBI-Codeathons/Using-PubMed-MEDLINE-Metadata-to-Generate-Knowledge/blob/master/README.md">
        <span class="mr-2">About</span>
      </v-btn>
    </v-app-bar>

    <v-content>
      <router-view />
    </v-content>
    <v-footer elevation="1">
      <v-container>
        <v-row>
          <v-col>
           <p class="text-left font-weight-light">NLM Internal Codeathon</p>
          </v-col>
          <v-col>
            <p class="text-right font-weight-regular">&copy; Dream Team 2019</p>
          </v-col>
        </v-row>
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
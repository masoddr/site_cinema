<template>
  <div id="app">
    <h1>Séances de cinéma</h1>
    <SeancesList :seances="seances" />
  </div>
</template>

<script>
import SeancesList from './components/SeancesList.vue'

export default {
  name: 'App',
  components: {
    SeancesList
  },
  data() {
    return {
      seances: []
    }
  },
  async created() {
    try {
      const response = await fetch('/seances.json')
      this.seances = await response.json()
    } catch (error) {
      console.error('Erreur lors du chargement des séances:', error)
    }
  }
}
</script> 
<template>
  <div id="app">
    <h1>Séances de cinéma</h1>
    
    <!-- Indicateur de chargement -->
    <div v-if="loading" class="loading">
      Chargement des séances...
    </div>
    
    <!-- Message d'erreur -->
    <div v-if="error" class="error">
      {{ error }}
    </div>
    
    <!-- Liste des séances -->
    <SeancesList v-if="!loading && !error" :seances="seances" />
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
      seances: [],
      loading: true,
      error: null
    }
  },
  async created() {
    try {
      const response = await fetch('/api/seances')
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
      this.seances = await response.json()
    } catch (error) {
      console.error('Erreur lors du chargement des séances:', error)
      this.error = "Impossible de charger les séances. Veuillez réessayer plus tard."
    } finally {
      this.loading = false
    }
  }
}
</script>

<style>
.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  text-align: center;
  padding: 2rem;
  color: #ff4444;
  background: #ffeeee;
  border-radius: 4px;
  margin: 1rem;
}
</style> 
</style> 
</script> 
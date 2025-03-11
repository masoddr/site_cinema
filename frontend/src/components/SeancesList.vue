<template>
  <div class="seances-container">
    <!-- Navigation des jours -->
    <div class="days-navigation">
      <button 
        v-for="(day, index) in uniqueDays" 
        :key="day"
        :class="{ active: selectedDay === day }"
        @click="selectedDay = day"
      >
        {{ formatDay(day) }}
      </button>
    </div>

    <!-- Affichage des séances du jour sélectionné -->
    <div class="seances-day">
      <div class="movies-grid">
        <div v-for="movie in moviesForSelectedDay" :key="movie.titre" class="movie-card">
          <img :src="movie.poster" :alt="movie.titre" class="movie-poster">
          <div class="movie-info">
            <h3>{{ movie.titre }}</h3>
            <div class="seances-times">
              <span 
                v-for="seance in movie.seances" 
                :key="seance.heure"
                class="seance-time"
              >
                {{ seance.heure }} 
                <span class="version">{{ seance.version }}</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'

export default {
  name: 'SeancesList',
  props: {
    seances: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const selectedDay = ref(null)

    // Obtenir tous les jours uniques des séances
    const uniqueDays = computed(() => {
      const days = [...new Set(props.seances.map(s => s.jour))]
      return days.sort()
    })

    // Initialiser avec le premier jour
    if (!selectedDay.value && uniqueDays.value.length > 0) {
      selectedDay.value = uniqueDays.value[0]
    }

    // Grouper les séances par film pour le jour sélectionné
    const moviesForSelectedDay = computed(() => {
      const daySeances = props.seances.filter(s => s.jour === selectedDay.value)
      const movieMap = new Map()

      daySeances.forEach(seance => {
        if (!movieMap.has(seance.titre)) {
          movieMap.set(seance.titre, {
            titre: seance.titre,
            poster: seance.poster,
            seances: []
          })
        }
        movieMap.get(seance.titre).seances.push({
          heure: seance.heure,
          version: seance.version
        })
      })

      return Array.from(movieMap.values())
    })

    const formatDay = (dateStr) => {
      const date = new Date(dateStr)
      return format(date, 'EEEE d MMMM', { locale: fr })
    }

    return {
      selectedDay,
      uniqueDays,
      moviesForSelectedDay,
      formatDay
    }
  }
}
</script>

<style scoped>
.seances-container {
  padding: 20px;
}

.days-navigation {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.days-navigation button {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background-color: #f0f0f0;
  cursor: pointer;
  white-space: nowrap;
}

.days-navigation button.active {
  background-color: #2c3e50;
  color: white;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.movie-card {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  background: white;
}

.movie-poster {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.movie-info {
  padding: 15px;
}

.seances-times {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.seance-time {
  background-color: #f0f0f0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}

.version {
  font-size: 0.8em;
  color: #666;
  margin-left: 4px;
}
</style> 
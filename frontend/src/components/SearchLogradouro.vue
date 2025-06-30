<template>
  <div class="search">
    <label>Logradouro:</label>
    <input 
      v-model="q" 
      @keyup.enter="search" 
      placeholder="Ex: R MARIANTE" />
    <button @click="search">Buscar</button>

    <!-- Primeiro os resultados -->
    <div v-if="total !== null" class="results">
      <p>Total: {{ total }}</p>
      <table v-if="results.length">
        <thead>
          <tr>
            <th>Implantação</th>
            <th>Logradouro</th>
            <th>Descrição</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="(r, idx) in results" 
            :key="`${r.implantacao}-${r.logradouro_nome}-${idx}`"
          >
            <td>{{ r.implantacao }}</td>
            <td>{{ r.logradouro_nome }}</td>
            <td>{{ r.descricao }}</td>
          </tr>
        </tbody>
      </table>
      <div class="pager">
        <button :disabled="page === 1" @click="changePage(page - 1)">‹</button>
        {{ page }} / {{ lastPage }}
        <button :disabled="page === lastPage" @click="changePage(page + 1)">›</button>
      </div>
      <div class="selector">
      <label>Ordem:</label>
      <select v-model="ordering" @change="search">
        <option value="asc">Ascendente</option>
        <option value="desc">Descendente</option>
      </select>
      </div>
    </div>

    <!-- Depois o mapa sempre presente -->
    <div ref="mapContainer" class="map-container"></div>
  </div>
</template>

<script>
import axios from 'axios'
import mapboxgl from 'mapbox-gl'

export default {
  name: 'SearchLogradouro',
  data() {
    return {
      q: '',
      results: [],
      total: null,
      page: 1,
      pagesize: 10,
      map: null,
      ordering: 'asc',
    }
  },
  watch: {
    results() {
      // só atualiza o mapa quando a source já estiver definida
      if (this.map && this.map.getSource('ciclovias')) {
        this.updateMapData()
      }
    }
  },
  computed: {
    lastPage() {
      return this.total ? Math.ceil(this.total / this.pagesize) : 1
    }
  },
  mounted() {
    // Inicializa o mapa só uma vez
    mapboxgl.accessToken = 'pk.eyJ1Ijoiam9hb3Zhc2MiLCJhIjoiY21iYTBnZHVrMTJuZDJxcTVhNzA0dDQ5aiJ9.jV3spZZnx6NZzRFOJBYe4A'
    this.map = new mapboxgl.Map({
      container: this.$refs.mapContainer,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-51.2300, -30.0400],
      zoom: 12
    })
    this.map.on('load', () => {
      this.map.addSource('ciclovias', {
        type: 'geojson',
        data: { type:'FeatureCollection', features: [] }
      })
      // círculo nos pontos
      this.map.addLayer({
        id: 'ciclovias-points',
        type: 'circle',
        source: 'ciclovias',
        paint: {
          'circle-radius': 5,
          'circle-color': '#e55e5e'
        }
      })
      // linha unindo todos os pontos
      this.map.addLayer({
        id: 'ciclovias-line',
        type: 'line',
        source: 'ciclovias',
        layout: {
          'line-join': 'round',
          'line-cap': 'round'
        },
        paint: {
          'line-color': '#e55e5e',
          'line-width': 3
        }
      })
    })
  },
  methods: {
    async search() {
      this.page = 1
      await this.loadPage()
    },
    async changePage(newPage) {
      if (newPage < 1 || newPage > this.lastPage) return
      this.page = newPage
      await this.loadPage()
    },
    async loadPage() {
      const resp = await axios.get('/api/busca-logradouro/', {
        params: {
          logradouro_nome: this.q,
          page: this.page,
          pagesize: this.pagesize,
          ordering: this.ordering
        }
      })
      this.results = resp.data.results
      this.total   = resp.data.total

      if (this.map && this.map.isStyleLoaded()) {
        this.updateMapData()
      } else if (this.map) {
        this.map.once('load', () => this.updateMapData())
      }
    },
    updateMapData() {
      const src = this.map.getSource('ciclovias')
      if (!src) return

      // ordena por num_inicial e filtra lat/lng válidos
      const pts = this.results
        .filter(r => r.latitude != null && r.longitude != null)
        .sort((a, b) => a.num_inicial - b.num_inicial)
        .map(r => [r.longitude, r.latitude])

      const features = []
      if (pts.length) {
        // linha única que segue o segmento
        features.push({
          type: 'Feature',
          geometry: { type: 'LineString', coordinates: pts },
          properties: {}
        })
        // pontos (opcional)
        pts.forEach(coord => {
          features.push({
            type: 'Feature',
            geometry: { type: 'Point', coordinates: coord },
            properties: {}
          })
        })
      }

      src.setData({ type: 'FeatureCollection', features })
      if (pts.length) {
        const bounds = new mapboxgl.LngLatBounds()
        pts.forEach(c => bounds.extend(c))
        this.map.fitBounds(bounds, { padding: 20 })
      }
    }
  }
}
</script>

<style scoped>
.search {
  display: grid;
  gap: 10px;
}
.search label {
  font-weight: bold;
}
.search input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.search button {
  padding: 8px 12px;
  background: var(--orange-pastel);
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.search button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.results p {
  margin: 0 0 10px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 10px;
}
th, td {
  padding: 8px;
  border-bottom: 1px solid #eee;
  text-align: left;
  font-size: 14px;
}
.pager {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}
.pager button {
  padding: 4px 8px;
  background: var(--blue-pastel);
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.pager button:disabled {
  opacity: 0.6;
}
.map-container {
  width: 100%;
  height: 300px;
  margin-top: 20px;
}
</style>
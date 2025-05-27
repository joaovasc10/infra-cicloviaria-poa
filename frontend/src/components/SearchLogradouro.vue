<template>
  <div>
    <h2>Buscar por Logradouro</h2>
    <input v-model="q" placeholder="Ex: R MARIANTE" @keyup.enter="fetch()" />
    <button @click="fetch">Buscar</button>
    <div v-if="total!==null">
      <p>Total: {{ total }}</p>
      <table v-if="results.length">
        <thead><tr><th>Implantação</th><th>Logradouro</th><th>Descrição</th></tr></thead>
        <tbody>
          <tr v-for="r in results" :key="r.implantacao+':' + r.logradouro_nome">
            <td>{{ r.implantacao }}</td>
            <td>{{ r.logradouro_nome }}</td>
            <td>{{ r.descricao }}</td>
          </tr>
        </tbody>
      </table>
      <div>
        <button :disabled="page===1" @click="page--;fetch()">‹</button>
        {{ page }} / {{ lastPage }}
        <button :disabled="page>=lastPage" @click="page++;fetch()">›</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { q: '', results: [], total: null, page: 1, pagesize: 10 }
  },
  computed: {
    lastPage() { return Math.ceil(this.total/this.pagesize) }
  },
  methods: {
    async fetch() {
      const resp = await axios.get('/api/busca-logradouro/', {
        params: { logradouro_nome: this.q, page: this.page, pagesize: this.pagesize }
      })
      this.results = resp.data.results
      this.total   = resp.data.total
    }
  }
}
</script>
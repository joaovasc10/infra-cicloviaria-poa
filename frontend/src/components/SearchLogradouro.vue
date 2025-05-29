<!-- frontend/src/components/SearchLogradouro.vue -->
<template>
  <div class="search">
    <label>Logradouro:</label>
    <input v-model="q" @keyup.enter="fetch" placeholder="Ex: R MARIANTE" />
    <button @click="search">Buscar</button>

    <div v-if="total!==null" class="results">
      <p>Total: {{ total }}</p>
      <table v-if="results.length">
        <thead>
          <tr><th>Implant.</th><th>Logradouro</th><th>Descrição</th></tr>
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
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      q: '',
      results: [],
      total: null,
      page: 1,
      pagesize: 10
    }
  },
  computed: {
    lastPage() {
      return this.total ? Math.ceil(this.total / this.pagesize) : 1
    }
  },
  methods: {
    // dispara a pesquisa sempre resetando para a página 1
    async search() {
      this.page = 1
      await this.loadPage()
    },

    // navega para a página passada (se válida) e carrega
    async changePage(newPage) {
      if (newPage < 1 || newPage > this.lastPage) return
      this.page = newPage
      await this.loadPage()
    },

    // única função que busca e SUBSTITUI results
    async loadPage() {
      const resp = await axios.get('/api/busca-logradouro/', {
        params: {
          logradouro_nome: this.q,
          page: this.page,
          pagesize: this.pagesize
        }
      })
      this.results = resp.data.results    // **substitui** o array
      this.total = resp.data.total
    }
  }
}
</script>

<style scoped>
.search {
  display: grid;
  gap: 10px;
}
.search label { font-weight: bold; }
.search input {
  padding: 8px; border:1px solid #ccc; border-radius:4px;
}
.search button {
  padding: 8px 12px;
  background: var(--orange-pastel);
  border:none;
  border-radius:4px;
  cursor:pointer;
}
.search button:disabled { opacity:0.6; cursor:not-allowed; }

.results p { margin:0 0 10px; }
table {
  width:100%; border-collapse:collapse; margin-bottom:10px;
}
th, td {
  padding:8px; border-bottom:1px solid #eee;
  text-align:left;
  font-size:14px;
}
.pager {
  text-align:center;
  display:flex; justify-content:center; align-items:center; gap:10px;
}
.pager button {
  padding:4px 8px;
  background: var(--blue-pastel);
  border:none; border-radius:4px; cursor:pointer;
}
.pager button:disabled { opacity:0.6 }
</style>
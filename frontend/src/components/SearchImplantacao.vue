<template>
  <div class="search">
    <label>Implantação:</label>
    <input
      v-model="q"
      type="date"
      @change="fetch"
      placeholder="Ex: 2018-06-21"
    />
    <button @click="fetch">Buscar</button>

    <div v-if="total !== null" class="results">
      <p>Total: {{ total }}</p>
      <table v-if="results.length">
        <thead>
          <tr>
            <th>Implant.</th>
            <th>Logradouro</th>
            <th>Descrição</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="r in results"
            :key="r.implantacao + r.logradouro_nome + r.data_extracao"
          >
            <td>{{ r.implantacao }}</td>
            <td>{{ r.logradouro_nome }}</td>
            <td>{{ r.descricao }}</td>
          </tr>
        </tbody>
      </table>
      <div class="pager">
        <button :disabled="page === 1" @click="prev">‹</button>
        {{ page }} / {{ lastPage }}
        <button :disabled="page >= lastPage" @click="next">›</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SearchImplantacao',
  data() {
    return {
      q: '',
      results: [],
      total: null,
      page: 1,
      pagesize: 10,
    }
  },
  computed: {
    lastPage() {
      return Math.ceil(this.total / this.pagesize)
    },
  },
  methods: {
    async fetch() {
      this.page = 1
      const resp = await axios.get('/api/busca-implantacao/', {
        params: {
          implantacao: this.q,
          page: this.page,
          pagesize: this.pagesize,
        },
      })
      this.results = resp.data.results
      this.total = resp.data.total
    },
    async loadPage() {
      const resp = await axios.get('/api/busca-implantacao/', {
        params: {
          implantacao: this.q,
          page: this.page,
          pagesize: this.pagesize,
        },
      })
      this.results = resp.data.results
    },
    prev() {
      if (this.page > 1) {
        this.page--
        this.loadPage()
      }
    },
    next() {
      if (this.page < this.lastPage) {
        this.page++
        this.loadPage()
      }
    },
  },
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
th,
td {
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
</style>
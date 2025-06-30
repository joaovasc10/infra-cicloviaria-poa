<!-- frontend/src/App.vue -->
<template>
  <div id="app">
    <h1>Infraestrutura Cicloviária POA</h1>

    <div class="selector">
      <label>Buscar por:</label>
      <select v-model="searchType">
        <option disabled value="">-- selecione --</option>
        <option value="logradouro">Logradouro</option>
        <option value="implantacao">Implantação</option>
      </select>
    </div>

    <div class="card">
      <SearchLogradouro v-if="searchType==='logradouro'" />
      <SearchImplantacao v-if="searchType==='implantacao'" />
      <p v-if="!searchType" class="info">Escolha um critério acima.</p>
    </div>
  </div>
</template>

<script>
import SearchLogradouro from './components/SearchLogradouro.vue'
import SearchImplantacao from './components/SearchImplantacao.vue'

export default {
  name: 'App',
  components: { SearchLogradouro, SearchImplantacao },
  data() { return { searchType: '' } }
}
</script>

<style>
:root {
  --blue-pastel: #688a7c; /* title */
  --orange-pastel: #FFD8A8;
  --neutral: #becec4; /* background */
  --text: #7f8c8d;
}

body {
  margin: 0;
  font-family: sans-serif;
  background: var(--neutral);
  color: var(--text);
}

#app {
  max-width: 700px;
  margin: 40px auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: var(--blue-pastel);
}

.selector {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 20px 0;
}

.selector select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.info {
  text-align: center;
  color: #666;
}
</style>
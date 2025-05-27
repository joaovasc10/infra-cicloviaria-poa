<template>
  <div id="app">
    <h1>Infraestrutura Cicloviária POA</h1>
    <SearchLogradouro />
    <hr/>
    <SearchImplantacao />
  </div>
</template>
<script>
import SearchLogradouro from './components/SearchLogradouro.vue'
import SearchImplantacao from './components/SearchImplantacao.vue'
export default { components: { SearchLogradouro, SearchImplantacao } }
</script>
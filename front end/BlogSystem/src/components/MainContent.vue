<template>
  <div class="container">
    <div class="main-content">
      <Sidebar />
      <div class="content">
        <ArticlesSection />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from './Sidebar.vue'
import ArticlesSection from './ArticlesSection.vue'

export default {
  components: {
    Sidebar,
    ArticlesSection
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}

@media (min-width: 992px) {
  .main-content {
    grid-template-columns: 340px 1fr;
  }
}
</style>
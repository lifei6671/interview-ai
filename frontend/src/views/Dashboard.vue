<template>
  <div class="dashboard-container">
    <WelcomeBanner />
    <OCRCard />
    <TranslationCard />
  </div>
</template>

<script setup lang="ts">
import WelcomeBanner from './dashboard/components/WelcomeBanner.vue'
import OCRCard from './dashboard/components/OCRCard.vue'
import TranslationCard from './dashboard/components/TranslationCard.vue'
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

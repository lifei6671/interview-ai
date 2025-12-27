<template>
  <div class="dashboard-container">
    <WelcomeBanner />

    <TranslationCard />
  </div>
</template>

<script setup lang="ts">
import WelcomeBanner from './dashboard/components/WelcomeBanner.vue'
import TranslationCard from './dashboard/components/TranslationCard.vue'
</script>

<style scoped>
.dashboard-container {
  max-width: 1440px;
  margin: 0 auto;
}
</style>

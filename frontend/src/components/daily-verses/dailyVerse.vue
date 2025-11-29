<template>
  <div class="daily-verse">
    <h2>📖 Today's Verse</h2>
    <p v-if="verse">{{ verse }}</p>
    <p v-else>Loading...</p>
  </div>
</template>

<script>
export default {
  name: "DailyVerse",
  data() {
    return {
      verse: null
    };
  },
  mounted() {
    // Simulate fetch
    this.verse = "📖 John 3:16 - For God so loved the world...";
  }
};
</script>

<style scoped>
.daily-verse {
  text-align: center;
  margin-top: 20px;
}
</style>


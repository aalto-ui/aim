<template lang="html">
  <b-progress id="progress_bar" height="2rem" :max="max">
    <b-progress-bar :value="progress" show-progress animated>
      <strong>{{ label() }}</strong>
    </b-progress-bar>
  </b-progress>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: mapGetters({
    progress: 'progress',
    max: 'maxProgress'
  }),
  methods: {
    label () {
      if (this.progress === 1) {
        return 'Fetching preview'
      }
      return 'Running metric ' + (this.progress - 1) + '/' + (this.max - 2)
    }
  }
}
</script>

<style lang="css">
</style>

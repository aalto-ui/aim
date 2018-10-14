<template lang="html">
  <div>
    <h2>Preview</h2>
    <p>1280x720 pixels at 72 dpi (URL) or original size and resolution (screenshot)</p>
    <img class="preview-img" :src="'data:image/png;base64, ' + b64" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: mapState({
    b64: state => state.preview
  })
}
</script>

<style lang="css">
.preview-img {
  width: 100%;
}
</style>

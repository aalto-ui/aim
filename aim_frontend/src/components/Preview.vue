<template lang="html">
  <div>
    <h2>Preview</h2>
    <p>1280 x 800 pixels at 72 dpi (URL) or original image resized to 1280 pixels width at 72 dpi (screenshot)</p>
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

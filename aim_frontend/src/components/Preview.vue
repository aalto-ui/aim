<template lang="html">
  <div>
    <div class="component-section">
      <b-row>
        <b-col cols="12">
          <h2 class="component-title">Preview</h2>
           <p>1280 x 800 pixels at 72 dpi (URL) or original image resized to 1280 pixels width at 72 dpi (screenshot)</p>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <img class="preview-img" :src="'data:image/png;base64, ' + b64" />
        </b-col>
      </b-row>
    </div>
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

<style lang="css" scoped>

.component-section{
  margin: 80px 0px 20px;
}

.preview-img {
  width: 100%;
}

img{
  border: 1px solid #DDD;
}

</style>

<template>
  <div id="app">
    <b-container>
      <Header />
      <b-row>
        <b-col>
          <AIMForm />
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Header from './components/Header'
import AIMForm from './components/AIMForm'

export default {
  name: 'App',
  components: {
    Header,
    AIMForm
  }
}
</script>

<style lang="scss">
$theme-colors: (
  "primary": #7553A0,
);

@import '../node_modules/bootstrap/scss/bootstrap.scss';
@import '../node_modules/bootstrap-vue/dist/bootstrap-vue.css';
</style>

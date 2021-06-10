<template>
<div>
  <b-jumbotron bg-variant="light">
    <template slot="header">
      <b-row>
        <b-col class="hero-image text-center">
          <img src="../assets/workflow.png" width="100%" alt="Workflow">
        </b-col>
      </b-row>
      <h1 id="service_title" class="display-4">AIM - Aalto Interface Metrics service</h1>
      <h2 class="text-muted">Compute how good your design is!</h2>
    </template>
    <template slot="lead">
      Welcome to AIM! Send your design and choose metrics: AIM computes numerous metrics and models that predict how users perceive, search, and experience your design. Download & contribute to the project at <a href="https://github.com/aalto-ui/aim" target="_blank">GitHub</a>.
    </template>
    <b-row v-if="generalError">
      <b-col>
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
          <h4 class="alert-heading">Technical Difficulties</h4>
          <hr>
          <p>
            <strong>Whoops!</strong> We are having some technical difficulties, please try again later.
          </p>
        </div>
      </b-col>
    </b-row>
    <b-row v-if="validationError">
      <b-col>
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          <h4 class="alert-heading">Validation Error</h4>
          <hr>
          <p>
            <strong>Whoops!</strong> We are having some problems with your input, please try again with a different URL or image.
          </p>
        </div>
      </b-col>
    </b-row>
    <b-row v-if="display.input">
      <b-col>
        <b-form id="aim-url-form" class="needs-validation" novalidate @submit="onSubmitURL">
          <b-input-group prepend="URL">
            <b-form-input id="url-input" type="url" v-model.trim="form.url" required placeholder="https://www.example.com"></b-form-input>
            <b-input-group-append>
              <b-btn id="btn-url-apply" type="submit" variant="primary">Apply</b-btn>
            </b-input-group-append>
            <div class="invalid-feedback">
              Please provide a valid URL.
            </div>
          </b-input-group>
        </b-form>
      </b-col>
      <b-col cols="12" class="col-lg-auto text-center or">
        - OR -
      </b-col>
      <b-col>
        <b-form id="aim-image-form" class="needs-validation" novalidate @submit="onSubmitImage">
          <b-input-group id="image-input-group" prepend="Image">
            <b-form-file id="image-input" required placeholder="Choose a PNG file..." accept="image/png" @change="onFileSelected"></b-form-file>
            <b-input-group-append>
              <b-btn id="btn-image-apply" type="submit" variant="primary">Apply</b-btn>
            </b-input-group-append>
          </b-input-group>
          <div v-if="fileTooLarge === false" class="invalid-feedback">
            Please provide a valid image.
          </div>
          <div v-if="fileTooLarge" class="invalid-feedback">
            File is too large (max 5 MB).
          </div>
        </b-form>
      </b-col>
    </b-row>
    <b-form id="aim-form" @submit="onSubmit" v-if="display.metrics">
      <div class="tablist" role="tablist">
        <b-card no-body active class="mb-4">
          <b-card-header header-tag="header" role="tab" class="p-0">
            <div variant="cat-one" class="rounded" block v-b-toggle.cat-one-accordion href="#">
              <span class="fa">
                <font-awesome-icon :icon="metricConfig.categories[0].icon" />
              </span>
              <span class="title">{{ metricConfig.categories[0].name }}</span>
            </div>
          </b-card-header>
          <b-collapse id="cat-one-accordion" visible role="tabpanel">
            <b-card-body>
              <table class="table table-striped table-bordered table-hover table-sm">
                <thead>
                  <tr>
                    <th class="text-center" scope="col">Selected</th>
                    <th scope="col">Metric</th>
                    <th scope="col">References</th>
                    <th scope="col">Evidence</th>
                    <th scope="col">Relevance</th>
                    <th scope="col">Computation time</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="metric in metricConfig.categories[0].metrics">
                    <tr :key="metric.id">
                      <td class="text-center">
                        <b-form-checkbox class="metric-checkbox" :id="'metric-cb-' + metric" v-model="selected[metric]"></b-form-checkbox>
                      </td>
                      <td>
                        {{metricConfig.metrics[metric].name}}
                        <span v-b-tooltip.hover :title="metricConfig.metrics[metric].description"><font-awesome-icon :icon="['fas', 'question-circle']" /></span>
                      </td>
                      <td>
                        [
                          <template v-for="(reference, index) in metricConfig.metrics[metric].references">
                            <template v-if="index > 0">, </template>
                            <a :href="reference.url" :title="reference.title" target="_blank" :key="index">{{ index + 1 }}</a>
                          </template>
                        ]
                      </td>
                      <td>
                        <span name="star" v-for="i in metricConfig.metrics[metric].evidence" :key="'evidence-star-' + metric + '-' + i">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span name="star-o" v-for="i in 5 - metricConfig.metrics[metric].evidence" :key="'evidence-star-o-' + metric + '-' + i">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                      </td>
                      <td>
                        <span name="star" v-for="i in metricConfig.metrics[metric].relevance" :key="'relevance-star-' + metric + '-' + i">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span name="star-o" v-for="i in 5 - metricConfig.metrics[metric].relevance" :key="'relevance-star-o-' + metric + '-' + i">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                      </td>
                      <td>
                        <template v-if="metricConfig.metrics[metric].speed === 2">
                          <div style="color: green">
                            Fast
                          </div>
                        </template>
                        <template v-else-if="metricConfig.metrics[metric].speed === 1">
                          <div style="color: orange">
                            Medium
                          </div>
                        </template>
                        <template v-else-if="metricConfig.metrics[metric].speed === 0">
                          <div style="color: red">
                            Slow
                          </div>
                        </template>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </b-card-body>
          </b-collapse>
        </b-card>
        <b-card no-body class="mb-4">
          <b-card-header header-tag="header" role="tab" class="p-0">
            <div variant="cat-two" class="rounded" block v-b-toggle.cat-two-accordion href="#">
              <span class="fa">
              <font-awesome-icon :icon="metricConfig.categories[1].icon" />
              </span>
              <span class="title">{{ metricConfig.categories[1].name }}</span>
            </div>
          </b-card-header>
          <b-collapse id="cat-two-accordion" visible role="tabpanel">
            <b-card-body>
              <table class="table table-striped table-bordered table-hover table-sm">
                <thead>
                  <tr>
                    <th class="text-center" scope="col">Selected</th>
                    <th scope="col">Metric</th>
                    <th scope="col">References</th>
                    <th scope="col">Evidence</th>
                    <th scope="col">Relevance</th>
                    <th scope="col">Computation time</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="metric in metricConfig.categories[1].metrics">
                    <tr :key="metric.id">
                      <td class="text-center">
                        <b-form-checkbox class="metric-checkbox" :id="'metric-cb-' + metric" v-model="selected[metric]"></b-form-checkbox>
                      </td>
                      <td>
                        {{metricConfig.metrics[metric].name}}
                        <span v-b-tooltip.hover :title="metricConfig.metrics[metric].description"><font-awesome-icon :icon="['fas', 'question-circle']" /></span>
                      </td>
                      <td>
                        [
                          <template v-for="(reference, index) in metricConfig.metrics[metric].references">
                            <template v-if="index > 0">, </template>
                            <a :href="reference.url" :title="reference.title" target="_blank" :key="index">{{ index + 1 }}</a>
                          </template>
                        ]
                      </td>
                      <td>
                        <span name="star" v-for="i in metricConfig.metrics[metric].evidence" :key="'evidence-star-' + metric + '-' + i">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span name="star-o" v-for="i in 5 - metricConfig.metrics[metric].evidence" :key="'evidence-star-o-' + metric + '-' + i">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                      </td>
                      <td>
                        <span name="star" v-for="i in metricConfig.metrics[metric].relevance" :key="'relevance-star-' + metric + '-' + i">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span name="star-o" v-for="i in 5 - metricConfig.metrics[metric].relevance" :key="'relevance-star-o-' + metric + '-' + i">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                      </td>
                      <td>
                        <template v-if="metricConfig.metrics[metric].speed === 2">
                          <div style="color: green">
                            Fast
                          </div>
                        </template>
                        <template v-else-if="metricConfig.metrics[metric].speed === 1">
                          <div style="color: orange">
                            Medium
                          </div>
                        </template>
                        <template v-else-if="metricConfig.metrics[metric].speed === 0">
                          <div style="color: red">
                            Slow
                          </div>
                        </template>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </b-card-body>
          </b-collapse>
        </b-card>
        <b-card no-body class="mb-4">
          <b-card-header header-tag="header" role="tab" class="p-0">
            <div variant="cat-three" class="rounded" block v-b-toggle.cat-three-accordion href="#">
              <span class="fa">
              <font-awesome-icon :icon="metricConfig.categories[2].icon" />
              </span>
              <span class="title">{{ metricConfig.categories[2].name }}</span>
            </div>
          </b-card-header>
          <b-collapse id="cat-three-accordion" visible role="tabpanel">
            <b-card-body>
              <table class="table table-striped table-bordered table-hover table-sm">
                <thead>
                  <tr>
                    <th class="text-center" scope="col">Selected</th>
                    <th scope="col">Metric</th>
                    <th scope="col">References</th>
                    <th scope="col">Evidence</th>
                    <th scope="col">Relevance</th>
                    <th scope="col">Computation time</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="metric in metricConfig.categories[2].metrics">
                    <tr :key="metric.id">
                      <td class="text-center">
                        <b-form-checkbox class="metric-checkbox" :id="'metric-cb-' + metric" v-model="selected[metric]"></b-form-checkbox>
                      </td>
                      <td>
                        {{metricConfig.metrics[metric].name}}
                        <span v-b-tooltip.hover :title="metricConfig.metrics[metric].description"><font-awesome-icon :icon="['fas', 'question-circle']" /></span>
                      </td>
                      <td>
                        [
                          <template v-for="(reference, index) in metricConfig.metrics[metric].references">
                            <template v-if="index > 0">, </template>
                            <a :href="reference.url" :title="reference.title" target="_blank" :key="index">{{ index + 1 }}</a>
                          </template>
                        ]
                      </td>
                      <td>
                        <span name="star" v-for="i in metricConfig.metrics[metric].evidence" :key="'evidence-star-' + metric + '-' + i">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span name="star-o" v-for="i in 5 - metricConfig.metrics[metric].evidence" :key="'evidence-star-o-' + metric + '-' + i">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                      </td>
                      <td>
                        <span name="star" v-for="i in metricConfig.metrics[metric].relevance" :key="'relevance-star-' + metric + '-' + i">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span name="star-o" v-for="i in 5 - metricConfig.metrics[metric].relevance" :key="'relevance-star-o-' + metric + '-' + i">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                      </td>
                      <td>
                        <template v-if="metricConfig.metrics[metric].speed === 2">
                          <div style="color: green">
                            Fast
                          </div>
                        </template>
                        <template v-else-if="metricConfig.metrics[metric].speed === 1">
                          <div style="color: orange">
                            Medium
                          </div>
                        </template>
                        <template v-else-if="metricConfig.metrics[metric].speed === 0">
                          <div style="color: red">
                            Slow
                          </div>
                        </template>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </b-card-body>
          </b-collapse>
        </b-card>
        <b-card no-body class="mb-4">
          <b-card-header header-tag="header" role="tab" class="p-0">
            <div variant="cat-four" class="rounded" block v-b-toggle.cat-four-accordion href="#">
              <span class="fa">
              <font-awesome-icon :icon="metricConfig.categories[3].icon" />
              </span>
              <span class="title">{{ metricConfig.categories[3].name }}</span>
            </div>
          </b-card-header>
          <b-collapse id="cat-four-accordion" visible role="tabpanel">
            <b-card-body>
              <table class="table table-striped table-bordered table-hover table-sm">
                <thead>
                  <tr>
                    <th class="text-center" scope="col">Selected</th>
                    <th scope="col">Metric</th>
                    <th scope="col">References</th>
                    <th scope="col">Evidence</th>
                    <th scope="col">Relevance</th>
                    <th scope="col">Computation time</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="metric in metricConfig.categories[3].metrics">
                    <tr :key="metric.id">
                      <td class="text-center">
                        <b-form-checkbox class="metric-checkbox" :id="'metric-cb-' + metric" v-model="selected[metric]"></b-form-checkbox>
                      </td>
                      <td>
                        {{metricConfig.metrics[metric].name}}
                        <span v-b-tooltip.hover :title="metricConfig.metrics[metric].description"><font-awesome-icon :icon="['fas', 'question-circle']" /></span>
                      </td>
                      <td>
                        [
                          <template v-for="(reference, index) in metricConfig.metrics[metric].references">
                            <template v-if="index > 0">, </template>
                            <a :href="reference.url" :title="reference.title" target="_blank" :key="index">{{ index + 1 }}</a>
                          </template>
                        ]
                      </td>
                      <td>
                        <span name="star" v-for="i in metricConfig.metrics[metric].evidence" :key="'evidence-star-' + metric + '-' + i">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span name="star-o" v-for="i in 5 - metricConfig.metrics[metric].evidence" :key="'evidence-star-o-' + metric + '-' + i">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                      </td>
                      <td>
                        <span name="star" v-for="i in metricConfig.metrics[metric].relevance" :key="'relevance-star-' + metric + '-' + i">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span name="star-o" v-for="i in 5 - metricConfig.metrics[metric].relevance" :key="'relevance-star-o-' + metric + '-' + i">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                      </td>
                      <td>
                        <template v-if="metricConfig.metrics[metric].speed === 2">
                          <div style="color: green">
                            Fast
                          </div>
                        </template>
                        <template v-else-if="metricConfig.metrics[metric].speed === 1">
                          <div style="color: orange">
                            Medium
                          </div>
                        </template>
                        <template v-else-if="metricConfig.metrics[metric].speed === 0">
                          <div style="color: red">
                            Slow
                          </div>
                        </template>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </b-card-body>
          </b-collapse>
        </b-card>
      </div>
      <b-btn class="mt-2" size="lg" type="submit" variant="primary">Submit</b-btn>
    </b-form>
  </b-jumbotron>
  <div class="mt-2" v-if="display.progressBar">
    <ProgressBar />
  </div>
  <div class="mt-2" v-if="display.summary">
    <Summary />
  </div>
  <div class="mt-2" v-if="display.preview">
    <Preview />
  </div>
  <div class="mt-2" v-if="display.results">
    <Results />
  </div>
</div>
</template>

<script>
import metricConfig from '../../../metrics.json'
import Results from './Results'
import ProgressBar from './ProgressBar'
import Summary from './Summary'
import Preview from './Preview'

import { mapState } from 'vuex'

export default {
  data () {
    return {
      selected: {},
      form: {
        url: null,
        data: null,
        filename: null
      },
      metricConfig,
      fileTooLarge: false,
      input: null
    }
  },
  methods: {
    onSubmitURL (event) {
      // Prevent the event
      event.preventDefault()
      event.stopPropagation()

      // Update input
      this.input = 'url'

      // Hide validation error
      this.$store.commit('hideValidationError')

      // Fix URL, if needed
      this.fixURL()

      // Reset image form
      this.resetForm(false, true, false, false)

      // Validate URL form
      let form = event.target
      if ((this.$store.state.generalError === false) && (form.checkValidity() === true && this.form.url !== null)) {
        this.$store.commit('showMetrics')
      } else {
        this.$store.commit('hideMetrics')
      }
      form.classList.add('was-validated')
    },
    onSubmitImage (event) {
      // Prevent the event
      event.preventDefault()
      event.stopPropagation()

      // Update input
      this.input = 'image'

      // Hide validation error
      this.$store.commit('hideValidationError')

      // Reset URL form
      this.resetForm(true, false, false, false)

      // Validate image form
      let form = event.target
      if ((this.$store.state.generalError === false) && (form.checkValidity() === true && this.form.data !== null && this.form.filename !== null)) {
        document.querySelector('#image-input-group').classList.remove('is-invalid') // Hack due to the use of Bootstrap's custom image upload
        this.$store.commit('showMetrics')
      } else {
        document.querySelector('#image-input-group').classList.add('is-invalid') // Hack due to the use of Bootstrap's custom image upload
        this.$store.commit('hideMetrics')
      }
      form.classList.add('was-validated')
    },
    onSubmit (event) {
      // Prevent the event
      event.preventDefault()
      event.stopPropagation()

      // Fix URL, if needed
      this.fixURL()

      // Validate URL and image forms
      let urlForm = document.querySelector('#aim-url-form')
      let imageForm = document.querySelector('#aim-image-form')
      if ((this.$store.state.generalError === false) && ((urlForm.checkValidity() === true && this.form.url !== null) || (imageForm.checkValidity() === true && this.form.data !== null && this.form.filename !== null))) {
        // Submit data
        this.$socket.sendObj({
          type: 'execute',
          input: this.input,
          url: this.form.url,
          data: this.form.data,
          filename: this.form.filename,
          metrics: this.selected
        })
        this.$store.commit('fetchResults', this.selected)

        // Reset URL and image forms
        this.resetForm(true, true, true, true)
      } else {
        this.$store.commit('hideMetrics')
      }
    },
    onFileSelected (event) {
      let thisObj = this
      let file = event.target.files[0]
      document.querySelector('#image-input ~ .custom-file-label').textContent = file.name // Hack due to a Vue.js's "bug"; filename doesn't get updated on the second upload

      // Validate file size
      if (this.isFileTooLarge(file)) {
        document.querySelector('#image-input-group').classList.add('is-invalid') // Hack due to the use of Bootstrap's custom image upload
        this.form.data = null
        this.form.filename = null
        this.fileTooLarge = true
        this.$store.commit('hideMetrics')
      } else {
        this.getBase64(file, function (e) {
          document.querySelector('#image-input-group').classList.remove('is-invalid') // Hack due to the use of Bootstrap's custom image upload
          thisObj.form.data = e.target.result
          thisObj.form.filename = file.name
          thisObj.fileTooLarge = false
        })
      }
      document.querySelector('#aim-image-form').classList.add('was-validated')
    },
    isFileTooLarge (file) {
      const MAX_FILE_SIZE = 5242880 // 5 MB

      // Validate file size
      return (file.size > MAX_FILE_SIZE)
    },
    getBase64 (file, onLoadCallback) {
      var reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = onLoadCallback
      reader.onerror = function (error) {
        console.log('Error: ', error)
      }
    },
    fixURL () {
      if (this.form.url !== null) {
        this.form.url = this.form.url.toLowerCase()
        if (!!this.form.url && !/^https?:\/\//i.test(this.form.url)) {
          document.querySelector('#url-input').value = 'http://' + this.form.url // Hack due to a Vue's "bug"; updating the value of this.form.url doesn't pass validation even though its bound to the form input field
          this.form.url = 'http://' + this.form.url
        }
      }
    },
    resetForm (url, image, metrics, input) {
      if (url) {
        document.querySelector('#aim-url-form').classList.remove('was-validated')
        this.form.url = null
      }

      if (image) {
        document.querySelector('#image-input').value = ''
        document.querySelector('#image-input ~ .custom-file-label').textContent = 'Choose a PNG file...'
        document.querySelector('#image-input-group').classList.remove('is-invalid')
        document.querySelector('#aim-image-form').classList.remove('was-validated')
        this.form.data = null
        this.form.filename = null
        this.fileTooLarge = false
      }

      if (metrics) {
        this.selected = {}
      }

      if (input) {
        this.input = null
      }
    }
  },
  components: {
    Results,
    ProgressBar,
    Preview,
    Summary
  },
  computed: mapState({
    display: state => state.display,
    generalError: state => state.generalError,
    validationError: state => state.validationError
  })
}
</script>

<style>
.jumbotron{
  position: relative;
}

table thead th{
  word-break: break-word;
}
table thead th:nth-child(1){
  width: 10%;
}
table thead th:nth-child(2){
  width: 30%;
}
table thead th:nth-child(3){
  width: 18%;
}
table thead th:nth-child(4){
  width: 12%;
}
table thead th:nth-child(5){
  width: 12%;
}
table thead th:nth-child(6){
  width: 18%;
}

table tbody td:nth-child(2) svg{
  margin-bottom: 2px;
}

#aim-url-form input:-webkit-autofill {
    box-shadow: 0 0 0 30px white inset;
    -webkit-box-shadow: 0 0 0 30px white inset;
}
#aim-form {
  margin-top: 5rem;
}
#aim-form svg {
  position: relative;
  top: 2px;
}
h1 {
  margin-bottom: 0px;
}

.lead {
  margin-bottom: 1rem;
}

h2.text-muted {
  color: #aea697 !important;
  font-size: 1.5rem;
  margin-bottom: 20px;
}
.fa-star,
.fa-question-circle {
  color: #555555;
}

.card-body {
    padding: 1rem;
}

header{
  border-bottom: none;
}
.card-header{
  border-bottom: none;
}

.tablist .card-header div{
  position: relative;
  color: #fff;
  background-color: #7553a0;
  border: 1px solid #7553a0;
  padding: 0px 10px 0px 10px;
  text-align: left;
}

.tablist .card-header .title{
  font-size: 1.8rem;
  font-weight: normal;
}

.tablist .card-header .fa{
  font-size: 3rem;
  margin-right: 5px;
  /* position: absolute; */
  /* top: 5px; */
  /* right: 10px; */
  color: rgba(255, 255, 255, 0.3);
}

.metric-checkbox.custom-control {
  padding-left: 1rem;
}

.jumbotron {
  padding-top: 2rem;
  padding-bottom: 2rem;
}
.hero-image {
  margin-bottom: 20px;
}
.or {
  padding-top: 6px;
  padding-bottom: 6px;
}
#btn-url-apply {
  border-top-right-radius: 0.25rem;
  border-bottom-right-radius: 0.25rem;
}
#btn-image-apply {
  border-top-right-radius: 0.25rem;
  border-bottom-right-radius: 0.25rem;
}
.was-validated .form-control:valid, .was-validated .form-control:valid:focus,
.was-validated .custom-file-input:valid ~ .custom-file-label, .was-validated .custom-file-input:valid:focus ~ .custom-file-label {
  border-color: #ced4da;
  box-shadow: none;
}
.was-validated .is-invalid .custom-file-input:valid ~ .custom-file-label, .was-validated .is-invalid .custom-file-input:valid:focus ~ .custom-file-label {
  border-color: #dc3545;
  box-shadow: none;
}
#image-input ~ .custom-file-label {
  color: #6D757D;
}
#image-input ~ .custom-file-label::after {
  display: none;
}
.input-group.is-invalid ~ .invalid-feedback {
  display: block;
}

.custom-control {
  display: inline;
}

h2.components-title{
  font-size: 1.8rem;
  color: #222;
  margin-bottom: 30px;
  /* border-bottom: 2px #222 solid; */
}

.bg-secondary {
    background-color: #aaa !important;
}

.component-title{
  font-weight: 400;
  /* border-bottom: 3px solid #555; */
  margin: 0 0 20px 0;
}

.component-section{
  position: relative;
  padding: 0 0 0 0;
  margin: 50px 0 0 0;
  /* border-bottom: 1px solid #aaa; */
}

hr {
    margin-top: 0;
    margin-bottom: 0;
    border-top: 1px solid rgba(0, 0, 0, 0.5)
}

th{
    font-weight: bold;
    font-size: 0.9rem;
    color: #333;
}

</style>

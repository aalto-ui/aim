<template>
  <b-jumbotron bg-variant="light">
    <template slot="header">
      <b-row>
          <b-col class="hero-image text-center">
              <img src="../assets/workflow.png" width="100%" alt="Workflow">
          </b-col>
      </b-row>
      <h1 class="display-4">AIM - Aalto Interface Metrics service</h1>
      <h2 class="text-muted">Compute how good your design is!</h2>
    </template>
    <template slot="lead">
      Welcome to AIM! Send your design and choose metrics: AIM computes numerous metrics and models that predict how users perceive, search, and experience your design. Download & contribute to the project at <a href="https://github.com/aalto-ui/aim" target="_blank">GitHub</a>.
    </template>
    <b-row v-if="wsError">
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
    <b-row v-if="display.input">
      <b-col>
        <b-form id="aim-url-form" class="needs-validation" novalidate @submit="onSubmitURL">
          <b-input-group prepend="URL">
            <b-form-input id="url-input" type="url" v-model.trim="form.url" aria-describedby="urlHelp" required placeholder="https://www.example.com"></b-form-input>
            <b-input-group-append>
              <b-btn id="btn-url-proceed" type="submit" variant="primary">Proceed</b-btn>
            </b-input-group-append>
            <div class="invalid-feedback">
              Please provide a valid URL.
            </div>
          </b-input-group>
          <small id="urlHelp" class="text-muted">
            
          </small>
        </b-form>
      </b-col>
      <b-col cols="12" class="col-lg-auto text-center or">
        - OR -
      </b-col>
      <b-col>
        <b-form id="aim-screenshot-form" class="needs-validation" novalidate @submit="onSubmitScreenshot">
          <b-input-group id="screenshot-input-group" prepend="Screenshot">
            <b-form-file id="screenshot-input" aria-describedby="screenshotHelp" required placeholder="Choose a PNG file..." accept="image/png" @change="onFileSelected"></b-form-file>
            <b-input-group-append>
              <b-btn id="btn-screenshot-proceed" type="submit" variant="primary">Proceed</b-btn>
            </b-input-group-append>
          </b-input-group>
          <div v-if="fileTooLarge === false" class="invalid-feedback">
            Please provide a valid screenshot image.
          </div>
          <div v-if="fileTooLarge" class="invalid-feedback">
            File is too large (max 3 MB).
          </div>
          <small id="screenshotHelp" class="text-muted">
            Recommendation: 1280x720 pixels at 72 dpi (experimental)
          </small>
        </b-form>
      </b-col>
    </b-row>
    <b-form id="aim-form" @submit="onSubmit" v-if="display.metrics">
      <div role="tablist">
        <b-card no-body active class="mb-1">
          <b-card-header header-tag="header" role="tab" class="p-0">
            <b-btn variant="cat-one" block v-b-toggle.cat-one-accordion href="#">
              Select metrics: {{ metricConfig.categories[0].name }}
            </b-btn>
          </b-card-header>
          <b-collapse id="cat-one-accordion" visible role="tabpanel">
            <b-card-body>
              <p></p>
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
                    <tr>
                      <td class="text-center">
                        <b-form-checkbox class="metric-checkbox" :id="'metric-cb-' + metric" v-model="selected[metric]"></b-form-checkbox>
                      </td>
                      <td>
                        {{metricConfig.metrics[metric].name}}
                        <icon class="question-circle" name="question-circle" v-b-tooltip.hover :title="metricConfig.metrics[metric].description"></icon>
                      </td>
                      <td>
                        [
                          <template v-for="(reference, index) in metricConfig.metrics[metric].references">
                            <template v-if="index > 0">, </template>
                            <a :href="'/static/publications/' + reference.fileName" :title="reference.title" target="_blank">{{ index + 1 }}</a>
                          </template>
                        ]
                      </td>
                      <td>
                        <icon class="star" name="star" v-for="i in metricConfig.metrics[metric].evidence" :key="'evidence-star-' + metric + '-' + i"></icon><icon class="star-o" name="star-o" v-for="i in 5 - metricConfig.metrics[metric].evidence" :key="'evidence-star-o-' + metric + '-' + i"></icon>
                      </td>
                      <td>
                        <icon class="star" name="star" v-for="i in metricConfig.metrics[metric].relevance" :key="'relevance-star-' + metric + '-' + i"></icon><icon class="star-o" name="star-o" v-for="i in 5 - metricConfig.metrics[metric].relevance" :key="'relevance-star-o-' + metric + '-' + i"></icon>
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
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" role="tab" class="p-0">
            <b-btn variant="cat-two" block v-b-toggle.cat-two-accordion href="#">
              Select metrics: {{ metricConfig.categories[1].name }}
            </b-btn>
          </b-card-header>
          <b-collapse id="cat-two-accordion" visible role="tabpanel">
            <b-card-body>
              <p></p>
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
                    <tr>
                      <td class="text-center">
                        <b-form-checkbox class="metric-checkbox" :id="'metric-cb-' + metric" v-model="selected[metric]"></b-form-checkbox>
                      </td>
                      <td>
                        {{metricConfig.metrics[metric].name}}
                        <icon class="question-circle" name="question-circle" v-b-tooltip.hover :title="metricConfig.metrics[metric].description"></icon>
                      </td>
                      <td>
                        [
                          <template v-for="(reference, index) in metricConfig.metrics[metric].references">
                            <template v-if="index > 0">, </template>
                            <a :href="'/static/publications/' + reference.fileName" :title="reference.title" target="_blank">{{ index + 1 }}</a>
                          </template>
                        ]
                      </td>
                      <td>
                        <icon class="star" name="star" v-for="i in metricConfig.metrics[metric].evidence" :key="'evidence-star-' + metric + '-' + i"></icon><icon class="star-o" name="star-o" v-for="i in 5 - metricConfig.metrics[metric].evidence" :key="'evidence-star-o-' + metric + '-' + i"></icon>
                      </td>
                      <td>
                        <icon class="star" name="star" v-for="i in metricConfig.metrics[metric].relevance" :key="'relevance-star-' + metric + '-' + i"></icon><icon class="star-o" name="star-o" v-for="i in 5 - metricConfig.metrics[metric].relevance" :key="'relevance-star-o-' + metric + '-' + i"></icon>
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
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" role="tab" class="p-0">
            <b-btn variant="cat-three" block v-b-toggle.cat-three-accordion href="#">
              Select metrics: {{ metricConfig.categories[2].name }}
            </b-btn>
          </b-card-header>
          <b-collapse id="cat-three-accordion" visible role="tabpanel">
            <b-card-body>
              <p></p>
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
                    <tr>
                      <td class="text-center">
                        <b-form-checkbox class="metric-checkbox" :id="'metric-cb-' + metric" v-model="selected[metric]"></b-form-checkbox>
                      </td>
                      <td>
                        {{metricConfig.metrics[metric].name}}
                        <icon class="question-circle" name="question-circle" v-b-tooltip.hover :title="metricConfig.metrics[metric].description"></icon>
                      </td>
                      <td>
                        [
                          <template v-for="(reference, index) in metricConfig.metrics[metric].references">
                            <template v-if="index > 0">, </template>
                            <a :href="'/static/publications/' + reference.fileName" :title="reference.title" target="_blank">{{ index + 1 }}</a>
                          </template>
                        ]
                      </td>
                      <td>
                        <icon name="star" v-for="i in metricConfig.metrics[metric].evidence" :key="'evidence-star-' + metric + '-' + i"></icon><icon name="star-o" v-for="i in 5 - metricConfig.metrics[metric].evidence" :key="'evidence-star-o-' + metric + '-' + i"></icon>
                      </td>
                      <td>
                        <icon class="star" name="star" v-for="i in metricConfig.metrics[metric].relevance" :key="'relevance-star-' + metric + '-' + i"></icon><icon class="star-o" name="star-o" v-for="i in 5 - metricConfig.metrics[metric].relevance" :key="'relevance-star-o-' + metric + '-' + i"></icon>
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
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" role="tab" class="p-0">
            <b-btn variant="cat-four" block v-b-toggle.cat-four-accordion href="#">
              Select metrics: {{ metricConfig.categories[3].name }}
            </b-btn>
          </b-card-header>
          <b-collapse id="cat-four-accordion" visible role="tabpanel">
            <b-card-body>
              <p><!--
                These metrics indicate information loss for users with color vision deficiencies.
                The metrics are physiologically motivated and currently handle anomalous
                trichromacy and dichromacy. Evidence for the metric come from controlled experiments.
              --></p>
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
                    <tr>
                      <td class="text-center">
                        <b-form-checkbox class="metric-checkbox" :id="'metric-cb-' + metric" v-model="selected[metric]"></b-form-checkbox>
                      </td>
                      <td>
                        {{metricConfig.metrics[metric].name}}
                        <icon class="question-circle" name="question-circle" v-b-tooltip.hover :title="metricConfig.metrics[metric].description"></icon>
                      </td>
                      <td>
                        [
                          <template v-for="(reference, index) in metricConfig.metrics[metric].references">
                            <template v-if="index > 0">, </template>
                            <a :href="'/static/publications/' + reference.fileName" :title="reference.title" target="_blank">{{ index + 1 }}</a>
                          </template>
                        ]
                      </td>
                      <td>
                        <icon class="star" name="star" v-for="i in metricConfig.metrics[metric].evidence" :key="'evidence-star-' + metric + '-' + i"></icon><icon class="star-o" name="star-o" v-for="i in 5 - metricConfig.metrics[metric].evidence" :key="'evidence-star-o-' + metric + '-' + i"></icon>
                      </td>
                      <td>
                        <icon class="star" name="star" v-for="i in metricConfig.metrics[metric].relevance" :key="'relevance-star-' + metric + '-' + i"></icon><icon class="star-o" name="star-o" v-for="i in 5 - metricConfig.metrics[metric].relevance" :key="'relevance-star-o-' + metric + '-' + i"></icon>
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
    <div class="mt-2" v-if="display.progressBar">
      <ProgressBar />
    </div>
    <div class="mt-2" v-if="display.preview">
      <Preview />
    </div>
    <div class="mt-2" v-if="display.results">
      <Results />
    </div>
  </b-jumbotron>
</template>

<script>
import metricConfig from '../config/metrics'
import Results from './Results'
import ProgressBar from './ProgressBar'
import Preview from './Preview'

import { mapState } from 'vuex'

export default {
  data () {
    return {
      selected: {},
      form: {
        url: '',
        data: null,
        filename: null
      },
      metricConfig,
      fileTooLarge: false
    }
  },
  methods: {
    onSubmitURL (event) {
      // Prevent the event
      event.preventDefault()
      event.stopPropagation()

      // Fix URL, if needed
      this.fixURL()

      // Reset screenshot form
      this.resetForm(false, true, false)

      // Validate URL form
      let form = event.target
      if ((this.$store.state.wsError === false) && (form.checkValidity() === true)) {
        this.$store.commit('showMetrics')
      }
      form.classList.add('was-validated')
    },
    onSubmitScreenshot (event) {
      // Prevent the event
      event.preventDefault()
      event.stopPropagation()

      // Reset URL form
      this.resetForm(true, false, false)

      // Validate screenshot form
      let form = event.target
      if ((this.$store.state.wsError === false) && (form.checkValidity() === true && this.form.data !== null && this.form.filename !== null)) {
        document.querySelector('#screenshot-input-group').classList.remove('is-invalid') // Hack due to the use of Bootstrap's custom image upload
        this.$store.commit('showMetrics')
      } else {
        document.querySelector('#screenshot-input-group').classList.add('is-invalid') // Hack due to the use of Bootstrap's custom image upload
      }
      form.classList.add('was-validated')
    },
    onSubmit (event) {
      // Prevent the event
      event.preventDefault()
      event.stopPropagation()

      // Fix URL, if needed
      this.fixURL()

      // Validate URL and screenshot forms
      let urlForm = document.querySelector('#aim-url-form')
      let screenshotForm = document.querySelector('#aim-screenshot-form')
      if ((this.$store.state.wsError === false) && (urlForm.checkValidity() === true) || (screenshotForm.checkValidity() === true && this.form.data !== null && this.form.filename !== null)) {
        // Submit data
        this.$socket.sendObj({
          type: 'execute',
          url: this.form.url,
          data: this.form.data,
          filename: this.form.filename,
          metrics: this.selected
        })
        this.$store.commit('fetchResults', this.selected)

        // Reset URL and screenshot forms
        this.resetForm(true, true, true)
      } else {
        this.$store.commit('hideMetrics')
      }
    },
    onFileSelected (event) {
      let thisObj = this
      let file = event.target.files[0]
      document.querySelector('#screenshot-input ~ .custom-file-label').textContent = file.name // Hack due to a Vue.js's "bug"; filename doesn't get updated on the second upload

      // Reset URL form
      this.resetForm(true, false, false)

      // Validate file size
      if (this.isFileTooLarge(file)) {
        document.querySelector('#screenshot-input-group').classList.add('is-invalid') // Hack due to the use of Bootstrap's custom image upload
        this.form.data = null
        this.form.filename = null
        this.fileTooLarge = true
      } else {
        this.getBase64(file, function (e) {
          document.querySelector('#screenshot-input-group').classList.remove('is-invalid') // Hack due to the use of Bootstrap's custom image upload
          thisObj.form.data = e.target.result
          thisObj.form.filename = file.name
          thisObj.fileTooLarge = false
        })
      }
      document.querySelector('#aim-screenshot-form').classList.add('was-validated')
    },
    isFileTooLarge (file) {
      const MAX_FILE_SIZE = 3145728 // 3 MB

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
      this.form.url = this.form.url.toLowerCase()
      if (!!this.form.url && !/^https?:\/\//i.test(this.form.url)) {
        document.querySelector('#url-input').value = 'http://' + this.form.url // Hack due to a Vue's "bug"; updating the value of this.form.url doesn't pass validation even though its bound to the form input field
        this.form.url = 'http://' + this.form.url
      }
    },
    resetForm (url, screenshot, metrics) {
      if (url) {
        document.querySelector('#aim-url-form').classList.remove('was-validated')
        this.form.url = ''
      }

      if (screenshot) {
        document.querySelector('#screenshot-input').value = ''
        document.querySelector('#screenshot-input ~ .custom-file-label').textContent = 'Choose a PNG file...'
        document.querySelector('#screenshot-input-group').classList.remove('is-invalid')
        document.querySelector('#aim-screenshot-form').classList.remove('was-validated')
        this.form.data = null
        this.form.filename = null
        this.fileTooLarge = false
      }

      if (metrics) {
        this.selected = {}
      }
    }
  },
  components: {
    Results,
    ProgressBar,
    Preview
  },
  computed: mapState({
    display: state => state.display,
    wsError: state => state.wsError
  })
}
</script>
<style>
#aim-url-form input:-webkit-autofill {
    -webkit-box-shadow: 0 0 0 30px white inset;
}
#aim-form {
  margin-top: 1rem;  
}
#aim-form svg {
  position: relative;
  top: 2px;
}
h1 {
  margin-bottom: 0px;
}
.lead {
  margin-bottom: 2rem;
}
h2.text-muted {
  color: #aea697 !important;
  font-size: 1.5rem;
  margin-bottom: 20px;
}
.fa-icon.star,
.fa-icon.star-o,
.fa-icon.question-circle {
  color: #555555;
}
.btn-cat-one {
  color: #000;
  background-color: #eef0e9;
}

.btn-cat-two {
  color: #000;
  background-color: #fceac6;
}

.btn-cat-three {
  color: #000;
  background-color: #e6b790;
}

.btn-cat-four {
  color: #000;
  background-color: #a55f41;
}
.metric-checkbox.custom-control-inline {
  margin-right: 0;
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
#btn-url-proceed {
  border-top-right-radius: 0.25rem;
  border-bottom-right-radius: 0.25rem;  
}
#btn-screenshot-proceed {
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
#screenshot-input ~ .custom-file-label {
  color: #6D757D;
}
#screenshot-input ~ .custom-file-label::after {
  display: none;
}
.input-group.is-invalid ~ .invalid-feedback {
  display: block;
}
</style>

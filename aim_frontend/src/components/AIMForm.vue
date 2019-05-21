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
    <b-row v-if="validationError">
      <b-col>
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          <h4 class="alert-heading">Validation Error</h4>
          <hr>
          <p>
            <strong>Whoops!</strong> We are having some problems with your input, please try again with a different URL or screenshot.
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
              <b-btn id="btn-url-proceed" type="submit" variant="primary">Proceed</b-btn>
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
        <b-form id="aim-screenshot-form" class="needs-validation" novalidate @submit="onSubmitScreenshot">
          <b-input-group id="screenshot-input-group" prepend="Screenshot">
            <b-form-file id="screenshot-input" required placeholder="Choose a PNG file..." accept="image/png" @change="onFileSelected"></b-form-file>
            <b-input-group-append>
              <b-btn id="btn-screenshot-proceed" type="submit" variant="primary">Proceed</b-btn>
            </b-input-group-append>
          </b-input-group>
          <div v-if="fileTooLarge === false" class="invalid-feedback">
            Please provide a valid screenshot image.
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
import metricConfig from '../config/metrics'
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

      // Hide validation error
      this.$store.commit('hideValidationError')

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

      // Hide validation error
      this.$store.commit('hideValidationError')

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
    Preview,
    Summary
  },
  computed: mapState({
    display: state => state.display,
    wsError: state => state.wsError,
    validationError: state => state.validationError
  })
}
</script>

<style>
.jumbotron{
  position: relative;
}

#aim-url-form input:-webkit-autofill {
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
.fa-icon.star,
.fa-icon.star-o,
.fa-icon.question-circle {
  color: #555555;
}

.card-body {
    padding: 1rem;
}

.tablist .card-header div{
  position: relative;
  color: #fff;
  background-color: #7553a0;
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

.btn-cat-one {
  /* border-bottom: 5px solid #3891A6; */
} 

.btn-cat-two {
  /* border-bottom: 5px solid #E83151;*/
} 

.btn-cat-three {
  /* border-bottom: 5px solid #519E8A;  */
} 

.btn-cat-four {
  /* border-bottom: 5px solid #FFBF00; */
}

/* .metric-checkbox.custom-control-inline {
  margin-right: 0;
} */
/* .metric-checkbox.custom-control {
  padding-left: 1rem;
} */
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
    font-weight: normal;
    /* text-align: center; */
    font-size: 0.9rem;
    color: #333;
}

.custom-control {
  padding-left: 0;
}

.custom-control-label::before {
    position: absolute;
    left: auto;
}

.custom-control-label::after {
    position: absolute;
    left: auto;
}

</style>

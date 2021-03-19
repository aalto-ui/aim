<template lang="html">
  <div>
    <div class="component-section">
      <b-row>
        <b-col cols="12">
          <h2 class="component-title">Results</h2>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
        <template v-for="category in categories">
          <div class="category-outer" v-if="categoryVisible(category.id, category.metrics) !== -1">
            <div class="category-title rounded">
              <span class="fa">
                  <font-awesome-icon :icon="category.icon" />
              </span>
              <span class="title mb-3" :id="category.id">{{category.name}}</span>
            </div>

          <template v-for="metric in category.metrics" v-if="metricVisible(metric)">
            <b-card no-body class="mb-1">

              <b-card-header header-tag="header" class="p-0" :id="metrics[metric].id">
                <b-btn :variant="category.color" block v-b-toggle="`${category}-${metric}-collapse`">{{metrics[metric].name}}</b-btn>
              </b-card-header>
              <b-collapse visible :id="`${category}-${metric}-collapse`">
                <b-card-body>
                  <p>{{metrics[metric].description}}</p>
                  <p>
                    References: [
                    <template v-for="(reference, index) in metrics[metric].references">
                      <template v-if="index > 0">, </template>
                      <a :href="'/static/publications/' + reference.fileName" :title="reference.title" target="_blank">{{ index + 1 }}</a>
                    </template>
                    ]
                  </p>
                  <p>
                    Evidence: 
                    <span name="star" v-for="i in metrics[metric].evidence" :key="'res-evidence-star-' + metric + '-' + i">
                      <font-awesome-icon :icon="['fas', 'star']" />
                    </span><span name="star-o" v-for="i in 5 - metrics[metric].evidence" :key="'res-evidence-star-o-' + metric + '-' + i">
                      <font-awesome-icon :icon="['far', 'star']" />
                    </span>
                    <br />
                    Relevance: 
                    <span name="star" v-for="i in metrics[metric].relevance" :key="'res-relevance-star-' + metric + '-' + i">
                      <font-awesome-icon :icon="['fas', 'star']" />
                    </span><span name="star-o" v-for="i in 5 - metrics[metric].relevance" :key="'res-relevance-star-o-' + metric + '-' + i">
                      <font-awesome-icon :icon="['far', 'star']" />
                    </span>
                    
                  </p>

                  <template v-if="metrics[metric].visualizationType==='table'">
                    <b-table striped hover :items="results[metric]" :fields="resultTableFields" class="mt-4">
                      <template slot="result" slot-scope="data">
                        {{data.value.name}}
                        <template v-if="data.value.description">
                          <span v-b-tooltip.hover :title="data.value.description">
                          <font-awesome-icon :icon="['fas', 'question-circle']" />
                          
                          </span>
                        </template>
                      </template>
                      <template slot="evaluation" slot-scope="data">
                        <div class="scores" :id="data.item.id" v-if="metrics[metric].results[data.index].scores.length > 1" >
                          <div v-for="score in metrics[metric].results[data.index].scores" :key="score.description">
                           <div class="score" v-show="getJoudgement(score, data.item.value)" :class="score.judgment">
                              {{score.description}}
                              <template v-if="(score.icon[0]!=null)">
                                <font-awesome-icon :icon="score.icon" />
                              </template>
                           </div> 
                          </div>  
                        </div>
                        <div v-else :id="data.item.id">
                          <span>-</span>
                        </div>
                      </template> 
                      <template slot="show_details" slot-scope="row">
                        <b-btn v-b-modal="`${row.item.id}-modal`" variant="link">Show Details</b-btn>
                        <b-modal size="lg" :title="row.item.result.name" :id="`${row.item.id}-modal`" ok-only ok-title="Close">
                          <template v-if="row.item.result.description">
                            <p>{{ row.item.result.description }}</p>
                          </template>
                          <h4>Your score: {{ row.item.value }}</h4>
                          <hr />
                          <p>The histogram below shows the results of this metric for <em>Alexa top 500 global sites</em>. The list of sites was retrieved from <a href="https://www.alexa.com/topsites" target="_blank">https://www.alexa.com/topsites</a> on July 2, 2018 and their respective GUI designs were evaluated on December 18-19, 2018<sup>*</sup>.</p>
                          <img class="histogram" :src="'/static/histograms/' + row.item.id + '.png'" />
                          <p style="font-size: 11px;"><sup>*</sup>Country-specific, non-representative, and non-relevant sites were excluded from the list.</p>
                        </b-modal>
                      </template>
                    </b-table>
                  </template>

                  <template v-else-if="metrics[metric].visualizationType==='b64'" >

                    <template v-for="result in results[metric]">
                      <div class="b64" :id="result.id">
                        <h3 class="mt-2">{{ result.result.name }}</h3>
                        <p v-if="result.result.description">{{ result.result.description }}</p>
                        <img v-if="result.value !== ''" class="result-img" :src="'data:image/png;base64, ' + result.value" />
                        <p v-else class="alert alert-danger" role="alert">
                          <strong>Whoops!</strong> Our experimental visual search performance metric failed to evaluate your image, please try again with a different one.
                        </p>
                      </div>
                    </template>

                  </template>
                </b-card-body>
              </b-collapse>
            </b-card>
          </template>
          </div>
          </template>
          <b-btn variant="primary" class="mt-4" @click="resetForm()">Restart</b-btn>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
// import { mapState } from 'vuex'
import _ from 'lodash'
import metricConfig from '../../../metrics.json'

import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      categories: metricConfig.categories,
      metrics: metricConfig.metrics,
      resultTableFields: ['result', 'value', 'evaluation', 'show_details']
    }
  },
  computed: mapGetters({
    results: 'resultsFormatted',
    fetching: 'fetchingMetrics'
  }),
  methods: {
    categoryVisible (category, metrics) {
      return (
        _.findIndex(_.keys(this.results), (key) => metrics.includes(key))
      )
    },
    metricVisible (metric) {
      return this.results[metric]
    },
    resetForm () {
      this.$store.commit('resetState')
    },
    getJoudgement (score, value) {
      // console.log(`---- getJoudgement Res ----`)
      // console.log(score, value)
      if (score.range[0] === null) {
        return false
      }
      const min = score.range[0]
      const max = score.range[1]
      // console.log(value)
      return (
        min <= value && (max >= value || max === null)
      )
    }
  },
  components: {
  }
}
</script>

<style lang="scss" scoped>

.component-section{
  margin-bottom: 40px;
}

table thead th{
  word-break: break-word;
}

.category-outer{
  margin-bottom: 20px;
}

.category-title{
  position: relative;
  color: #fff;
  background-color: #7553a0;
  padding: 0px 10px 0px 10px;
  text-align: left;
  font-size: 1.8rem;
  font-weight: normal;
}

.category-title .fa{
  font-size: 3rem;
  margin-right: 5px;
  color: rgba(255, 255, 255, 0.3);
}

.score.good{
  color: #1e7e56;
}

.score.bad{
  color: #E83151;
}

.result-img {
  width: 100%;
  border: 1px solid lightgrey;
}

.btn-cat-one {
  color: #fff;
  background-color: #999;
}

.btn-cat-two {
  color: #fff;
  background-color: #999;
}

.btn-cat-three {
  color: #fff;
  background-color: #999;
}

.btn-cat-four {
  color: #fff;
  background-color: #999;
}

.card-body table .btn {
    padding: 0;
}

.histogram {
  max-width: 100%;
}

.b64{
  margin-bottom: 50px;
}
</style>

<template lang="html">
<div>
  <h2>Results</h2>
  <template v-for="category in categories">
    <div v-if="categoryVisible(category.id) !== -1">
      <h4 class="mb-3">{{category.name}}</h4>
      <template v-for="metric in category.metrics" v-if="metricVisible(metric)">
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-0">
            <b-btn :variant="category.color" block href="#" v-b-toggle="`${category}-${metric}-collapse`">{{metrics[metric].name}}</b-btn>
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
                Evidence: <icon name="star" v-for="i in metrics[metric].evidence" :key="'res-evidence-star-' + metric + '-' + i"></icon><icon name="star-o" v-for="i in 5 - metrics[metric].evidence" :key="'res-evidence-star-o-' + metric + '-' + i"></icon>
                <br />
                Relevance: <icon name="star" v-for="i in metrics[metric].relevance" :key="'res-relevance-star-' + metric + '-' + i"></icon><icon name="star-o" v-for="i in 5 - metrics[metric].relevance" :key="'res-relevance-star-o-' + metric + '-' + i"></icon>
              </p>
              <template v-if="metrics[metric].visualizationType === 'table'">
                <b-table striped hover :items="results[metric]" :fields="resultTableFields"  class="mt-4">
                  <template slot="result" slot-scope="data">
                    {{data.value.name}}
                    <template v-if="data.value.description">
                      <icon name="question-circle" v-b-tooltip.hover :title="data.value.description"></icon>
                    </template>
                  </template>
                  <template slot="show_details" slot-scope="row">
                    <b-btn v-if="metric !== 'pf8' && metric !== 'cp10'" v-b-modal="`${row.item.id}-modal`" variant="link">Show Details</b-btn>
                    <b-modal v-if="metric !== 'pf8' && metric !== 'cp10'" size="lg" :title="row.item.result.name" :id="`${row.item.id}-modal`" ok-only ok-title="Close">
                      <template v-if="row.item.result.description">
                        <p>{{ row.item.result.description }}</p>
                      </template>
                      <h4>Your score: {{ row.item.value }}</h4>
                      <hr />
                      <p>The histogram below shows the results of this metric for <em>Alexa top 500 global sites</em>. The list of sites was retrieved from <a href="https://www.alexa.com/topsites" target="_blank">https://www.alexa.com/topsites</a> on July 2, 2018 and their respective GUI designs were evaluated on July 6-8, 2018<sup>*</sup>.</p>
                      <img class="histogram" :src="'/static/histograms/' + row.item.id + '.png'" />
                      <p style="font-size: 11px;"><sup>*</sup>Country-specific, non-representative, and non-relevant sites were excluded from the list.</p>
                    </b-modal>
                  </template>
                </b-table>
              </template>
              <template v-else-if="metrics[metric].visualizationType === 'b64'">
                <template v-for="result in results[metric]">
                  <h3 class="mt-2">{{ result.result.name }}</h3>
                  <p v-if="result.result.description">{{ result.result.description }}</p>
                  <img v-if="result.value !== ''" class="result-img" :src="'data:image/png;base64, ' + result.value" />
                  <p v-else class="alert alert-danger" role="alert">
                    <strong>Whoops!</strong> Our experimental visual search performance metric failed to evaluate your image, please try again with a different one.
                  </p>
                  <hr />
                </template>
              </template>
            </b-card-body>
          </b-collapse>
        </b-card>
      </template>
    </div>
  </template>
  <b-btn variant="primary" class="mt-4" @click="resetForm()">Restart</b-btn>
</div>
</template>

<script>
// import { mapState } from 'vuex'
import _ from 'lodash'
import metricConfig from '../config/metrics'

import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      categories: metricConfig.categories,
      metrics: metricConfig.metrics,
      resultTableFields: ['result', 'value', 'show_details']
    }
  },
  computed: mapGetters({
    results: 'resultsFormatted',
    fetching: 'fetchingMetrics'
  }),
  methods: {
    categoryVisible (category) {
      return (
        _.findIndex(_.keys(this.results), (key) => key.match(new RegExp(category + '[0-9]+')))
      )
    },
    metricVisible (metric) {
      return this.results[metric]
    },
    resetForm () {
      this.$store.commit('resetState')
    }
  },
  components: {
  }
}
</script>

<style lang="scss">
.result-img {
  width: 100%;
  border: 1px solid lightgrey;
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
.histogram {
  max-width: 100%;
}
</style>

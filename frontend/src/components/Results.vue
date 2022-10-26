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
          <template v-for="(category, catIdx) in categories.filter(c => categoryVisible(c.id, c.metrics) !== -1)">
            <div :key="catIdx" class="category-outer">
              <div class="category-title rounded">
                <span class="fa">
                  <font-awesome-icon :icon="category.icon" />
                </span>
                <span :id="category.id" class="title mb-3">{{ category.name }}</span>
              </div>
              <template v-for="(metric, metricIdx) in category.metrics.filter(m => metricVisible(m))">
                <b-card :key="metricIdx" no-body class="mb-1">
                  <b-card-header :id="metrics[metric].id" header-tag="header" class="p-0">
                    <b-btn v-b-toggle="`${category.id}-${metric}-collapse`" :variant="category.color" block>{{ metrics[metric].name }}</b-btn>
                  </b-card-header>
                  <b-collapse :id="`${category.id}-${metric}-collapse`" visible>
                    <b-card-body>
                      <p>{{ metrics[metric].description }}</p>
                      <p>
                        References: [
                        <template v-for="(reference, index) in metrics[metric].references">
                          <template v-if="index > 0">, </template>
                          <a :key="index" :href="reference.url" :title="reference.title" target="_blank">{{ index + 1 }}</a>
                        </template>
                        ]
                      </p>
                      <p>
                        Evidence:
                        <span v-for="i in metrics[metric].evidence" :key="'res-evidence-star-' + metric + '-' + i" name="star">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span v-for="i in 5 - metrics[metric].evidence" :key="'res-evidence-star-o-' + metric + '-' + i" name="star-o">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                        <br>
                        Relevance:
                        <span v-for="i in metrics[metric].relevance" :key="'res-relevance-star-' + metric + '-' + i" name="star">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </span><span v-for="i in 5 - metrics[metric].relevance" :key="'res-relevance-star-o-' + metric + '-' + i" name="star-o">
                          <font-awesome-icon :icon="['far', 'star']" />
                        </span>
                      </p>
                      <b-table striped hover :items="results[metric]" :fields="resultTableFields" class="mt-4">
                        <template #cell(result)="data">
                          {{ data.item.result.name }}
                          <template v-if="data.item.result.description">
                            <span v-b-tooltip.hover :title="data.item.result.description">
                              <font-awesome-icon :icon="['fas', 'question-circle']" />
                            </span>
                          </template>
                        </template>
                        <template #cell(value)="data">
                          <template v-if="data.item.result.type!=='b64'">
                            {{ data.item.value }}
                          </template>
                        </template>
                        <template #cell(evaluation)="data">
                          <template v-if="data.item.result.type!=='b64'">
                            <div v-if="metrics[metric].results[data.index].scores && metrics[metric].results[data.index].scores.length > 1" :id="data.item.id" class="scores">
                              <div v-for="score in metrics[metric].results[data.index].scores" :key="score.id">
                                <div v-show="getJudgment(score, data.item.value)" :class="score.judgment" class="score">
                                  {{ score.description }}
                                  <template v-if="(score.icon[0]!=null)">
                                    <font-awesome-icon :icon="score.icon" />
                                  </template>
                                </div>
                              </div>
                            </div>
                            <div v-else :id="data.item.id">
                              -
                            </div>
                          </template>
                        </template>
                        <template #cell(show_details)="data">
                          <template v-if="data.item.result.type!=='b64'">
                            <b-btn v-b-modal="`${data.item.id}-modal`" variant="link">Show Details</b-btn>
                            <b-modal :id="`${data.item.id}-modal`" :title="data.item.result.name" size="lg" ok-only ok-title="Close">
                              <template v-if="data.item.result.description">
                                <p>{{ data.item.result.description }}</p>
                              </template>
                              <h4>Your score: {{ data.item.value }}</h4>
                              <hr>
                              <p>The histogram below shows the results of this metric for <em>Alexa Top 500 Global Sites</em>. The list of sites was retrieved from <a href="https://www.alexa.com/topsites" target="_blank">https://www.alexa.com/topsites</a> on April 9, 2021 and their respective GUI designs were evaluated on April 11-13, 2021<sup>*</sup>.</p>
                              <recorded-results-chart
                                v-if="chartData[data.item.id]"
                                :chart-data="chartData[data.item.id]"
                                :options="chartOptions[data.item.id]"
                                :width="null"
                                :height="null"
                                :plugins="chartPlugins[data.item.id]"
                              />
                              <p style="font-size: 11px;"><sup>*</sup>Country-specific, non-representative, and non-relevant sites were excluded from the list.</p>
                            </b-modal>
                          </template>
                        </template>
                        <template #row-details="data">
                          <img v-if="data.item.result.type==='b64'" class="result-img" :src="'data:image/png;base64, ' + data.item.value">
                        </template>
                      </b-table>
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
import _ from 'lodash'
import { RecordedResultsChart, fillData } from './RecordedResultsChart'
import metricConfig from '../../../metrics.json'

import { mapGetters } from 'vuex'

export default {
  components: { RecordedResultsChart },
  data () {
    return {
      categories: metricConfig.categories,
      metrics: metricConfig.metrics,
      resultTableFields: [
        {
          key: 'result',
          thStyle: 'width: 50%'
        },
        {
          key: 'value',
          thStyle: 'width: 15%'
        },
        {
          key: 'evaluation',
          thStyle: 'width: 15%'
        },
        {
          key: 'show_details',
          thStyle: 'width: 20%'
        }
      ],
      chartData: {},
      chartOptions: {},
      chartPlugins: {},
    }
  },
  computed: mapGetters({
    results: 'resultsFormatted',
    fetching: 'fetchingMetrics'
  }),
  mounted() {
    fillData({
      chartData: this.chartData,
      chartOptions: this.chartOptions,
      chartPlugins: this.chartPlugins,
      results: this.results,
    })
  },
  updated () {
    fillData({
      chartData: this.chartData,
      chartOptions: this.chartOptions,
      chartPlugins: this.chartPlugins,
      results: this.results,
    })
  },
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
    getJudgment (score, value) {
      if (score.range[0] === null) {
        return false
      }
      const min = score.range[0]
      const max = score.range[1]
      return (
        min <= value && (value <= max || max === null)
      )
    }
  }
}
</script>

<style lang="css" scoped>

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

.b64{
  margin-bottom: 50px;
}
</style>

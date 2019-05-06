<template lang="html">
  <div>
    <div class="component-section">
      <b-row>
        <b-col cols="12">
          <h2 class="component-title">Summary</h2>
        </b-col>
      </b-row>
    <b-row>
    <template v-for="category in categories" lang="html">
      <b-col cols="3">
        <div class="category-title rounded" :class="{ 'bg-primary' : categoryVisible(category.id) !== -1, 'bg-secondary' : categoryVisible(category.id) == -1, }">
          <div class="loader-bg" :class="{done: fetching}" v-if="!metricLoading()" >
            <div class="loader">Loading...</div>
          </div>
          
          <font-awesome-icon :icon="category.icon" />
          <!-- if any metrics are selected -->
          <div class="category-title-inner" v-if="categoryVisible(category.id) !== -1" >
            <a :href="'#'+category.id">
              <h4 class="title">{{category.name}}</h4>
            </a>
          </div>
          <!-- if no metrics is selected -->
          <div v-else class="category-title-inner" >
              <h4 class="title">{{category.name}}</h4>
              <div class="info" v-if="metricLoading()">
                <div class="msg">not selected</div>
              </div>
          </div>
        </div><!-- category-title -->

        <div class="metrics">
          <template v-for="metric in category.metrics" v-if="metricVisible(metric)" > 
            <div class="metric">
              <div class="title text-primary">
                <a :href="'#'+ metrics[metric].id" >
                  <div class="inner" :class="{'up': category.evaluation=='good','down': category.evaluation=='bad'}" >
                    {{metrics[metric].name}}
                    <!-- <font-awesome-icon :icon="['fas', 'angle-double-down']" /> -->
                    <font-awesome-icon :icon="['fas', 'angle-down']" />
                  </div>
                </a>
              </div>
              <template v-if="metrics[metric].visualizationType==='table'">
                <b-list-group class="results" v-for="result in metrics[metric].results">
                  <div class="info">
                    <a :href="'#'+ result.id" >
                      <div class="result-name">{{result.name}}</div>
                    </a>
                  </div>
                  <div class="scores" v-if="result.scores.length > 1">
                    <template v-for="score in result.scores">
                      <div class="score" v-show="getJoudgement(score, results[metric][0].value)"> 
                        <div class="description" :class="score.judgment" >
                           {{score.description}}
                           <template v-if="(score.icon[0]!='null')">
                            <font-awesome-icon :icon="score.icon" />
                          </template>
                        </div> 
                      </div>
                    </template> 
                  </div>
                </b-list-group>
              </template>

                <div v-if="metrics[metric].visualizationType==='b64'" class="results">
                  <div v-for="result in results[metric]" class="result">
                    <div class="info">
                      <a :href="'#'+ result.id" >
                        <span>{{result.result.name}}</span>
                      </a>
                    </div>
                    <img v-if="result.value !== ''" 
                          class="result-img" 
                          :src="'data:image/png;base64, ' + result.value" />
                  </div>
                </div>
                </div><!-- metric -->        
              </template>
            </div><!-- metrics -->

          </b-col>
        </template><!-- //// categories -->
      </b-row>
    </div><!-- //// summary-section -->
  </div>
</template>

<script>
import _ from 'lodash'
import { mapGetters } from 'vuex'
import metricConfig from '../config/metrics'

export default {
  data () {
    return {
      categories: metricConfig.categories,
      metrics: metricConfig.metrics,
      resultTableFields: ['result', 'value']
    }
  },
  computed: mapGetters({
    results: 'resultsFormatted',
    fetching: 'fetchingMetrics'
  }),
  methods: {
    categoryVisible (category) {
      // console.log(_.keys(this.results))
      return (
        _.findIndex(_.keys(this.results), (key) => key.match(new RegExp(category + '[0-9]+')))
      )
    },
    metricLoading () {
      // console.log(this.$store.state.fetchingCount)
      if (this.$store.state.fetchingCount === this.$store.state.fetchedCount) {
        return true
      }
      return false
    },
    metricVisible (metric) {
      return this.results[metric]
    },
    resetForm () {
      this.$store.commit('resetState')
    },
    getJoudgement (score, value) {
      // console.log(`---- getJoudgement ----`)
      const min = score.range[0]
      const max = score.range[1]
      // console.log(value)
      return (
        min < value && (max > value || max === null)
      )
    }
  },
  components: {
  }
}

</script>

<style lang="css" scoped>

.component-section{
  padding: 0 0 50px 0;
  margin: 50px 0px 20px;
  border-bottom: 1px solid #999;
}

.component-title{
  font-weight: 400;
}


/* ------------ category-title ------------  */

.category-title {
    position: relative;
    height: 100px;
    color: #fff;
    font-weight: 200;
    padding: 15px 20px 5px;
    overflow: hidden;
    line-height: normal;
}

.category-title .title{
    position: relative;
    /* letter-spacing: 0.02rem; */
    color: #fff;
    font-size: 1.6rem;
    font-weight: 200;
    /* height: 25px; */
    margin-top: 0;
    margin-bottom: 0;
}

.category-title .title a {
    color: #fff;
    text-decoration: none;
    background-color: none;
}

.category-title svg{
    font-size: 120px;
    position: absolute;
    top: 5px;
    right: 10px;
    color: rgba(255, 255, 255, 0.1);
}

.category-title .info {
    position: relative;
    /* height: 80px; */
}

.category-title .info .evalation {
    position: absolute;
    bottom: 10px;
    font-size: 3rem; 
    text-transform: capitalize;
}

.category-title .info .msg {
    margin-top: 25px;
    font-size: 1rem; 
    text-transform: capitalize;
}

/* ------------ metric ------------  */

.metrics{
    position: relative;
    width: 100%;
    background: none;
    padding: 10px 5px;
}

.metric{
    position: relative;
    width: 100%;
    background: none;
}

.metric .title{
  position: relative;
  background: none;
  font-size: 0.9rem;
  color: #555 !important;
  /* color: #7553a0 !important; */
  border-bottom: 2px solid #998bac;
  text-align: left;
}

.metric .title .inner{
  padding: 10px 25px 2px 0px;
  position: relative;
}

.metric .title .btn{
    border-radius: 0;
    border: none;
    background: none;
}

.metric .title .inner svg{
    font-size: 1rem;
    position: absolute;
    right: 0px;
    top: 14px;
    cursor: pointer;
    /* color: #7553a0 !important; */
    color: #555 !important;
}

.metric .title i{
    position: absolute;
    font-size: 1rem;
    right: 15px;
    top: 5px;
    cursor: pointer;
}

.metric .results{
  position: relative;
  padding: 10px 0px 0px 10px;
  background: none;
  font-size: 0.8rem;
  color: #555 !important;
  margin-left:10px;
  /* border-left: 2px solid #7553a0; */
  /* border-bottom: 2px solid #7553a0; */
  border-left: 2px solid #9d94a8;
  border-bottom: 2px solid #9d94a8;
  text-align: left; 
}

.metric .results .scores{
  position: absolute;
  right: 0px;
  width: 100px;
  text-align: right;
  font-size: .7rem;
}

.metric .results .score{
  position: relative;
  width: 100%;
}

.metric .results .score .description.good {
    color: #1e7e56;
}

.metric .results .score .description.bad{
    color: #E83151;
}

.metric .results .score .description svg{
    font-size: 1rem;
}

.metric .results .score .bar{
  width: 100%;
  height: 4px;
}

.metric .results .scale{
  position: absolute;
  color: #555;
  font-size: 0.5rem;
  top: 4px;
}

.metric .results .scale.min-line{
  right: -1rem;
}

.metric .results .scale.max-line{
  left: -1rem;
}

.metric .results .score:nth-of-type(1) .bar{
  background: #739ea3;
}

.metric .results .score:nth-of-type(2) .bar{
  background: rgb(160, 218, 0) ;
}

.metric .results .score:nth-of-type(3) .bar{
  background: #7553A0;
}

.metric .results .arrow{
  position: relative;
  top: -120%;
  z-index: 1000;
  text-align: center;
  border-radius: 50%;
}
.metric .results .arrow .description{
  font-size: 0.6rem;
  white-space: nowrap;
}

.metric .results .arrow:after {
  position: relative;
  content: '▼';
  color: #555;
  font-size: 0.5rem;
  top: -0.5rem;
}

.metric .results .info{
    color: #555;
    margin: 0 90px 10px 0;
}

.metric .results .info .value{
    font-size: .8rem;
}

.metric .results .info .result-name{
    font-size: .7rem;
}

.metric .result img{
  width: 100%;
}

.spacer{
  width: 100%;
  height: 1px;
}
/* ------------ loader ------------ */

.loader-bg{
  background: #999;
    position: absolute;
    width: 100%;
    height: 125px;
    top: 0;
    left: 0;
    z-index: 1;
    opacity: 0.6;
}

.loader,
.loader:before,
.loader:after {
  background: #ffffff;
  -webkit-animation: load1 1s infinite ease-in-out;
  animation: load1 1s infinite ease-in-out;
  width: 1em;
  height: 4em;
}
.loader {
  color: #ffffff;
  text-indent: -9999em;
  margin: 40px auto;
  position: relative;
  font-size: 11px;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-animation-delay: -0.16s;
  animation-delay: -0.16s;
}
.loader:before,
.loader:after {
  position: absolute;
  top: 0;
  content: '';
}
.loader:before {
  left: -1.5em;
  -webkit-animation-delay: -0.32s;
  animation-delay: -0.32s;
}
.loader:after {
  left: 1.5em;
}

@-webkit-keyframes load1 {
  0%,
  80%,
  100% {
    box-shadow: 0 0;
    height: 4em;
  }
  40% {
    box-shadow: 0 -2em;
    height: 5em;
  }
}
@keyframes load1 {
  0%,
  80%,
  100% {
    box-shadow: 0 0;
    height: 4em;
  }
  40% {
    box-shadow: 0 -2em;
    height: 5em;
  }
}
</style>

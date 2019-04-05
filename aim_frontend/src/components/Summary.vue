<template lang="html">
<div>
<template v-for="category in categories" lang="html">
  <div v-if="categoryVisible(category.id) !== -1">
    <div class="topic-title bg-primary rounded">
      <font-awesome-icon icon="palette" />
      <h4 class="title">{{category.name}}</h4>
      <div class="info">
        <!-- <span class="score"></span> -->
        <p class="evalation up">GOOD</p>
      </div>
    </div><!-- topic Title -->

    <template v-for="metric in category.metrics" v-if="metricVisible(metric)">
      <div class="metric">
        <div class="title text-primary">
          <div class="inner">
            <!-- 結果のマトリック名 -->
            <!-- <b-card-header header-tag="header" class="p-0"> -->
              <b-btn :variant="category.color" block href="#" v-b-toggle="`${category}-${metric}-collapse`">{{metrics[metric].name}}</b-btn>
            <!-- </b-card-header> -->
          </div>
        </div>
    
        <b-collapse visible :id="`${category}-${metric}-collapse`">
          <!-- <b-card-body> -->
          <template v-if="metrics[metric].visualizationType === 'table'">
              <b-table :items="results[metric]" :fields="resultTableFields"  class="mt-4">
                <template slot="result" slot-scope="data">
                  {{data.value.name}}
                  <!-- マトリックの少トピックの名前 -->
                </template>
              </b-table>
          </template>
        </b-collapse>
      </div><!-- metric -->        
    </template>
  </div>
</template><!-- //// categories -->
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

<style lang="css">
.topic-title {
    position: relative;
    height: 125px;
    color: #fff;
    font-weight: 200;
    padding: 15px 20px 5px;
    overflow: hidden;
    line-height: normal;
}

h4.title {
    letter-spacing: 0.02rem;
    font-size: 1.1rem;
    font-weight: normal;
    height: 25px;
    margin-top: 0;
    margin-bottom: 0;
}

.topic-title .info {
    position: relative;
    height: 80px;
}

.topic-title .info .score {
    position: relative;
    font-size: 72px;
    margin-right: 10px;
}

.topic-title .info .evalation {
    position: absolute;
    bottom: 20px;
    right: 60px;
}

.topic-title .info .evalation.up::after {
    color: greenyellow;
    content: "▲";
    font-size: 1.2rem;
    margin-left: 5px;
}

.topic-title .far, .topic-title .fas, .topic-title .font-awesome-icon {
    font-size: 150px;
    position: absolute;
    top: 5px;
    right: 10px;
    color: rgba(255, 255, 255, 0.2);
}

.metric{
    position: relative;
    width: 100%;
    background: #fff;
    min-height: 60px;
    border-bottom: #bbb 1px solid;
    border-right: #ccc 1px solid;
    /* margin-top: 5px; */
    /* padding-bottom: 16px; */
    background: #E8E8F8;
}

.metric .title,
.btn-cat-one,
.btn-cat-two,
.btn-cat-three,
.btn-cat-four {
    background: #fff !important;
    font-size: 0.8rem;
    /* color: #555 !important; */
    color: #7553a0 !important;
    border-bottom: 1px solid #ccc;
    /* padding: 5px 10px; */
    text-align: left;
}

.metric .title .btn{
    border-radius: 0.25rem;
    border: none;
}

.metric .title::after{
    font-family: "Font Awesome 5 Free";
    content: "\f150";
    font-size: 1rem;
    position: absolute;
    right: 10px;
    top: 2px;
    cursor: pointer;
}

.metric .title i{
    position: absolute;
    font-size: 1rem;
    right: 15px;
    top: 5px;
    cursor: pointer;
}

.metric .info{
    color: #555;
    /* font-size: 0.6rem; */
    /* width: 50%; */
    /* margin-bottom: 6px; */
    position: relative;
    padding: 10px 10px 0px 10px;
    /* float: left; */
}

.metric .info-l{
    color: #555;
    font-size: 0.6rem;
    padding-right: 0px;
    position: relative;
    float: left;
}

.metric .info-l .evalation{
    color: #fff;
    position: relative;
    left: 0px;
    margin-top: 5px;
    padding: 3px 10px;
    width: 70px;
}

.metric .info-r .evalation{
    color: #fff;
    position: absolute;
    right: 0px;
    text-align: right;
    /* margin-top: 5px; */
    /* margin-right: 0px; */
    padding: 3px 10px;
    width: 70px;
}

.metric .evalation.down::after{
    content: '▼';
    color: red;
    font-size: .7rem;
    margin-left: 5px;
}

.metric .evalation.up::after{
    color: Lime;
    content: '▲';
    font-size: .7rem;
    margin-left: 5px;
}



.metric .info-r{
    color: #555;
    font-size: 0.6rem;
    position: relative;
    float: left;
}

.metric .info-l .result{
    padding: 10px 20px;
}

.metric .info-l .result>em{
    font-size: 1.2rem;
    font-style: normal;
    margin-right: 5px;
}

.metric .graf{
    padding: 10px 10px 0px 0px;
    color: #555555;
    font-size: .75rem;
}
</style>

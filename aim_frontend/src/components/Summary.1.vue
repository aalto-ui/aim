<template lang="html">

  <div>
    <div class="summary-section">
      <b-row>
        <b-col cols="12">
          <h2 class="components-title">Summary</h2>
        </b-col>
      </b-row>
      <b-row>

        <template v-for="category in categories" lang="html">
          <b-col v-if="categoryVisible(category.id) !== -1" cols="3">

            <div class="topic-title bg-primary rounded">
              <font-awesome-icon :icon="category.icon" />
              <h4 class="title">{{category.name}}</h4>
              <div class="info">
                <!-- <span class="score"></span> -->
                <div class ="evalation" :class="{'up': category.evaluation=='good','down': category.evaluation=='bad'}" >{{category.evaluation}}</div>
              </div>
            </div><!-- topic Title -->

            <div class="metrics">
              <template v-for="metric in category.metrics" v-if="metricVisible(metric)">
                <div class="metric">
                  <div class="title text-primary" href="#">
                    <div class="inner" :class="{'up': category.evaluation=='good','down': category.evaluation=='bad'}">
                      {{metrics[metric].name}}
                    </div>
                  </div>
                </div><!-- metric -->        
              </template>
            </div><!-- metrics -->

          </b-col> 
          <b-col v-else cols="3">
            <div class="topic-title bg-secondary rounded">
              <font-awesome-icon :icon="category.icon" />
              <h4 class="title">{{category.name}}</h4>
              <div class="info">
                <div class="msg">not selected</div>
              </div>
            </div><!-- topic Title -->
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

<style lang="css" scoped>

.summary-section{
  margin: 100px 0px;
}

.topic-title {
    position: relative;
    height: 125px;
    color: #fff;
    font-weight: 200;
    padding: 15px 20px 5px;
    overflow: hidden;
    line-height: normal;
}

.topic-title .title {
    letter-spacing: 0.02rem;
    font-size: 1.1rem;
    font-weight: normal;
    height: 25px;
    margin-top: 0;
    margin-bottom: 0;
}

.topic-title svg{
    font-size: 150px;
    position: absolute;
    top: 5px;
    right: 10px;
    color: rgba(255, 255, 255, 0.1);
}

.topic-title .info {
    position: relative;
    height: 80px;
}

.topic-title .info .evalation {
    position: absolute;
    bottom: 10px;
    /* left: 60px; */
    font-size: 3rem; 
    text-transform: capitalize;
    /* text-transform: uppercase; */
    /* font-weight: bolder; */
}

.topic-title .info .msg {
    position: absolute;
    /* right: 0px; */
    bottom: 15px;
    font-size: 1.5rem; 
    text-transform: capitalize;
}

.topic-title .info .evalation.up::after {
    color: greenyellow;
    content: "▲";
    font-size: 1.2rem;
    margin-left: 15px;
}

.topic-title .info .evalation.down::after {
    content: '▼';
    color: #E83151;
    font-size: 1.2rem;
    margin-left: 15px;
}

/* .metric .evalation.down::after{
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
} */

/* .topic-title .info .score {
    position: relative;
    font-size: 72px;
    margin-right: 10px;
} */

.metrics{
    position: relative;
    width: 100%;
    background: none;
    /* border-bottom: #bbb 1px solid; */
    /* border-right: #ccc 1px solid; */
    /* margin-top: 5px; */
    padding: 10px 5px;
    /* background: #E8E8F8; */
}

.metric{
    position: relative;
    width: 100%;
    background: none;
}

.metric .title,
.btn-cat-one,
.btn-cat-two,
.btn-cat-three,
.btn-cat-four {
  position: relative;
  background: none;
  font-size: 0.8rem;
  color: #555 !important;
  color: #7553a0 !important;
  border-bottom: 2px solid #7553a0;
  text-align: left;
}

.metric .title .inner{
  padding: 10px 0px 2px 30px;
  position: relative;
}

.metric .title .btn{
    border-radius: 0;
    border: none;
    background: none;
}

.metric .title .inner::before{
    font-family: "Font Awesome 5 Free";
    content: "\f058";
    font-size: 1rem;
    position: absolute;
    left: 5px;
    bottom: 0px;
    cursor: pointer;
    color: #7553a0 !important;
}

.metric .title .inner::after{
    font-family: "Font Awesome 5 Free";
    content: "\f150";
    font-size: 1rem;
    position: absolute;
    right: 10px;
    bottom: 0px;
    cursor: pointer;
    color: #7553a0 !important;
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

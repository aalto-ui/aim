<template lang="html">
<div>
  <template v-for="category in categories">
    <div v-if="categoryVisible(category.id) !== -1">
      <div class="row">

      <div class="col-md-4">
          <div class="topic-title bg-primary rounded">
            <font-awesome-icon icon="palette" />
            <h4 class="title">{{category.name}}</h4>
            <div class="info">
              <!-- <span class="score"></span> -->
              <p class="evalation up">GOOD</p>
            </div>
          </div>
      </div> 
      <!-- col-md-4 -->

      
      <template v-for="metric in category.metrics" v-if="metricVisible(metric)">
        <div class="col-md-4">
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
            <!-- <template slot="result" slot-scope="data"> -->
              <!-- <div>
                {{data.value.name}} test
              </div> -->
            <!-- </template> -->
            
            <!-- <div class="row">
              <div class="info-l col-6">
                <div class="result"><em>396090</em> byte</div>
              </div>
              <div class="info-r col-6">
                <div class="graf">
                  <div class="result-arrow" style="left:20px;">▼</div>
                  <div class="progress" style="height: 2px;">

                    <div class="progress-bar" role="progressbar"
                      style="width: 60%; position: relative; left: 10%;" aria-valuenow="25" aria-valuemin="0"
                      aria-valuemax="100"></div>
                  </div>
                  <div class="optimum">opt</div>
                  <div class="optimum">100000 - 900000</div>
                </div>
              </div>
            </div>
            <div class="spacer-1"></div> -->
            <!-- </b-card-body> -->
          </b-collapse>
        </div><!-- metric -->

        <!-- <b-card no-body class="mb-1"> -->
          <!-- <b-card-header header-tag="header" class="p-0">
            <b-btn :variant="category.color" block href="#" v-b-toggle="`${category}-${metric}-collapse`">{{metrics[metric].name}}</b-btn>
          </b-card-header> -->
          <!-- <b-collapse visible :id="`${category}-${metric}-collapse`"> -->
            <!-- <b-card-body> -->
              <!-- <p>{{metrics[metric].description}}</p> -->
              <!-- <p>
                References: [
                <template v-for="(reference, index) in metrics[metric].references">
                  <template v-if="index > 0">, </template>
                  <a :href="'/static/publications/' + reference.fileName" :title="reference.title" target="_blank">{{ index + 1 }}</a>
                </template>
                ]
              </p> -->
              <!-- <p>
                Evidence: <icon name="star" v-for="i in metrics[metric].evidence" :key="'res-evidence-star-' + metric + '-' + i"></icon><icon name="star-o" v-for="i in 5 - metrics[metric].evidence" :key="'res-evidence-star-o-' + metric + '-' + i"></icon>
                <br />
                Relevance: <icon name="star" v-for="i in metrics[metric].relevance" :key="'res-relevance-star-' + metric + '-' + i"></icon><icon name="star-o" v-for="i in 5 - metrics[metric].relevance" :key="'res-relevance-star-o-' + metric + '-' + i"></icon>
              </p> -->
              <!-- <template v-if="metrics[metric].visualizationType === 'table'"> -->
                <!-- <b-table hover :items="results[metric]" :fields="resultTableFields"> -->
                  <!-- <template slot="result" slot-scope="data"> -->
                    <!-- {{data.value.name}} -->
                    <!-- <template v-if="data.value.description">
                      <icon name="question-circle" v-b-tooltip.hover :title="data.value.description"></icon>
                    </template> -->
                  <!-- </template> -->
                  <!-- <template slot="show_details" slot-scope="row">
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
                  </template> -->
                <!-- </b-table> -->
              <!-- </template> -->

              <!-- <template v-else-if="metrics[metric].visualizationType === 'b64'"> -->
                <!-- <template v-for="result in results[metric]"> -->
                  <!-- <h3 class="mt-2">{{ result.result.name }}</h3>
                  <p v-if="result.result.description">{{ result.result.description }}</p>
                  <img v-if="result.value !== ''" class="result-img" :src="'data:image/png;base64, ' + result.value" />
                  <p v-else class="alert alert-danger" role="alert">
                    <strong>Whoops!</strong> Our experimental visual search performance metric failed to evaluate your image, please try again with a different one.
                  </p> -->
                  <!-- <hr /> -->
                <!-- </template> -->
              <!-- </template> -->
            <!-- </b-card-body> -->
          <!-- </b-collapse> -->
        <!-- </b-card> -->
        </div><!-- col-mb-4 each result-->
      </template>
      <!-- //// template metricVisible -->
      </div><!-- ////row -->
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
    color: #555 !important;
    /* padding: 5px 10px; */
    text-align: left;
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

import { Bar, mixins } from 'vue-chartjs'
import metricsConfig from '../../../metrics.json'
import recordedResults from '../assets/results.json'

const intl = new Intl.NumberFormat('en-US', { notation: 'compact' })

export const RecordedResultsChart = {
  extends: Bar,
  mixins: [mixins.reactiveProp],
  props: ['options'],
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}

export const fillData = ({
  chartData,
  chartOptions,
  chartPlugins,
  results,
}, noBins=20) => {
  // Styling constants
  const fontSize = 14
  const padding = 6

  Object.keys(results).forEach(metricName => {
    const metricId = `${metricName}_0`
    const metricData = results[metricName][0]
    const metricRange = metricsConfig.metrics[metricName].results[0].scores[1].range
    const data = recordedResults.map(e => e[metricId])
    const maxValue = Math.max(...data, metricData.value)

    // Compute bin size
    let binSize = maxValue / noBins
    const maxF = Math.ceil(Math.log10(binSize)) + 1
    binSize =
      maxValue > 1 && maxF > 1
        ? new Array(maxF)
            .fill(0)
            .map((_, i) => maxF - i)
            .map((i) => Math.ceil(binSize / 10 ** i) * 10 ** i)
            .map((i) => [
              i,
              (noBins - 1) * i < maxValue && noBins * i > maxValue,
            ])
            .filter((i) => i[1] === true)[0][0]
        : maxValue / noBins;

    // Compute data frequency bins
    const valueIndex = Math.floor(metricData.value / binSize)
    const bins = data.map(e => Math.floor(e / binSize)).reduce((acc, curr) => {
      acc[curr] += 1
      return acc
    }, new Array(noBins + 1).fill(0))

    // Max y axis height
    const factor = Math.floor(Math.log10(Math.max(...bins)))
    const yAxisMax = (Math.floor(Math.max(...bins) / (10 ** factor)) + 2) * (10 ** factor)

    chartData[metricId] = {
      labels: bins.map((_, i) => intl.format(binSize * i)),
      datasets: [{
        backgroundColor: bins.map((_, i) => i === valueIndex ? '#7553A0' : "rgba(0, 0, 0, 0.1)"),
        categoryPercentage: 1.0,
        barPercentage: 0.8,
        data: bins,
      }]
    }

    chartOptions[metricId] = {
      lineAtIndex: [2,4,8],
      responsive: true,
      legend: { display: false },
      tooltips: { enabled: false },
      scales: {
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: metricData.result.name,
            fontSize,
          },
          ticks: {
            min: 0,
            max: noBins,
            stepSize: binSize,
            maxTicksLimit: Math.floor(noBins / 2),
            maxRotation: 0,
            labelOffset: -20
          },
          gridLines: {
            drawOnChartArea: false,
            offsetGridLines: true
          }
        }],
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: "Frequency",
            fontSize,
          },
          ticks: { max: yAxisMax },
          gridLines: { drawOnChartArea: false },
        }],
      },
    }

    chartPlugins[metricId] = [{
      id: 'dataset-label-plugin',
      afterDatasetsDraw: (chart) => {
        const ctx = chart.ctx
        const meta = chart.getDatasetMeta(0)

        ctx.textAlign = 'center'
        ctx.font = `${fontSize}px "Helvetica Neue", "Helvetica", "Arial", sans-serif`

        if (!meta.hidden) {
          meta.data.forEach((element, idx) => {
            if (idx == valueIndex) {
              const position = element.tooltipPosition()
              ctx.fillText(intl.format(metricData.value), position.x, position.y - (fontSize / 2) - padding)
            }
          })
        }
      }
    }, {
      id: 'dataset-quantile-plugin',
      afterDatasetsDraw: (chart) => {
        const rangeToCoordinate = (min, max, v) => min + v * (max - min)

        const ctx = chart.ctx
        const h = ctx.canvas.clientHeight
        const w = ctx.canvas.clientWidth

        ctx.textAlign = 'center'
        ctx.font = `${fontSize - 2}px "Helvetica Neue", "Helvetica", "Arial", sans-serif`

        // the limits [w, h] are [(52, w - 40), (0, h - 55)]
        const limitLow = rangeToCoordinate(52, w - 40, metricRange[0] / maxValue)
        const limitHigh = rangeToCoordinate(52, w - 40, metricRange[1] / maxValue)
        const drawQuartile = (limit, text, value) => {
          ctx.beginPath()
          ctx.moveTo(limit, 40)
          ctx.lineTo(limit, h - 55)
          ctx.strokeStyle="#7553A0"
          ctx.stroke()
          ctx.fillText(text, limit, 15)
          ctx.fillText(value, limit, 30)
        }

        // draw inferior limit
        drawQuartile(limitLow, "1st quartile", intl.format(metricRange[0]))
        // draw superior limit
        drawQuartile(limitHigh, "3rd quartile", intl.format(metricRange[1]))
      },
    }]
  })
}

export default { RecordedResultsChart, fillData }

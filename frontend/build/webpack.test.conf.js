// This is the webpack config used for unit tests.

const ESLintPlugin = require('eslint-webpack-plugin')
const { VueLoaderPlugin } = require('vue-loader')
const webpack = require('webpack')
const { merge } = require('webpack-merge')
const utils = require('./utils')
const baseConfig = require('./webpack.base.conf')

const webpackConfig = merge(baseConfig, {
  mode: 'testing',
  // use inline sourcemap for karma-sourcemap-loader
  module: {
    rules: utils.styleLoaders()
  },
  devtool: '#inline-source-map',
  resolveLoader: {
    alias: {
      // necessary to to make lang="scss" work in test when using vue-loader's ?inject option
      // see discussion at https://github.com/vuejs/vue-loader/issues/724
      'scss-loader': 'sass-loader'
    }
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': require('../config/test.env')
    }),
    new VueLoaderPlugin(),
    new ESLintPlugin({
      extensions: ['js', 'vue'],
      files: ['src', 'test'],
      formatter: require('eslint-friendly-formatter')
    }),
  ]
})

// no need for app entry during tests
delete webpackConfig.entry

module.exports = webpackConfig

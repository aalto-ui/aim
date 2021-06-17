// see http://vuejs-templates.github.io/webpack for documentation.
const path = require('path')

const env = {
  NODE_ENV: process.env.NODE_ENV ? `"${process.env.NODE_ENV}"` : '"development"',
  WS_URL: process.env.WS_URL ? `"${process.env.WS_URL}"` : '"ws://localhost:8888/"',
}

module.exports = {
  env,
  build: {
    index: path.resolve(__dirname, '../dist/index.html'),
    assetsRoot: path.resolve(__dirname, '../dist'),
    assetsSubDirectory: 'static',
    assetsPublicPath: '/',
    productionSourceMap: true,
    productionGzipExtensions: ['js', 'css'],
  },
  dev: {
    port: 8080,
    autoOpenBrowser: true,
    assetsSubDirectory: 'static',
    assetsPublicPath: '/',
    proxyTable: {},
    // CSS Sourcemaps off by default because relative paths are "buggy"
    // with this option, according to the CSS-Loader README
    // (https://github.com/webpack/css-loader#sourcemaps)
    // In our experience, they generally work as expected,
    // just be aware of this issue when enabling this option.
    cssSourceMap: false
  }
}

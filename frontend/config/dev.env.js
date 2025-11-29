'use strict'
// const merge = require('webpack-merge')
const { merge } = require('webpack-merge');
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  BASE_URL: '"http://ruaraka.localhost:8000"'
})

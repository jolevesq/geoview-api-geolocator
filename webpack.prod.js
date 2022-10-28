const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');

const config = {
  mode: 'production',
  optimization: {
    minimizer: [],
  },
  plugins: [],
};

module.exports = merge(common, config);

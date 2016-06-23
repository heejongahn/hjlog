var path = require('path');
var webpack = require('webpack');

var ExtractTextPlugin = require('extract-text-webpack-plugin');

var rootAssetPath = './hjlog/assets';
var absRootAssetPath = path.resolve(rootAssetPath);

var plugins = [
  new ExtractTextPlugin('style.css'),
];

module.exports = {
  entry: {
    bundle: rootAssetPath + '/js/hjlog.js',
  },
  output: {
    path: 'hjlog/static/build',
    publicPath: '/static/build/',
    filename: '[name].js',
  },
  resolve: {
    extensions: ['', '.js', '.css']
  },
  module: {
    loaders: [
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract('style-loader', ['css-loader', 'sass-loader?outputStyle=nested'])
      },
      /* Font-Awesome */
      { test: /\.(woff2?|svg|jpe?g|png|gif|ico)$/, loader: 'url?limit=10000' },
      { test: /\.(ttf|eot)$/, loader: 'file' }
    ]
  },
  plugins: plugins
};

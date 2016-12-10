import path from 'path'
import webpack from 'webpack'

import ExtractTextPlugin from 'extract-text-webpack-plugin'
import autoprefixer from 'autoprefixer'

const rootAssetPath = './hjlog/assets';
const absRootAssetPath = path.resolve(rootAssetPath);

const plugins = [
  new ExtractTextPlugin('style.css')
];

export default {
  entry: {
    bundle: `${rootAssetPath}/js/hjlog.js`,
  },
  output: {
    path: 'hjlog/static/build',
    publicPath: '/static/build/',
    filename: '[name].js',
  },
  resolve: {
    extensions: ['', '.js', '.css', 'styl']
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        include: [
          path.resolve(`${rootAssetPath}/js`)
        ],
        loader: 'babel',
        query: { presets: ['es2015'] }
      },
      {
        test: /\.styl$/,
        loader: ExtractTextPlugin.extract('style-loader', ['css!postcss!stylus'])
      },
      /* Font-Awesome */
      { test: /\.(woff2?|svg|jpe?g|png|gif|ico)$/, loader: 'url?limit=10000' },
      { test: /\.(ttf|eot)$/, loader: 'file' }
    ]
  },
  plugins: plugins,
  postcss: [ autoprefixer() ]
};

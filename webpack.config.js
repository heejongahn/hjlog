var path = require('path');
var webpack = require('webpack');

var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

var rootAssetPath = './hjlog/static';
var absRootAssetPath = path.resolve(rootAssetPath);

var plugins = [
  new ExtractTextPlugin('[name].[hash].css'),
  new ManifestRevisionPlugin(path.join('.', 'manifest.json'), {
    rootAssetPath: rootAssetPath,
    ignorePaths: [/.DS_Store$/, '/css', '/js', '/public']
  })
];

if (process.env.WEBPACK === 'release') {
  plugins.push(new webpack.optimize.UglifyJsPlugin({ compress: { warnings: false } }));
}

module.exports = {
  entry: {
    bundle: rootAssetPath + '/js/hjlog.js',
    style: rootAssetPath + '/css/hjlog.scss'
  },
  output: {
    path: 'hjlog/static/public',
    publicPath: '/static/public/',
    filename: '[name].[hash].js',
  },
  resolve: {
    root: [absRootAssetPath + '/js', absRootAssetPath + '/css'],
    extensions: ['', '.js', '.css']
  },
  module: {
    loaders: [
      {
        test: /\.(jpe?g|png|gif|svg([\?]?.*))$/i,
        loaders: [
          'file?context=' + rootAssetPath + '&name=[path][name].[hash].[ext]',
          'image?bypassOnDebug&optimizationLevel=7&interlaced=false'
        ]
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader')
      },
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract('style-loader', ['css-loader', 'sass-loader?outputStyle=nested'])
      }
    ]
  },
  plugins: plugins
};

var path = require('path');

var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

var rootAssetPath = './hjlog/static';
var jsPath = rootAssetPath + '/js/hjlog.js';

module.exports = {
    entry: {
        app_js: rootAssetPath + '/js/hjlog.js'
    },
    output: {
        path: 'hjlog/static/build',
        publicPath: '/static/build/',
        filename: '[name].[hash].js',
    },
    resolve: {
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
            }
        ]
    },
    plugins: [
        new ManifestRevisionPlugin(path.join('.', 'manifest.json'), {
            rootAssetPath: rootAssetPath,
            ignorePaths: [/.DS_Store$/, '/css', '/js', '/build']
        })
    ]
};

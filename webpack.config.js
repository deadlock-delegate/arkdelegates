const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  context: path.resolve(__dirname, 'static-source/app'),
  entry: ['./js/main.js', './css/main.scss'],
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'main.js'
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            'css-loader',
            {
              loader: 'sass-loader',
              options: {
                includePaths: [
                  path.resolve(__dirname, 'node_modules/foundation-sites/scss'),
                ]
              }
            }
          ]
        }),
      },
      {
        test: /\.(eot|svg|ttf|woff|woff2)(\?\S*)?$/,
        loader: 'file-loader',
      }
    ]
  },
  resolve: {
    modules: [
      path.resolve(__dirname, 'node_modules/foundation-sites/scss'),
    ],
  },
  plugins: [
    new ExtractTextPlugin('style.css')
  ],
  externals: [
    'foundation-sites'
  ],
};

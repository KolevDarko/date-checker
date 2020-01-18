const path = require("path");
var BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  context: __dirname,

  entry: {
    bundle: "./frontend/src/index.js"
  },
  mode: 'development',
  output: {
    filename: "[name].js",
    path: path.resolve("./frontend/bundles")
  },

  devtool: "source-map",

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new MiniCssExtractPlugin({
      filename: '../../datecheck/static/css/mystyles.css'
    }),
  ],

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: [
          /node_modules/
        ],
        use: [
          { loader: "babel-loader" }
        ]
      },
      {
      test: /\.scss$/,
      use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader'
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
            }
          }
        ]
    }]
  }
};

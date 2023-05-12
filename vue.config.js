const { defineConfig } = require('@vue/cli-service')
const ComponentsPlugin = require('unplugin-vue-components/webpack');
const NutUIResolver = () => {
  return (name) => {
    if (name.startsWith('Nut')) {
      const partialName = name.slice(3);
      return {
        name: partialName,
        from: '@nutui/nutui',
        sideEffects: `@nutui/nutui/dist/packages/${partialName.toLowerCase()}/style`
      }
    }
  }
}

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      ComponentsPlugin({
        resolvers: [NutUIResolver()],
      }),
    ],
  },
  css: {
    loaderOptions: {
      scss: {
        additionalData: `@import "@nutui/nutui/dist/styles/variables.scss";`,
      },
    },
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://0.0.0.0:8079',
        changeOrigin: true,
        pathRewrite: {
          '^/api/buy': '/buy',
          '^/api/get': '/get',
        },
      },
      '/SDK': {
        target: 'http://0.0.0.0:8081',
        changeOrigin: true,
        pathRewrite: {
          '^/SDK/buy': '/SDK/epayapi.php',
        },
      },
    },
  },
})

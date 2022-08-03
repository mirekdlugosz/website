module.exports = {
  content: ['../output/**/*.html'],
  css: ['../output/theme/css/*.css'],
  output: '/tmp/style/',
  safelist: {
      standard: [/where/]
  }
}

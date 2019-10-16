const ip = process.env.BACKEND_IP || 'localhost'
const port = process.env.BACKEND_PORT || '5001'

// By default we build static into development location of backend app.
// In TC it will be build locally to pack artifact.
const outputDir = process.env.RESULT_LOCATION || '../backend/src/web_backend/front'


module.exports = {
    outputDir: outputDir,
    assetsDir: 'static',
    devServer: {
        disableHostCheck: true,
        allowedHosts: ['*'],
        host: '0.0.0.0',
        hot: true,
        proxy: {
            '/api/*': {
                // Forward frontend dev server request for /api to django dev server
                target: 'http://' + ip + ':' + port + '/'
            }
        }
    }
}

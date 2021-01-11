const lambdaLocal = require('lambda-local');
const path = require('path');
 
var jsonPayload = {
    'key': 1,
    'another_key': "Some text"
}
 
lambdaLocal.execute({
    event: jsonPayload,
    lambdaPath: path.join(__dirname, 'index.js'),
    profilePath: '~/.aws/credentials',
    profileName: 'TempPlayground',
    timeoutMs: 30000
}).then(function(done) {
    console.log(done);
}).catch(function(err) {
    console.log(err);
});
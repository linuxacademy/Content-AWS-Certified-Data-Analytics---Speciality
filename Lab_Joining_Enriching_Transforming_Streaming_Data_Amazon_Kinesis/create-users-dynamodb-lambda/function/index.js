// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');
var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
AWS.config.update({region: 'us-east-1'});
var fs = require('fs');
var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

exports.handler = async (event, context, callback) => {
    var filePath = './user_json.json';
    var allUsers = JSON.parse(fs.readFileSync(filePath));
    var allPromises = new Array();

    for (var i = 0; i < allUsers.length; i++) {
        var user = allUsers[i];
        var params = {
            Item: {
                "user_id":  { S: user.user_id }, 
                "first_name":  { S: user.first_name }, 
                "last_name":  { S: user.last_name }, 
                "street_number":  { N: user.street_number.toString() }, 
                "street_name":  { S: user.street_name }, 
                "city":  { S: user.city }, 
                "state":  { S: user.state }, 
                "country":  { S: user.country }, 
                "postcode":  { S: user.postcode.toString() }, 
                "latitude":  { N: user.latitude.toString() }, 
                "longitude":  { N: user.longitude.toString() }
            },
            TableName: "users-information"
        };

        var promise = ddb.putItem(params).promise();
        allPromises.push(promise);
    }
    return Promise.all(allPromises);
};

    
    
    
    

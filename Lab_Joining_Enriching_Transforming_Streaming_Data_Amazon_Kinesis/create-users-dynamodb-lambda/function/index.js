// Load the AWS SDK for Node.js
var response = require('cfn-response')
var AWS = require('aws-sdk');
var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
AWS.config.update({region: 'us-east-1'});
var fs = require('fs');
var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
const TABLE_NAME = 'users-information'

exports.handler = async (event, context, callback) => {
    console.log('Received event: %s', event);

    if (event.RequestType == "Delete") {
        return response.send(event, context, "SUCCESS")
    }
    console.log('Populating DynamoDB %s table with users.', TABLE_NAME);
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
            TableName: TABLE_NAME
        };

        var promise = ddb.putItem(params).promise();
        allPromises.push(promise);
    }
    console.log("Creating %s users.", allPromises.length);
    
    var responseStatus = "FAILED"
    var responseData = {}
    
    if (allPromises.length == 0) {
        responseData = {Error: "Invoke call failed - no items where put into DynamoDB table"};
        console.log(responseData.Error);
    }
    else {
        responseStatus = "SUCCESS";
        responseData = {Success: "Users added to " + TABLE_NAME + " DynamoDB table."};
        console.log("Response body: %s", responseData);
    } 
    
    return Promise.all(allPromises).then((values) => {
        return send(event, context, responseStatus, responseData);
    });
};

async function send(event, context, responseStatus, responseData, physicalResourceId, noEcho) {
    var responsePromise = new Promise((resolve, reject) => {
        console.log("Sending signal back to CloudFormation.");

        var responseBody = JSON.stringify({
            Status: responseStatus,
            Reason: "See the details in CloudWatch Log Stream: " + context.logStreamName,
            PhysicalResourceId: physicalResourceId || context.logStreamName,
            StackId: event.StackId,
            RequestId: event.RequestId,
            LogicalResourceId: event.LogicalResourceId,
            NoEcho: noEcho || false,
            Data: responseData
        });
    
        console.log("Response body:\n", responseBody);
    
        var https = require("https");
        var url = require("url");
    
        var parsedUrl = url.parse(event.ResponseURL);
        var options = {
            hostname: parsedUrl.hostname,
            port: 443,
            path: parsedUrl.path,
            method: "PUT",
            headers: {
                "content-type": "",
                "content-length": responseBody.length
            }
        };
    
        console.log("SENDING RESPONSE...\n");
        var request = https.request(options, function(response) {
            console.log("STATUS: " + response.statusCode);
            console.log("HEADERS: " + JSON.stringify(response.headers));
            resolve(JSON.parse(responseBody));
            context.done();
        });
        request.on("error", function(error) {
            console.log("sendResponse Error:" + error);
            reject(error);
            context.done();
        });
        request.write(responseBody);
        request.end();
    });
    return await responsePromise;
}



    
    
    
    

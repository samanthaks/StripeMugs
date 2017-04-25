'use strict';

console.log('Loading function');

const doc = require('dynamodb-doc');

const dynamo = new doc.DynamoDB();

const request = require('request');


/**
 * Demonstrates a simple HTTP endpoint using API Gateway. You have full
 * access to the request and response payload, including headers and
 * status code.
 *
 * To scan a DynamoDB table, make a GET request with the TableName as a
 * query string parameter. To put, update, or delete an item, make a POST,
 * PUT, or DELETE request respectively, passing in the payload to the
 * DynamoDB API as a JSON body.
 */
exports.handler = (event, context, callback) => {
    process.env[‘PATH’] = process.env[‘PATH’] + ‘:’ + process.env[‘LAMBDA_TASK_ROOT’];
    //console.log('Received event:', JSON.stringify(event, null, 2));

    const done = (err, res) => callback(null, {
        statusCode: err ? '400' : '200',
        body: err ? err.message : res,
        headers: {
            'Content-Type': 'application/json',
        },
    });
    
    var params;

    switch (event.httpMethod) {
        case 'GETALL':
        
        request.post(
            'https://hooks.slack.com/services/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',
            { payload: {"text": "[GETALL] Store accessed"} },
            function (error, response, body) {
                if (!error && response.statusCode == 200) {
                    console.log(body)
                }
            }
        );
        
        
    params = {
        TableName : 'items'
    };
            dynamo.scan(params, done);
            break;
        case 'DELETE':
            dynamo.deleteItem(JSON.parse(event.body), done);
            break;
        case 'GET':
            
        console.log(event.body.path.id);
        var id  = parseInt(event.body.path.id);
    params = {
        Key: {"id": id},
        TableName : 'items'
    };
            dynamo.getItem(params, done);
            break;
        case 'POST':
            console.log(event.querystring);
            params = { Item: event.body, TableName: 'items'};
            dynamo.putItem(params, done);
            break;
        case 'PUT':
            dynamo.updateItem(JSON.parse(event.body), done);
            break;
        default:
            done(new Error(`Unsupported method "${event.httpMethod}"`));
    }
};
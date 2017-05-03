'use strict';

console.log('Loading function');

var nJwt = require('njwt');

const doc = require('dynamodb-doc');
// var uuid = require('uuid/v1');

const dynamo = new doc.DynamoDB();


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
    //console.log('Received event:', JSON.stringify(event, null, 2));

    const done = (err, res, jwt) => callback(null, {
        statusCode: err ? '400' : '200',
        body: err ? err.message : JSON.stringify(res),
        headers: {
            'Content-Type': 'application/json',
            'authorizationToken': jwt
        },
    });
    
    var params;
    console.log(event);
    switch (event.httpMethod) {
        case 'DELETE':
            dynamo.deleteItem(JSON.parse(event.body), done);
            break;
        case 'GETALL':
            var username = event.body.querystring.username;
            var password = event.body.querystring.password;
            params = {
                Key: {"username": username},
                TableName : 'Customers'
            };
            dynamo.getItem(params, function(err, data) {
                console.log(data);
                if (!(Object.keys(data).length === 0 && data.constructor === Object) && data.Item.password === password) {
                    var signingKey = "secret";
                    var claims = {};
                    var jwt = nJwt.create(claims, signingKey);
                    console.log(jwt);

                    var token = jwt.compact();
                    console.log(token);

                    return done(err, data, token);
                } else {
                    return done(err, null, null);
                }
            });
            break;
        case 'POST':
            var username = event.body.querystring.username;
            var password = event.body.querystring.password;
            // var c_id = uuid.v1(); // generate new unique id
            params = {
                Item: {
                    'username': username,
                    'password': password
                    // 'c_id': c_id
                },
                TableName: 'Customers'};
            console.log(params);
            dynamo.putItem(params, done);
            break;
        case 'PUT':
            dynamo.updateItem(JSON.parse(event.body), done);
            break;
        default:
            done(new Error(`Unsupported method "${event.httpMethod}"`));
    }
};


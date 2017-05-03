var nJwt = require('njwt');
var AWS = require('aws-sdk');
var signingKey = "secret";


exports.handler =  (event, context, callback) => {
    console.log('authorizationToken: ' + event.authorizationToken);
    var token = event.authorizationToken;
    
    try {
      verifiedJwt = nJwt.verify(event.authorizationToken, signingKey);
      console.log(verifiedJwt);
      callback(null, generatePolicy('user', 'Allow', event.methodArn));
    } catch (e) {
      callback("Unauthorized");
    }
};

var generatePolicy = function(principalId, effect, resource) {
    var authResponse = {};
    
    authResponse.principalId = principalId;
    if (effect && resource) {
        var policyDocument = {};
        policyDocument.Version = '2012-10-17'; // default version
        policyDocument.Statement = [];
        var statementOne = {};
        statementOne.Action = 'execute-api:Invoke'; // default action
        statementOne.Effect = effect;
        statementOne.Resource = resource;
        policyDocument.Statement[0] = statementOne;
        authResponse.policyDocument = policyDocument;
    }
    
    return authResponse;
}
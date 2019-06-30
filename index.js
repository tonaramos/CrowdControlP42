'use strict';

require('dotenv').config();

/**
 * Require the dependencies
 * @type {*|createApplication}
 */
var express = require('express');
var app = express();
var path = require('path');
var OAuthClient = require('intuit-oauth');
var bodyParser = require('body-parser');
var ngrok =  (process.env.NGROK_ENABLED==="true") ? require('ngrok'):null;
var AWS = require('aws-sdk');
let {PythonShell} = require('python-shell')
var options = {

  args: 'crowd.jpg'
};



/**
 * Configure View and Handlebars
 */
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(path.join(__dirname, '/public')));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use(bodyParser.json())

var urlencodedParser = bodyParser.urlencoded({ extended: false });

/**
 * App Variables
 * @type {null}
 */
var oauth2_token_json = null,
  redirectUri = '';


/**
 * Instantiate new Client
 * @type {OAuthClient}
 */

var oauthClient = null;


/**
 * Home Route
 */
app.get('/', function(req, res) {

  res.render('index');
});

app.post('/rekognition',function(req,res){

  console.log('The rekognition is caled on the express framework  ');

  PythonShell.run('imports.py', options, function (err, results) {
    if (err)
      throw err;
    // Results is an array consisting of messages collected during execution
    console.log('results: %j', results);

      PythonShell.run('aws-rekognition.py', options, function (err, results) {
        if (err)
          throw err;
        // Results is an array consisting of messages collected during execution
        console.log('results: %j', results);
      });


  });

});


/**
 * Start server on HTTP (will use ngrok for HTTPS forwarding)
 */
const server = app.listen(process.env.PORT || 8080, () => {
  console.log(`💻 Server listening on port ${server.address().port}`);
  if(!ngrok){
    redirectUri = `${server.address().port}` + '/callback';
    console.log(`Paste this URL in your browser : ` + 'http://localhost:' + `${server.address().port}`);

  }

});

/**
 * Optional : If NGROK is enabled
 */
if (ngrok) {

  console.log("NGROK Enabled");
  ngrok.connect({addr: process.env.PORT || 8080}, (err, url) => {
      if (err) {
        process.exit(1);
      }
      else {
        redirectUri = url + '/callback';
        console.log(`Paste this URL in your browser :  ${url}`);

      }
    }
  );
}


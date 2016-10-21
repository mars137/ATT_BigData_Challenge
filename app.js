var sentiment = require('sentiment');
var express = require('express');
var app = express();
var bodyParser = require('body-parser');

app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

app.post('/', function(req, res) {
	text = req.body.text;
	res.send(sentiment(text));
});

var server = app.listen(process.env.PORT || 3000, function () {
	    console.log("Listening on port %s...", server.address().port);
});

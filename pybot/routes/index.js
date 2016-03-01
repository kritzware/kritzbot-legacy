var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'PyBot' });
});

//var audio = new Audio('../public/audio/test.mp3');
//audio.volume = 0.1;
//audio.play();
//console.log('Audio clip playing!')

module.exports = router;
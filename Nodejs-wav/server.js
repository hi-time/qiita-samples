'use strict';

// ================ web server ================ //
const express = require('express');
const fs = require('fs');
const WavEncoder = require('wav-encoder');
const app = express();

var user = process.env.USER;
var pass = process.env.PASS;

var config = JSON.parse(fs.readFileSync(__dirname + "/json/config.json"));
var options = {
	key: fs.readFileSync(config.key),
	cert: fs.readFileSync(config.cert)
};

const port = process.env.PORT || 443;
const server = require('https').createServer(options, app);
const io = require('socket.io').listen(server);

if (user && pass) {
    app.use(express.basicAuth(user, pass));
}

app.use(express.compress());
app.use(express.static(__dirname + '/public'));

// サーバ開始
server.listen(port, function() {
    console.log('Server listening on port %s', port);
});

// ================ config ================ //
const sampleRateHertz = 16000;


// ================ socket.io ================ //
io.on('connection', function(socket) {
    console.log('connection socket server');
    // 録音開始
    socket.on('start', function(data) {
        console.log('start record');
    });

    // 録音終了
    socket.on('stop', function(data) {
        exportWAV(data, sampleRateHertz);
        console.log('stop record');
    });
});

// ================ functions ================ //
function exportWAV(data, sampleRate) {
    var mergeBuffers = function(data) {
        var sampleLength = 0;
        for(var i = 0; i < data.length; i++) {
            sampleLength += Objlen(data[i]);
        }

        var samples = new Float32Array(sampleLength);
        var sampleIndex = 0;

        for(var i = 0; i < data.length; i++) {
            for(var j = 0; j < Objlen(data[i]); j++) {
                samples[sampleIndex] = data[i][j]
                sampleIndex++;
            }
        }
        return samples;
    };

    var audioData = {
            sampleRate: 44100,
            channelData: [mergeBuffers(data)]
        };

    WavEncoder.encode(audioData).then((buffer) => {
        fs.writeFile('demo.wav', Buffer.from(buffer), function(e) {
            if (e) {
                console.log(e)
            } else {
                console.log("Success")
            }
        });

    });
}

function Objlen(data) {
    return Object.keys(data).length;
}

'use strict'

// ================ config ================ //
const socket = io();
let buffer = 2048;
let context;
let processor;
let input;
let globalStream;
var audioData = [];
const property = {
    audio: true,
    video: false
};

// ================ interface ================ //
var startButton = document.getElementById("startButton");
startButton.addEventListener("click", start);

var stopButton = document.getElementById("stopButton");
stopButton.addEventListener("click", stop);

// ================ functions ================ //
function record() {
    context = new AudioContext();
    processor = context.createScriptProcessor(buffer, 1, 1);
    processor.connect(context.destination);
    context.resume();

    var recording = function(stream) {
        globalStream = stream;
        input = context.createMediaStreamSource(stream);
        input.connect(processor);
        processor.onaudioprocess = function(audio) {
            audioStream(audio);
        };
    };
    navigator.mediaDevices.getUserMedia(property).then(recording);
}

function audioStream(audio) {
    var input = audio.inputBuffer.getChannelData(0);
    var bufferData = new Float32Array(buffer);

    for (var i = 0; i < buffer; i++) {
        bufferData[i] = input[i];
    }
    audioData.push(bufferData);
}

function start() {
    startButton.disabled = true;
    stopButton.disabled = false;
    socket.emit('start', '');
    record();
}

function stop() {
    startButton.disabled = false;
    stopButton.disabled = true;
    socket.emit('stop', audioData);
    let track = globalStream.getTracks()[0];
    track.stop();
    audioData = [];
    input.disconnect(processor);
    processor.disconnect(context.destination);
    context.close().then(function() {
        input = null;
        processor = null;
        context = null;
        startButton.disabled = false;
    });
}

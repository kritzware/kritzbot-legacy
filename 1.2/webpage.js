var net = require('net');

var HOST = '127.0.0.1';
var PORT = 8080;

// Create a server instance, and chain the listen function to it
net.createServer(function(socket) {
    console.log('CONNECTED: ' + socket.remoteAddress +':'+ socket.remotePort);
    
    // Add a 'data' event handler to this instance of socket
    socket.on('data', function(data) {
        console.log('DATA ' + socket.remoteAddress + ': ' + data);
        socket.write('This is your request: "' + data + '"');
    });
    
    // Add a 'close' event handler to this instance of socket
    socket.on('close', function(data) {
        console.log('Socket connection closed... ');
    });
}).listen(PORT, HOST);

console.log('Server listening on ' + HOST +':'+ PORT);
document.addEventListener('DOMContentLoaded', function()
{
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/logs');

    socket.on('showLogs', function(data)
    {
        console.log('Updating logs')
        var log = data.logs;
        var outputList = document.getElementById('logs-output');
        var logItem = document.createElement('li');
        logItem.textContent = log;
        outputList.appendChild(logItem);
    });

    socket.on('logsCleared', function()
    {
        console.log('Logs cleared');
        var outputList = document.getElementById('logs-output');
        outputList.innerHTML = ''; // Clear the displayed logs
    });

    var clearLogsButton = document.getElementById('clear-logs-button');
    clearLogsButton.addEventListener('click', function()
    {
        socket.emit('clearLogs');
    });
});
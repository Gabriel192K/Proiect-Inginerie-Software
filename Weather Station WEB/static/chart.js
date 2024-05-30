document.addEventListener('DOMContentLoaded', function()
{
    var ctx = document.getElementById('chart').getContext('2d');
    var chart = new Chart(ctx,
    {
        type: 'scatter',
        data:
        {
            datasets:
            [{
                label: 'Temperature',
                backgroundColor: 'rgba(0, 123, 255, 0.5)',
                borderColor: 'rgba(0, 123, 255, 1)',
                data: [],
                showLine: true,
                fill: false
            }]
        },
        options:
        {
            responsive: true,
            maintainAspectRatio: true,
            tooltips: {
                enabled: false, // Disable tooltips
            },
            scales:
            {
                xAxes:
                [{
                    type: 'time',
                    time:
                    {
                        parser: 'HH:mm:ss',
                        displayFormats:
                        {
                            second: 'HH:mm:ss',
                            minute: 'HH:mm:ss',
                            hour: 'HH:mm:ss'
                        }
                    },
                    ticks:
                    {
                        source: 'data', // Show only ticks at data points
                        maxRotation: 0,
                        callback: function(value, index, values)
                        {
                            // Show labels at a readable interval
                            return index % Math.ceil(values.length / 5) === 0 ? value : '';
                        }
                    },
                    bounds: 'data', // Fit to the data width
                    offset: true, // Adjusted by the data's data time
                    // Add some padding to the right of the graph
                    max: moment().add(1, 'minute').toDate() // Adjust the duration as needed
                }],
                yAxes:
                [{
                    ticks:
                    {
                        beginAtZero: true
                    },
                    scaleLabel:
                    {
                        display: true,
                        labelString: 'Temperature (°C)' // Default label
                    }
                }]
            }
        }
    });

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/charts');
    var currentTimestamp = '';
    var pointsOnGraph = 0;
    var dataStore =
    {
        temperature: [],
        pressure: [],
        altitude: []
    };

    const yAxisRanges =
    {
        temperature: { min: 0, max: 100, label: 'Temperature (°C)' },
        pressure: { min: 0, max: 200, label: 'Pressure (kPa)' },
        altitude: { min: 0, max: 8848, label: 'Altitude (m)' }
    };

    socket.on('initialData', function(data)
    {
        data.forEach(function(entry)
        {
            var newDataPoints =
            {
                temperature: { x: moment(entry.Timestamp.slice(1, -1), 'HH:mm:ss').toDate(), y: entry.Temperature },
                pressure: { x: moment(entry.Timestamp.slice(1, -1), 'HH:mm:ss').toDate(), y: entry.Pressure },
                altitude: { x: moment(entry.Timestamp.slice(1, -1), 'HH:mm:ss').toDate(), y: entry.Altitude }
            };

            Object.keys(newDataPoints).forEach(function(key) {
                dataStore[key].push(newDataPoints[key]);
            });
        });
        updateChart();
    });

    socket.on('setPointsOnGraph', function(data)
    {
        pointsOnGraph = data.pointsOnGraph;
    });

    socket.on('updateGraph', function(data)
    {
        currentTimestamp = data.timestamp;
        // Take new data points
        var newDataPoints =
        {
            temperature: { x: moment(currentTimestamp, 'HH:mm:ss').toDate(), y: data.temperature },
            pressure: { x: moment(currentTimestamp, 'HH:mm:ss').toDate(), y: data.pressure },
            altitude: { x: moment(currentTimestamp, 'HH:mm:ss').toDate(), y: data.altitude }
        };
        // Iterate through all new data points
        Object.keys(newDataPoints).forEach(function(key)
        {
            var dataset = dataStore[key];
            if (dataset.length >= pointsOnGraph) // If max length achieved
                dataset.shift();
            dataset.push(newDataPoints[key]);
        });

        var selectedValue = document.getElementById('select-data').value; // What graph should we print
        updateYAxisRange(chart, newDataPoints[selectedValue].y);
        chart.data.datasets[0].data = dataStore[selectedValue];
        chart.update();
    });

    document.getElementById('select-data').addEventListener('change', function()
    {
        updateChart();
    });

    function updateChart()
    {
        var selectedValue = document.getElementById('select-data').value;
        var label = selectedValue.charAt(0).toUpperCase() + selectedValue.slice(1);
        var yRange = yAxisRanges[selectedValue];
        chart.data.datasets[0].label = label;
        chart.data.datasets[0].data = dataStore[selectedValue];
        chart.options.scales.yAxes[0].ticks.min = yRange.min;
        chart.options.scales.yAxes[0].ticks.max = yRange.max;
        chart.options.scales.yAxes[0].scaleLabel.labelString = yRange.label;
        chart.update();
    }

    function updateYAxisRange(chart, newValue)
    {
        var range = 5;
        var minY = Math.max(newValue - range, chart.options.scales.yAxes[0].ticks.min);
        var maxY = Math.min(newValue + range, chart.options.scales.yAxes[0].ticks.max);
        chart.options.scales.yAxes[0].ticks.min = minY;
        chart.options.scales.yAxes[0].ticks.max = maxY;
    }

    updateChart();
});

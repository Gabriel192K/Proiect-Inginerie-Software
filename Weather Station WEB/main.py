# Using Flask 3.0.3
# Using Flask Socket IO 5.3.6
# Using PySerial 3.5
from SensorCommunication import SensorCommunication
from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from threading import Thread, Lock
from datetime import datetime
from Logger import erase, log

threadLock: Lock = Lock()
sensor_communication: SensorCommunication = SensorCommunication(threadLock)
app: Flask = Flask(__name__)
socketio: SocketIO = SocketIO(app)
socketio_thread = None
settings: dict = {}


def read_settings_file():
    try:
        with open("settings.txt", 'r') as file:
            for line in file:
                key, value = map(str.strip, line.split('='))
                settings[key] = value
    except FileNotFoundError:
        log("logs.txt", f"Settings file not found: settings.txt")
        exit(0)
    except Exception as error:
        log("logs.txt", f"Error reading settings file: {error}")
        exit(0)


def get_initial_graph():
    try:
        with open("graph.txt", "r") as file:
            lines = file.readlines()[-int(settings['POINTS_ON_GRAPH']):]
    except IOError as error:
        log("logs.txt", f"Error reading graph.txt: {error}")
        return []
    data = []
    for line in lines:
        timestamp, temperature, pressure, altitude = line.strip().split(',')
        data.append({
            'Timestamp': timestamp,
            'Temperature': int(temperature),
            'Pressure': int(pressure),
            'Altitude': int(altitude)
        })
    return data


def update_graph(timestamp, temperature, pressure, altitude):
    try:
        # Read all existing lines
        with open("graph.txt", "r") as file:
            lines = file.readlines()

        # Append the new data to the end
        new_line = f"{timestamp},{temperature},{pressure},{altitude}\n"
        lines.append(new_line)

        # If the number of lines exceeds max points on graph, remove the oldest lines
        if len(lines) > int(settings['POINTS_ON_GRAPH']):
            lines = lines[-int(settings['POINTS_ON_GRAPH']):]

        # Write back the lines to the file
        with open("graph.txt", "w") as file:
            file.writelines(lines)
    except IOError as error:
        log("logs.txt", f"Error writing to graph.txt: {error}")


def socket_io_run():
    while True:
        with threadLock:  # Ensure thread lock is on
            temperature = sensor_communication.get_temperature()
            pressure = sensor_communication.get_pressure()
            altitude = sensor_communication.get_altitude()
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        update_graph(timestamp, temperature, pressure, altitude)

        socketio.emit('setPointsOnGraph',
                      {'pointsOnGraph': settings['POINTS_ON_GRAPH']},
                      namespace='/charts')

        # Emit data to socket
        socketio.emit('updateGraph',
                      {'timestamp': timestamp,
                            'temperature': temperature,
                            'pressure': pressure,
                            'altitude': altitude},
                      namespace='/charts')
        time.sleep(1)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/charts')
def charts():
    return render_template('charts.html')


@app.route('/logs')
def logs():
    return render_template('logs.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@socketio.on('connect', namespace='/')
def handle_connect_root():
    log("logs.txt", "Client connected to /")


@socketio.on('disconnect', namespace='/')
def handle_disconnect_root():
    log("logs.txt", "Client disconnected from /")


@socketio.on('connect', namespace='/charts')
def handle_connect_charts():
    log("logs.txt", "Client connected to /charts")
    graph_data = get_initial_graph()
    socketio.emit('initialData', graph_data, namespace='/charts')


@socketio.on('disconnect', namespace='/charts')
def handle_disconnect_charts():
    log("logs.txt", "Client disconnected from /charts")


@socketio.on('connect', namespace='/logs')
def handle_connect_logs():
    log("logs.txt", "Client connected to /logs")


@socketio.on('disconnect', namespace='/logs')
def handle_disconnect_logs():
    log("logs.txt", "Client disconnected from /logs")


@socketio.on('connect', namespace='/contact')
def handle_connect_contact():
    log("logs.txt", "Client connected to /contact")


@socketio.on('disconnect', namespace='/contact')
def handle_disconnect_contact():
    log("logs.txt", "Client disconnected from /contact")


@socketio.on('connect', namespace='/logs')
def handle_connect_logs():
    log("logs.txt", "Client connected to /logs")
    try:
        with open("logs.txt", "r") as file:  # Open file and append it
            for line in file:
                socketio.emit('showLogs',
                              {'logs': line},
                              namespace='/logs')
    except IOError as e:  # Raise exception if failed
        print(f"Error writing to file: {e}")


@socketio.on('disconnect', namespace='/logs')
def handle_disconnect_logs():
    log("logs.txt", "Client disconnected from /logs")


@socketio.on('clearLogs', namespace='/logs')
def handle_clear_logs():
    if erase("logs.txt"):
        socketio.emit('logsCleared', namespace='/logs')


if __name__ == '__main__':
    read_settings_file()
    sensor_communication.begin(settings['COM_PORT'], int(settings['BAUD_RATE']), int(settings['TIMEOUT']))
    socketio_thread = Thread(target=socket_io_run)  # Create thread for socket
    socketio_thread.daemon = True  # Make thread daemon
    socketio_thread.start()
    socketio.run(app=app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)  # Run the socket

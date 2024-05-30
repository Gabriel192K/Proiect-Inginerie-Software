# Using Flask 3.0.3
# Using Flask Socket IO 5.3.6
# Using PySerial 3.5
from SensorCommunication import SensorCommunication
from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from threading import Thread, Lock
from datetime import datetime
from Logger import log

threadLock = Lock()
sensor_communication = SensorCommunication(threadLock)
app = Flask(__name__)
socketio = SocketIO(app)
socketio_thread = None
settings = {}


def read_settings_file():
    try:
        with open("settings.txt", 'r') as file:
            for line in file:
                key, value = map(str.strip, line.split('='))
                settings[key] = value
    except FileNotFoundError:
        log(f"Settings file not found: {"settings.txt"}")
        exit(0)
    except Exception as e:
        log(f"Error reading settings file: {e}")
        exit(0)


def socket_io_run():
    while True:
        with threadLock:  # Ensure thread lock is on
            temperature = sensor_communication.get_temperature()
            pressure = sensor_communication.get_pressure()
            altitude = sensor_communication.get_altitude()

        t = datetime.now().strftime("[%H:%M:%S]")

        socketio.emit('setPointsOnGraph',
                      {'pointsOnGraph': settings['POINTS_ON_GRAPH']},
                      namespace='/charts')

        # Emit data to socket
        socketio.emit('updateGraph',
                      {'timestamp': t,
                            'temperature': temperature,
                            'pressure': pressure,
                            'altitude': altitude},
                      namespace='/charts')
        time.sleep(1)


@app.route('/')
def index():
    print("Accessing /")
    return render_template('index.html')


@app.route('/charts')
def charts():
    print("Accessing /charts")
    return render_template('charts.html')


@app.route('/logs')
def logs():
    print("Accessing /logs")
    return render_template('logs.html')


@app.route('/contact')
def contact():
    print("Accessing /contact")
    return render_template('contact.html')


@socketio.on('connect', namespace='/')
def handle_connect_root():
    log("Client connected to /")
    if not socketio_thread.is_alive():  # If socket IO thread is not alive
        socketio_thread.start()         # Start socket IO thread


@socketio.on('disconnect', namespace='/')
def handle_disconnect_root():
    log("Client disconnected from /")


@socketio.on('connect', namespace='/charts')
def handle_connect_charts():
    log("Client connected to /charts")


@socketio.on('disconnect', namespace='/charts')
def handle_disconnect_charts():
    log("Client disconnected from /charts")


@socketio.on('connect', namespace='/logs')
def handle_connect_logs():
    log("Client connected to /logs")


@socketio.on('disconnect', namespace='/logs')
def handle_disconnect_logs():
    log("Client disconnected from /logs")


@socketio.on('connect', namespace='/contact')
def handle_connect_contact():
    log("Client connected to /contact")


@socketio.on('disconnect', namespace='/contact')
def handle_disconnect_contact():
    log("Client disconnected from /contact")


@socketio.on('connect', namespace='/logs')
def handle_connect_logs():
    log("Client connected to /logs")
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
    log("Client disconnected from /logs")


@socketio.on('clearLogs', namespace='/logs')
def handle_clear_logs():
    print("Clearing logs")
    try:
        with open("logs.txt", "w") as file:
            file.write("")  # Clear the file
        socketio.emit('logsCleared', namespace='/logs')
    except IOError as e:
        print(f"Error clearing file: {e}")
    print("Logs cleared")


if __name__ == '__main__':
    read_settings_file()
    sensor_communication.begin(settings['COM_PORT'],int(settings['BAUD_RATE']),int(settings['TIMEOUT']))
    socketio_thread = Thread(target=socket_io_run)  # Create thread for socket
    socketio_thread.daemon = True  # Make thread daemon
    socketio.run(app=app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)  # Run the socket

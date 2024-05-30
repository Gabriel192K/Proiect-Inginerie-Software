from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import time
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)


class ServerCommunication:
    def __init__(self, thread_lock):
        self.temperature = 0
        self.pressure = 0
        self.altitude = 0
        self.socketIO_thread = None
        self.flask_instance = app
        self.socketIO_instance = socketio
        self.thread_lock = thread_lock

    def begin(self):
        self.socketIO_thread = Thread(target=self.run)
        self.socketIO_thread.daemon = True  # Make thread daemon
        self.socketIO_thread.start()
        self.socketIO_instance.run(app=self.flask_instance, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

    def run(self):
        while True:
            with self.thread_lock:  # Ensure thread lock is on
                temperature = self.temperature()
                pressure = self.pressure()
                altitude = self.altitude()

            t = datetime.now().strftime("[%H:%M:%S]")
            s = 3600

            # Emit timestamp to socket
            self.socketIO_instance.emit('time',
                          {'timestamp': t},
                          namespace='/')

            self.socketIO_instance.emit('samples',
                          {'samples': s},
                          namespace='/')

            # Emit data to socket
            self.socketIO_instance.emit('updateGraph',
                          {'temperature': temperature,
                           'pressure': pressure,
                           'altitude': altitude},
                          namespace='/')
            time.sleep(1)

    def set_temperature(self, temperature):
        self.temperature = temperature

    def set_pressure(self, pressure):
        self.pressure = pressure

    def set_altitude(self, altitude):
        self.altitude = altitude

    @app.route('/')
    def index(self):
        return render_template('index.html')

    @app.route('/logs')
    def logs(self):
        return render_template('logs.html')

    @socketio.on('connect', namespace='/')
    def handle_connect_root(self):
        print("Client connected to /")

    @socketio.on('disconnect', namespace='/')
    def handle_disconnect_root(self):
        print("Client disconnected from /")

    @socketio.on('connect', namespace='/logs')
    def handle_connect_logs(self):
        print("Client connected to /logs")
        try:
            with open("logs.txt", "r") as file:  # Open file and append it
                for line in file:
                    socketio.emit('showLogs',
                                  {'logs': line},
                                  namespace='/logs')
        except IOError as e:  # Raise exception if failed
            print(f"Error writing to file: {e}")

    @socketio.on('disconnect', namespace='/logs')
    def handle_disconnect_logs(self):
        print("Client disconnected from /logs")

    @socketio.on('clearLogs', namespace='/logs')
    def handle_clear_logs(self):
        print("Clearing logs")
        try:
            with open("logs.txt", "w") as file:
                file.write("")  # Clear the file
            socketio.emit('logsCleared', namespace='/logs')
        except IOError as e:
            print(f"Error clearing file: {e}")


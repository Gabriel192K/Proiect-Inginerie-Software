from serial import Serial, SerialException
from threading import Thread
import time
from Logger import log


class SensorCommunication:
    def __init__(self, thread_lock):
        self.serial_instance = None
        self.serial_thread = None
        self.com_port = ''
        self.baud_rate = 0
        self.timeout = 0
        self.thread_lock = thread_lock
        self.temperature = 0
        self.pressure = 0
        self.altitude = 0

    def begin(self, com_port, baud_rate, timeout):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        try:
            self.serial_instance = Serial(port=self.com_port, baudrate=self.baud_rate, timeout=self.timeout)
        except SerialException:
            log("Can't connect to sensor, check COM port or wiring")
            exit(0)
        self.serial_thread = Thread(target=self.run)
        self.serial_thread.daemon = True
        self.serial_thread.start()
        log(f"Connected with sensor with: {self.com_port}, baud rate {self.baud_rate}")

    def run(self):
        while True:
            try:
                reading = self.serial_instance.readline().decode('ascii').strip()
                parts = reading.split(',')
                if len(parts) == 3:
                    with self.thread_lock:  # Ensure thread lock is on
                        self.temperature = int(parts[0])
                        self.pressure = int(parts[1])
                        self.altitude = int(parts[2])

                        # print(f'Temperature: {readings[0]} Celsius')
                        # print(f'Pressure: {readings[1]} kPascals')
                        # print(f'Altitude: {readings[2]} meters')
            except (SerialException, ValueError, IndexError):
                log(f"Error reading data from sensor")
            time.sleep(1)

    def get_temperature(self):
        return self.temperature

    def get_pressure(self):
        return self.pressure

    def get_altitude(self):
        return self.altitude

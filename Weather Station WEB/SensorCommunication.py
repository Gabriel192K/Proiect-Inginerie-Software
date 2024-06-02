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
            log("logs.txt", "Can't connect to sensor, check COM port or wiring")
            exit(0)
        self.serial_thread = Thread(target=self.run)
        self.serial_thread.daemon = True
        self.serial_thread.start()
        log("logs.txt", f"Connected with sensor with: {self.com_port}, baud rate {self.baud_rate}")
        time.sleep(1)

    def run(self):
        state = "WAIT_FOR_START"
        data = []
        while True:
            try:
                if self.serial_instance.in_waiting:
                    byte = self.serial_instance.read(1)
                    if state == "WAIT_FOR_START":
                        if byte == b'\x02':  # Start byte
                            data = []
                            state = "READ_DATA"

                    elif state == "READ_DATA":
                        data.append(byte)
                        if len(data) == 4:
                            state = "WAIT_FOR_STOP"

                    elif state == "WAIT_FOR_STOP":
                        if byte == b'\x03':  # Stop byte
                            with self.thread_lock:
                                self.temperature = data[0][0]
                                self.pressure = data[1][0]
                                self.altitude = data[2][0] | (data[3][0] << 8)
                        else:
                            log("logs.txt", "Invalid stop byte on UART communication")
                        state = "WAIT_FOR_START"
            except (SerialException, ValueError, IndexError) as e:
                log("logs.txt", f"Error reading data from sensor: {e}")
            time.sleep(0.1)  # Shorter sleep to ensure we catch data promptly

    def get_temperature(self):
        return self.temperature

    def get_pressure(self):
        return self.pressure

    def get_altitude(self):
        return self.altitude

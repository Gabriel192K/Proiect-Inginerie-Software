from serial import Serial, SerialException
from threading import Thread, Lock
import time
from Logger import log


class SensorCommunication:
    def __init__(self, thread_lock: Lock) -> None:
        self._serial_instance = None
        self._serial_thread = None
        self._com_port: str = ''
        self._baud_rate: int = 0
        self._timeout: int = 0
        self._thread_lock: Lock = thread_lock
        self._temperature: int = 0
        self._pressure: int = 0
        self._altitude: int = 0

    def begin(self, com_port: str, baud_rate: int, timeout: int) -> bool:
        self._com_port = com_port
        self._baud_rate = baud_rate
        self._timeout = timeout
        try:
            self._serial_instance = Serial(port=self._com_port, baudrate=self._baud_rate, timeout=self._timeout)
        except SerialException:
            log("logs.txt", "Can't connect to sensor, check COM port or wiring")
            exit(0)
        self._serial_thread = Thread(target=self.run)
        self._serial_thread.daemon = True
        self._serial_thread.start()
        log("logs.txt", f"Connected with sensor with: {self._com_port}, baud rate {self._baud_rate}")
        time.sleep(1)
        return True

    def run(self) -> None:
        state = "WAIT_FOR_START"
        data: list = []
        while True:
            try:
                if self._serial_instance.in_waiting:
                    byte = self._serial_instance.read(1)
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
                            with self._thread_lock:
                                self._temperature = data[0][0]
                                self._pressure = data[1][0]
                                self._altitude = data[2][0] | (data[3][0] << 8)
                        else:
                            log("logs.txt", "Invalid stop byte on UART communication")
                        state = "WAIT_FOR_START"
            except (SerialException, ValueError, IndexError) as e:
                log("logs.txt", f"Error reading data from sensor: {e}")
            time.sleep(0.1)  # Shorter sleep to ensure we catch data promptly

    def get_temperature(self) -> int:
        return self._temperature

    def get_pressure(self) -> int:
        return self._pressure

    def get_altitude(self) -> int:
        return self._altitude

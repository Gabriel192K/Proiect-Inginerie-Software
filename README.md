# BMP280 Sensor Data Logging and Web Interface

## Project Overview

This project utilizes a BMP280 sensor connected to an ATmega328PB microcontroller. The microcontroller reads temperature, pressure, and altitude data from the BMP280 over the TWI bus and sends this data via UART to a UART-to-USB converter, which then communicates with a computer through a COM port. The received data follows a custom transmission scheme and is processed using a multi-threaded Python application. A Flask web server with Flask-SocketIO handles data visualization and user interaction.

## Hardware Setup
- BMP280 Sensor: Measures temperature, pressure, and altitude.
- ATmega328PB Microcontroller: Reads sensor data over TWI and sends it over UART.
- UART-to-USB Converter: Connects microcontroller to the computer via USB.
- Computer: Receives data on a COM port.

## Software Components
### Microcontroller Code
- TWI Communication: Reads data from the BMP280 sensor.
- UART Communication: Sends data to the computer in a predefined format.

### Python Application
- PySerial: Handles serial communication with the microcontroller.
- Threading: Processes incoming data on a separate thread with thread locking to prevent race conditions.
- Flask & Flask-SocketIO: Implements the web server and handles real-time data updates.

## Communication Protocol
The microcontroller sends data using a custom scheme:
```START_BYTE, TEMPERATURE_BYTE, PRESSURE_BYTE, ALTITUDE_MSB_BYTE, ALTITUDE_LSB_BYTE, STOP_BYTE```
- Temperature: 0-255°C
- Pressure: 0-255 kPa
- Altitude: 0-65,535 meters (16-bit value)

## Data Processing
- Threading and Locking: Incoming data is processed on an independent thread with thread locking to ensure safe access to shared variables.
- Data Storage: Latest data points are stored and used for graph plotting and logging.

## Web Interface
### Pages
- Root Page: Welcome message and navigation bar.
- Graph Page: Displays a real-time graph of the selected parameter (temperature, pressure, altitude). The graph auto-scales to focus on the current range of values.
- Logs Page: Displays the content of logs.txt and includes a button to clear the logs.
- Contact Page: Provides contact information.

### Features
- Real-Time Graphing: Select and plot different parameters with auto-scaling.
- Log Viewing and Management: View and clear log files directly from the web interface.

## Configuration
Settings are stored in a configuration file and include:
- COM Port: Number assigned to the COM port.
- Baud Rate: Communication speed.
- Timeout: Serial read timeout in seconds.
- Points on Graph: Number of data points to display on the graph.

## Logging
The Logger module manages logging with three functions:
- append(): Appends a line of text to log.txt.
- log(): Appends a line of text with a timestamp.
- erase(): Clears the log file.

## Usage
- Setup Hardware: Connect BMP280 sensor to the ATmega328PB and set up the UART-to-USB converter.
- Configure Software: Update the configuration file with the correct COM port settings.
- Run Python Application: Start the application to begin reading sensor data and serving the web interface.
- Access Web Interface: Navigate to the provided URL to view and interact with the data.

## Clone the repository:
- ```git clone https://github.com/Gabriel192K/Proiect-Inginerie-Software.git```

## Install dependencies:
- ```pip install Flask==3.0.3```
- ```pip install Flask-SocketIO==5.3.6```
- ```pip install pyserial==3.5```

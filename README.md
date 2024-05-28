# Description
  This semester project for Software Engineering involves receiving real-time data from a microcontroller equipped with a sensor via a USB connection to a PC. The data includes information on various environmental properties such as:
- Temperature
- Pressure
- Altitude

A key feature of this project is the real-time visualization of the received data on a graph within a browser. This is achieved through a web server created using Flask and Flask-SocketIO. Additionally, the project logs status information (such as errors, route connections, and disconnections) to a file and reads initial settings from a configuration file.
Features

    Real-Time Data Reception: Receive data from a microcontroller with an attached sensor via USB.
    Web-Based Visualization: Real-time graphing of temperature, pressure, and altitude data in a web browser.
    Configurable Graph Behavior: Adjust the number of points plotted, enable accurate timestamps for each data point, and configure other graph settings.
    USB Serial Communication Settings: Easily configure USB serial communication parameters for seamless data reception.
    Status Logging: Log status information including errors, route connections, and disconnections to a file.
    Log Management: View the log file directly in the web interface, and clear logs with a button click, including the option to clear the log file.
    Web Server Implementation: Built using Flask and Flask-SocketIO for robust real-time data handling.

Setup and Installation

    Clone the repository:

    bash

git clone https://github.com/yourusername/Proiect-Inginerie-Software.git
cd Proiect-Inginerie-Software

Install dependencies:

bash

pip install -r requirements.txt

Run the application:

bash

    python app.py

    Access the web interface:
    Open your browser and go to http://localhost:5000.

Configuration

    USB Serial Communication: Settings can be adjusted in the config.json file to match the microcontroller's parameters.
    Graph Behavior: Modify the graph_settings.json file to configure how many data points are displayed, timestamp accuracy, and other graph-related settings.

Usage

    Data Visualization: View the real-time graph on the main page.
    Log Viewing: Navigate to the "Logs" tab to view status logs including errors, route connections, and disconnections.
    Clear Logs: Press the "Clear Logs" button in the "Logs" tab to clear all status logs and the log file.

from datetime import datetime


def log(message):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    try:
        with open("logs.txt", "a") as f:          # Open file and append it
            f.write(f"{timestamp} - {message}\n")
    except IOError as e:                          # Raise exception if failed
        print(f"Error writing to file: {e}")

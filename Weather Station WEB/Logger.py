from datetime import datetime


def append(path, content):
    try:
        with open(path, "a") as file:
            file.write(f"{content}\n")
        return True
    except IOError as error:
        print(f"Error opening file {path}: {error}")
    return False


def erase(path):
    try:
        with open(path, 'w'):
            pass
        return True
    except IOError as error:
        print(f"Error opening file {path}: {error}")
    return False


def log(path, content):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    append(path, f"{timestamp} - {content}")


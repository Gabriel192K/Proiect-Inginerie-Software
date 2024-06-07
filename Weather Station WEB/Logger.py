from datetime import datetime


def append(path: str, content: str) -> bool:
    try:
        with open(path, "a") as file:
            file.write(f"{content}\n")
        return True
    except IOError as error:
        print(f"Error opening file {path}: {error}")
    return False


def erase(path: str) -> bool:
    try:
        with open(path, 'w'):
            pass
        return True
    except IOError as error:
        print(f"Error opening file {path}: {error}")
    return False


def log(path: str, content: str):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    return append(path, f"{timestamp} - {content}")


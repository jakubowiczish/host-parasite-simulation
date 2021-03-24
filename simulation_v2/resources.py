import os


def path(filename: str) -> str:
    application_path = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(application_path, "resources")
    return os.path.join(directory, filename)

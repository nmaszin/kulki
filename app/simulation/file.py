import pickle
from datetime import datetime

class FrameFile:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'rb') as f:
            return pickle.load(f)

    def write(self, frame):
        with open(self.path, 'wb') as f:
            pickle.dump(frame, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def generate_name():
        time_string = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        extension = 'sim'
        return f'{time_string}.{extension}'
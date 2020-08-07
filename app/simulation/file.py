import pickle


class FrameFile:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'rb') as f:
            return pickle.load(f)

    def write(self, frame):
        with open(self.path, 'wb') as f:
            pickle.dump(frame, f, pickle.HIGHEST_PROTOCOL)

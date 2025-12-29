class CountdownTimer:
    def __init__(self, seconds: int):
        self.seconds = seconds

    def reset(self):
        self.remaining = self.seconds

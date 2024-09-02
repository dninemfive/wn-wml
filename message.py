from typing import Self

class Message(object):
    """ Wrapper for the {msg}...Done! pattern in a readable way """
    def __init__(self: Self, msg: str, end: str | None = ""):
        self.msg = msg
        self.end = end
    
    def __enter__(self):
        print(f'{self.msg}...', end=self.end)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print('Done!')    
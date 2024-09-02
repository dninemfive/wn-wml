from typing import Self

class Message(object):
    """ Wrapper for the {msg}...Done! pattern in a readable way """
    def __init__(self: Self, msg: str, indent: int = 0):
        self.msg = msg
        self.indent = indent
        self.has_nested = False
    
    def __enter__(self: Self):
        print(f'{self.msg}...', end="")
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        print('Done!')

    def nest(self: Self, msg: str) -> Self:
        if not self.has_nested:
            print()
            self.has_nested = True
        return Message(msg, self.indent + 1)
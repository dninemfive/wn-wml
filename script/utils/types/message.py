from typing import Self
from time import time_ns

PADDING = 100

def _fmt(start: int, end: int) -> str:
    return f'{(end - start) / 1e9:.3f}s'.rjust(9)

class Message(object):
    """ Wrapper for the {msg}...Done! pattern in a readable way """
    def __init__(self: Self, msg: str, indent: int = 0, force_nested = False):
        self.msg = msg
        self.indent = indent
        self.has_nested = force_nested
        self.start_time = time_ns()
    
    def __enter__(self: Self):
        self.printed_msg = f'{self.indent_str}{self.msg}...'
        print(self.printed_msg, end="", flush=True)
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        report = ""
        if exc_type is not None or exc_value is not None or traceback is not None:
            report = f"Failed: {exc_type} {exc_value}"
        else:
            report = "Done!"
        indents_or_periods = self.indent_str if self.has_nested else "".ljust(max(PADDING - len(self.printed_msg), 0), ".")
        print(f'{indents_or_periods}{report} {_fmt(self.start_time, time_ns())}')

    def fail(self: Self, exc_type, exc_value, traceback) -> None:
        self.__exit__(exc_type, exc_value, traceback)
    
    @property
    def indent_str(self: Self) -> str:
        return '  ' * self.indent

    def nest(self: Self, msg: str, padding: int = 0, child_padding: int = 0, *args, **kwargs) -> Self:
        if not self.has_nested:
            print()
            self.has_nested = True
        return Message(msg, self.indent + 1, max(self.immediate_child_padding, padding), child_padding, *args, *kwargs)
    
def try_nest(parent: Message | None, msg: str, *args, **kwargs) -> Message:
    if parent is None:
        return Message(msg, *args, **kwargs)
    else:
        return parent.nest(msg, *args, **kwargs)
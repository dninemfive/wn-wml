from typing import Self
from time import time_ns

PADDING = 128

def _fmt(start: int, end: int) -> str:
    return f'{(end - start) / 1e9:.3f}s'.rjust(9)

class Message(object):
    """ Wrapper for the {msg}...Done! pattern in a readable way """
    def __init__(self: Self, msg: str, indent: int = 0, force_nested = False):
        self.indent = indent
        self.msg = msg.replace('\n', f'\n{self.indent_str}')
        self.has_nested = force_nested
        self.has_failed = False
    
    def __enter__(self: Self):
        self.printed_msg = f'{self.indent_str}{self.msg}...'
        end = '\n' if self.has_nested else ''
        print(self.printed_msg, end=end, flush=True)
        self.start_time = time_ns()
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        if self.has_failed:
            return
        success = not (exc_type is not None or exc_value is not None or traceback is not None)
        self._print_report("Done!" if success else f"Failed: {exc_type} {exc_value}")
        

    def fail(self: Self, msg) -> None:
        self._print_report(f'Failed: {msg}')
        self.has_failed = True
        self.__exit__()

    def _print_report(self: Self, report: str):
        indents_or_periods = self.indent_str if self.has_nested else "".ljust(max(PADDING - len(self.printed_msg), 0), ".")
        print(f'{indents_or_periods}{report} {_fmt(self.start_time, time_ns())}')
    
    @property
    def indent_str(self: Self) -> str:
        return '  ' * self.indent

    def nest(self: Self, msg: str, *args, **kwargs) -> Self:
        if not self.has_nested:
            print()
            self.has_nested = True
        return Message(msg, self.indent + 1, *args, *kwargs)
    
def try_nest(parent: Message | None, msg: str, *args, **kwargs) -> Message:
    if parent is None:
        return Message(msg, *args, **kwargs)
    else:
        return parent.nest(msg, *args, **kwargs)
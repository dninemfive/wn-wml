from typing import Any, Callable

from ndf_parse.model import List
from utils.types.message import Message, try_nest


def editing_or_reading(save: bool):
    return 'Editing' if save else 'Reading'

def ndf_path(path: str, save: bool = True):
    """
    Decorator which allows defining NDF edits to a particular file:

    @ndf_path("Divisions.ndf")
    """
    def decorate(f: Callable[..., None]):
        # @wraps doesn't understand self (afaict) so using it here is counterproductive
        def wrap(self: Any, ndf: dict[str, List], msg: Message | None, *args: Any, **kwargs: Any):
            with try_nest(msg, f"{editing_or_reading(save)} {path}") as _:
                return f(self, ndf[path], *args, **kwargs)
        return wrap
    # lost the link but this was suggested in a StackExchange post
    decorate._ndf_path = path
    return decorate
    
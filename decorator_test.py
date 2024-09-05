from script.message import Message, try_nest
# shoutout to the only explanation which made sense to me: https://realpython.com/primer-on-python-decorators/#fancy-decorators
def ndf_path(path: str, save: bool = True):
    """
    Decorator which allows defining NDF edits to a particular file:

    @ndf_path("Divisions.ndf")
    """
    def dec_path(f):
        def wrap_f(self, s, msg):
            with try_nest(msg, f"{path}") as new_msg:
                return f(self, s, new_msg)
        return wrap_f
    return dec_path

class test_class(object):
    def __init__(self, asdfawsfe):
        self.asdfawsfe = asdfawsfe

    @ndf_path("hi")
    def test_thingy(self, s, msg):
        with msg.nest(s) as _:
            pass

with Message("initial message") as msg:
    test_class("fiejwioj").test_thingy("itouw", msg)
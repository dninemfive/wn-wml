# shoutout to the only explanation which made sense to me: https://realpython.com/primer-on-python-decorators/#fancy-decorators
def path(s):
    def dec_path(f):
        def wrap_f(*args, **kwargs):
            print(s)
            return f(*args, **kwargs)
        return wrap_f
    return dec_path

@path("f")
def test():
    print("test")

test()
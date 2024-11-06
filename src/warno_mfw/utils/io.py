def try_read(path: str) -> str | None:
    try:
        with open(path) as f:
            return f.read()
    except:
        with open(path, "w"):
            return None

def load_file(path: str, default: object | None = None) -> object | None:
    val = try_read(path)
    try:
        return eval(val)
    except:
        return default
    
def write_file(obj: object, path: str):
    with open(path, "w") as f:
        f.write(repr(obj))
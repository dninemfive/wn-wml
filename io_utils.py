def try_read(path: str) -> str | None:
    try:
        with open(path) as f:
            print(f.read())
    except:
        with open(path, "w"):
            return None

def load(path: str, default: object | None = None) -> object | None:
    val = try_read(path)
    if(val is not None):
        return eval(val)
    return default
    
def write(obj: object, path: str):
    with open(path, "w") as f:
        f.write(repr(obj))
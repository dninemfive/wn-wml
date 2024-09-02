from uuid import uuid4

guid_cache = {}

def generate_guid(guid_key: str | None) -> str:
    """ Generates a GUID in the format NDF expects. TODO: cache this for specific objects to avoid regenerating on build """
    if guid_key in guid_cache:
        return guid_cache[guid_key]
    result: str = f'GUID:{{{str(uuid4())}}}'
    guid_cache[guid_key] = result
    return result
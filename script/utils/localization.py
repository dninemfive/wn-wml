def capitalize(s: str) -> str:
    """ Capitalizes a string consistent with in-game capitalization rules. Mostly all-caps, but caliber designations and certain specific model names are lowercase """
    raise NotImplemented

def delocalize(localized_name: str) -> str:
    result: str = "_".join(localized_name.split())
    for c in [".", "(", ")", "-", "[", "]", "#"]:
        result = result.replace(c, "")
    return result
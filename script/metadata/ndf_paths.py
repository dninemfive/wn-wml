from typing import Self
from utils.ndf import root_paths

class NdfPaths(object):
    def __init__(self: Self, base_path: str = "", *paths: str):
        self.paths = root_paths(base_path, paths)

    def __iter__(self: Self):
        yield from self.paths

    @property
    def max_path_len(self: Self):
        return max([len(x) for x in self.paths])
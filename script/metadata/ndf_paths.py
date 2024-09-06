from typing import Self
from utils.ndf import root_paths

class NdfPaths(object):
    def __init__(self: Self, base_path: str = "", *paths: str):
        self.base_path = base_path
        self.relative_paths = paths
        self.rooted_paths = root_paths(base_path, paths)

    def __iter__(self: Self):
        yield from self.rooted_paths

    @property
    def max_path_len(self: Self):
        return max([len(x) for x in self.rooted_paths])
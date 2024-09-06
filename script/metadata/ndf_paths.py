from typing import Self
from utils.ndf import root_paths

class NdfPaths(object):
    def __init__(self: Self, base_path: str = "", *paths: str):
        self.base_path = base_path
        self.relative_paths = paths
        for x in root_paths(base_path, paths):
            print(x)
        self.rooted_paths = root_paths(base_path, paths)

    @property
    def max_path_len(self: Self):
        return max([len(x) for x in self.rooted_paths])
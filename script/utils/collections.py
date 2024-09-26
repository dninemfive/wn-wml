from typing import Iterable, TypeVar

T = TypeVar['T']

def flatten(lists: Iterable[Iterable[T]]) -> Iterable[T]:
     for list in lists:
         for item in list:
             yield item

# how the *fuck* is this not a default function in python
def unique(list: Iterable[T]) -> Iterable[T]:
    yielded = []
    for item in list:
        if not item in yielded:
            yield item
            yielded.append(item)

def with_indices(list: Iterable[T], start: int = 0) -> Iterable[tuple[int, T]]:
    index = start
    for item in list:
        yield (index, item)
        index += 1
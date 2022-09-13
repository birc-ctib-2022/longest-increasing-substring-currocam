"""Computing increasing substrings."""

# The Any annotations here is saying that we will accept any type.
# They *should* be comparable, and it *is* possible to make such
# an annotation, but it is tricky, and I don't want to confuse you
# more than strictly necessary.
# https://stackoverflow.com/questions/68372599/how-to-type-hint-supportsordering-in-a-function-parameter
from __future__ import annotations
from re import sub
from typing import Sequence, Any, Protocol, runtime_checkable, TypeVar
from abc import abstractmethod


@runtime_checkable
class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: SupportsOrdering, other: SupportsOrdering) -> bool:
        pass

    @abstractmethod
    def __eq__(self: SupportsOrdering, other: object) -> bool:
        pass


SupportsOrdering = TypeVar("SupportsOrdering", bound=Comparable)


def is_increasing(x: Sequence[SupportsOrdering]) -> bool:
    """
    Determine if x is an increasing sequence.

    >>> is_increasing([])
    True
    >>> is_increasing([42])
    True
    >>> is_increasing([1, 4, 6])
    True
    >>> is_increasing("abc")
    True
    >>> is_increasing("cba")
    False
    """
    for i in range(len(x) - 1):
        if not x[i] < x[i+1]:
            return False
    return True


def substring_length(substring: tuple[int, int]) -> int:
    """Give us the length of a substring, represented as a pair."""
    return substring[1] - substring[0]


def find_increasing_upper_limit(x: Sequence[SupportsOrdering]) -> int:
    for i, v in enumerate(x):
        if not is_increasing(x[:i]):
            return i
    return i + 1


def longest_increasing_substring(x: Sequence[SupportsOrdering]) -> tuple[int, int]:
    """
    Locate the (leftmost) longest increasing substring.

    If x[i:j] is the longest increasing substring, then return the pair (i,j).

    >>> longest_increasing_substring('abcabc')
    (0, 3)
    >>> longest_increasing_substring('ababc')
    (2, 5)
    >>> longest_increasing_substring([12, 45, 32, 65, 78, 23, 35, 45, 57])
    (5, 9)
    """
    # The leftmost empty string is our first best bet
    best = (0, 0)
    lower, upper = best
    for i, v in enumerate(x):
        j = i + 1
        if is_increasing(x[lower:j]):
            best = (lower, j)
        else:
            lower = j - 1
        if substring_length(best) >= substring_length((lower, len(x))):
            break
    return best

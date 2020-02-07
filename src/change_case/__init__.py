# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from typing import Callable, Match, Optional

from pkg_resources import DistributionNotFound, get_distribution

from .expressions import CAMEL_CASE_REGEXP, CAMEL_CASE_UPPER_REGEXP, NON_WORD_REGEXP


def replacer_factory(replacement: Optional[str]) -> Callable[[Match], str]:
    replacement = replacement if isinstance(replacement, str) else " "

    def replace(match: Match) -> str:
        start, _ = match.span()
        if start in (0, len(match.string) - len(match.group(0))):
            return ""

        return replacement

    return replace


def camel(s: str, merge: bool = False) -> str:
    s = no(s)

    if not merge:
        s = re.sub(r" (?=\d)", "_", s)

    return re.sub(r" (.)", lambda match: upper(match.group(1)), s)


def lower(s: str) -> str:
    return str.lower(s)


def upper(s: str) -> str:
    return str.upper(s)


def upper_first(s: str) -> str:
    if s is None:
        return ""

    return upper(s[0]) + s[1:]


def dot(s: str) -> str:
    return no(s, ".")


def header(s: str) -> str:
    return re.sub(r"^.|-.", lambda match: upper(match.group(0)), no(s, "-"))


def no(s: str, replacement: Optional[str] = None) -> str:
    if s is None:
        return ""

    replacer = replacer_factory(replacement)
    s = CAMEL_CASE_REGEXP.sub(r"\g<1> \g<2>", s)
    s = CAMEL_CASE_UPPER_REGEXP.sub(r"\g<1> \g<2>", s)
    s = NON_WORD_REGEXP.sub(replacer, s)
    return lower(s)


def param(s: str) -> str:
    return no(s, "-")


def title(s: str) -> str:
    return re.sub(r"^.| .", lambda match: upper(match.group(0)), no(s))


def sentence(s: str) -> str:
    return upper_first(no(s))


def snake(s: str) -> str:
    return no(s, "_")


def pascal(s: str, merge: bool = False) -> str:
    return upper_first(camel(s, merge))


def path(s: str, sep: str = "/") -> str:
    return no(s, sep)


def constant(s: str) -> str:
    return upper(snake(s))


try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

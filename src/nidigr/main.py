from typing import Literal
import sys
from pprint import pp
from random import choices, random, randint
from argparse import ArgumentParser
from dataclasses import dataclass

from requests import get


@dataclass
class Settings:
    verbosity: int


SETTINGS: Settings | None = None


def set_settings(settings) -> None:
    global SETTINGS
    SETTINGS = settings


def get_settings() -> Settings:
    assert SETTINGS is not None
    return SETTINGS


def evaluate_digraphs_from_web(dst: dict[str, int], site: Literal["any"] = "any"):
    settings = get_settings()
    urls = [
        "https://www.ietf.org/rfc/rfc2324.txt",
        "https://www.ietf.org/rfc/rfc1068.txt",
        "https://www.ietf.org/rfc/rfc1086.txt",
        "https://www.ietf.org/rfc/rfc1088.txt",
        "https://www.ietf.org/rfc/rfc1158.txt",
    ]
    result = dict()
    for url in urls:
        r = get(url)
        prev = None
        if settings.verbosity >= 1:
            pp(r.text)
        for i in r.text:
            if not i.isalpha():
                prev = None
                continue
            curr = i
            if prev is not None:
                digr = prev+curr
                if digr.isupper():
                    # is may be a part of acronym
                    continue
                result.setdefault(digr.lower(), 0)
                result[digr.lower()] += 1
            prev = curr

    if settings.verbosity >= 1:
        for k, v in sorted(result.items(), key=lambda x: x[1]):
            print(f"{k}: {v}")

    dst.extend(list(result.items()))


class NicknameGenerator:
    def __init__(self, digraphs: list[str, int], noise_factor: int = 1):
        self._digraphs = digraphs.copy()

        total_count = 0
        distinct_count = 0
        for n, (digr, count) in enumerate(self._digraphs):
            total_count += count
        mean_count = total_count / len(self._digraphs)

        for n, (digr, count) in enumerate(self._digraphs):
            self._digraphs[n] = digr, count + mean_count * noise_factor

        # pp(self._digraphs)

        self._previous: str | None = None
        self.seq_hits = 0

    def _choose(self, variants: list[tuple[str, int]]):
        variants = dict(variants)
        return choices(list(variants.keys()), weights=list(variants.values()))[0]

    def next_token(self):
        variants: list[str, int] = self._digraphs
        is_first = self._previous is None

        if not is_first:
            prev_letter = self._previous[-1]
            variants = filter(lambda x: x[0][0] == prev_letter, variants)
            variants = list(variants)

        if not variants:
            variants = self._digraphs
        else:
            self.seq_hits += 1

        digraph = self._choose(variants)
        self._previous = digraph

        result = digraph
        if not is_first:
            result = result[-1]

        return result


def make_parser():
    parser = ArgumentParser(
            epilog="",
            description=(
                "Digraph-based nickname generator."
                " Automatically collects digraph statitics from web (currently, statically, from some IETF standards),"
                " and generates letter sequences based on this statistics.  First digraph is selects randomly, than,"
                " for the rest of nickname, wee lookup for digraphs that starts from last letter of word, and choise"
                " from them.  If there are no such digraphs, we choise from all digraphs.  Each choise is random but"
                "  weighted with collected digraphs statistics.  Also there is a noise added that is flattenizes"
                "  distribution (each digraph weight is increased by `noise_factor * mean_weight`)."
            ),
    )

    parser.add_argument("--length", dest="length_fixed", type=int)
    parser.add_argument("--length-min", dest="length_min", type=int, default=5)
    parser.add_argument("--length-max", dest="length_max", type=int, default=10)
    parser.add_argument("--samples-count", dest="samples_count", type=int, default=50)
    parser.add_argument("--noise-factor",
                        dest="noise_factor",
                        type=float,
                        default=0.1,
                        help="It seems that you can think about it as about LLM models"
                             " temperature.  ")
    parser.add_argument("-v", dest="verbosity", action="store_const", const=1, default=0, help="Verbose output")

    return parser


def main():
    parser = make_parser()
    ns = parser.parse_args(sys.argv[1:])
    set_settings(Settings(verbosity=ns.verbosity))
    settings = get_settings()

    digraphs: list[str, int] = []
    evaluate_digraphs_from_web(digraphs)

    if settings.verbosity >= 1:
        print("=================================\nDSH = Digraphs sequence hits\nL = Length\n=================================")
    for _ in range(ns.samples_count):
        desired_length = ns.length_fixed or randint(ns.length_min, ns.length_max)
        generator = NicknameGenerator(digraphs, noise_factor=ns.noise_factor)
        result = ""
        while True:
            result += generator.next_token()
            if len(result) >= desired_length:
                break
        
        if settings.verbosity >= 1:
            print("================================================")
            print(f"Generation result: {result.capitalize()}")
            print(f"SDH: {generator.seq_hits}, L: {len(result)}")
        else:
            print(result.capitalize())


if __name__ == "__main__":
    main()


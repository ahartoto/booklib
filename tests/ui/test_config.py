# Filename: test_config.py

# Standard libraries
import typing

# BookLib
from booklib.ui import config


class TestLabel:

    def equal_keys(self, got: typing.Mapping[str, typing.Any],
                   want: typing.Mapping[str, typing.Any]) -> bool:
        if set(got.keys()) ^ set(want.keys()):
            return False
        for k, v in want.items():
            if type(v) is dict:
                if not self.equal_keys(v, got[k]):
                    return False
        return True

    def test_equivalent_labels(self):
        langs = sorted(config.LABELS.keys())
        if len(langs) <= 1:
            return
        primary = langs[0]
        want = config.LABELS[primary]
        # Recursively compare all the keys to make sure they exist.
        for other in langs[1:]:
            got = config.LABELS[other]
            assert self.equal_keys(got, want)

# coding: utf-8
from __future__ import unicode_literals

import pytest


@pytest.mark.parametrize(
    "text,expected_tokens",
    [
        (
            "ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་  tr",
            ["ལེ_གས", "།_", "བཀྲ་ཤིས་", "མཐ", "འི་", "_༆_", "ཤི་", "བཀྲ་ཤིས་__", "tr"],
        )
    ],
)
def test_bo_tokenizer(bo_tokenizer, text, expected_tokens):
    tokens = [token.text for token in bo_tokenizer(text)]
    assert tokens == expected_tokens

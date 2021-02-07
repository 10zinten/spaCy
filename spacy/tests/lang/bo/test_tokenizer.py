# coding: utf-8
from __future__ import unicode_literals

import pytest


@pytest.mark.parametrize(
    "text,expected_tokens",
    [
        (
            "ཁྱེད་རང་གི་མཚན་ལ་ག་རེ་ཞུ་གི་ཡོད།",
            ["ཁྱེད", "རང", "གི", "མཚན", "ལ", "ག", "རེ", "ཞུ", "གི", "ཡོད།"],
        )
    ],
)
def test_bo_tokenizer(bo_tokenizer, text, expected_tokens):
    tokens = [token.text for token in bo_tokenizer(text)]
    assert tokens == expected_tokens

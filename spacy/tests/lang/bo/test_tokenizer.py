# coding: utf-8
from __future__ import unicode_literals

import pytest


@pytest.mark.parametrize(
    "text,expected_tokens",
    [
        (
            "རྣལ་འབྱོར་བླ་མེད་ཀྱི་རྒྱུད་དོན་ལ་འཇུག་པ་ལས།",
            [
                "རྣལ",
                "འབྱོར",
                "བླ",
                "མེད",
                "ཀྱི",
                "རྒྱུད",
                "དོན",
                "ལ",
                "འཇུག",
                "པ",
                "ལས།",
            ],
        )
    ],
)
def test_bo_tokenizer_syl(bo_tokenizer_syl, text, expected_tokens):
    tokens = [token.text for token in bo_tokenizer_syl(text)]
    assert tokens == expected_tokens


@pytest.mark.parametrize(
    "text,expected_tokens",
    [
        (
            "རྣལ་འབྱོར་བླ་མེད་ཀྱི་རྒྱུད་དོན་ལ་འཇུག་པ་ལས།",
            [
                "རྣལ་འབྱོར་",
                "བླ་མེད་",
                "ཀྱི་",
                "རྒྱུད་",
                "དོན་",
                "ལ་",
                "འཇུག་པ་",
                "ལ",
                "ས",
                "།",
            ],
        )
    ],
)
def test_bo_tokenizer_botok(bo_tokenizer_botok, text, expected_tokens):
    tokens = [token.text for token in bo_tokenizer_botok(text)]
    assert tokens == expected_tokens

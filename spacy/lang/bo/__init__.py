import warnings
from enum import Enum
from typing import Dict

from thinc.config import SECTION_PREFIX

from ... import util
from ...attrs import LANG
from ...errors import Warnings
from ...language import DEFAULT_CONFIG, Language
from ...tokens import Doc
from ...util import DummyTokenizer, registry
from .stop_words import STOP_WORDS

DEFAULT_CONFIG = """
[nlp]

[nlp.tokenizer]
@tokenizers = "spacy.bo.TibetanTokenizer"
segmenter = "syl"
"""


class Segmenter(str, Enum):
    syl = "syl"
    botok = "botok"

    @classmethod
    def values(cls):
        return list(cls.__members__.keys())


@registry.tokenizers("spacy.bo.TibetanTokenizer")
def create_tibetan_tokenizer(segmenter: Segmenter = Segmenter.syl, config: Dict = {}):
    def tibetan_tokenizer_factory(nlp):
        return TibetanTokenizer(nlp, segmenter=segmenter, config=config)

    return tibetan_tokenizer_factory


class TibetanTokenizer(DummyTokenizer):
    def __init__(self, nlp, segmenter: Segmenter = Segmenter.syl, config={}):
        self.vocab = nlp.vocab
        self.config = config
        if isinstance(segmenter, Segmenter):
            segmenter = segmenter.value
        self.segmenter = segmenter
        self.botok_seg = None
        if segmenter not in Segmenter.values():
            warn_msg = Warnings.W102.format(
                lang="Tibetan",
                segmenter=segmenter,
                supported=", ".join(Segmenter.values()),
                default="'syl' (syllable segmentation)",
            )
            warnings.warn(warn_msg)
            self.segmenter = Segmenter.syl
        if segmenter == Segmenter.botok:
            self.botok_seg = try_botok_import()

    def __call__(self, text) -> Doc:
        if self.segmenter == Segmenter.botok:
            words = self.botok_seg(text).tokenize_words_raw_lines.split()
        else:
            words = text.split("་")
        spaces = [False] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)


class TibetanDefaults(Language.Defaults):
    config = util.load_config_from_str(DEFAULT_CONFIG)
    stop_words = STOP_WORDS
    writing_system = {"direction": "ltr", "has_case": False, "has_letters": False}


class Tibetan(Language):
    lang = "bo"
    Defaults = TibetanDefaults


def try_botok_import() -> None:
    try:
        from botok import Text

        # tokenized a short text to have botok created its trie in advance
        Text("བཀྲ་ཤིས་").tokenize_words_raw_lines

        return Text
    except ImportError:
        msg = (
            "botok not installed. Install it with `pip install botok` ",
            "or from https://github.com/Esukhia/botok",
        )
        raise ImportError(msg)


__all__ = ["Tibetan"]

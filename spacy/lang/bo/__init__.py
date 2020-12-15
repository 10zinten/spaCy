from ... import util
from ...attrs import LANG
from ...language import Language
from ...tokens import Doc
from ..tokenizer_exceptions import BASE_EXCEPTIONS
from .stop_words import STOP_WORDS


def try_botok_import(use_botok):
    try:
        from botok import Text

        Text("བཀྲ་ཤིས་").tokenize_words_raw_lines
        return Text
    except ImportError:
        if use_botok:
            msg = (
                "botok not installed. Install it with `pip install botok` ",
                "or from https://github.com/Esukhia/botok",
            )
            raise ImportError(msg)


class TibetanTokenizer(util.DummyTokenizer):
    def __init__(self, cls, nlp=None, config={}):
        self.use_botok = config.get("use_botok", cls.use_botok)
        self.vocab = nlp.vocab if nlp is not None else cls.create_vocab(nlp)
        self.word_tokenizer = try_botok_import(self.use_botok)

    def __call__(self, text):
        if self.use_botok:
            words = self.word_tokenizer(text).tokenize_words_raw_lines.split()
        else:
            words = text.split("་")

        spaces = [False] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)


class TibetanDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters[LANG] = lambda text: "bo"
    tokenizer_exceptions = BASE_EXCEPTIONS
    stop_words = STOP_WORDS
    writing_system = {"direction": "ltr", "has_case": False, "has_letters": False}
    use_botok = True

    @classmethod
    def create_tokenizer(cls, nlp=None, config={}):
        return TibetanTokenizer(cls, nlp, config=config)


class Tibetan(Language):
    lang = "bo"
    Defaults = TibetanDefaults

    def make_doc(self, text):
        return self.tokenizer(text)


__all__ = ["Tibetan"]

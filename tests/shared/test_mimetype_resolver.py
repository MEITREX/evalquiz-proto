from evalquiz_proto.shared.mimetype_resolver import MimetypeResolver

allowed_extensions = [
    ".md",
    ".pptx",
    ".csv",
    ".tsv",
    ".docx",
    ".epub",
    ".html",
    ".ipynb",
    ".json",
    ".latex",
    ".markdown",
    ".man",
    ".odt",
    ".opml",
    ".org",
    ".ris",
    ".rtf",
    ".rst",
    ".tex",
]


def test_resolve_allowed_extensions() -> None:
    for extension in allowed_extensions:
        type = MimetypeResolver.fixed_guess_type(extension)
        if type is None:
            raise Exception
        MimetypeResolver.fixed_guess_extension(type)

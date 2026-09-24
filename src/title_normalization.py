import re
import unicodedata


def normalize_title(title):
    """
    Normalize game titles for controlled cross-dataset matching.
    """

    if title is None:
        return ""

    title = str(title)

    # Unicode normalization
    title = unicodedata.normalize("NFKD", title)

    # Remove accents
    title = "".join(
        char for char in title
        if not unicodedata.combining(char)
    )

    # Lowercase
    title = title.lower()

    # Convert punctuation/separators into spaces
    title = re.sub(r"[^a-z0-9]+", " ", title)

    # Normalize whitespace
    title = re.sub(r"\s+", " ", title).strip()

    return title
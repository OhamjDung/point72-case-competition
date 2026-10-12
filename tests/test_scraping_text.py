import pytest

from scraping.text import author_hash, state_code, tag_companies


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Dick's had huge markdowns", ["DKS"]),
        ("dicks sporting goods is hiring", ["DKS"]),
        ("my manager is a dick", []),
        ("he's such a dick sometimes", []),
        ("Dick’s House of Sport opened", ["DKS"]),
        ("Dick's Last Resort was fun", []),
        ("I left Foot Locker for Academy Sports", ["ACADEMY", "FL"]),
        ("hit my sales target today", []),
        ("I work at Target", ["TARGET"]),
    ],
)
def test_tag_companies(text, expected):
    assert tag_companies(text) == expected


def test_author_hash():
    assert author_hash("u1", "s") == author_hash("u1", "s")
    assert author_hash("u1", "s") != author_hash("u1", "other")
    assert len(author_hash("u1", "s")) == 16
    assert author_hash("[deleted]", "s") is None
    assert author_hash(None, "s") is None
    with pytest.raises(ValueError, match="salt"):
        author_hash("u1", "")


def test_state_code():
    assert state_code("Texas") == "TX"
    assert state_code("tx") == "TX"
    assert state_code("Ontario") is None
    assert state_code(None) is None

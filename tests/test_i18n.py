"""The editor's translations: every language has the same text keys and placeholders as
English, English matches what the server says, and the scripts show no English of their own."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from ios_homescreen.ui import errors

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src" / "ios_homescreen" / "ui" / "static"
I18N = STATIC / "i18n"
SCRIPTS = sorted((STATIC / "js").glob("*.js"))
LANGUAGES = re.findall(
    r'\{ code: "([^"]+)", name: ', (STATIC / "js" / "i18n.js").read_text(encoding="utf-8")
)
PLACEHOLDER = re.compile(r"\{(\w+)\}")


def _load(code: str) -> dict:
    return json.loads((I18N / f"{code}.json").read_text(encoding="utf-8"))


ENGLISH = _load("en")


def _forms(value) -> list[str]:
    if isinstance(value, dict):
        return list(value.values())
    if isinstance(value, list):
        return value
    return [value]


def _placeholders(value) -> set[str]:
    return {name for text in _forms(value) for name in PLACEHOLDER.findall(text)}


def _code_lines(script: Path) -> str:
    text = script.read_text(encoding="utf-8")
    return "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("//"))


def _code(value) -> set[str]:
    """`code` spans: commands and flags stay as they are in every language."""
    return {span for text in _forms(value) for span in re.findall(r"`[^`]+`", text)}


def test_the_eight_languages_are_offered_and_shipped():
    assert LANGUAGES == ["en", "tr", "de", "es", "fr", "ja", "pt-BR", "zh-Hans"]
    assert sorted(p.stem for p in I18N.glob("*.json")) == sorted(LANGUAGES)


@pytest.mark.parametrize("code", LANGUAGES[1:])
def test_every_language_has_the_english_keys_and_placeholders(code):
    strings = _load(code)

    assert list(strings) == list(ENGLISH)
    for key, english in ENGLISH.items():
        value = strings[key]
        if isinstance(english, list):
            assert isinstance(value, list), key
            assert len(value) == len(english), key
        elif isinstance(value, dict):
            assert isinstance(english, dict), key
            assert "other" in value, key
        else:
            assert isinstance(value, str), key
        assert all(text.strip() for text in _forms(value)), key
        assert _placeholders(value) == _placeholders(english), key
        assert _code(value) == _code(english), key


def test_plural_entries_have_an_other_form():
    for key, value in ENGLISH.items():
        if isinstance(value, dict):
            assert set(value) == {"one", "other"}, key


def test_every_key_the_scripts_use_exists():
    used = set()
    for script in SCRIPTS:
        text = _code_lines(script)
        used |= set(re.findall(r'\b(?:t|has|tList)\("([a-z][\w.]*)"', text))
        used |= set(re.findall(r'\? "([a-z_]+\.[\w.]+)" : "', text))
        used |= set(re.findall(r'\? "[a-z_]+\.[\w.]+" : "([a-z_]+\.[\w.]+)"', text))
    assert used
    assert used - set(ENGLISH) == set()


# ------------------------------------------------------------------ English = the server


def test_english_error_text_matches_the_server():
    platform = {"darwin": "darwin", "win32": "win32"}.get(errors.sys.platform, "linux")
    for code, (title, steps) in errors._KNOWN.items():
        key = f"error.{code}"
        if code == "usbmuxd_unreachable":
            key = f"error.usbmuxd_unreachable.{platform}"
        expected = ENGLISH[f"{key}.steps"]
        if code in ("timeout", "connection_failed"):
            expected = [*expected, ENGLISH[f"error.restart.{platform}"]]
        assert ENGLISH[f"{key}.title"] == title, code
        assert expected == steps, code


def test_generic_error_titles_are_the_servers():
    source = (ROOT / "src" / "ios_homescreen" / "ui" / "errors.py").read_text(encoding="utf-8")
    messages = (STATIC / "js" / "messages.js").read_text(encoding="utf-8")
    for kind in ("layout", "state", "device", "other"):
        title = ENGLISH[f"error.generic.{kind}.title"]
        assert f'title = "{title}"' in source
        assert f'"{title}": "{kind}"' in messages
        assert ENGLISH[f"error.generic.{kind}.steps"] == ["Check the details below and try again."]


def test_every_event_the_server_sends_has_a_translation():
    sources = "".join(
        p.read_text(encoding="utf-8") for p in (ROOT / "src" / "ios_homescreen").rglob("*.py")
    )
    codes = set(re.findall(r'Event\(\s*"([a-z_]+)"', sources))
    codes |= set(re.findall(r'\bemit\(\s*"([a-z_]+)"', sources))
    assert {"connecting", "writing", "verified", "rolled_back"} <= codes
    handled = {"reading", "failed"}  # reading: two texts by step count; failed: the error title
    assert {c for c in codes - handled if f"event.{c}" not in ENGLISH} == set()


# ------------------------------------------------------------------ no English in the code

VISIBLE = [
    # attributes a person sees or hears, written as plain text
    re.compile(r'\b(?:title|aria-label|placeholder|alt)="[A-Za-z]'),
    # text between tags: >Some words<
    re.compile(r">\s*[A-Z][a-z]+(?: [A-Za-z]+)*[.?!]?\s*<"),
    # toasts, menu entries and labels built from literals
    re.compile(r'\btoast\(\s*["`]'),
    re.compile(r'\blabel: ["`][A-Z]'),
]


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_scripts_show_no_hardcoded_english(script):
    code = _code_lines(script)
    for pattern in VISIBLE:
        assert not pattern.findall(code), (script.name, pattern.pattern, pattern.findall(code))


def test_the_page_starts_in_english_and_scripts_set_the_language():
    page = (STATIC / "index.html").read_text(encoding="utf-8")
    assert '<html lang="en">' in page
    assert "document.documentElement.lang = code" in (STATIC / "js" / "i18n.js").read_text(
        encoding="utf-8"
    )

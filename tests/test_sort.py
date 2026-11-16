"""A-Z page sorting, shared by the ``sort`` command and the editor's /api/sort."""

from __future__ import annotations

import io
import sys
from pathlib import Path

import pytest

import samples
from fakes import FakeSpringBoard, opener_for
from ios_homescreen import api
from ios_homescreen.cli import main
from ios_homescreen.sort import sort_state, sort_view
from ios_homescreen.state import is_folder, is_widget, item_name


def _screen():
    """A dict state out of order: a widget, two folders and four apps over two pages."""
    weather = samples.widget(
        "weather-1",
        "medium",
        container="com.apple.weather",
        extension="com.apple.weather.widget",
        kind="com.apple.weather.forecast",
    )
    utilities = samples.folder("Utilities", [samples.app("com.apple.calculator", "Calculator")])
    games = samples.folder("Games", [samples.app("com.example.zelda", "Zelda")])
    state = {
        "buttonBar": [samples.app("com.apple.mobilephone", "Phone")],
        "iconLists": [
            [weather, samples.app("com.example.zoom", "Zoom"), utilities],
            [samples.app("com.example.alfa", "Alfa"), games],
        ],
    }
    return state, weather, utilities, games


def _names(page) -> list[str]:
    return [item.get("displayName", item.get("displayIdentifier", "?")) for item in page]


# ------------------------------------------------------------------ sort_state


def test_sort_redeals_movable_items_across_all_pages_in_name_order():
    state, *_ = _screen()

    result = sort_state(state)

    assert _names(result["iconLists"][0]) == ["weather-1", "Alfa", "Games"]
    assert _names(result["iconLists"][1]) == ["Utilities", "Zoom"]


def test_sort_leaves_the_dock_widgets_and_folder_contents_alone():
    state, weather, utilities, games = _screen()

    result = sort_state(state)

    assert result["buttonBar"] == state["buttonBar"]
    assert result["iconLists"][0][0] == weather
    flat = [item for page in result["iconLists"] for item in page]
    assert utilities in flat
    assert games in flat
    assert [i["displayIdentifier"] for i in utilities["iconLists"][0]] == ["com.apple.calculator"]


def test_sort_accepts_the_list_shape_get_icon_state_returns():
    state, _, _, _ = _screen()
    listed = [state["buttonBar"], *state["iconLists"]]

    result = sort_state(listed)

    assert result["buttonBar"] == state["buttonBar"]
    assert _names(result["iconLists"][0]) == ["weather-1", "Alfa", "Games"]


def test_sort_folds_case_so_lower_and_capital_names_mingle():
    state = {
        "iconLists": [
            [
                samples.app("com.example.zulu", "zulu"),
                samples.app("com.example.apple", "apple"),
                samples.app("com.example.banana", "Banana"),
            ]
        ]
    }

    [page] = sort_state(state)["iconLists"]

    assert _names(page) == ["apple", "Banana", "zulu"]


# ------------------------------------------------------------------ sort_view


def test_sort_view_keeps_the_dock_pins_widgets_and_sorts_by_view_name():
    view = {
        "dock": [{"id": "d1", "type": "app", "name": "Phone"}],
        "pages": [
            {
                "items": [
                    {"id": "w1", "type": "widget", "name": "Weather"},
                    {"id": "a2", "type": "app", "name": "Zoom"},
                    {"id": "f1", "type": "folder", "name": "Utilities", "pages": []},
                ]
            },
            {"items": [{"id": "a1", "type": "app", "name": "Alfa"}]},
        ],
    }

    result = sort_view(view)

    assert result["dock"] == view["dock"]
    assert result["pages"][0]["items"] == [
        view["pages"][0]["items"][0],
        view["pages"][1]["items"][0],
        view["pages"][0]["items"][2],
    ]
    assert result["pages"][1]["items"] == [view["pages"][0]["items"][1]]


# ------------------------------------------------------------------ the command


@pytest.fixture
def home(tmp_path, monkeypatch) -> Path:
    """An isolated data dir and an empty working directory, like test_cli's."""
    monkeypatch.setenv("IOS_HOMESCREEN_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    return tmp_path / "data"


def _pull(home) -> FakeSpringBoard:
    device = FakeSpringBoard(samples.home_screen(), samples.installed_apps())
    assert main(["pull"], open_device=opener_for(device)) == 0
    return device


def _planned(home, layout: Path = Path("layout.toml")):
    """The layout file resolved against its pull: item names and real positions."""
    (snapshot,) = (home / "pulls").glob("pull-*.plist")
    read = api.load_pull(snapshot)
    return api.plan_layout(api.load_layout(layout), read)


def _page_items(payload):
    return [item for page in payload["iconLists"] for item in page]


def test_sort_rewrites_the_layout_file_in_name_order(home):
    _pull(home)

    assert main(["sort"]) == 0

    plan = _planned(home)
    names = [
        item_name(item).casefold() for item in _page_items(plan.payload) if not is_widget(item)
    ]
    assert names == sorted(names)
    assert len(names) > 3


def test_sort_keeps_the_dock_widget_cells_and_folder_contents(home):
    _pull(home)
    before = _planned(home).payload

    assert main(["sort"]) == 0

    after = _planned(home).payload
    assert after["buttonBar"] == before["buttonBar"]
    for p, page in enumerate(before["iconLists"]):
        for i, item in enumerate(page):
            if is_widget(item):
                assert after["iconLists"][p][i] == item
            if is_folder(item):
                kept = next(
                    x
                    for x in _page_items(after)
                    if is_folder(x) and x.get("displayName") == item.get("displayName")
                )
                assert kept["iconLists"] == item["iconLists"]


def test_sort_keeps_the_pull_table_and_says_nothing_to_do_when_sorted(home, capsys):
    _pull(home)
    assert main(["sort"]) == 0
    text = Path("layout.toml").read_text(encoding="utf-8")
    assert "[pull]" in text
    capsys.readouterr()

    assert main(["sort"]) == 0

    assert "already in A-Z order" in capsys.readouterr().out
    assert Path("layout.toml").read_text(encoding="utf-8") == text


def test_sort_help_lists_it_among_the_commands(capsys):
    with pytest.raises(SystemExit) as exit_:
        main(["sort", "--help"])
    assert exit_.value.code == 0
    assert "A-Z" in capsys.readouterr().out

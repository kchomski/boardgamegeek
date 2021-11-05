from __future__ import unicode_literals

import pytest

from _common import *
from boardgamegeek import BGGError, BGGValueError, BGGItemNotFoundError
from boardgamegeek.objects.geeklist import GeekList, GeekListItem, GeekListObject
import time


def test_get_geeklist_with_invalid_parameters(legacy_bgg):
    for invalid in [None, ""]:
        with pytest.raises(BGGValueError):
            legacy_bgg.geeklist(invalid)


def test_get_invalid_id_geeklist(legacy_bgg, mocker):
    mock_get = mocker.patch("requests.sessions.Session.get")
    mock_get.side_effect = simulate_legacy_bgg

    with pytest.raises(BGGItemNotFoundError):
        legacy_bgg.geeklist(TEST_GEEKLIST_INVALID_ID)


def test_get_valid_id_geeklist(legacy_bgg, mocker, null_logger):
    mock_get = mocker.patch("requests.sessions.Session.get")
    mock_get.side_effect = simulate_legacy_bgg

    geeklist = legacy_bgg.geeklist(TEST_GEEKLIST_ID, comments=True)

    assert geeklist is not None
    assert geeklist.id == TEST_GEEKLIST_ID
    assert type(len(geeklist)) == int
    assert type(geeklist.items) == list

    # make sure we can iterate through the geeklist
    for g in geeklist:
        assert type(g) == GeekListItem
        assert g.id is not None
        assert type(g.id) is str
        assert type(g.description) in STR_TYPES_OR_NONE
        if g.object is not None:
            assert type(g.object) == GeekListObject
        repr(g)

    str(geeklist)
    repr(geeklist)

    # for coverage's sake
    geeklist._format(null_logger)
    assert type(geeklist.data()) == dict

    geeklist = legacy_bgg.geeklist(TEST_GEEKLIST_ID, comments=False)
    for g in geeklist:
        assert len(g.comments) is 0

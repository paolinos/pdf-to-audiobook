import sys
import tempfile

import pytest

from validators import parse_args


def test_parse_args_invalid_args(capsys):
    with pytest.raises(SystemExit):
        parse_args()

    captured = capsys.readouterr()
    assert "the following arguments are required" in captured.err


def test_parse_args_invalid_path():
    with pytest.raises(FileNotFoundError, match=r"filepath was not found*"):
        sys.argv = ["", "./path"]
        assert parse_args()


def test_parse_args():
    with tempfile.NamedTemporaryFile(prefix="test_", suffix=".pdf") as fp:
        sys.argv = ["", fp.name]
        options = parse_args()
        assert options.input_path == fp.name
        assert options.audio_speed == 1.0


def test_parse_args_with_speed():
    with tempfile.NamedTemporaryFile(prefix="test_", suffix=".pdf") as fp:
        speed = 1.5
        sys.argv = ["", fp.name, f"--speed={speed}"]
        options = parse_args()
        assert options.input_path == fp.name
        assert options.audio_speed == speed

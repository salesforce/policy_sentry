from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from policy_sentry.util.file import read_yaml_file


def test_read_yaml_file_valid(tmp_path: Path):
    path = tmp_path / "ok.yml"
    path.write_text("mode: crud\nname: demo\n", encoding="utf-8")
    cfg = read_yaml_file(path)
    assert cfg["mode"] == "crud"
    assert cfg["name"] == "demo"


def test_read_yaml_file_invalid_yaml_raises_yaml_error(tmp_path: Path):
    path = tmp_path / "bad.yml"
    path.write_text("foo: [bar\n", encoding="utf-8")  # unclosed sequence
    with pytest.raises(yaml.YAMLError):
        read_yaml_file(path)


def test_read_yaml_file_non_mapping_root_raises_value_error(tmp_path: Path):
    path = tmp_path / "list.yml"
    path.write_text("- just\n- a\n- list\n", encoding="utf-8")
    with pytest.raises(ValueError, match="mapping at the root"):
        read_yaml_file(path)


def test_read_yaml_file_empty_raises_value_error(tmp_path: Path):
    path = tmp_path / "empty.yml"
    path.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="mapping at the root"):
        read_yaml_file(path)

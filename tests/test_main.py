import pytest
import os
import pathlib
from click.testing import CliRunner
from yarasilly2 import main

def test_main_happy_path(tmp_path: pathlib.Path):
    runner = CliRunner()

    input_dir = tmp_path / "input_samples"
    input_dir.mkdir()

    dummy_file1 = input_dir / "sample1.bin"
    dummy_file1.write_bytes(b"dummy data string 1\ndummy data string 2\n")

    dummy_file2 = input_dir / "sample2.bin"
    dummy_file2.write_bytes(b"dummy data string 1\nother data\n")

    output_dir = tmp_path / "output"
    output_dir.mkdir()
    match_file = output_dir / "matched-pattern.txt"

    result = runner.invoke(main, [
        '-r', 'TestRule',
        '-f', 'office',
        '-i', str(input_dir),
        '-m', str(match_file),
        '-o', '2',
        '-t', 'TestTag',
        '-a', 'Test Author',
        '-d', 'Test Description'
    ], catch_exceptions=False)

    assert result.exit_code == 0

    yara_file = output_dir / "testrule.yar"
    assert yara_file.exists()

    yara_content = yara_file.read_text()
    assert "rule TestRule : TestTag {" in yara_content
    assert "author = \"Test Author\"" in yara_content
    assert "description = \"Test Description\"" in yara_content
    assert "sample_filetype = \"office\"" in yara_content
    assert "$string1 = \"dummy data string 1\"" in yara_content
    assert "any of them" in yara_content


def test_main_invalid_rulename(tmp_path: pathlib.Path):
    runner = CliRunner()

    result = runner.invoke(main, [
        '-r', '123InvalidRule',
        '-f', 'office'
    ])

    assert result.exit_code == 1


def test_main_no_matching_pattern(tmp_path: pathlib.Path):
    runner = CliRunner()

    input_dir = tmp_path / "input_samples_no_match"
    input_dir.mkdir()

    dummy_file1 = input_dir / "sample1.bin"
    dummy_file1.write_bytes(b"data string A\ndata string B\n")

    dummy_file2 = input_dir / "sample2.bin"
    dummy_file2.write_bytes(b"data string C\ndata string D\n")

    output_dir = tmp_path / "output_no_match"
    output_dir.mkdir()
    match_file = output_dir / "matched-pattern-none.txt"

    result = runner.invoke(main, [
        '-r', 'NoMatchRule',
        '-f', 'office',
        '-i', str(input_dir),
        '-m', str(match_file),
        '-o', '2'
    ])

    assert result.exit_code == 0
    assert not match_file.exists()

import os
import tempfile
import pytest
from click.testing import CliRunner
import yarasilly2

def test_main_invalid_rulename(mocker):
    mocker.patch('yarasilly2.puts')
    runner = CliRunner()
    result = runner.invoke(yarasilly2.main, ['-r', '123invalid', '-f', 'office'])
    assert result.exit_code == 1

def test_main_abort_create_folder(mocker):
    mocker.patch('yarasilly2.puts')
    runner = CliRunner()
    result = runner.invoke(yarasilly2.main, ['-r', 'ValidRule', '-f', 'office', '-i', '/tmp/nonexistent_yara_silly', '--loglevel', 'DEBUG'], input='n\n')
    assert result.exit_code == 0
    assert "Exciting application." in result.output

def test_main_keyboard_interrupt(mocker):
    mocker.patch('yarasilly2.puts')
    mocker.patch('yarasilly2.os.makedirs', side_effect=KeyboardInterrupt)
    runner = CliRunner()
    result = runner.invoke(yarasilly2.main, ['-r', 'ValidRule', '-f', 'office', '-i', '/tmp/should_create_yara_silly', '--loglevel', 'DEBUG'], input='y\n')
    assert result.exit_code == 1

def test_main_oserror(mocker):
    mocker.patch('yarasilly2.puts')
    mocker.patch('yarasilly2.os.makedirs', side_effect=OSError)
    runner = CliRunner()
    result = runner.invoke(yarasilly2.main, ['-r', 'ValidRule', '-f', 'office', '-i', '/tmp/should_create_yara_silly2', '--loglevel', 'DEBUG'], input='y\n')
    assert result.exit_code == 1

def test_main_no_pattern_found(mocker):
    mocker.patch('yarasilly2.puts')
    mocker.patch('yarasilly2.os.remove')

    # Mocking FindFiles to return empty list
    mocker.patch('yarasilly2.FindFiles.searchFiles', return_value=[])
    mocker.patch('yarasilly2.StringDump.dumpStringsToTempFile')

    # Mocking listdir to return an empty list or let SearchPattern find 0
    mocker.patch('yarasilly2.listdir', return_value=['dummy_file'])
    mocker.patch('yarasilly2.SearchPattern.search', return_value=0)

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, 'input')
        os.makedirs(input_dir)
        match_file = os.path.join(temp_dir, 'match.txt')

        result = runner.invoke(yarasilly2.main, ['-r', 'ValidRule', '-f', 'office', '-i', input_dir, '-m', match_file, '--loglevel', 'DEBUG'])

        assert result.exit_code == 0
        yarasilly2.os.remove.assert_called_with(match_file)

def test_main_pattern_found(mocker):
    mocker.patch('yarasilly2.puts')

    # Mocking FindFiles
    mocker.patch('yarasilly2.FindFiles.searchFiles', return_value=['/dummy/path/to/virus.exe'])
    mocker.patch('yarasilly2.StringDump.dumpStringsToTempFile')
    mocker.patch('yarasilly2.md5sum', return_value='dummyhash')

    # Mocking SearchPattern to find 1
    mocker.patch('yarasilly2.listdir', return_value=['dummy_file'])
    mocker.patch('yarasilly2.SearchPattern.search', return_value=1)

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, 'input')
        os.makedirs(input_dir)
        match_file = os.path.join(temp_dir, 'match.txt')

        with open(match_file, 'w') as f:
            f.write("dummyhash-this_is_a_dummy_string\n")
            f.write("dummyhash-another_string_with_\x00\n")

        result = runner.invoke(yarasilly2.main, ['-r', 'ValidRule', '-f', 'office', '-i', input_dir, '-m', match_file, '--loglevel', 'DEBUG'])

        assert result.exit_code == 0

        yara_file = os.path.join(temp_dir, 'validrule.yar')
        assert os.path.exists(yara_file)
        with open(yara_file, 'r') as f:
            content = f.read()
            assert "ValidRule" in content
            assert "this_is_a_dummy_string" in content
            assert "another_string_with_" in content

def test_main_fuzzymatch(mocker):
    mocker.patch('yarasilly2.puts')
    mock_fuzzy = mocker.patch('yarasilly2.FuzzyMatch')

    mocker.patch('yarasilly2.FindFiles.searchFiles', return_value=[])
    mocker.patch('yarasilly2.listdir', return_value=[])

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, 'input')
        os.makedirs(input_dir)
        match_file = os.path.join(temp_dir, 'match.txt')

        # Mock os.remove to prevent errors during failure paths
        mocker.patch('yarasilly2.os.remove')

        confirm_dir = os.path.join(temp_dir, 'confirm')
        probable_dir = os.path.join(temp_dir, 'probable')

        result = runner.invoke(yarasilly2.main, ['-r', 'ValidRule', '-f', 'office', '-i', input_dir, '-m', match_file, '-fm', confirm_dir, '80', probable_dir, '60', '--loglevel', 'DEBUG'])

        assert result.exit_code == 0
        mock_fuzzy.assert_called_with(confirm_dir, 80, probable_dir, 60, input_dir)
        mock_fuzzy.return_value.searchFiles.assert_called_once()

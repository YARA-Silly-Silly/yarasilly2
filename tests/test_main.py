import pytest
import os
import shutil
from click.testing import CliRunner
import yarasilly2
from yarasilly2 import main

def test_main_invalid_rulename(mocker):
    mock_puts = mocker.patch('yarasilly2.puts')
    runner = CliRunner()
    result = runner.invoke(main, ['--rulename', '1Invalid', '--filetype', 'office'])
    assert result.exit_code == 1
    assert mock_puts.called

def test_main_success(mocker):
    mock_puts = mocker.patch('yarasilly2.puts')
    mocker.patch('yarasilly2.FileSystemLoader')
    mock_env = mocker.patch('yarasilly2.Environment')
    mock_template = mocker.Mock()
    mock_env.return_value.get_template.return_value = mock_template
    mock_template.render.return_value = "rule ValidRule {}"

    class FakeConfig:
        def read(self, path):
            pass
        def __getitem__(self, key):
            if key == 'DEFAULT':
                return {
                    'inputFilesPath': './input-folder',
                    'matchPatternFilePath': './output',
                    'matchPatternFileName': 'matched-pattern.txt',
                    'folderDepth': '1',
                    'occurance': '5',
                    'blocksize': '8192'
                }
            elif key == 'LOG':
                return {
                    'logFilePath': './log',
                    'logFileName': 'yarasilly2.log'
                }
            return {}

    mocker.patch('yarasilly2.configparser.ConfigParser', return_value=FakeConfig())

    mocker.patch('yarasilly2.os.path.exists', return_value=True)
    mocker.patch('yarasilly2.os.makedirs')
    mocker.patch('yarasilly2.os.remove')
    mocker.patch('yarasilly2.shutil.rmtree')

    mocker.patch('yarasilly2.FuzzyMatch')
    mock_find_files = mocker.patch('yarasilly2.FindFiles')
    mock_find_files.return_value.searchFiles.return_value = ['dummy_file.doc']

    mocker.patch('yarasilly2.StringDump')
    mocker.patch('yarasilly2.md5sum', return_value='d41d8cd98f00b204e9800998ecf8427e')
    mocker.patch('yarasilly2.listdir', return_value=['dummy_tmp_file.tmp'])

    mock_search = mocker.patch('yarasilly2.SearchPattern')
    mock_search.return_value.search.return_value = 1

    mock_file = mocker.mock_open(read_data='10-pattern1\n')
    mocker.patch('builtins.open', mock_file)

    runner = CliRunner()
    result = runner.invoke(main, ['--rulename', 'ValidRule', '--filetype', 'office', '--loglevel', 'INFO'])

    assert result.exit_code == 0
    assert mock_template.render.called

def test_main_no_matching_pattern(mocker):
    mock_puts = mocker.patch('yarasilly2.puts')
    mocker.patch('yarasilly2.FileSystemLoader')
    mock_env = mocker.patch('yarasilly2.Environment')

    class FakeConfig:
        def read(self, path):
            pass
        def __getitem__(self, key):
            if key == 'DEFAULT':
                return {
                    'inputFilesPath': './input-folder',
                    'matchPatternFilePath': './output',
                    'matchPatternFileName': 'matched-pattern.txt',
                    'folderDepth': '1',
                    'occurance': '5',
                    'blocksize': '8192'
                }
            elif key == 'LOG':
                return {
                    'logFilePath': './log',
                    'logFileName': 'yarasilly2.log'
                }
            return {}

    mocker.patch('yarasilly2.configparser.ConfigParser', return_value=FakeConfig())
    mocker.patch('yarasilly2.os.path.exists', return_value=True)
    mocker.patch('yarasilly2.os.makedirs')
    mock_remove = mocker.patch('yarasilly2.os.remove')
    mocker.patch('yarasilly2.shutil.rmtree')

    mocker.patch('yarasilly2.FindFiles')
    mocker.patch('yarasilly2.StringDump')
    mocker.patch('yarasilly2.listdir', return_value=[])

    mock_search = mocker.patch('yarasilly2.SearchPattern')
    mock_search.return_value.search.return_value = 0

    runner = CliRunner()
    result = runner.invoke(main, ['--rulename', 'ValidRule', '--filetype', 'office'])

    assert result.exit_code == 0
    assert mock_remove.called

def test_main_abort_dir_creation(mocker):
    mocker.patch('yarasilly2.FileSystemLoader')
    mock_env = mocker.patch('yarasilly2.Environment')

    class FakeConfig:
        def read(self, path):
            pass
        def __getitem__(self, key):
            if key == 'DEFAULT':
                return {
                    'inputFilesPath': './input-folder',
                    'matchPatternFilePath': './output',
                    'matchPatternFileName': 'matched-pattern.txt',
                    'folderDepth': '1',
                    'occurance': '5',
                    'blocksize': '8192'
                }
            elif key == 'LOG':
                return {
                    'logFilePath': './log',
                    'logFileName': 'yarasilly2.log'
                }
            return {}

    mocker.patch('yarasilly2.configparser.ConfigParser', return_value=FakeConfig())
    mocker.patch('yarasilly2.os.path.exists', return_value=False)

    runner = CliRunner()
    result = runner.invoke(main, ['--rulename', 'ValidRule', '--filetype', 'office'], input='n\n')

    assert result.exit_code == 0

def test_main_exception(mocker):
    mock_puts = mocker.patch('yarasilly2.puts')
    mocker.patch('yarasilly2.FileSystemLoader')
    mock_env = mocker.patch('yarasilly2.Environment')

    mocker.patch('yarasilly2.configparser.ConfigParser', side_effect=Exception("Test Exception"))

    runner = CliRunner()
    result = runner.invoke(main, ['--rulename', 'ValidRule', '--filetype', 'office'])

    assert result.exit_code == 1
    assert mock_puts.called

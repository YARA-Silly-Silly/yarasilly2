import pytest
from click.testing import CliRunner
import yarasilly2

def test_rulename_validation_valid(mocker):
    # Mock puts and sys.exit to avoid exiting during normal flow if there are other errors
    mock_puts = mocker.patch('yarasilly2.puts')
    mock_exit = mocker.patch('sys.exit')

    # We patch FileSystemLoader and Environment so the rest of the script doesn't fail
    mocker.patch('yarasilly2.FileSystemLoader')
    mocker.patch('yarasilly2.Environment')
    mocker.patch('yarasilly2.configparser.ConfigParser')

    runner = CliRunner()
    runner.invoke(yarasilly2.main, ['-r', 'ValidRuleName_123', '-f', 'office'])

    # puts should not be called with the error message
    for call in mock_puts.call_args_list:
        assert 'Wrong pattern for rule name.' not in str(call)

def test_rulename_validation_invalid_path_traversal(mocker):
    mock_puts = mocker.patch('yarasilly2.puts')
    mock_exit = mocker.patch('sys.exit')

    runner = CliRunner()
    runner.invoke(yarasilly2.main, ['-r', '../invalid/rule', '-f', 'office'])

    # puts should be called with the error message
    called_with_error = False
    for call in mock_puts.call_args_list:
        if 'Wrong pattern for rule name.' in str(call):
            called_with_error = True
            break

    assert called_with_error, "Expected puts to be called with 'Wrong pattern for rule name.'"

    # Check if mock_exit was called with 1 at least once
    assert mocker.call(1) in mock_exit.call_args_list, "Expected sys.exit(1) to be called"

def test_rulename_validation_invalid_characters(mocker):
    mock_puts = mocker.patch('yarasilly2.puts')
    mock_exit = mocker.patch('sys.exit')

    runner = CliRunner()
    runner.invoke(yarasilly2.main, ['-r', 'rule@name!', '-f', 'office'])

    called_with_error = False
    for call in mock_puts.call_args_list:
        if 'Wrong pattern for rule name.' in str(call):
            called_with_error = True
            break

    assert called_with_error, "Expected puts to be called with 'Wrong pattern for rule name.'"

    # Check if mock_exit was called with 1 at least once
    assert mocker.call(1) in mock_exit.call_args_list, "Expected sys.exit(1) to be called"

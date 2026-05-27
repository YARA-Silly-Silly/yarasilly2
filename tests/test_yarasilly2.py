import pytest
from click.testing import CliRunner
from unittest.mock import patch
import sys

import yarasilly2

def test_main_generic_exception():
    runner = CliRunner()

    with patch('configparser.ConfigParser.read', side_effect=Exception("Generic Error")):
        with patch('yarasilly2.puts') as mock_puts:
            result = runner.invoke(yarasilly2.main, ['-r', 'testrule', '-f', 'office'])

            assert result.exit_code == 1

            mock_puts.assert_called()
            # Verify the printed error message by checking if the expected text is in any of the call arguments
            called_with_error = any("[!] Error executing application." in str(call.args[0]) for call in mock_puts.call_args_list)
            assert called_with_error

def test_main_oserror():
    runner = CliRunner()

    with patch('configparser.ConfigParser.read', side_effect=OSError("OS Error")):
        with patch('yarasilly2.puts') as mock_puts:
            result = runner.invoke(yarasilly2.main, ['-r', 'testrule', '-f', 'office'])

            assert result.exit_code == 1

            mock_puts.assert_called()
            called_with_error = any("[!] Error executing application." in str(call.args[0]) for call in mock_puts.call_args_list)
            assert called_with_error

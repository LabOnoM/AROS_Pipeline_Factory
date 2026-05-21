import sys
import os
import importlib.util
from unittest.mock import patch, MagicMock
import tempfile
import pytest

script_path = os.path.expanduser("~/.gemini/skills/iterative-validator/scripts/main.py")
spec = importlib.util.spec_from_file_location("validator_main", script_path)
validator_main = importlib.util.module_from_spec(spec)
sys.modules["validator_main"] = validator_main
spec.loader.exec_module(validator_main)

class TestIterativeValidator:
    @patch('validator_main._run_gtb_validator')
    def test_successful_validation(self, mock_validator, tmpdir):
        # Setup mock
        mock_validator.return_value = (True, {"passed": True, "score": 9.0})
        
        dest_path = os.path.join(tmpdir, "dest.md")
        
        test_args = ["main.py", "--content", "Initial draft", "--destination", dest_path, "--task-type", "code_generation"]
        
        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit) as e:
                validator_main.main()
                
            assert e.value.code == 0
        
        assert mock_validator.call_count == 1
        assert os.path.exists(dest_path)
        with open(dest_path, "r") as f:
            assert f.read() == "Initial draft"

    @patch('validator_main._run_gtb_validator')
    @patch('validator_main._regenerate_content_with_feedback')
    def test_self_correction_loop(self, mock_regenerate, mock_validator, tmpdir):
        # Mock validator to fail once, then succeed
        mock_validator.side_effect = [
            (False, {"passed": False, "score": 5.0, "reasoning": "Needs improvement"}),
            (True, {"passed": True, "score": 8.5})
        ]
        
        # Mock regeneration to return updated content
        mock_regenerate.return_value = "Improved draft"
        
        dest_path = os.path.join(tmpdir, "dest2.md")
        test_args = ["main.py", "--content", "Initial draft", "--destination", dest_path, "--task-type", "code_generation"]
        
        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit) as e:
                validator_main.main()
                
            assert e.value.code == 0
            
        assert mock_validator.call_count == 2
        assert mock_regenerate.call_count == 1
        
        assert os.path.exists(dest_path)
        with open(dest_path, "r") as f:
            assert f.read() == "Improved draft"

    @patch('validator_main._run_gtb_validator')
    @patch('validator_main._escalate_for_review')
    def test_infinite_recursion_prevention(self, mock_escalate, mock_validator, tmpdir):
        # Mock validator to fail always
        mock_validator.return_value = (False, {"passed": False, "score": 4.0, "reasoning": "Still bad"})
        
        dest_path = os.path.join(tmpdir, "dest3.md")
        test_args = ["main.py", "--content", "Initial draft", "--destination", dest_path, "--task-type", "code_generation"]
        
        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit) as e:
                validator_main.main()
                
            assert e.value.code == 1
            
        assert mock_validator.call_count == validator_main.MAX_RETRIES
        assert mock_escalate.call_count == 1

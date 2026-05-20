# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import unittest
from task_executor import TaskExecutor, CriticalInputMissingError

class TestTaskExecutor(unittest.TestCase):
    def setUp(self):
        self.task_def = {
            'name': 'GenerateUserReport',
            'critical_inputs': ['user_id', 'database_connection_string'],
            'alternative_strategies': [
                'Generate a generic report for all users.',
                'Cancel report generation.'
            ]
        }
        self.executor = TaskExecutor(self.task_def)

    def test_missing_inputs_halts_execution(self):
        inputs = {'user_id': 'user-123'} # missing database_connection_string
        with self.assertRaises(CriticalInputMissingError) as context:
            self.executor.execute_task(inputs)
        
        # Verify it identifies the missing input
        self.assertIn('database_connection_string', context.exception.missing_inputs)
        self.assertNotIn('user_id', context.exception.missing_inputs)
        
        # Verify the formatted message requests user input
        message = context.exception.formatted_message()
        self.assertIn("Execution HALTED", message)
        self.assertIn("Critical input(s) missing", message)
        self.assertIn("Please provide the missing information", message)
        
        # Verify alternative strategies are present
        self.assertIn("Generate a generic report for all users.", message)

    def test_complete_inputs_executes_successfully(self):
        inputs = {
            'user_id': 'user-123',
            'database_connection_string': 'postgresql://user:pass@host:port/db'
        }
        try:
            result = self.executor.execute_task(inputs)
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['task'], 'GenerateUserReport')
        except CriticalInputMissingError:
            self.fail("execute_task() raised CriticalInputMissingError unexpectedly!")

if __name__ == '__main__':
    unittest.main()

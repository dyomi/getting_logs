from unittest import TestCase
from unittest.mock import patch, Mock


class TestGetLog(TestCase):
    @patch('getting_logs.GetLog')
    def test_logs_get(self, Mock):
        logs = Mock()

        logs.get.return_value = {
            'error': '',
            'logs': [{
                'сreated_at': '2021-01-23T12:33:14',
                'first_name': 'Матвей',
                'message': 'I"m not sure. Come on!',
                'second_name': 'Иванов',
                'user_id': '726462'
            }]
        }

        response = logs.get('123')
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(response, logs.get.return_value)

    @patch('getting_logs.GetLog')
    def test_error_get(self, Mock):
        logs = Mock()

        logs.get.return_value = {
            'error': 'created_day: does not match format 20200105'
        }

        response = logs.get('123')
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(response, logs.get.return_value)

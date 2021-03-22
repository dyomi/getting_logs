from unittest import TestCase
from unittest.mock import patch, Mock


class TestGetLog(TestCase):
    """Testing of getting logs from a third-party resource,
    saving them to a local database."""

    @patch('getting_logs.GetLog')
    def test_logs_get(self, MockGetLog):
        logs = MockGetLog()

        logs.get.return_value = {
            'error': '',
            'logs': [{
                'сreated_at': '2021-01-23T12:33:14',
                'first_name': 'А',
                'message': 'Write the code!',
                'second_name': 'B',
                'user_id': '123456'
            }]
        }

        response = logs.get()
        self.assertIsNotNone(response, 'Ошибка. Пустой объект.')
        self.assertIsInstance(response, dict, 'Ошибка. Получен не json.')
        self.assertEqual(
            response,
            logs.get.return_value,
            'Ошибка. Получены неверные данные.')

    @patch('getting_logs.GetLog')
    def test_error_get(self, MockGetLog):
        logs = MockGetLog()

        logs.get.return_value = {
            'error': 'created_day: does not match format 20200105'
        }

        response = logs.get()
        self.assertIsNotNone(response, 'Ошибка. Пустой объект.')
        self.assertIsInstance(response, dict, 'Ошибка. Получен не json.')
        self.assertEqual(response,
                         logs.get.return_value,
                         'Ошибка. Получены неверные данные.')

    @patch('getting_logs.GetLog')
    def test_saving_logs(self, mock_saving_logs):
        return_value = {
            'error': '',
            'logs': [{
                'сreated_at': '2021-01-23T12:33:14',
                'first_name': 'А',
                'message': 'Write the code!',
                'second_name': 'B',
                'user_id': '123456'
            }]
        }
        logs = Mock(return_value)
        mock_saving_logs.return_value = logs
        self.assertIsInstance(mock_saving_logs.return_value, dict,
                              'Ошибка. Сохранение в базу происходит неверно')
        self.assertTrue(mock_saving_logs.return_value,
                        'Ошибка. В базу данных ничего не сохраняется')

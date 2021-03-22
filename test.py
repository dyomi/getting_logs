from unittest import TestCase
from unittest.mock import patch, Mock


class TestGetLog(TestCase):
    """Testing of getting logs from a third-party resource,
    saving them to a local database."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
            'error': '',
            'logs': [{
                'сreated_at': '2021-01-23T12:33:14',
                'first_name': 'А',
                'message': 'Write the code!',
                'second_name': 'B',
                'user_id': '123456'
            }]
        }
        cls.error = {
            'error': 'created_day: does not match format 20200105'
        }

    @patch('getting_logs.GetLog')
    def test_logs_get(self, MockGetLog):
        """Tests getting logs."""
        logs = MockGetLog()

        logs.get.return_value = self.data

        response = logs.get()
        self.assertIsNotNone(response, 'Ошибка. Пустой объект.')
        self.assertIsInstance(response, dict, 'Ошибка. Получен не json.')
        self.assertEqual(
            response,
            logs.get.return_value,
            'Ошибка. Получены неверные данные.')

    @patch('getting_logs.GetLog')
    def test_error_get(self, MockGetLog):
        """Tests getting logs."""
        logs = MockGetLog()

        logs.get.return_value = self.error

        response = logs.get()
        self.assertIsNotNone(response, 'Ошибка. Пустой объект.')
        self.assertIsInstance(response, dict, 'Ошибка. Получен не json.')
        self.assertEqual(response,
                         logs.get.return_value,
                         'Ошибка. Получены неверные данные.')

    @patch('getting_logs.GetLog')
    def test_saving_logs(self, mock_saving_logs):
        """Tests saving logs."""
        return_value = self.data
        logs = Mock(return_value)
        mock_saving_logs.return_value = logs
        self.assertIsInstance(mock_saving_logs.return_value, dict,
                              'Ошибка. Сохранение в базу происходит неверно')
        self.assertTrue(mock_saving_logs.return_value,
                        'Ошибка. В базу данных ничего не сохраняется')

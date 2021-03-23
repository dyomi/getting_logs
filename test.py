from unittest import TestCase
from unittest.mock import patch


class TestGetLog(TestCase):
    """Testing of getting logs from a third-party resource."""

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

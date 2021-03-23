from unittest import TestCase
from unittest.mock import patch

import getting_logs


class TestGetLog(TestCase):
    """Testing of getting logs from a third-party resource.
    Testing the correctness of the transmitted data
    for saving to the database."""

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
    def test_saving_logs(self, MockGetLog):
        """Tests the correctness of the transmitted data."""
        get_log = MockGetLog()
        get_log.get.return_value = self.data
        logs = get_log.get()
        get_log.saving_logs(logs)
        self.assertEqual(
            MockGetLog,
            getting_logs.GetLog,
            'Ошибка. На сохранение в базу передаются неправильные данные.')
        self.assertIsNotNone(
            MockGetLog.called,
            'Ошибка. В базу ничего не сохраняется.')
        get_log.get.assert_called_with()

        get_log.saving_logs.assert_called_once_with(get_log.get.return_value)

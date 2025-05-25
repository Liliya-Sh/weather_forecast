import unittest

from weather_forecast.app.location import location


class Testlibrary(unittest.TestCase):
    """Тесты на для проверки работы функций"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_location(self):
        """Тестируем функцию location(определить широту и долготу по наименованию города.)"""
        city = (55.625578, 37.6063916)

        actual_result = location('Москва')
        self.assertEqual(actual_result, city)

    def test_location_none(self):
        """Тестируем функцию location(определить широту и долготу без данных.)"""
        city = (None, None)

        actual_result = location('')
        self.assertEqual(actual_result, city)


if __name__ == '__main__':
    unittest.main()

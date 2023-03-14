from freezegun import freeze_time
import unittest
import sys

sys.path.insert(1, "../module2")

from app import app
from decoder import decrypt
from database import Person


class TestViews(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_can_get_correct_username_with_weekdate(self):
        freezer = freeze_time("2023-03-12")

        name = "Хорошего воскресенья"

        url = f"/hello-world/{name}"
        freezer.start()
        response = self.app.get(url)
        freezer.stop()

        response_text = response.data.decode()
        self.assertIn('воскресенья!', response_text)
        # Проверяется именно последнее значение дня недели, потому что только оно идет с восклицательным знаком

    def test_is_decrypt_work_good(self):
        examples = (
            ('абра-кадабра.', 'абра-кадабра'),
            ('абраа..-кадабра', 'абра-кадабра'),
            ('абраа..-.кадабра', 'абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра'),
            ('абрау...-кадабра', 'абра-кадабра'),
            ('абра........', ''),
            ('абр......a.', 'a'),
            ('1..2.3', '23'),
            ('1.......................', '')
        )

        for example in examples:
            self.assertEqual(example[1], decrypt(example[0]))

    def test_finance_accounting_add_new(self):
        data = {
            20220413: 1000,
            20220516: 4000,
            2013: 1442
        }

        for date, value in data.items():
            url = f"/add/{date}/{value}"
            response = self.app.get(url)
            self.assertIn("записана", response.data.decode())

    def test_finance_accounting_calculate_by_year(self):
        years = [2022, 1942, 2023]
        for year in years:
            url = f"/calculate/{year}"
            response_text = self.app.get(url).data.decode()
            self.assertIn("Сумма", response_text)

    def test_finance_accounting_calculate_by_year_and_month(self):
        data = {
            2022: 12,
            2020: 11,
            2024: 150
        }

        for year, month in data.items():
            url = f"/calculate/{year}/{month}"
            response_text = self.app.get(url).data.decode()
            self.assertIn("Сумма", response_text)

    def test_database_profile(self):
        person = Person(name='test', year_of_birth=2000)

        returned_age = person.get_age()
        current_age = 23
        self.assertEqual(current_age, returned_age)

        name = 'other_test'
        person.set_name(name)
        returned_name = person.get_name()
        self.assertEqual(name, returned_name)

        address = 'Moscow'
        person.set_address(address)
        returned_address = person.get_address()
        self.assertEqual(address, returned_address)

        returned_is_homeless = person.is_homeless()
        self.assertEqual(False, returned_is_homeless)

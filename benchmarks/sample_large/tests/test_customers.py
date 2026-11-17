import unittest

from depot.core.errors import CreditLimitExceeded, ValidationError
from depot.customers.credit import check_credit
from depot.customers.customer import Customer
from depot.customers.loyalty import points_for, tier


class CustomerTests(unittest.TestCase):
    def test_tiers(self):
        self.assertEqual([tier(0), tier(500), tier(1000)], ["standard", "silver", "gold"])

    def test_points(self):
        self.assertEqual(points_for(1999), 19)

    def test_bad_email(self):
        with self.assertRaises(ValidationError):
            Customer("C2", "Bob", "not-an-email")

    def test_credit(self):
        with self.assertRaises(CreditLimitExceeded):
            check_credit(499_00, 2_00)

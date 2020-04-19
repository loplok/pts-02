import unittest
from itertools import count

from pts2 import Library


class ReservationMockTrue(object):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        self._id = next(ReservationMockTrue._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0

    def overlapping(self, other):
        return True

    def includes(self, date):
        return True


class ReservationMockFalse(ReservationMockTrue):
    def overlapping(self, other):
        return False

    def includes(self, date):
        return False


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.true = Library(ReservationMockTrue)
        self.false = Library(ReservationMockFalse)
        self.true.add_user("Patrik")
        self.false.add_user("Patrik")
        self.true.add_user("Rici")
        self.true.add_book("1")
        self.false.add_book("1")
        self.true.reserve_book("Patrik", "1", 1, 5)
        self.false.reserve_book("Patrik", "1", 1, 5)

    def test___init__(self):
        self.assertEqual(len(self.true._reservations), 1)
        self.assertEqual(len(self.true._users), 2)
        self.assertEqual(len(self.true._books), 1)

    def test_add_user(self):
        self.assertTrue(self.true.add_user("ja"))
        self.assertEqual(len(self.true._users), 3)
        self.assertEqual(len(self.true._books), 1)
        self.assertEqual(len(self.true._reservations), 1)
        self.assertTrue(self.true.add_user("Feri"))
        self.assertEqual(len(self.true._users), 4)
        self.assertEqual(len(self.true._books), 1)
        self.assertEqual(len(self.true._reservations), 1)

    def test_add_book(self):
        self.assertEqual(len(self.true._books), 1)
        self.true.add_book("2")
        self.true.add_book("3")
        self.assertEqual(len(self.true._books), 3)

    def test_reserve_book(self):
        self.assertEqual(self.false.reserve_book("Feri", "book", 1, 5), -1)
        self.assertEqual(self.false.reserve_book("Patrik", "1", 1, 5), -1)

    def test_reserve_failure(self):
        self.assertEqual(self.true.reserve_book("Patrik", "1", 5, 1), -1)
        self.assertEqual(self.true.reserve_book("Feri", "1", 10, 15), -1)
        self.assertEqual(self.true.reserve_book("Patrik", "3", 1, 5), -1)
        self.assertEqual(self.true.reserve_book("Patrik", "1", 1, 4), -1)

    def test_check_reservation(self):
        self.assertTrue(self.true.check_reservation("Patrik", "1", 2))
        self.assertTrue(self.true.check_reservation("Patrik", "1", 5))
        self.assertTrue(self.true.check_reservation("Patrik", "1", 1))
        self.assertFalse(self.true.check_reservation("Patrik", "1", 8))

    def test_change_reservation(self):
        self.assertEqual(self.false.change_reservation("Patrik", "1", 1, "Rici"), False)
        self.assertEqual(self.false.change_reservation("Patrik", "2", 1, "Feri"), False)
        self.assertEqual(self.true.change_reservation("Patrik", "1", 1, "Rici"), True)

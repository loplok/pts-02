import unittest
from pts2 import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = Library()

    def test___init__(self):
        self.assertEqual(len(self.lib._reservations), 0)
        self.assertEqual(len(self.lib._users), 0)
        self.assertEqual(len(self.lib._books), 0)

    def test_add_user(self):
        self.assertTrue(self.lib.add_user("ja"))
        self.assertEquals(len(self.lib._users), 1)
        self.assertEquals(len(self.lib._books), 0)
        self.assertEquals(len(self.lib._reservations), 0)
        self.assertTrue(self.lib.add_user("User2"))
        self.assertEquals(len(self.lib._users), 2)
        self.assertEquals(len(self.lib._books), 0)
        self.assertEquals(len(self.lib._reservations), 0)

    def test_add_book(self):
        self.lib.add_book("book")

    def test_reserve_book(self):
        self.assertFalse(self.lib.reserve_book("User1", "Book1", 1, 5))
        self.assertTrue(self.lib.add_user("User1"))
        self.assertFalse(self.lib.reserve_book("User1", "Book1", 1, 5))
        self.lib.add_book("Book1")
        self.assertFalse(self.lib.reserve_book("User1", "Book2", 1, 5))
        self.assertFalse(self.lib.reserve_book("User2", "Book1", 1, 5))
        self.assertFalse(self.lib.reserve_book("User1", "Book1", 3, 2))
        self.assertTrue(self.lib.reserve_book("User1", "Book1", 1, 5))
        self.assertFalse(self.lib.reserve_book("User1", "Book1", 1, 5))
        self.assertTrue(self.lib.add_user("User2"))
        self.assertTrue(self.lib.reserve_book("User2", "Book1", 6, 7))

    def test_check_reservation(self):
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 1))
        self.assertTrue(self.lib1.add_user("User1"))
        self.lib1.add_book("Book1")
        self.assertTrue(self.lib1.reserve_book("User1", "Book1", 1, 5))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 0))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 6))
        self.assertTrue(self.lib1.check_reservation("User1", "Book1", 1))
        self.assertTrue(self.lib1.check_reservation("User1", "Book1", 5))
        self.assertTrue(self.lib1.reserve_book("User1", "Book1", 7, 7))
        self.assertTrue(self.lib1.check_reservation("User1", "Book1", 7))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 6))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 8))

    def test_change_reservation(self):
        self.assertFalse(self.lib1.change_reservation("User1", "Book1", 1, "User2"))
        self.assertTrue(self.lib1.add_user("User1"))
        self.lib1.add_book("Book1")
        self.assertTrue(self.lib1.reserve_book("User1", "Book1", 1, 5))
        self.assertFalse(self.lib1.change_reservation("User1", "Book1", 1, "User2"))
        self.assertTrue(self.lib1.add_user("User2"))
        self.assertFalse(self.lib1.check_reservation("User2", "Book1", 1))
        self.assertTrue(self.lib1.change_reservation("User1", "Book1", 1, "User2"))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 1))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 5))
        self.assertTrue(self.lib1.check_reservation("User2", "Book1", 1))

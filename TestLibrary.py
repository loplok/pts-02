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
        self.assertFalse(self.lib.reserve_book("user", "book", 1, 5))


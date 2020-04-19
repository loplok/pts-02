import unittest
from pts2 import Reservation
from itertools import count


class MyTestCase(unittest.TestCase):
    def setUp(self):
        Reservation._ids = count(0)
        self.first_res = Reservation("1", "2", "book1", "user")

    def test___init__(self):
        self.assertEqual(self.first_res._from, "1")
        self.assertEqual(self.first_res._to, "2")
        self.assertEqual(self.first_res._book, "book1")
        self.assertEqual(self.first_res._for, "user")

    def test_overlapping(self):
        self.assertTrue(self.first_res.overlapping(Reservation("2", "4", "book1", "user")))
        self.assertTrue(self.first_res.overlapping(Reservation("0", "1", "book1", "user2")))
        self.assertTrue(self.first_res.overlapping(Reservation("1", "2", "book1", "user3")))

    def test_overlapping_false(self):
        self.assertFalse(self.first_res.overlapping(Reservation("1", "2", "book2", "user")))
        self.assertFalse(self.first_res.overlapping(Reservation("20", "25", "book1", "user")))
        self.assertFalse(self.first_res.overlapping(Reservation("1", "9", "book2", "user")))

    def test_includes(self):
        self.assertTrue(self.first_res.includes("1"))
        self.assertFalse(self.first_res.includes("5"))
        self.assertTrue(self.first_res.includes("2"))
        self.assertFalse(self.first_res.includes("0"))

    def test_identify(self):
        self.assertTrue(self.first_res.identify("1", "book1", "user"))
        self.assertFalse(self.first_res.identify("1", "book2", "user"))
        self.assertFalse(self.first_res.identify("1", "book1", "user2"))
        self.assertFalse(self.first_res.identify("5", "book1", "user"))

    def test_change_for(self):
        self.first_res.change_for("vlado")
        self.assertEqual(self.first_res._for, "vlado")
        self.assertTrue(self.first_res.identify("1", "book1", "vlado"))

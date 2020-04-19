import unittest
from pts2 import Reservation, ReservationMess, LibraryMess
from itertools import count


class TestReservationMess(unittest.TestCase):

    def setUp(self):
        Reservation._ids = count(0)
        self.first_res = ReservationMess(1, 5, "Inferno", "Patrik")

    def test_reservation_init(self):
        self.assertEqual(self.first_res._message, "Created a reservation with id 0 of Inferno from 1 to 5 for Patrik.")

    def test_reservation_overlap(self):
        second_res = ReservationMess(5, 6, "Inferno2", "Martin")
        self.first_res.overlapping(second_res)
        self.assertEqual(self.first_res._message, "Reservations 0 and 1 do not overlap")

        third_res = Reservation(2, 3, "Inferno", "Richard")
        self.first_res.overlapping(third_res)
        self.assertEqual(self._message, "Reservations 0 and 2 do overlap.")

    def test_reserve_change_for(self):
        self.first_res.change_for("Martin")
        self.assertEqual(self._message, "Reservation 0 moved from Patrik to Martin")

    def test_reservation_includes(self):
        pass


class TestLibraryMsg(unittest.TestCase):

    def setUp(self):
        self.library = LibraryMess()
        Reservation._ids = count(0)

    def test_library_init(self):
        self.assertEqual(self.library._message, "Library created.")

    def test_library_add_book(self):
        self.library.add_book("First")
        self.assertEqual(self.library._message, "Book First added. We have 1 copies of the book.")

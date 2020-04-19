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
        self.assertEqual(self.first_res._message, "Reservations 0 and 2 do overlap")

    def test_reserve_change_for(self):
        self.first_res.change_for("Martin")
        self.assertEqual(self.first_res._message, "Reservation 0 moved from Patrik to Martin")

    def test_reserve_identify_false2(self):
        self.first_res.identify(1, "Inferno", "Tomas")
        self.assertEqual(self.first_res._message, "Reservation 0 is for Patrik not Tomas.")

    def test_reserve_identify_false3(self):
        self.first_res.identify(1, "Inferno2", "Patrik")
        self.assertEqual(self.first_res._message, "Reservation 0 reserves Inferno not Inferno2.")

    def test_reserve_identify_false4(self):
        self.first_res.identify(20, "Inferno", "Patrik")
        self.assertEqual(self.first_res._message, "Reservation 0 is from 1 to 5 which does not include 20.")

    def test_reserve_identify_true(self):
        self.first_res.identify(1, "Inferno", "Patrik")
        self.assertEqual(self.first_res._message, "Reservation 0 is valid Patrik of Inferno on 1.")

    def test_reservation_includes(self):
        self.first_res.includes(5)
        self.assertEqual(self.first_res._message, "Reservation 0 includes 5")

    def test_reservation_includes_false1(self):
        self.first_res.includes(10)
        self.assertEqual(self.first_res._message, "Reservation 0 does not include 10")


class TestLibraryMsg(unittest.TestCase):

    def setUp(self):
        self.library = LibraryMess()
        Reservation._ids = count(0)

    def test_library_init(self):
        self.assertEqual(self.library._message, "Library created.")

    def test_library_add_book(self):
        self.library.add_book("Inferno1")
        self.assertEqual(self.library._message, "Book Inferno1 added. We have 1 copies of the book.")
        self.library.add_book("Inferno2")
        self.assertEqual(self.library._message, "Book Inferno2 added. We have 1 copies of the book.")
        self.library.add_book("Inferno2")
        self.assertEqual(self.library._message, "Book Inferno2 added. We have 2 copies of the book.")

    def test_library_add_user_true_and_false(self):
        self.library.add_user("Rici")
        self.assertEqual(self.library._message, "User Rici created.")
        self.library.add_user("Rici")
        self.assertEqual(self.library._message, "User not created, user with name Rici already exists.")

    def test_library_reserve_book_mixed(self):
        self.library.reserve_book("Patrik", "Inferno", 1, 5)
        self.assertEqual(self.library._message,
                         "We cannot reserve book Inferno for Patrik from 1 to 5. User does not exist.")

        self.library.add_user("Patrik")
        self.library.reserve_book("Patrik", "Inferno", 5, 1)
        self.assertEqual(self.library._message,
                         "We cannot reserve book Inferno for Patrik from 5 to 1. Incorrect dates.")

        self.library.reserve_book("Patrik", "Inferno", 1, 5)
        self.assertEqual(self.library._message,
                         "We cannot reserve book Inferno for Patrik from 1 to 5. We do not have that book.")

        self.library.add_book("Inferno")
        self.library.add_user("Rici")
        self.library.reserve_book("Rici", "Inferno", 1, 5)
        self.library.reserve_book("Patrik", "Inferno", 1, 5)
        self.assertEqual(self.library._message,
                         "We cannot reserve book Inferno for Patrik from 1 to 5. We do not have enough books.")

        self.library.reserve_book("Rici", "Inferno", 10, 15)
        self.assertEqual(self.library._message, "Reservation 2 included.")

    def test_library_check_reservation(self):
        self.library.add_book("Inferno")
        self.library.add_user("Patrik")
        self.library.reserve_book("Patrik", "Inferno", 1, 5)
        self.library.check_reservation("Patrik", "Inferno", 3)
        self.assertEqual(self.library._message, "Reservation for Patrik of Inferno on 3 exists.")

    def test_library_change_reservation(self):
        self.library.add_book("Inferno")
        self.library.add_user("Patrik")
        self.library.add_user("Rici")
        self.assertEqual(self.library.reserve_book("Patrik", "Inferno", 1, 5), True)

        self.library.change_reservation("Patrik", "Inferno", 1, "Rici")
        self.assertEqual("Reservation for Patrik of Inferno on 1 changed to Rici.", self.library._message)

        self.library.check_reservation("Rici", "Inferno", 1)
        self.assertEqual(self.library._message, "Reservation for Rici of Inferno on 1 exists.")









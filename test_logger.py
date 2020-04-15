import unittest
from pts2 import LoggerForReservations
from pts2 import Library, Reservation
from itertools import count


class LoggerTest(unittest.TestCase):

    def setUp(self):
        self.first_res = Reservation(1, 5, "Inferno", "Patrik")

    def test_reservation_init(self):
        self.assertEquals(self.first_res.messageToPrint, "Created a reservation with id {} of Inferno from 1 "
                                                         "to 5 for Patrik".format(self.first_res._id))

    def test_reservation_overlap(self):
        self.second_res = Reservation(5, 6, "Inferno2", "Martin")
        LoggerForReservations.reservation_is_overlapping(Reservation.overlapping(self.first_res, self.second_res))
        self.assertEquals(self.first_res.messageToPrint, "Reservations {} and {} do overlap.".
                          format(self.first_res._id, self.second_res._id))

        self.second_res = Reservation(2, 3, "Inferno3", "Richard")
        LoggerForReservations.reservation_is_overlapping(Reservation.overlapping(self.first_res, self.second_res))
        self.assertEquals(self.first_res.messageToPrint, "Reservations {} and {} do not overlap.".
                          format(self.first_res._id, self.second_res._id))

        self.second_res = Reservation(6, 10, "Inferno", "Martin")
        LoggerForReservations.reservation_is_overlapping(Reservation.overlapping(self.first_res, self.second_res))
        self.assertEquals(self.first_res.messageToPrint, "Reservations {} and {} do not overlap.".
                          format(self.first_res._id, self.second_res._id))

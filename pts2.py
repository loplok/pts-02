from itertools import count


# decorators used for Library - type functions used for creating strings
class LoggerForReservations():
    def __init__(self):
        self.messageToPrint = ''

    def LoggerPrinter(function):
        def wrapper(self, *args, **kwargs):
            result = function(self, args, kwargs)
            print(self.messageToPrint)
            return result

        return wrapper

    def library_init(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, *args, **kwargs):
            function(self, *args, **kwargs)
            self.messageToPrint = "Library created."

        return wrapper

    def library_add_user(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, name):
            is_added = function(self, name)
            self.messageToPrint = "User {} created".format(name)
            if not is_added:
                self.messageToPrint = "User {} cannot be created, one with that name exists.".format(name)
            return is_added

        return wrapper

    def library_add_book(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, name):
            function(self, name)
            self.messageToPrint = "Book {} added. We have {} copies of the book".format(name, self._books[name])
            return wrapper

    def library_reserve_book(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, user, book, date_from, date_to):
            is_reserved = function(self, user, book, date_from, date_to)
            if is_reserved >= 0:
                self.messageToPrint = "Reservation {} included".format(is_reserved)
            else:
                if user not in self._users:
                    self.messageToPrint = ("We cannot reserve book {} for {} ".format(book, user) +
                                           "from {} to {}. User does not exist.".format(date_from, date_to))
                    return False
                elif date_to < date_from:
                    self.messageToPrint = ("We cannot reserve book {} for {}".format(book, user) +
                                           " from {} to {}.".format(date_from, date_to) + " Incorrect dates.")
                    return False
                elif self._books.get(book, 0) == 0:
                    self.messageToPrint = ("We cannot reserve book {} for {} from {} ".format(book, user, date_from)
                                           + "to {}. We do not have that book.".format(date_to))
                    return False
                else:
                    self.messageToPrint = ("We cannot reserve book {} for {} from {} ".format(book, user, date_from)
                                           + "to {} . We do not have enough books.".format(date_to))
                    return False
            return True

        return wrapper

    def library_check_reservation(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, user, book, date):
            is_added = function(self, user, book, date)
            str = 'exists'
            if not is_added:
                str = 'does not exist'
            self.messageToPrint = "Reservation for {} of {} on {} {}.".format(user, book, date, str)
            return is_added

        return wrapper

    def library_change_reservation(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, user, book, date, new_user):
            is_identical_reservation = function(self, user, book, date, new_user)
            if not is_identical_reservation:
                self.messageToPrint = "Reservation for {} of {} on {} does not exist".format(user, book, date)
            elif new_user not in self._users:
                self.messageToPrint = "Cannot change the reservation as {} does not exist.".format(new_user)
            else:
                self.messageToPrint = "Reservation for {} of {} on {} change to {}.".format(user, book, date, new_user)
            return is_identical_reservation

        return wrapper

    # decorators for Reservation - type functions used for creating strings
    def reservation_init(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, *args, **kwargs):
            function(self, *args, **kwargs)
            self.messageToPrint = "Reservation create for {} of book {} from {} to {}.".format(self._id, self._book,
                                                                                               self._from, self._to)

        return wrapper

    def reservation_is_overlapping(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, other):
            ret = function(self, other)
            str = 'overlaps'
            if not ret:
                str = 'does not overlap'
            self.messageToPrint = "The {} reservation {} with the {} reservation.".format(self._id, str, other._id)
            return ret

        return wrapper

    def reservation_includes(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, date):
            ret = function(self, date)
            str = 'includes'
            if not ret:
                str = 'does not include'
            self.messageToPrint = "Reservation {} {} {}".format(self._id, str, date)
            return ret

        return wrapper

    def reservation_identify(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, date, book, for_):
            ret = function(self, date, book, for_)
            if not ret:
                if book != self._book:
                    self.messageToPrint = "Reservation {} reserver {} not {}.".format(self._id, self._book, book)
                elif for_ != self._for:
                    self.messageToPrint = ("Reservation {} is for {} not {}".format(self._id, self._for, for_))
                elif not self.includes(date):
                    self.messageToPrint = ("Reservation {} is from {} to ".format(self._id, self._from) +
                                           "{} which does not include {}.".format(self._to, date))
            else:
                self.messageToPrint = "Reservation {} is valid {} of {} on {}.".format(self._id, for_, book, date)
            return ret

        return wrapper

    def reservation_change_for(function):
        @LoggerForReservations.LoggerPrinter
        def wrapper(self, for_):
            function(self, for_)
            self.messageToPrint = "Reservation updated to {}.".format(for_)

        return wrapper


class Reservation(object):
    _ids = count(0)

    @LoggerForReservations.library_init
    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0

    @LoggerForReservations.reservation_is_overlapping
    def overlapping(self, other):
        return (self._book == other._book and self._to >= other._from
                and self._to >= other._from)

    @LoggerForReservations.reservation_includes
    def includes(self, date):
        ret = (self._from <= date <= self._to)
        return ret

    @LoggerForReservations.reservation_identify
    def identify(self, date, book, for_):
        if book != self._book:
            return False
        if for_ != self._for:
            return False
        if not self.includes(date):
            return False
        return True

    @LoggerForReservations.reservation_change_for
    def change_for(self, for_):
        self._for = for_


class Library(object):
    @LoggerForReservations.library_init
    def __init__(self):
        self._users = set()
        self._books = {}  # maps name to count
        self._reservations = []  # Reservations sorted by from

    @LoggerForReservations.library_add_book
    def add_user(self, name):
        if name in self._users:
            return False
        self._users.add(name)
        return True

    @LoggerForReservations.library_add_book
    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1

    @LoggerForReservations.library_resNoneerve_book
    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return False
        if date_from > date_to:
            return False
        if book_count == 0:
            return False
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        # we check that if we add this reservation then for every reservation record that starts
        # between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return False
        self._reservations += [desired_reservation]
        self._reservations.sort(key=lambda x: x._from)  # to lazy to make a getter
        return True

    @LoggerForReservations.library_check_reservation
    def check_reservation(self, user, book, date):
        res = any([res.identify(date, book, user) for res in self._reservations])
        return res

    @LoggerForReservations.library_change_reservation
    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        if not relevant_reservations:
            return False
        if new_user not in self._users:
            return False
        relevant_reservations[0].change_for(new_user)
        return True

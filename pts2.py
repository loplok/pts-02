from itertools import count


class Reservation(object):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0

    def overlapping(self, other):
        return self._book == other._book and self._to >= other._from

    def includes(self, date):
        ret = (self._from <= date <= self._to)
        return ret

    def identify(self, date, book, for_):
        if book != self._book:
            return False
        if for_ != self._for:
            return False
        if not self.includes(date):
            return False
        return True

    def change_for(self, for_):
        self._for = for_
        self._changes += 1


class ReservationMess(Reservation):
    def __init__(self, from_, to, book, for_):
        super().__init__(from_, to, book, for_)
        self._message = "Created a reservation with id {} of {}".format(self._id, self._book)
        self._message += " from {} to {} for {}.".format(self._from, self._to, self._for)

    def overlapping(self, other):
        result = super().overlapping(other)
        str = 'do'
        if not result:
            str = 'do not'
        self._message = "Reservations {} and {} {} overlap".format(self._id, other._id, str)
        return result

    def includes(self, date):
        result = super().includes(date)
        str = 'includes'
        if not result:
            str = 'does not include'
        self._message = "Reservation {} {} {}".format(self._id, str, date)
        return result

    def identify(self, date, book, for_):
        result = super().identify(date, book, for_)
        if result[0]:
            self._message = "Reservation {} is valid {} of {} on {}.".format(self._id, for_, book, date)
        else:
            if result[1] == "book":
                self._message = "Reservation {} reserves {} not {}.".format(self._id, self._book, book)
            elif result[1] == "for":
                self._message = "Reservation {} is for {} not {}.".format(self._id, self._for, for_)
            elif result[1] == "date":
                self._message = "Reservation {} is from {} to {} which ".format(self._id, self._from, self._to)
                self._message += "does not include {}.".format(date)
        return result

    def change_for(self, for_):
        old_for = self._for
        result = super().change_for(for_)
        self._message = "Reservation {} moved from {} to {}".format(self._id, old_for, for_)
        return result


class LoggerForReservations(ReservationMess):
    def __init__(self, from_, to, book, for_):
        super().__init__(from_, to, book, for_)
        print(super()._message)

    def includes(self, date):
        ret = super().includes(date)
        print(super()._message)
        return ret

    def overlapping(self, other):
        ret = super().overlapping(other)
        print(super()._message)
        return ret

    def change_for(self, for_):
        ret = super().change_for(for_)
        print(super()._message)
        return ret

    def identify(self, date, book, for_):
        ret = super().identify(date, book, for_)
        print(super()._message)
        return ret


class Library(object):
    def __init__(self, reservations_factory = Reservation):
        self._users = set()
        self._books = {}  # maps name to count
        self._reservations = []  # Reservations sorted by from

    def add_user(self, name):
        if name in self._users:
            return False
        self._users.add(name)
        return True

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1

    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return -1
        if date_from > date_to:
            return -1
        if book_count == 0:
            return -1
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        # we check that if we add this reservation then for every reservation record that starts
        # between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return -1
        self._reservations += [desired_reservation]
        self._reservations.sort(key=lambda x: x._from)  # to lazy to make a getter
        return desired_reservation._id

    def check_reservation(self, user, book, date):
        return any([res.identify(date, book, user) for res in self._reservations])

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        if not relevant_reservations:
            return False
        if new_user not in self._users:
            return False
        relevant_reservations[0].change_for(new_user)
        return True


class LibraryMess(Library):
    def __init__(self, reservations_factory=Reservation):
        super().__init__(reservations_factory)
        self._message = "Library created."

    def add_user(self, name):
        result = super().add_user(name)
        if result:
            self._message = "User {} created.".format(name)
        else:
            self._message = "User not created, user with name {} already exists.".format(name)
        return result

    def add_book(self, name):
        result = super().add_book(name)
        self._message = "Book {} added. We have {} copies of the book.".format(name, self._books[name])
        return result

    def reserve_book(self, user, book, date_from, date_to):
        is_reserved = super().reserve_book(user, book, date_from, date_to)
        if is_reserved >= 0:
            LoggerForReservations.messageToPrint = "Reservation {} included".format(is_reserved)
        else:
            if user not in self._users:
                LoggerForReservations.messageToPrint = ("We cannot reserve book"
                                                        " {} for {} ".format(book, user) +
                                                        "from {} to {}. User does not exist.".format(date_from,
                                                                                                     date_to))
                return False
            elif date_to < date_from:
                LoggerForReservations.messageToPrint = ("We cannot reserve book {} for {}".format(book, user) +
                                                        " from {} to {}.".format(date_from,
                                                                                 date_to) + " Incorrect dates.")
                return False
            elif self._books.get(book, 0) == 0:
                LoggerForReservations.messageToPrint = (
                    "We cannot reserve book {} for {} from {} "
                    "to {}. We do not have that book.".format(book, user, date_from, date_to))
                return False
            else:
                LoggerForReservations.messageToPrint = ("We cannot reserve book"
                                                        " {} for {} from {} ".format(book, user, date_from))
                ("to {} . We do not have enough books.".format(date_to))
                return False
        return True

    def check_reservation(self, user, book, date):
        is_added = super().check_reservation(user, book, date)
        str = 'exists'
        if not is_added:
            str = 'does not exist'
        LoggerForReservations.messageToPrint = "Reservation for {} of {} on {} {}.".format(user, book, date, str)
        return is_added

    def change_reservation(self, user, book, date, new_user):
        is_identical_reservation = super().change_reservation(user, book, date, new_user)
        if not is_identical_reservation:
            LoggerForReservations.messageToPrint = "Reservation for {} of {} on {} does not exist".format(user,
                                                                                                          book,
                                                                                                          date)
        elif new_user not in self._users:
            LoggerForReservations.messageToPrint = ("Cannot change the reservation as {} " +
                                                    "does not exist.").format(new_user)
        else:
            LoggerForReservations.messageToPrint = "Reservation for {} of {} on {} change to {}.".format(user, book,
                                                                                                         date,
                                                                                                         new_user)
        return is_identical_reservation


class LoggerForLibraryMess(LibraryMess):
    def __init__(self, reservations_factory=Reservation):
        super().__init__(reservations_factory)
        print(super()._message)

    def add_user(self, name):
        ret = super().add_user(name)
        print(super()._message)
        return ret

    def add_book(self, name):
        ret = super().add_book(name)
        print(super()._message)
        return ret

    def reserve_book(self, user, book, date_from, date_to):
        ret = super().reserve_book(user, book, date_from, date_to)
        print(super()._message)
        return ret

    def check_reservation(self, user, book, date):
        ret = super().check_reservation(user, book, date)
        print(super()._message)
        return ret

    def change_reservation(self, user, book, date, new_user):
        ret = super().change_reservation(user, book, date, new_user)
        print(super()._message)
        return ret

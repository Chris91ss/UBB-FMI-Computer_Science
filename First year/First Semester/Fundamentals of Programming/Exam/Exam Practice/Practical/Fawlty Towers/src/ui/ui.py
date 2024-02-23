from datetime import datetime

from texttable import Texttable

from src.controller.controller import Controller


class Ui:

    def __init__(self, controller: Controller):
        self.controller = controller

    def run_ui(self):
        Ui.print_title()

        options = {
            "1": self.display_reservations,
            "2": self.create_reservation,
            "3": self.delete_reservation,
            "4": self.monthly_report,
            "x": Ui.exit
        }

        while True:
            Ui.print_options()
            option = Ui.get_option()

            try:
                options[option]()

            except Exception as error:
                print("\nInvalid input:", error)

    def display_reservations(self):
        reservations = self.controller.get_all_reservations()

        printed_something = False
        for month in ["January", "February", "March", "April", "May", "June", "July",
                      "August", "September", "October", "November", "December"]:
            table = Texttable()
            table.header([month, "Name", "Guests"])

            for reservation in reservations[month]:
                arrival_date = datetime.strftime(reservation.arrival_date, "%m.%d")
                departure_date = datetime.strftime(reservation.departure_date, "%m.%d")

                persons = "persons"
                if reservation.number_of_guests == 1:
                    persons = "person"

                table.add_row([f"{arrival_date} - {departure_date}",
                               reservation.name, f"{reservation.number_of_guests} {persons}"])

            if reservations[month]:
                print(f"\n{table.draw()}")
                printed_something = True

        if not printed_something:
            print("\nNo reservations")

    def create_reservation(self):
        # getting arrival and departure dates
        arrival_date = input("\nArrival date: ")
        arrival_date = datetime.strptime(arrival_date, "%m.%d")

        departure_date = input("Departure date: ")
        departure_date = datetime.strptime(departure_date, "%m.%d")

        # showing available rooms
        available_rooms = self.controller.get_available_rooms(arrival_date, departure_date)
        if available_rooms:
            print("\nAvailable rooms:")
            for room in available_rooms:
                print(f"-> {room.id} - {room.type}")

        # option to cancel
        print("\nTo cancel press: X\nPress any other key to continue.")
        cancel = input(">: ")
        if cancel == "x" or cancel == "X":
            return

        # making the reservation
        room_number = input("\nRoom number: ")
        if room_number not in [room.id for room in available_rooms]:
            raise ValueError("wrong room number")

        name = input("Guest name: ")
        number_of_guests = int(input("Number of guests: "))

        self.controller.create_reservation(room_number, name, number_of_guests, arrival_date, departure_date)

    def delete_reservation(self):
        print("\nPress '1' to delete by reservation id.")
        print("Press '2' to delete by date.")

        option = input(">: ")
        if option == "1":  # BY ID
            reservation_id_to_delete = int(input("\nReservation number: "))
            self.controller.delete_by_id(reservation_id_to_delete)

        elif option == "2":  # BY DATE
            delete_arrival_date = input("\nArrival date: ")
            delete_arrival_date = datetime.strptime(delete_arrival_date, "%m.%d")
            delete_departure_date = input("Departure date: ")
            delete_departure_date = datetime.strptime(delete_departure_date, "%m.%d")
            room_number = input("Room number: ")

            deleted_reservations = self.controller.delete_by_date(delete_arrival_date, delete_departure_date,
                                                                  room_number)
            # displaying the deleted reservations
            printed_something = False
            for month in ["January", "February", "March", "April", "May", "June", "July",
                          "August", "September", "October", "November", "December"]:
                table = Texttable()
                table.header([month, "Name", "Guests"])

                for reservation in deleted_reservations[month]:
                    arrival_date = datetime.strftime(reservation.arrival_date, "%m.%d")
                    departure_date = datetime.strftime(reservation.departure_date, "%m.%d")

                    persons = "persons"
                    if reservation.number_of_guests == 1:
                        persons = "person"

                    table.add_row([f"{arrival_date} - {departure_date}",
                                   reservation.name, f"{reservation.number_of_guests} {persons}"])

                if deleted_reservations[month]:
                    print(f"\n{table.draw()}")
                    printed_something = True

            if not printed_something:
                print("\nNo deleted reservations")

        else:
            print("\nInvalid input")

    def monthly_report(self):
        month = input("\nMonth: ")
        monthly_report = self.controller.get_monthly_report(month)

    @staticmethod
    def exit():
        print("\nGoodbye!")
        exit(1)

    @staticmethod
    def get_option() -> str:
        option = input("\n>: ")
        return option

    @staticmethod
    def print_title():
        print()
        print("# ----------------------------- #")
        print("# ------- Fawlty Towers ------- #")
        print("# ----------------------------- #")

    @staticmethod
    def print_options():
        print("\n1: Display")
        print("2: Create")
        print("3: Delete")
        print("4: Monthly Report")
        print("x: Exit")

from src.repository.txt_repository import TxtRepository
from src.service.flight_service import FlightService
from src.ui.console_menu import ConsoleMenu

if __name__ == "__main__":
    flight_repository = TxtRepository("data/flights.txt")
    flight_service = FlightService(flight_repository)
    ui = ConsoleMenu(flight_service)

    ui.start_ui()

#
# This module is used to invoke the program's UI and start it. It should not contain a lot of code.
#
import ui
import tests


def start():
    ui.print_ui()
    tests.run_all_tests()


start()

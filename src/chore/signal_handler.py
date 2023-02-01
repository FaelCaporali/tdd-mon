from src.tdd_mon import EXIT_EVENT


def exit_handler(signal_number, frame):
    if signal_number == 2:
        print("\n-----\n")
        print("Exiting... Thanks for using!")
        print("\n-----")
    EXIT_EVENT.set()

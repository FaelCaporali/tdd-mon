import threading


EXIT_EVENT = threading.Event()


def exit_handler(signal_number, frame):
    if signal_number == 2:
        print("\n-----\n")
        print("Exiting... Thanks for using!")
        print("\n-----")
    EXIT_EVENT.set()

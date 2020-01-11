import os
import sys

#  /home/kostas/Desktop/TestFolder


def check_path(p):
    if os.path.exists(p):
        print("Given path exists!\n")
    else:
        print("Given path doesn't exit, exiting the script\n")
    # sys.exit()


def check_user_naming(un):
    if not un:
        yield 1
        print("The naming will start from 1 for all files because no convention was selected\n")
    else:
        print("Naming convention accepted")


def checking_folders(p, n):

    for dirpath, dirnames, filenames in os.walk(p):
        counter = 0
        for f in filenames:

            splited_filename = f.split(".")

            try:
                os.rename(dirpath + "/" + f, dirpath + "/" + n + str(counter) + "." + splited_filename[1])
                counter += 1
            except IndexError:
                print("\n")


def main():
    user_path = input("Please give the name of the path that you want to test the script\n")

    user_naming = input("Please give the name of the files\n")

    check_path(user_path)

    checking_folders(user_path, user_naming)

    print("Program finished")


if __name__ == "__main__":
    main()

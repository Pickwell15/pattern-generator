#!/usr/bin/python


from turtle import Turtle, Screen
from json import loads, dumps
from pathlib import Path
from time import sleep
from sys import exit as sysexit
from re import findall
from random import choice
from string import digits, ascii_letters
from os import listdir

_DEFAULT_CONFIG_FILE: str = r"./config.json"
_ALT_CONFIGS_FOLDER: str = r"./alt-configs/"

_NECESSARY_KEYS: tuple[str, ...] = "speed", "height", "width", "side_length", "colours"

_MENU_ITEMS: tuple[str, ...] = "draw pattern", "change config file", "new config file", "quit"

_HEX_CODE_REGEX: str = r"^#(?:[0-9a-fA-F]{3}){1,2}$"


def _load_config(file: str = _DEFAULT_CONFIG_FILE) -> dict[str, int | list[str]]:
    """
    :type file: str
    :param file: The file to load the data from

    :rtype: dict[str, int | list[str]]
    :return: The contents of the specified config file
    """

    return loads(open(file, "r").read())


def _check_valid_file(file: str) -> bool:
    """
    :type file: str
    :param file: File to validate

    :rtype: bool
    :return: If the file is valid or not
    """

    # Checks if file exists and is correct type
    if Path(file).is_file() and Path(file).suffix == ".json":
        for item in _NECESSARY_KEYS:
            # Checks if the file contains the correct items
            if item not in _load_config(file).keys():
                return False
        return True
    return False


def _int_input(text: str) -> int:
    """
    :type text: str
    :param text: The text to display when getting the user input

    :rtype: int
    :return: The user input
    """

    while True:
        try:
            return int(input(text))
        except ValueError:
            print("\nERROR: You didn't enter a number. Please try again...")


def _range_input(text: str, lower: int, upper: int) -> int:
    """
    :type text: str
    :param text: The text to display when getting the user input
    :type lower: int
    :param lower: The lower bound for the user input
    :type upper: int
    :param upper: The upper bound for the user input

    :rtype: int
    :return: A user inputted integer
    """

    while True:
        tmp: int = _int_input(text)

        if lower <= tmp <= upper:
            return tmp

        print(f"\nERROR: Your number wasn't in the correct range of {lower} to {upper}. Please try again...")


def _colour_input(text: str, text_2: str, max_: int = 10) -> list[str]:
    """
    :type text: str
    :param text: The text to display when getting the user input
    :type text_2: str
    :param text_2: The text to be displayed after the use has input a satisfactory amount of colours
    :type max_: int
    :param max_: The maximum amount of colours the user can input

    :rtype: list[str]
    :return: A list of user inputted colours
    """

    results: list[str] = []

    while len(results) <= max_:
        tmp: str = input(text if len(results) < 2 else text_2)

        if findall(_HEX_CODE_REGEX, tmp):
            results.append(tmp)

        else:
            if tmp == "$$$":
                if len(results) > 1:
                    break
                else:
                    print("\nERROR: You can't exit with less than 2 colours chosen. Please try again...")

            print("\nERROR: Invalid hex code input. Please try again...")

    return results


_DEFAULT_CONFIG: dict[str, int | list[str]] = _load_config()


class Main:
    __slots__: tuple[str, ...] = "__previous_drawing", "__colours", "__pattern", "__width", "__height", \
                                       "__speed", "__side_length", "__config_contents"

    __t: Turtle = Turtle()
    __win: Screen = Screen()

    def __init__(self) -> None:
        self.__previous_drawing: list[list[str]] = []

    def run(self, file: str = _DEFAULT_CONFIG_FILE) -> None:
        """
        :rtype: None
        :return: None
        """

        self.__config(file)
        self.__menu()

    def __menu(self) -> None:
        """
        :rtype: None
        :return: None
        """

        while True:
            print("\nPlease enter the number of the function you would like to execute: ")
            for index, item in enumerate(_MENU_ITEMS):
                print(f"\t[{index + 1}] {item.title()}")

            match input(""):
                case "1":
                    self.__draw_pattern()
                case "2":
                    self.__change_config_file()
                case "3":
                    self.__create_config_file()
                case "4":
                    break
                case _:
                    print("\nERROR: Invalid input. Please try again...")

    def __change_config_file(self) -> None:
        """
        :rtype: None
        :return: None
        """

        print("\nCurrent config files: ")
        for item in listdir(_ALT_CONFIGS_FOLDER):
            print(item)

        while True:
            fn: str = input("\nEnter the name of the file you want to use: ")
            if _check_valid_file(f"{_ALT_CONFIGS_FOLDER}{fn}"):
                break
            print("\nERROR: You didn't enter a valid file name. Please try again...")

        self.__config(f"{_ALT_CONFIGS_FOLDER}{fn}")

    @staticmethod
    def __create_config_file() -> None:
        """
        :rtype: None
        :return: None
        """

        width: int = _range_input("\nEnter the screen width (max. 1000): ", 0, 1000)
        height: int = _range_input("\nEnter the screen height (max. 1000): ", 0, 1000)
        speed: int = _range_input("\nEnter the drawing speed (max. 10): ", 0, 10)
        side_length: int = _range_input("\nEnter the side length of the square/s (max. 250): ", 0, 250)

        colours: list[str] = _colour_input("\nEnter a colour (max. 10): ",
                                           "\nEnter a colour or '$$$' to finish (max. 10): ", 10)

        contents: dict = {
            "speed": speed,
            "width": width,
            "height": height,
            "side_length": side_length,
            "colours": colours
        }

        # Unique config file identifier
        rand_str: str = ''.join([choice(digits + ascii_letters) for _ in range(5)])
        fn: str = f"{_ALT_CONFIGS_FOLDER}-w{width}-h{height}-s{speed}-sl{side_length}-c{''.join([item.strip('#') for item in colours])}-{rand_str}-.json"

        with open(fn, "w+") as f:
            f.write(dumps(contents, indent=4, sort_keys=True))

        print("\nNew config file created...")

    def __draw_pattern(self) -> None:
        """
        :rtype: None
        :return: None
        """

        # Initialise
        self.__win.setup(self.__width, self.__height)  # window size / start co-ords
        self.__t.hideturtle()
        self.__t.speed(self.__speed)

        # Go to top left
        self.__t.penup()
        self.__t.goto(-self.__width / 2, self.__height / 2)

        # Do each row in the pattern
        for row in self.__pattern:

            # Do each item in the row
            for item in row:
                # Initialise
                self.__t.pendown()
                self.__t.color(item)
                self.__t.begin_fill()

                # Draw square
                for _ in range(4):
                    self.__t.forward(self.__side_length)
                    self.__t.right(90)

                # Reset position
                self.__t.end_fill()
                self.__t.forward(self.__side_length)

            # Start new line
            self.__t.penup()
            self.__t.goto(-self.__width / 2, self.__t.ycor() - self.__side_length)

        sleep(10)
        self.__win.bye()
        sysexit()

    @staticmethod
    def __gen_pattern(width: int, height: int, colours: list[str]) -> list[list[str]]:
        """
        :type width: int
        :param width: The width dimension of the list
        :type height: int
        :param height: The height dimension of the list
        :type colours: list[str]
        :param colours: A list of the possible colours for the pattern

        :rtype: list[list[str]]
        :return: The generated pattern
        """

        return [[choice(colours) for _ in range(width)] for _ in range(height)]

    def __config(self, file: str = _DEFAULT_CONFIG_FILE) -> None:
        """
        :type file: str
        :param file: The file location to read configuration data from

        :rtype: None
        :return: None
        """

        self.__config_contents: dict[str, int | list[str]] = _load_config(file) if _check_valid_file(
            file) else _load_config()

        self.__speed: int = self.__config_contents["speed"] if "speed" in self.__config_contents.keys() else \
            _DEFAULT_CONFIG["speed"]

        self.__width: int = self.__config_contents["width"] if "width" in self.__config_contents.keys() else \
            _DEFAULT_CONFIG["width"]
        self.__height: int = self.__config_contents["height"] if "height" in self.__config_contents.keys() else \
            _DEFAULT_CONFIG["height"]

        self.__side_length: int = self.__config_contents[
            "side_length"] if "side_length" in self.__config_contents.keys() else \
            _DEFAULT_CONFIG["side_length"]

        self.__colours: list[str] = self.__config_contents["colours"] if "colours" in self.__config_contents.keys() else \
            _DEFAULT_CONFIG["colours"]

        self.__pattern: list[list[str]] = self.__gen_pattern(
            round(self.__width / self.__side_length),
            round(self.__height / self.__side_length),
            self.__colours
        )


def run() -> None:
    """
    :rtype: None
    :return: None
    """

    # Start program
    main: Main = Main()
    main.run()


if __name__ == "__main__":
    run()

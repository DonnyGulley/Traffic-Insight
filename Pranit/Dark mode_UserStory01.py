from colorama import Fore, Back, Style, init

init(autoreset=True)

# Light mode colors
LIGHT_MODE = {
    "background": Back.WHITE,
    "text": Fore.BLACK,
}

# Dark mode colors
DARK_MODE = {
    "background": Back.BLACK,
    "text": Fore.WHITE,
}


def display_message(theme):
    print(theme["background"] + theme["text"] + "Welcome to Traffic Insight!")
    print(theme["background"] + theme["text"] + "Here are your weekly transit reports.")
    print(Style.RESET_ALL)  # Reset styling after output

def color_mode():
    print("Select Theme:")
    print("1. Light Mode")
    print("2. Dark Mode")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        theme = LIGHT_MODE
    elif choice == "2":
        theme = DARK_MODE
    else:
        print("Invalid choice. Defaulting to Light Mode.")
        theme = LIGHT_MODE

    




import json

def save_theme_preference(theme_name):
    with open("theme_preference.json", "w") as file:
        json.dump({"theme": theme_name}, file)

def load_theme_preference():
    try:
        with open("theme_preference.json", "r") as file:
            return json.load(file)["theme"]
    except FileNotFoundError:
        return "light"  # Default theme

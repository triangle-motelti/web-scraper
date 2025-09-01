import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)

def ascii_art(text: str, font: str = "slant", color: str = "cyan"):
    art = pyfiglet.figlet_format(text, font=font, justify="center")

    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE
    }

    print(colors.get(color.lower(), Fore.WHITE) + art + Style.RESET_ALL)

if __name__ == "__main__":
    ascii_art("motelti   triangle scraper", font="slant", color="blue")
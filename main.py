from src.earthquake import Earthquake
from src.ui import UI


def main():
    earthquake = Earthquake()
    ui = UI()

    earthquake.connect()
    ui.core(earthquake)

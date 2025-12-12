from src.earthquake import Earthquake
from src.ui import UI


def main():
    earthquake = Earthquake()
    ui = UI()

    if earthquake.data is None:
        earthquake.connect()

    ui.core(earthquake)

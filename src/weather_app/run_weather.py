import os
import sys

sys.path.insert(0,os.path.join(os.path.dirname(__file__),'../..'))

from src.gui.UserInterface import UserInterface

def main():
    weather_window=UserInterface()
    weather_window.show()


if __name__=="__main__":
    main()
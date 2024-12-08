import os
import sys

#For compatibility:
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'../..'))

#User interface window
from src.gui.UserInterface import UserInterface

def main():
    #Create and open the interface window:
    weather_window=UserInterface()
    weather_window.show()


if __name__=="__main__":
    main()
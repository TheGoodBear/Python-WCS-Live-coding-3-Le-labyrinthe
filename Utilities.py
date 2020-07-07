# coding: utf-8

# import modules
import random
import os
import sys

# additional code
import Variables


def GetData(Message, MinimumValue = 0, MaximumValue = 0, DefaultValue = None):
    """
        This function gets en entry from the user
        Entry must be integer

        Parameters :
            Message : the message to show to the user
            MinimumValue : the minimum acceptable value 
            MaximumValue : the maximum acceptable value 
            DefaultValue : 
                - if None : there is no default value
                - if positive gets the default value
                - if -1 draw a random number between MinimumValue and MaximumValue
    """
    DataOK = False

    # Do until user entry is valid
    while not DataOK:
        MyData = input(Message)
        if not MyData.isdigit() or int(MyData) < MinimumValue or int(MyData) > MaximumValue:
            # user entry is not an expected value
            if DefaultValue == None:
                # no default value specified, so ask again
                print(f"Merci de rentrer une valeur comprise entre {MinimumValue} et {MaximumValue}")
            elif DefaultValue != -1 :
                # get specified default value
                MyData = DefaultValue
                DataOK = True
            else:
                # draw an random number between Min and Max
                MyData = random.randint(MinimumValue, MaximumValue)
                DataOK = True
        else:
            # user entry is valid
            DataOK = True

    # return user entry
    return int(MyData)


def ClearConsole():
    """
        This function clears the console depending on OS
    """

    if "win" in sys.platform.lower():
        # for windows
        os.system("cls")
    elif "linux" in sys.platform.lower():
        # for linux
        os.system("clear")


# file main entry (for example to check the functions)
if __name__ == "__main__":
    ClearConsole()
    print("Bonjour")

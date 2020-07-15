"""
    Global variables
"""

# character
CharacterSymbol = "\033[34m☻\033[0m"
CharacterPosition = {"X" : 0, "Y" : 0}
CharacterTotalActions = 0
CharacterBadActions = 0

# maze (MazeElements is a dictionary of dictionaries)
MazeMap = []
MazeElements = {
    " " : {
        "Name" : "sol",
        "Image" : " ",
        "CanWalk" : True},
    "*" : {
        "Name" : "mur",
        "Image" : "\033[30m▒\033[0m",
        "CanWalk" : False},
    "T" : {
        "Name" : "arbre",
        "Image" : "\033[32m♣\033[0m",
        "CanWalk" : False
        },
    "E" : {
        "Name" : "entrée",
        "Image" : " ",
        "CanWalk" : True
        },
    "X" : {
        "Name" : "sortie",
        "Image" : "\033[33m☼\033[0m",
        "CanWalk" : True
        }
    }

# game
GameInProgress = True
GameMessage = ""
GameFileName = "SavedGames\CurrentGame"
# coding: utf-8

"""
    Game functions
"""

# import additional code
import Variables
import Utilities
import Game 

def ShowTitleAndRules():
    """
        Prints title ans rules
    """

    Utilities.ClearConsole()

    print("Jeu du labyrinthe")
    print("-----------------\n")

    print (f"L'objectif est de faire sortir le personnage {Variables.CharacterSymbol} du labyrinthe")
    print ("On peut le déplacer en choisissant sa direction :")
    print ("(H)aut, (B)as, (G)auche, (D)roite ou (Q)uitter\n")


def LoadMapFromFile(FileName):
    """
        Loads a labyrinth map from specified file name
    """

    with open(FileName, "r", encoding="utf-8") as MyFile:
        Y = 0
        for Line in MyFile:
            Columns = []
            X = 0
            for Character in Line:
                # ignore line ends
                if Character == "\n":
                    continue
                # add character to map
                Columns.append(Character)
                # place character at map entry
                if Character == "E":
                    Variables.CharacterPosition["X"] = X
                    Variables.CharacterPosition["Y"] = Y
                X += 1
            # add line to map
            Variables.MazeMap.append(Columns)
            Y += 1
        
    # print(Variables.MazeMap)


def DrawMaze():
    """
        Draw maze on console from 2 dimensional list
    """

    # draw maze
    for Y in range(len(Variables.MazeMap)):
        for X in range(len(Variables.MazeMap[Y])):
            if (Y == Variables.CharacterPosition["Y"]
                and X == Variables.CharacterPosition["X"]):
                # this is character position, draw it
                print(Variables.CharacterSymbol, end="")
            else:
                # no character here, draw maze
                print(Variables.MazeElements[Variables.MazeMap[Y][X]]["Image"], end="")
        print()

    # show message if any
    if Variables.GameMessage != "":
        print(Variables.GameMessage)
        Variables.GameMessage = ""
    else:
        print()


def GetCharacterAction():
    """
        Ask for character action
    """

    # list of possible actions
    PossibleActions = ["H", "B", "G", "D", "Q"]

    # wait for a valid action
    Action = ""
    while Action not in PossibleActions:
        Action = input("Que doit faire le personnage ? ").upper()

    # execute action
    ExecuteCharacterAction(Action)

    # refresh maze
    Game.ShowTitleAndRules()
    Game.DrawMaze()


def ExecuteCharacterAction(Action):
    """
        Executes choosen action
    """

    # store new character position
    NewCharacterPositionX = Variables.CharacterPosition["X"]
    NewCharacterPositionY = Variables.CharacterPosition["Y"]

    # prepare action
    if Action == "H":
        NewCharacterPositionY -= 1
        Variables.GameMessage = "\nLe personnage se déplace vers le haut\n"
    elif Action == "B":
        NewCharacterPositionY += 1
        Variables.GameMessage = "\nLe personnage se déplace vers le bas\n"
    elif Action == "G":
        NewCharacterPositionX -= 1
        Variables.GameMessage = "\nLe personnage se déplace vers la gauche\n"
    elif Action == "D":
        NewCharacterPositionX += 1
        Variables.GameMessage = "\nLe personnage se déplace vers la droite\n"
    elif Action == "Q":
        Variables.GameMessage = "\nCouard, tu choisis la fuite !\n"
        Variables.GameInProgress = False
        return

    # check if action is allowed
    if (NewCharacterPositionY < 0
        or NewCharacterPositionY >= len(Variables.MazeMap)
        or NewCharacterPositionX < 0 
        or NewCharacterPositionX >= len(Variables.MazeMap[0])):
        # new position is out of maze, can't move
        Variables.GameMessage = "\nImpossible d'aller par là !\n"
        return
    elif not Variables.MazeElements[
        Variables.MazeMap[NewCharacterPositionY][NewCharacterPositionX]]["CanWalk"]:
        # new position blocks movement, can't move
        Variables.GameMessage = f"\nAïe, un {Variables.MazeElements[Variables.MazeMap[NewCharacterPositionY][NewCharacterPositionX]]['Name']} !\n"
        return
    elif Variables.MazeMap[NewCharacterPositionY][NewCharacterPositionX] == "X":
        # player quits
        Variables.GameMessage = "\nBRAVO, tu es sorti du labyrinthe !"
        Variables.GameInProgress = False
        return

    # execute action
    Variables.CharacterPosition["X"] = NewCharacterPositionX
    Variables.CharacterPosition["Y"] = NewCharacterPositionY

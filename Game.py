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
    print ("(H)aut, (B)as, (G)auche, (D)roite ou (Q)uitter")
    print ("Il est également possible de (S)auvegarder la partie en cours ou de la re(C)harger\n")


def AskGameData():
    """
        Ask map number
    """
    MapNumber = input("Quelle carte veux-tu (1 ou 2) ? ")
    if MapNumber == "" or not MapNumber.isdigit():
        MapNumber = "1"
    print()
    return MapNumber


def LoadMapFromFile(FileName):
    """
        Loads a labyrinth map from specified file name
    """

    try:
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
    except FileNotFoundError:
        Variables.GameInProgress = False
        print("\nCette carte n'existe pas.\n")


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

    # show game data
    print(f"Nombre d'actions effectuées : {Variables.CharacterTotalActions} (dont {Variables.CharacterBadActions} mauvaises)\n")


def GetCharacterAction():
    """
        Ask for character action
    """

    # list of possible actions
    PossibleActions = ["H", "B", "G", "D", "S", "C", "Q"]

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
        Variables.CharacterTotalActions += 1
        NewCharacterPositionY -= 1
        Variables.GameMessage = "\nLe personnage se déplace vers le haut\n"
    elif Action == "B":
        Variables.CharacterTotalActions += 1
        NewCharacterPositionY += 1
        Variables.GameMessage = "\nLe personnage se déplace vers le bas\n"
    elif Action == "G":
        Variables.CharacterTotalActions += 1
        NewCharacterPositionX -= 1
        Variables.GameMessage = "\nLe personnage se déplace vers la gauche\n"
    elif Action == "D":
        Variables.CharacterTotalActions += 1
        NewCharacterPositionX += 1
        Variables.GameMessage = "\nLe personnage se déplace vers la droite\n"
    elif Action == "S":
        try:
            # open game file in write mode
            with open(Variables.GameFileName, "w", encoding="utf-8") as MyFile:
                # save maze
                for LineIndex, Line in enumerate(Variables.MazeMap):
                    MyFile.write("Map:")
                    MyFile.writelines(Variables.MazeMap[LineIndex])
                    MyFile.write("\n")
                # save character position
                MyFile.write(f"X:{Variables.CharacterPosition['X']}\n")
                MyFile.write(f"Y:{Variables.CharacterPosition['Y']}\n")
                # save game data
                MyFile.write(f"TotalActions:{Variables.CharacterTotalActions}\n")
                MyFile.write(f"BadActions:{Variables.CharacterBadActions}\n")
                Variables.GameMessage = "\nLa partie en cours a été sauvegardée.\n"
        except:
            Variables.GameMessage = "\nSauvegarde de la partie impossible.\n"
    elif Action == "C":
        try:
            # open game file in read mode
            with open(Variables.GameFileName, "r", encoding="utf-8") as MyFile:
                # reset map
                Variables.MazeMap = []
                # load maze
                # read 1st line
                Line = MyFile.readline()
                # while line contains something
                while Line:
                    # remove last character (\n) at end of line
                    Line = Line[:-1]
                    if Line.startswith("Map:"):
                        # this data is part of map
                        MapLine = []
                        for Character in Line[len("Map:"):]:
                            MapLine.append(Character)
                        Variables.MazeMap.append(MapLine)
                    elif Line.startswith("X:"):
                        # this data is player position
                        NewCharacterPositionX = int(Line[len("X:"):])
                    elif Line.startswith("Y:"):
                        # this data is player position
                        NewCharacterPositionY = int(Line[len("Y:"):])
                    elif Line.startswith("TotalActions:"):
                        # this data is game data
                        Variables.CharacterTotalActions = int(Line[len("TotalActions:"):])
                    elif Line.startswith("BadActions:"):
                        # this data is game data
                        Variables.CharacterBadActions = int(Line[len("BadActions:"):])
                    
                    # read next line
                    Line = MyFile.readline()

                Variables.GameMessage = "\nLa partie a été chargée.\n"
        except:
            Variables.GameMessage = "\Chargement de la partie impossible.\n"
            input("Chargement terminé")
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
        Variables.CharacterBadActions += 1
        return
    elif not Variables.MazeElements[
        Variables.MazeMap[NewCharacterPositionY][NewCharacterPositionX]]["CanWalk"]:
        # new position blocks movement, can't move
        Variables.GameMessage = f"\nAïe, un {Variables.MazeElements[Variables.MazeMap[NewCharacterPositionY][NewCharacterPositionX]]['Name']} !\n"
        Variables.CharacterBadActions += 1
        return
    elif Variables.MazeMap[NewCharacterPositionY][NewCharacterPositionX] == "X":
        # player quits
        Variables.GameMessage = "\nBRAVO, tu es sorti du labyrinthe !"
        Variables.GameInProgress = False
        return

    # execute action
    Variables.CharacterPosition["X"] = NewCharacterPositionX
    Variables.CharacterPosition["Y"] = NewCharacterPositionY

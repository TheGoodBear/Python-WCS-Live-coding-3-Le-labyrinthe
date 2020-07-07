# coding: utf-8

# import additional code
import Variables
import Game

def Start():
    """
        Game start
    """

    # initialize game
    Game.ShowTitleAndRules()
    Game.LoadMapFromFile("Map 1")
    Game.DrawMaze()

    # main game loopg
    while Variables.GameInProgress:
        Game.GetCharacterAction()

    # game end
    print("\nAu revoir.\n")


# Main entry point
if __name__ == "__main__":
    Start()
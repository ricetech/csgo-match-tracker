import os


class Team:
    """
    Basic definition for a team.
    """
    def __init__(self):
        self.score = 0
        self.team = ""

    def roundWin(self):
        self.score += 1

    def reverseWin(self):
        if self.score > 0:
            self.score -= 1

    def reset(self):
        self.score = 0
        self.team = ""


MAX_ROUND_NUM = 30
HALFTIME_ROUND_NUM = 15
WIN_SCORE = 16
TEAM_ONE = "CT"
TEAM_TWO = "T"
ourTeam = Team()
otherTeam = Team()


def cls():
    """This function clears the console. It does not work in IDEs."""
    os.system('cls' if os.name == 'nt' else 'clear')


def switch_sides():
    """This function switches the two teams. Usually called at halftime."""
    global ourTeam, otherTeam
    if ourTeam.team == TEAM_ONE:
        ourTeam.team = TEAM_TWO
        otherTeam.team = TEAM_ONE
    else:
        ourTeam.team = TEAM_ONE
        otherTeam.team = TEAM_TWO


def endGame(result):
    """
    This function is called at the end of a game. It displays the result (who won), the ending score,
    and then asks if another game is to be played.
    :type result: str
    :param result: The result of the game, usually "WIN", "LOSS", or "DRAW".
    :return: Nothing.
    """
    global ourTeam, otherTeam, playAgain

    while True:
        cls()
        print("=== " + result + ": " + str(ourTeam.score) + " to " + str(otherTeam.score) + " ===")
        playOption = input("Play again? (Y/N)\n")
        playOption = playOption.upper()
        if playOption == "Y":
            ourTeam.reset()
            otherTeam.reset()
            playAgain = True
            break
        elif playOption == "N":
            playAgain = False
            break
        else:
            input("\n>> Error: Not a valid option. Push Enter to try again.\n")


while True:
    while True:
        try:
            cls()
            initTeam = input("Starting team: (CT/T):\n")
            initTeam = initTeam.upper()
            if initTeam == TEAM_ONE:
                otherTeam.team = TEAM_TWO
                ourTeam.team = TEAM_ONE
                break
            elif initTeam == TEAM_TWO:
                otherTeam.team = TEAM_ONE
                ourTeam.team = TEAM_TWO
                break
            else:
                input("\n>> Error: Not a valid option. Push Enter to try again.\n")
        except ValueError:
            input("\n>> Error: Invalid input. Push Enter to try again.\n")
    cls()

    roundNum = 1
    lastScored = []  # Using a list as a stack to store last winners
    playAgain = True

    while True:
        while True:
            cls()
            print("Round " + str(roundNum) + "/" + str(MAX_ROUND_NUM) + ": " + ourTeam.team)
            print("Score: " + str(ourTeam.score) + " to " + str(otherTeam.score))
            if HALFTIME_ROUND_NUM - roundNum == 0:
                print("== LAST ROUND UNTIL HALFTIME ==")
            elif roundNum < HALFTIME_ROUND_NUM:
                # Will not print after halftime
                print(str(HALFTIME_ROUND_NUM - roundNum + 1) + " rounds until halftime")
            print("")
            if WIN_SCORE - ourTeam.score == 1 or WIN_SCORE - otherTeam.score == 1 or MAX_ROUND_NUM - roundNum == 0:
                print("== MATCH POINT ==")
            else:
                print("We are:   " + str(WIN_SCORE - ourTeam.score) + " from winning\n" +
                      "They are: " + str(WIN_SCORE - otherTeam.score) + " from winning\n" +
                      "MAX " + str(MAX_ROUND_NUM - roundNum) + " round(s) left")

            try:
                option = int(input("\nSelect:\n"
                                   "1: Our team (" + ourTeam.team + ") wins\n" +
                                   "2: Their team (" + otherTeam.team + ") wins\n" +
                                   "3: Accidental advance (backtrack one round)\n" +
                                   "4: Reset Match\n"
                                   "5: Exit\n"
                                   ))
                if option == 1:
                    ourTeam.roundWin()
                    roundNum += 1
                    lastScored.append(ourTeam)
                    break
                elif option == 2:
                    otherTeam.roundWin()
                    roundNum += 1
                    lastScored.append(otherTeam)
                    break
                elif option == 3:
                    if not len(lastScored) == 0:  # Prevent indexError
                        roundNum -= 1
                        if roundNum == 15:
                            switch_sides()
                        lastScored.pop().reverseWin()
                    else:
                        input("\n>> Error: There is no valid round to reverse. Press Enter to continue.")
                    break
                elif option == 5:
                    exit()
                else:
                    input("\n>> Error: Not a valid option. Push Enter to try again.\n")
            except ValueError:
                input("\n>> Error: Invalid input. Push Enter to try again.\n")
        if roundNum == 16:
            # Halftime reached, switch sides
            switch_sides()
        elif ourTeam.score == WIN_SCORE - 1 and otherTeam.score == WIN_SCORE - 1:
            endGame("DRAW")
            break
        elif ourTeam.score == WIN_SCORE:
            endGame("WIN")
            break
        elif otherTeam.score == WIN_SCORE:
            endGame("LOSS")
            break
        if not playAgain:  # playAgain is set in endgame()
            exit()

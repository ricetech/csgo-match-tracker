import os
from enum import Enum, auto

# Constants - change to fit your game
MAX_ROUND_NUM = 30
HALFTIME_ROUND_NUM = 15
WIN_SCORE = 16
TEAM_ONE = "CT"
TEAM_TWO = "T"


class Team:
    """
    Basic definition for a team.
    :var self.score: Stores how many rounds this team has won.
    :var self.team: The side that this team is currently play on.
    :var self.switchTeam: The side that this team will switch to during team switch.
    """

    def __init__(self):
        self.score = 0  # Variable to store
        self.team = ""
        self.switchTeam = ""

    def roundWin(self):
        self.score += 1

    def reverseWin(self):
        if self.score > 0:
            self.score -= 1

    def reset(self):
        self.score = 0
        self.team = ""
        self.switchTeam = ""


class Result(Enum):
    WIN = auto
    LOSS = auto
    DRAW = auto


# Variable Initialization
ourTeam = Team()
otherTeam = Team()


def cls():
    """This function clears the console. It does not work in IDEs."""
    os.system('cls' if os.name == 'nt' else 'clear')


def switch_sides():
    """This function switches the two teams. Usually called at halftime."""
    global ourTeam, otherTeam
    temp = ourTeam.team
    ourTeam.team = ourTeam.switchTeam
    ourTeam.switchTeam = temp

    temp = otherTeam.team
    otherTeam.team = otherTeam.switchTeam
    otherTeam.switchTeam = temp


def print_match_summary(rounds, halftime, team):
    """
    This is a helper function for endGame(). It displays which team won which round.
    :type rounds: list[Team]
    :type halftime: int
    :type team: Team
    :param rounds: A list containing Team objects, ordered based on which team won which round.
    :param halftime: The round number where teams switch sides. Defined in the outer scope as HALFTIME_ROUND_NUM.
    :param team: The team that was being tracked (ourTeam).
    :return: Nothing.
    """

    print("=== MATCH SUMMARY: ===")
    for r in range(1, len(rounds) + 1):
        roundWinner = rounds[r - 1]
        roundText = "Round " + str(r) + " - "

        if r < halftime + 1:
            currentTeam = team.switchTeam
            winningTeam = roundWinner.switchTeam
            roundText += currentTeam + ": "
        else:
            currentTeam = team.team
            winningTeam = roundWinner.team
            roundText += currentTeam + ": "

        if currentTeam == winningTeam:
            roundText += Result.WIN.name
        else:
            roundText += Result.LOSS.name

        print(roundText)


def endGame(result, rounds):
    """
    This function is called at the end of a game. It displays the result (who won), the ending score,
    and then asks if another game is to be played.
    :type result: Result
    :type rounds: list[Team]
    :param result: The result of the game, usually "WIN", "LOSS", or "DRAW".
    :param rounds: A list containing Team objects, ordered based on which team won which round.
    :return: Nothing.
    """
    global ourTeam, otherTeam, playAgain

    cls()

    while True:
        try:
            print("=== " + result.name + ": " + str(ourTeam.score) + " to " + str(otherTeam.score) + " ===")
            summaryOption = int(input("Enter one of the following options:\n" +
                                      "1: Display match summary\n" +
                                      "2: Play Again\n" +
                                      "3: Quit\n"))

            if summaryOption == 1:
                cls()
                print_match_summary(rounds, HALFTIME_ROUND_NUM, ourTeam)
                print("=== " + result.name + ": " + str(ourTeam.score) + " to " + str(otherTeam.score) + " ===")
                input("Push Enter to continue.\n")
                cls()
            elif summaryOption == 2:
                ourTeam.reset()
                otherTeam.reset()
                playAgain = True
                break
            elif summaryOption == 3:
                exit()
            else:
                input("\n>> Error: Not a valid option. Push Enter to try again.\n")
                cls()
        except ValueError:
            input(">> Error: Invalid input. Push Enter to try again.\n")
            cls()


# Main program loop
while True:
    while True:
        try:
            cls()
            initTeam = input("Starting team: (CT/T):\n")
            initTeam = initTeam.upper()
            if initTeam == TEAM_ONE:
                otherTeam.team = ourTeam.switchTeam = TEAM_TWO
                ourTeam.team = otherTeam.switchTeam = TEAM_ONE
                break
            elif initTeam == TEAM_TWO:
                otherTeam.team = ourTeam.switchTeam = TEAM_ONE
                ourTeam.team = otherTeam.switchTeam = TEAM_TWO
                break
            else:
                input("\n>> Error: Not a valid option. Push Enter to try again.\n")
        except ValueError:
            input("\n>> Error: Invalid input. Push Enter to try again.\n")
    cls()

    roundNum = 1
    lastScored = []  # Using a list as a stack to store last winners (sort of like an undo operation stack)
    playAgain = True  # Used to stay in the main while loop
    reset = ""

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
                if MAX_ROUND_NUM - roundNum == 1:
                    text = " round"
                else:
                    text = " rounds"
                print("We are:   " + str(WIN_SCORE - ourTeam.score) + " from winning\n" +
                      "They are: " + str(WIN_SCORE - otherTeam.score) + " from winning\n" +
                      "At most " + str(MAX_ROUND_NUM - roundNum) + text + " left after current round")

            try:
                option = int(input("\nEnter one of the following options:\n"
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
                        input("\n>> Error: Cannot go further back than the first round. Press Enter to continue.\n")
                    break
                elif option == 4:
                    while True:
                        reset = input("Confirm reset? (Y/N)\n")
                        if reset.upper() == "Y":
                            # The first statement breaks out of the input checker
                            reset = True
                            break
                        elif reset.upper() == "N":
                            reset = False
                            break
                        else:
                            input("\n>> Error: Not a valid option. Push Enter to try again.\n")
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
            endGame(Result.DRAW, lastScored)
            break
        elif ourTeam.score == WIN_SCORE:
            endGame(Result.WIN, lastScored)
            break
        elif otherTeam.score == WIN_SCORE:
            endGame(Result.LOSS, lastScored)
            break
        if reset:
            ourTeam.reset()
            otherTeam.reset()
            break

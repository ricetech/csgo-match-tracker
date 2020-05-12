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

    def round_win(self):
        self.score += 1

    def reverse_win(self):
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
our_team = Team()
other_team = Team()


def clear_screen():
    """This function clears the console. It does not work in IDEs."""
    os.system('clear_screen' if os.name == 'nt' else 'clear')


def switch_sides():
    """This function switches the two teams. Usually called at halftime."""
    global our_team, other_team
    temp = our_team.team
    our_team.team = our_team.switchTeam
    our_team.switchTeam = temp

    temp = other_team.team
    other_team.team = other_team.switchTeam
    other_team.switchTeam = temp


def print_match_summary(rounds, halftime, team):
    """
    This is a helper function for end_game(). It displays which team won which round.
    :param rounds: A list containing Team objects, ordered based on which team won which round.
    :param halftime: The round number where teams switch sides. Defined in the outer scope as HALFTIME_ROUND_NUM.
    :param team: The team that was being tracked (our_team).
    :type rounds: list[Team]
    :type halftime: int
    :type team: Team
    :return: Nothing.
    """

    print("=== MATCH SUMMARY: ===")
    for r in range(1, len(rounds) + 1):
        round_winner = rounds[r - 1]
        round_text = "Round " + str(r) + " - "

        if r < halftime + 1:
            current_team = team.switchTeam
            winning_team = round_winner.switchTeam
            round_text += current_team + ": "
        else:
            current_team = team.team
            winning_team = round_winner.team
            round_text += current_team + ": "

        if current_team == winning_team:
            round_text += Result.WIN.name
        else:
            round_text += Result.LOSS.name

        print(round_text)


def end_game(result, rounds):
    """
    This function is called at the end of a game. It displays the result (who won), the ending score,
    and then asks if another game is to be played.
    :param result: The result of the game, usually "WIN", "LOSS", or "DRAW".
    :param rounds: A list containing Team objects, ordered based on which team won which round.
    :type result: Result
    :type rounds: list[Team]
    :return: Nothing.
    """
    global our_team, other_team, play_again

    clear_screen()

    while True:
        try:
            print("=== " + result.name + ": " + str(our_team.score) + " to " + str(other_team.score) + " ===")
            summaryOption = int(input("Enter one of the following options:\n" +
                                      "1: Display match summary\n" +
                                      "2: Play Again\n" +
                                      "3: Quit\n"))

            if summaryOption == 1:
                clear_screen()
                print_match_summary(rounds, HALFTIME_ROUND_NUM, our_team)
                print("=== " + result.name + ": " + str(our_team.score) + " to " + str(other_team.score) + " ===")
                input("Push Enter to continue.\n")
                clear_screen()
            elif summaryOption == 2:
                our_team.reset()
                other_team.reset()
                play_again = True
                break
            elif summaryOption == 3:
                exit()
            else:
                input("\n>> Error: Not a valid option. Push Enter to try again.\n")
                clear_screen()
        except ValueError:
            input(">> Error: Invalid input. Push Enter to try again.\n")
            clear_screen()


# Main program loop
while True:
    while True:
        try:
            clear_screen()
            init_team = input("Starting team: (CT/T):\n")
            init_team = init_team.upper()
            if init_team == TEAM_ONE:
                other_team.team = our_team.switchTeam = TEAM_TWO
                our_team.team = other_team.switchTeam = TEAM_ONE
                break
            elif init_team == TEAM_TWO:
                other_team.team = our_team.switchTeam = TEAM_ONE
                our_team.team = other_team.switchTeam = TEAM_TWO
                break
            else:
                input("\n>> Error: Not a valid option. Push Enter to try again.\n")
        except ValueError:
            input("\n>> Error: Invalid input. Push Enter to try again.\n")
    clear_screen()

    round_num = 1
    last_scored = []  # Using a list as a stack to store last winners (sort of like an undo operation stack)
    play_again = True  # Used to stay in the main while loop
    reset = ""

    while True:
        while True:
            clear_screen()
            print("Round " + str(round_num) + "/" + str(MAX_ROUND_NUM) + ": " + our_team.team)
            print("Score: " + str(our_team.score) + " to " + str(other_team.score))
            if HALFTIME_ROUND_NUM - round_num == 0:
                print("== LAST ROUND UNTIL HALFTIME ==")
            elif round_num < HALFTIME_ROUND_NUM:
                # Will not print after halftime
                print(str(HALFTIME_ROUND_NUM - round_num + 1) + " rounds until halftime")
            print("")
            if WIN_SCORE - our_team.score == 1 or WIN_SCORE - other_team.score == 1 or MAX_ROUND_NUM - round_num == 0:
                print("== MATCH POINT ==")
            else:
                if MAX_ROUND_NUM - round_num == 1:
                    text = " round"
                else:
                    text = " rounds"
                print("We are:   " + str(WIN_SCORE - our_team.score) + " from winning\n" +
                      "They are: " + str(WIN_SCORE - other_team.score) + " from winning\n" +
                      "At most " + str(MAX_ROUND_NUM - round_num) + text + " left after current round")

            try:
                option = int(input("\nEnter one of the following options:\n"
                                   "1: Our team (" + our_team.team + ") wins\n" +
                                   "2: Their team (" + other_team.team + ") wins\n" +
                                   "3: Accidental advance (backtrack one round)\n" +
                                   "4: Reset Match\n"
                                   "5: Exit\n"
                                   ))
                if option == 1:
                    our_team.round_win()
                    round_num += 1
                    last_scored.append(our_team)
                    break
                elif option == 2:
                    other_team.round_win()
                    round_num += 1
                    last_scored.append(other_team)
                    break
                elif option == 3:
                    if not len(last_scored) == 0:  # Prevent indexError
                        round_num -= 1
                        if round_num == 15:
                            switch_sides()
                        last_scored.pop().reverse_win()
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
        if round_num == 16:
            # Halftime reached, switch sides
            switch_sides()
        elif our_team.score == WIN_SCORE - 1 and other_team.score == WIN_SCORE - 1:
            end_game(Result.DRAW, last_scored)
            break
        elif our_team.score == WIN_SCORE:
            end_game(Result.WIN, last_scored)
            break
        elif other_team.score == WIN_SCORE:
            end_game(Result.LOSS, last_scored)
            break
        if reset:
            our_team.reset()
            other_team.reset()
            break

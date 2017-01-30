# This file will be responsible for managing/running the game
import GenerateGameBoard as gb
import sys
import pprint as pp
from prettytable import PrettyTable
import time

# BOARD IS IN FORMAT:
# (round, category, value, question, answer)

# PURPOSE: Run the game and put together all the peices
# COMMAND LINE ARGS: <master_list_file_name> (with the /)
def main(argv):
    if len(argv) < 1:
        print "ABORTING: Need 1 command line arguments: "
        print "<master_list_file_name>"
        exit(1)
    csv_file = argv[0]
    board = gb.GenerateBoard(csv_file, 1)
    PlayRoundWithBoard(board)
    board = gb.GenerateBoard(csv_file, 2)
    PlayRoundWithBoard(board)
    board = gb.GenerateBoard(csv_file, 3)
    PlayFinalJeopardyWithBoard(board)

def PlayRoundWithBoard(board):
    print "Playing new round!"
    categories = [board[0][0][1], board[1][0][1], board[2][0][1], board[3][0][1], board[4][0][1], board[5][0][1]]
    count = 0
    num_questions = 30
    while count < num_questions:
        PrintBoard(categories, board)
        col = input("Enter a column (0 indexed): ")
        value = input("Enter a value: ")
        row = ConvertValueToRow(value, board[0][0][0])
        while board[col][row][2] == "x":
            print "That question has already been played, please pick another one (without an x)"
            col = input("Enter a column (0 indexed): ")
            value = input("Enter a value: ")
            row = ConvertValueToRow(value, board[0][0][0])
        board[col][row] = (board[col][row][0], board[col][row][1], "x", board[col][row][3], board[col][row][4])
        print "\n\n", board[col][row][3], "\n\n"
        count+=1
        sleeps = 0
        # while sleeps < 10:
        #     print 10-sleeps, "Seconds left"
        #     time.sleep(1)
        #     sleeps +=1
        myinput("Press any button when ready for answer: ")
        print "\n\n", board[col][row][4], "\n\n"
    # PrintBoard(categories, board)

def PlayFinalJeopardyWithBoard(board):
    print "Playing final jeopardy!"
    print "\n\n", board[0][0][1], "\n\n"
    myinput("Press any button when ready for question: ")
    print "\n\n", board[0][0][3], "\n\n"
    myinput("Press any button when ready for answer: ")
    print "\n\n", board[0][0][4], "\n\n"

def PrintBoard(categories, board):
    x = PrettyTable(categories)
    x.padding_width = 1 # One space between column edges and contents (default)
    x.add_row([board[0][0][2], board[1][0][2], board[2][0][2], board[3][0][2], board[4][0][2], board[5][0][2]])
    x.add_row([board[0][1][2], board[1][1][2], board[2][1][2], board[3][1][2], board[4][1][2], board[5][1][2]])
    x.add_row([board[0][2][2], board[1][2][2], board[2][2][2], board[3][2][2], board[4][2][2], board[5][2][2]])
    x.add_row([board[0][3][2], board[1][3][2], board[2][3][2], board[3][3][2], board[4][3][2], board[5][3][2]])
    x.add_row([board[0][4][2], board[1][4][2], board[2][4][2], board[3][4][2], board[4][4][2], board[5][4][2]])
    print x

def ConvertValueToRow(value, round_string):
    row = 0
    if round_string == "Jeopardy!":
        if value == 400:
            row = 1
        elif value == 600:
            row = 2
        elif value == 800:
            row = 3
        elif value == 1000:
            row = 4
    elif round_string == "Double Jeopardy!":
        if value == 800:
            row = 1
        elif value == 1200:
            row = 2
        elif value == 1600:
            row = 3
        elif value == 2000:
            row = 4
    return row

def myinput(prompt):
    try:
        return raw_input(prompt)
    except NameError:
        return input(prompt)

if __name__ == "__main__":
    main(sys.argv[1:])
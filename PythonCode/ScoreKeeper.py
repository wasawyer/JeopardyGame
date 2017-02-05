# This file is responsible for managing player scores
scores = {}
final_wagers = {}

# PURPOSE: Populates scores dictionary with people playing the game
# INPUTS: none
# RETURNS: nothing
def InitPlayers():
    player = myinput("Enter the name of a player ('exit' to add no more): ")
    while player != 'exit':
        scores[player] = 0
        player = myinput("Enter the name of a player ('exit' to add no more): ")

# PURPOSE: Prints how many points each person has
# INPUTS: none
# RETURNS: nothing
def PrintScores():
    print "\n\nLeaderboard:"
    for key,value in scores.iteritems():
        print key, "has", value, "points"
    print "\n"

# PURPOSE: Prints how many points each person has
# INPUTS: none
# RETURNS: nothing
def PrintFinalStandings():
    print "\n\nAnd the final leaderboard is!!!:"
    for key,value in scores.iteritems():
        print key, "has", value, "points!"
    print "\n"

# PURPOSE: Checks and updates scores for each player in the Scores dictionary
# INPUTS: questionValue (how much the question was worth)
# RETURNS: nothing
def CheckAndUpdateScores(questionValue):
    for key,value in scores.iteritems():
        prompt_string = "Did " + key + " get the question right (r), wrong (w), or not answer (na)?"
        response = myinput(prompt_string)
        if response == 'r':
            scores[key] = value + questionValue
        elif response == 'w':
            scores[key] = value - questionValue

# PURPOSE: Checks and updates scores for each player in the Scores dictionary after final jeopardy
# INPUTS: none
# RETURNS: nothing
def CheckAndUpdateFinalScores():
    for key,value in final_wagers.iteritems():
        prompt_string = "Did " + key + " get the question right (r), wrong (w)?"
        response = myinput(prompt_string)
        if response == 'r':
            scores[key] = scores[key] + value
        elif response == 'w':
            scores[key] = scores[key] + value

# PURPOSE: Gets wagers for final jeopardy for each contestant
# INPUTS: none
# RETURNS: nothing
def ManageWagers():
    for key,value in scores.iteritems():
        if value < 0:
            print key, "was below 0 so can't participate"
            continue
        prompt_string = "How much does " + key + " want to wager?"
        response = int(myinput(prompt_string))
        while response > value or response < 0:
            prompt_string = "How much does " + key + " want to wager? (between 0 and " + str(value) + ")"
            response = int(myinput(prompt_string))
        final_wagers[key] = response

# PURPOSE: Tries to use raw_input to get input
#           If not possible because of python version it falls back to normal input
# INPUTS: prompt to be printed for input
# RETURNS: the input
def myinput(prompt):
    try:
        return raw_input(prompt)
    except NameError:
        return input(prompt)
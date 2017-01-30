# This file will be responsible for populating the gameboard from the master CSV
import csv
import os
import pprint as pp
from datetime import datetime
import time
from sets import Set
import random

# list of tuples, where each tuple is in the format: 
# (round, category, value, question, answer)
master_list = []

# PURPOSE: Reads in csv_file, import it into data structure and returns gameboard
# INPUTS: string of csv infile name, round_type
#           roundtype: 1=Jeopardy, 2=Double Jeopardy, 3=Final Jeopardy
# RETURNS: 5x6 list of tuples with question info (gameboard)
def GenerateBoard(csv_infile, round_type):
    gameboard = []
    # Initialize master list (only once)
    if not master_list:
        ReadAndPopulateMasterList(csv_infile)
    num_categories = 6
    round_string = "Jeopardy!"
    if round_type == 1:
        print "Normal Jeopardy"
    elif round_type == 2:
        print "Double Jeopardy"
        round_string = "Double Jeopardy!"
    elif round_type == 3:
        print "Final Jeopardy"
        round_string = "Final Jeopardy!"
        num_categories = 1
    else:
        print "ERROR: round_type must be either 1,2, or 3"
        exit(1)
    categories = GetCategories(num_categories, round_string)
    categories_list = list(categories)
    # pp.pprint(categories_list)
    for x in range(0,len(categories_list)):
        question_list = PopulateCategory(categories_list[x], round_string)
        while len(question_list) == 0:
            print "Replacing category:", categories_list[x]
            categories_list = ReplaceCategory(x, categories_list, round_string)
            question_list = PopulateCategory(categories_list[x], round_string)
        gameboard.append(question_list)
    # pp.pprint(categories_list)
    return gameboard

# PURPOSE: Reads in csv_file and populates master_list structure with it
# INPUTS: string of csv infile name
# RETURNS: nothing, but populates master_list
def ReadAndPopulateMasterList(csv_infile):
    print "Populating master list"
    # print datetime.now().time()
    with open(csv_infile, 'rb') as csvfile:
        # Skip header
        csvfile.next()
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            master_list.append((row[2],row[3],row[4],row[5],row[6]))
        csvfile.close()
    # print datetime.now().time()
    # pp.pprint(master_list)

# PURPOSE: picks 5 random categories from master_list
# INPUTS: how many categories we want to get and what round
# RETURNS: set of categories
def GetCategories(size, round_string):
    categories = Set()
    upper_bound = len(master_list) - 1
    while len(categories) < size:
        rand_num = random.randint(0,upper_bound)
        if master_list[rand_num][1] not in categories and master_list[rand_num][0] == round_string:
            categories.add(master_list[rand_num][1])
    return categories

# PURPOSE: picks 5 questions for a given category and a given round
# INPUTS: category name and what round
# RETURNS: list of tuples of questions for category
def PopulateCategory(category, round_string):
    # Populate info for search
    start_time = time.time()
    max_time_out = 2
    num_questions = 1
    values = Set(["None"])
    category_questions = [1]
    questions_found = 0
    upper_bound = len(master_list) - 1

    # Change neccessary values for single and double jeopardy
    if round_string == "Jeopardy!":
        values = Set(["$200", "$400", "$600", "$800", "$1000"])
        num_questions = 5
        category_questions = [1,2,3,4,5]
    elif round_string == "Double Jeopardy!":
        values = Set(["$400", "$800", "$1200", "$1600", "$2000"])
        num_questions = 5
        category_questions = [1,2,3,4,5]

    # Start search
    index = random.randint(0,upper_bound)
    while questions_found < num_questions:
        # Abandon search if took too long
        if time.time() - start_time > max_time_out:
            print "Couldn't populate questions for category:", category, "and round:", round_string
            return []
        for x in range(index,upper_bound):
            if master_list[x][1] == category and master_list[x][2] in values:
                category_questions = InsertQuestion(category_questions, master_list[x], round_string)
                values.remove(master_list[x][2])
                if len(values) == 0:
                    return category_questions
        for x in range(0,index):
            if master_list[x][1] == category and master_list[x][2] in values:
                category_questions = InsertQuestion(category_questions, master_list[x], round_string)
                values.remove(master_list[x][2])
                if len(values) == 0:
                    return category_questions

# PURPOSE: insert question into correct spot in list
# INPUTS: question list, question, and what round
# RETURNS: list of tuples of questions for category
def InsertQuestion(question_list, question, round_string):
    index = 0
    if round_string == "Jeopardy!":
        if question[2] == "$400":
            index = 1
        elif question[2] == "$600":
            index = 2
        elif question[2] == "$800":
            index = 3
        elif question[2] == "$1000":
            index = 4
    elif round_string == "Double Jeopardy!":
        if question[2] == "$800":
            index = 1
        elif question[2] == "$1200":
            index = 2
        elif question[2] == "$1600":
            index = 3
        elif question[2] == "$2000":
            index = 4
    question_list[index] = question
    return question_list

# PURPOSE: replace a category in the category list
# INPUTS: index of category to be replaced, list of categories, what round it is
# RETURNS: list of categories
def ReplaceCategory(index, categories_list, round_string):
    upper_bound = len(master_list) - 1
    starting_point = random.randint(0, upper_bound)
    x = starting_point
    while x < upper_bound:
        if master_list[x][0] == round_string and master_list[x][1] not in categories_list:
            categories_list[index] = master_list[x][1]
            return categories_list
        x+=1
    x = 0
    while x < starting_point:
        if master_list[x][0] == round_string and master_list[x][1] not in categories_list:
            categories_list[index] = master_list[x][1]
            return categories_list
        x+=1
    print "Somehow found unreplaceable category"
    exit(1)




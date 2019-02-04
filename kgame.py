#
# NWEN 241 Programming Assignment 5
# kgame.py Python Source File
#
# Name:
# Student ID:
#
# IMPORTANT: Implement the functions specified in kgame.h here.
# You are free to implement additional functions that are not specified in kgame.h here.
#

import random
import time

# This is the title of the game
KGAME_TITLE = "The K-Game (Python Edition)"

# This is the file name of the saved game state
KGAME_SAVE_FILE = "kgame.sav"

# Number of tiles per side
KGAME_SIDES = 4

# Output buffer size in bytess
KGAME_OUTPUT_BUFLEN = ((18*40)+1)

# Arrow keys
dirs = { 'UP': 1, 'DOWN': 2, 'LEFT': 3, 'RIGHT': 4 }

# Keys accepted by game
inputs = { 'LOAD': 5, 'SAVE': 6, 'EXIT': 7}

def next_char(input):

    """
    Helper function to return the next letter in the alphabet
    """

    if input == 'A':
        return 'B'
    elif input == 'B':
        return 'C'
    elif input == 'C':
        return 'D'
    elif input == 'D':
        return 'E'
    elif input == 'E':
        return 'F'
    elif input == 'F':
        return 'G'
    elif input == 'G':
        return 'H'
    elif input == 'H':
        return 'I'
    elif input == 'I':
        return 'J'
    elif input == 'J':
        return 'K'

    return ' '


def char_value(input):

    """
    Helper function to return the value of the input char; helps to properly increment the score
    """

    if input == 'A':
        return 2
    elif input == 'B':
        return 4
    elif input == 'C':
        return 8
    elif input == 'D':
        return 16
    elif input == 'E':
        return 32
    elif input == 'F':
        return 64
    elif input == 'G':
        return 128
    elif input == 'H':
        return 256
    elif input == 'I':
        return 512
    elif input == 'J':
        return 1024
    elif input == 'K':
        return 2048

    return 0


def kgame_init(game):
    game['score'] = 0
    game['board'] = [[' ' for x in range(KGAME_SIDES)] for y in range(KGAME_SIDES)]

    kgame_add_random_tile(game)
    kgame_add_random_tile(game) #start each game with two tiles

def kgame_add_random_tile(game):
    # find random, but empty tile

    # makes flat list for easy searching
    flat_list = [game['board'][y][x] for y in range(KGAME_SIDES) for x in range(KGAME_SIDES)]

    if ' ' in flat_list: # prevents infinite loop in case no empty tile

        while True:
            row = random.randint(0, KGAME_SIDES-1) # -1 adjusts to proper boundaries
            col = random.randint(0, KGAME_SIDES-1) # -1 adjusts to proper boundaries
            if game['board'][row][col] == ' ':
                break

        # place to the random position 'A' or 'B' tile
        game['board'][row][col] = 'A'
        if random.randint(0, 2) == 1:
            game['board'][row][col] = 'B'


def kgame_render(game):

    """
    Shows the score and game board
    """

    output_buffer = "Current score: " + str(game['score']) + "\n"

    for rows in range(KGAME_SIDES): # iterates through each row

        output_buffer += "+---+---+---+---+\n"

        for cols in range(KGAME_SIDES): # iterates through each column

            output_buffer += "| " + game['board'][rows][cols] + " "

        output_buffer += "|\n"

    output_buffer += "+---+---+---+---+\n"

    return output_buffer


def kgame_is_won(game):

    """
    Checks if the game has been won, i.e. a 'K' tile is on the board
    """

    if 'K' in [game['board'][y][x] for y in range(KGAME_SIDES) for x in range(KGAME_SIDES)]:
        return True # game is won

    return False # game not won


def kgame_is_move_possible(game):

    """
    Checks if a move can still be made, i.e. there is at least one empty field (tile) in the game field,
    or at least two adjacent tiles of the same character are located either vertically or horizontally in the grid
    """

    if ' ' in [game['board'][y][x] for y in range(KGAME_SIDES) for x in range(KGAME_SIDES)]:
        return True # there is an empty field

    for y in range(KGAME_SIDES):
        for x in range(1, KGAME_SIDES):
            if game['board'][y][x] == game['board'][y][x-1]:
                return True # there are two adjacent tiles of the same character horizontally

    for y in range(KGAME_SIDES):
        for x in range(KGAME_SIDES-1):
            if game['board'][y][x] == game['board'][y][x+1]:
                return True # there are two adjacent tiles of the same character horizontally

    for y in range(1, KGAME_SIDES):
        for x in range(KGAME_SIDES):
            if game['board'][y][x] == game['board'][y-1][x]:
                return True # there are two adjacent tiles of the same character vertically

    for y in range(KGAME_SIDES-1):
        for x in range(KGAME_SIDES):
            if game['board'][y][x] == game['board'][y+1][x]:
                return True # there are two adjacent tiles of the same character vertically

    return False; # no move possible


def kgame_update(game, direction):

    """
    Performs the slide (move) in the selected direction and add a new tile with either ’A’ or ’B’ character at a random unoccupied (empty) position (tile).
    Slides can be made in 4 directions: up, down, left and right.
    Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid (game field).
    If two tiles of the same character collide while moving,
    they will merge into a tile with the next letter in the alphabet of the two tiles that collided
    """

    isChanged = False

    # if left arrow key is pressed
    if direction == dirs['LEFT']:

        for y in range(KGAME_SIDES):
            for x in range(KGAME_SIDES-1):
                for matchIndex in range(x+1, KGAME_SIDES):
                    flag = 0 # 1 if there is a non-matching tile between the two matching tiles, 0 if there are none
                    if game['board'][y][x] == game['board'][y][matchIndex]:
                        for spaceCount in range(x+1, matchIndex): # ensures the two tiles can merge because there is nothing between them
                            if game['board'][y][spaceCount] != ' ': # if there is a non-matching tile between the two matching tiles
                                flag = 1
                                break

                        if flag == 0: # if the tiles can come together and merge
                            game['score'] += char_value(next_char(game['board'][y][x])) # updates score
                            game['board'][y][x] = next_char(game['board'][y][x]) # updates tile
                            game['board'][y][matchIndex] = ' '
                            isChanged = True
                            break

        # shifts board LEFT
        for count in range(KGAME_SIDES):
            for y in range(KGAME_SIDES):
                for x in range(KGAME_SIDES-1, 0, -1):
                    if game['board'][y][x-1] == ' ' and game['board'][y][x] != ' ':
                        game['board'][y][x-1] = game['board'][y][x]
                        game['board'][y][x] = ' '
                        isChanged = True

        kgame_add_random_tile(game)

    # else if right arrow key is pressed
    elif direction == dirs['RIGHT']:

        for y in range(KGAME_SIDES):
            for x in range(KGAME_SIDES-1, 0, -1):
                for matchIndex in range(x-1, -1, -1):
                    flag = 0 # 1 if there is a non-matching tile between the two matching tiles, 0 if there are none
                    if game['board'][y][x] == game['board'][y][matchIndex]:
                        for spaceCount in range(x-1, matchIndex, -1): # ensures the two tiles can merge because there is nothing between them
                            if game['board'][y][spaceCount] != ' ': # if there is a non-matching tile between the two matching tiles
                                flag = 1
                                break

                        if flag == 0: # if the tiles can come together and merge
                            game['score'] += char_value(next_char(game['board'][y][x])) # updates score
                            game['board'][y][x] = next_char(game['board'][y][x]) # updates tile
                            game['board'][y][matchIndex] = ' '
                            isChanged = True
                            break

        # shifts board RIGHT
        for count in range(KGAME_SIDES):
            for y in range(KGAME_SIDES):
                for x in range (KGAME_SIDES-1):
                    if game['board'][y][x+1] == ' ' and game['board'][y][x] != ' ':
                        game['board'][y][x+1] = game['board'][y][x]
                        game['board'][y][x] = ' '
                        isChanged = True

        kgame_add_random_tile(game)

    # else if up arrow key is pressed
    elif direction == dirs['UP']:

        for y in range(KGAME_SIDES-1):
            for x in range(KGAME_SIDES):
                for matchIndex in range(y+1, KGAME_SIDES):
                    flag = 0 # 1 if there is a non-matching tile between the two matching tiles, 0 if there are none
                    if game['board'][y][x] == game['board'][matchIndex][x]:
                        for spaceCount in range(y+1, matchIndex): # ensures the two tiles can merge because there is nothing between them
                            if game['board'][spaceCount][x] != ' ': # if there is a non-matching tile between the two matching tiles
                                flag = 1
                                break

                        if flag == 0: # if the tiles can come together and merge
                            game['score'] += char_value(next_char(game['board'][y][x])) # updates score
                            game['board'][y][x] = next_char(game['board'][y][x]) # updates tile
                            game['board'][matchIndex][x] = ' '
                            isChanged = True
                            break

        # shifts board UP
        for count in range(KGAME_SIDES):
            for y in range(KGAME_SIDES-1, 0, -1):
                for x in range(KGAME_SIDES):
                    if game['board'][y-1][x] == ' ' and game['board'][y][x] != ' ':
                        game['board'][y-1][x] = game['board'][y][x]
                        game['board'][y][x] = ' '
                        isChanged = True

        kgame_add_random_tile(game)

    # else if down arrow key is pressed
    elif direction == dirs['DOWN']:

        for y in range(KGAME_SIDES-1, 0, -1):
            for x in range(KGAME_SIDES):
                for matchIndex in range(y-1, -1, -1):
                    flag = 0 # 1 if there is a non-matching tile between the two matching tiles, 0 if there are none
                    if game['board'][y][x] == game['board'][matchIndex][x]:
                        for spaceCount in range(y-1, matchIndex, -1): # ensures the two tiles can merge because there is nothing between them
                            if game['board'][spaceCount][x] != ' ': # if there is a non-matching tile between the two matching tiles
                                flag = 1
                                break

                        if flag == 0: # if the tiles can come together and merge
                            game['score'] += char_value(next_char(game['board'][y][x])) # updates score
                            game['board'][y][x] = next_char(game['board'][y][x]) # updates tile
                            game['board'][matchIndex][x] = ' '
                            isChanged = True
                            break

        # shifts board DOWN
        for count in range(KGAME_SIDES):
            for y in range(KGAME_SIDES-1):
                for x in range(KGAME_SIDES):
                    if game['board'][y+1][x] == ' ' and game['board'][y][x] != ' ':
                        game['board'][y+1][x] = game['board'][y][x]
                        game['board'][y][x] = ' '
                        isChanged = True

        kgame_add_random_tile(game)

    return isChanged;


def kgame_save(game):

    """
    Saves the state of the game by writing the contents of the game to a file
    """

    # the name of the file is specified by variable KGAME_SAVE_FILE
    saveFile = open(KGAME_SAVE_FILE, "w")

    if saveFile == None:
        print("Invalid file.\n")
        return

    for y in range(KGAME_SIDES):
        for x in range(KGAME_SIDES): # nested loop iterates through board tiles
            if game['board'][y][x] != ' ':
                saveFile.write(game['board'][y][x]) # writes tile to save file
            else:
                saveFile.write('-') # empty tile

    saveFile.write(" " + str(game['score'])) # writes score to save file

    saveFile.close() # closes file

def kgame_load(game):

    """
    Loads the saved state of the game by writing the contents of the save file to the field
    """

    myFile = open(KGAME_SAVE_FILE, "r") # the name of the file is specified by variable KGAME_SAVE_FILE

    if myFile == None:
        print("Invalid file.\n")
        return False # load unsuccessful

    for y in range(KGAME_SIDES):
        for x in range(KGAME_SIDES): # nested loop iterates through board tiles
            character = myFile.read(1) # reads file contents one character at a time
            if character == '-': # represents a blank tile
                character = ' '
            # invalid file if character is not a letter from A to K, and not a blank space
            if (ord(character) < ord('A') or ord(character) > ord('K')) and character != ' ':
                print("Invalid file.\n")
                return False # load unsuccessful

            game['board'][y][x] = character # loads character to tile

    holder = myFile.read(1) # holder for the blank space
    game['score'] = int(myFile.read()) # loads the score

    myFile.close() # closes file
    return True # load successful

# -*- coding: utf-8 -*-

#!/bin/env python3
#
# NWEN 241 Programming Assignment 5
# main.py Python3 Source File

# This program is provide as-is without any warranty. You may use this file to
# test your function implementations.
  
# This program will accept the following keystrokes as valid:
# - UP/DOWN/LEFT/RIGHT arrow keys for making a move
# - S or s to save game
# - L or l to load a saved game
# - X or x to exit


import curses
from curses import wrapper
import kgame

VALID_INPUTS_STRING = "Valid Inputs: [UP/DN/LT/RT] [S/s:Save] [L/l:Load] [X/x:Exit]"

dir_string = ("UNKNOWN", "UP", "DOWN", "LEFT", "RIGHT")

def init_screen(stdscr):
    curses.cbreak() 
    curses.noecho()
    curses.nonl()  
    curses.intrflush(False)
    stdscr.keypad(True)    
    stdscr.refresh()


def get_user_input(stdscr):
    while True:
        c = stdscr.getch()
        if c == curses.KEY_UP:
            return kgame.dirs['UP']
        elif c == curses.KEY_DOWN:
            return kgame.dirs['DOWN']
        elif c == curses.KEY_LEFT:
            return kgame.dirs['LEFT']
        elif c == curses.KEY_RIGHT:
            return kgame.dirs['RIGHT']
        elif chr(c) == 'S' or chr(c) == 's':
            return kgame.inputs['SAVE']  
        elif chr(c) == 'L' or chr(c) == 'l':
            return kgame.inputs['LOAD']
        elif chr(c) == 'X' or chr(c) == 'x':
            return kgame.inputs['EXIT'] 


def init_header():
    header = curses.newwin(3, curses.COLS-1, 0, 0)
    header.move(0, (curses.COLS-len(kgame.KGAME_TITLE))//2)
    header.addstr(kgame.KGAME_TITLE)
    header.move(1, (curses.COLS-len(VALID_INPUTS_STRING))//2)
    header.addstr(VALID_INPUTS_STRING)
    header.refresh()
    return header


def init_status():
    status = curses.newwin(1, curses.COLS-1, curses.LINES-1, 0)
    status.move(0, 0)
    status.addstr("Game started. Press any valid input key to proceed... ")
    status.refresh()
    return status


def init_field():
    field = curses.newwin(curses.LINES-4, curses.COLS-1, 3, 0)
    return field


def update_status(status, s):
    status.clear()
    status.move(0, 0)
    status.addstr(s)
    status.refresh()


def main(stdscr):
    render = True

    # Initialize the screen 
    stdscr = curses.initscr()
    init_screen(stdscr) 
    
    # Initialize the game object
    game = {}
    kgame.kgame_init(game);

    # Initialize the "windows" 
    header = init_header()
    field = init_field()
    status = init_status()

    # Game loop 
    while True: 
        if isinstance(game, dict) == False or 'board' not in game.keys() or 'score' not in game.keys():
            update_status(status, "Invalid game data structure. Press any key to exit...")
            break

        # Render 
        if render == True:
            buff = kgame.kgame_render(game);
            field.clear()
            field.move(0, 0)
            field.addstr(buff)
            field.refresh()
            status.refresh()

        # Check if game is won, and do what is right 
        if kgame.kgame_is_won(game) == True:
            update_status(status, "Congratulations! You won the game. Press any key to exit...")
            break
        
        # Check if move is still possible, and do what is right 
        if kgame.kgame_is_move_possible(game) == False:
            update_status(status, "Sorry, you ran out of moves. Game over! Press any key to exit...");
            break
        
        # Get a valid input 
        key = get_user_input(stdscr)
        if key == kgame.inputs['EXIT']:
            update_status(status, "Press any key to exit...")
            break
        elif key == kgame.inputs['SAVE']:
            kgame.kgame_save(game)
            update_status(status, "Tried to save game.")
        elif key == kgame.inputs['LOAD']:
            render = kgame.kgame_load(game)
            update_status(status, "Tried to load game.")
        else:
            render = kgame.kgame_update(game, key)
            update_status(status, "Last move: " + dir_string[key]);

        stdscr.refresh()

    stdscr.getch()
    curses.endwin()

wrapper(main)

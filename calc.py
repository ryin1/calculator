#  Homework 10
#   Due Sunday, Apr. 5th at 23:59
#   Always write the final code yourself
#   Cite any websites you referenced
#   Use the PEP-8 checker for full style points:
#   https://pypi.python.org/pypi/pep8

import argparse
import curses
import tkinter as tk
from functools import partial
import math

# The goal of this homework is to create a user interface for a
# calculator.
#
# You must include a README.txt which explains briefly
#  - Which version(s) you implemented
#  - How to use it (clicking/keyboard controls)
#  - Which extra credit you did
#   - Why it's cool
#   - How many points you think it's worth
#
# The calculator is required to support the following features:
#   - A text display that shows the current expression to evaluate
#   - A grid of buttons which manipulate the text display
#   - A return button that replaces the display with the evaluated results
#   The buttons must include:
#    - Digits 0-9
#    - Operators +, -, *, /
#    - Clear (Clears the display)
#    - Enter (Evaluates the display -- you can use Python's eval('a_string'))
#
# This program takes command line arguments to determine what UI to create
#  - python3 hw10.py    -> will give you a help message for the CL args
#  - python3 hw10.py -t -> will run the tkinter calculator app
#  - python3 hw10.py -c -> will run the curses calculator app
#
# You are only required to write *One* of the UIs (tkinter or curses)
#
# Grading:
#  - This homework will be *manually graded* -> There is no test.py
#  - Implementing all required features for one style of UI -> Full Credit
#  Extra Credit:
#   - You can get up to 20 points Extra Credit
#   - Final grade will be (min(120, Required_Features + Style + Extra Credit))
#   - 20 points -> Implementing the required features for curses and tkinter
#   - 5 points each -> Implementing a *Cool* non-required feature
#  Potential *Cool* features:
#   - Supporting a few additional operations (logs, exponents, trig-functions)
#   - Evaluating the display without using Python's built-in eval
#   - Having both a mouse and keyboard interface
#   - Keeping a command history and selecting previous commands
#   - Making it look good (Background colors, ...)


# curses
class CursesCalculator(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def run(self):
        while True:
            key = self.stdscr.getch()
            break

FONT_SIZE = 20


# tkinter
class TkinterCalculator(tk.Frame):
    '''
    You can group a bunch of widgets together as one widget with a Frame
      self.f = tk.Frame(self)
      self.f.grid()
      new_wid = tk.Button(self.f)

    Make a widget expand to fill the grid cell with the sticky attribute
      w.grid(row=r, column=c, sticky=tk.N+tk.S+tk.E+tk.W)
      This makes w expand to meet the north, south, east, and west walls
    '''
    OPS = ['+', '-', '*', '/']
    MORE_OPS = ['mod', '√']
    PARENS = ['(', ')']
    STICKY = tk.N + tk.S + tk.E + tk.W
    reset_input = True
    full_reset_input = False

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.make_label()
        self.make_buttons()

    def make_label(self):
        self.info = ''
        self.calc_line = tk.Label(self, justify='center', )
        self.calc_line['text'] = ''
        self.calc_line['font'] = self.calc_line['font'][0], 15
        self.calc_line.grid(row=0, column=1)

    def make_buttons(self):
        self.buttons = dict()
        f = tk.Frame(self)
        f.grid(row=1, column=1)
        row_others = ['0', 'Clear', 'Enter']
        for r, c in ((x, y) for x in range(4) for y in range(5)):
            button = tk.Button(f)
            button.grid(row=r, column=c, sticky=self.STICKY)
            if r < 3 and c < 3:
                button['text'] = str(3*r + c + 1)
            elif c < 3:
                button['text'] = row_others[c]
            elif c == 3:
                button['text'] = self.OPS[r]
            elif r < 2:
                # Parentheses buttons
                button['text'] = self.PARENS[r]
            else:
                button['text'] = self.MORE_OPS[r - 2]
            self.buttons[(r, c)] = button
            button['command'] = partial(self.button_handler, button['text'])

    def button_handler(self, s):
        math_dict = {'(': '(', 'mod': '%', '√': 'math.sqrt('}  
        if s in self.MORE_OPS:
            s = math_dict[s]
        if self.full_reset_input:
            self.calc_line['text'] = s
            self.full_reset_input = False
        elif s == 'Clear':
            self.calc_line['text'] = ''
        elif s == 'Enter':
            if self.calc_line['text']:
                # VARIOUS EXCEPTIONS: BAD OPERATION HANDLING
                try:
                    self.calc_line['text'] = str(eval(self.calc_line['text']))
                except ZeroDivisionError:
                    self.calc_line['text'] = 'Can\'t divide by 0.'
                    self.full_reset_input = True
                except:
                    pass
                try:
                    self.calc_line['text'] = str(eval(self.calc_line['text']
                                                      .replace('(', '*(')))
                except:
                    self.calc_line['text'] = 'Error.'
                    self.full_reset_input = True
            self.reset_input = True
        elif s in self.OPS or s in list(math_dict.values()) or s in self.PARENS:
            self.calc_line['text'] += s
            self.reset_input = False
        elif self.reset_input:
            self.calc_line['text'] = s
            self.reset_input = False
        # 0-9 DIGITS
        else:
            self.calc_line['text'] += s


def tkinter_main():
    root = tk.Tk()
    app = TkinterCalculator(master=root)
    app.mainloop()


def curses_main(stdscr):
    app = CursesCalculator(stdscr)
    app.run()


# parse command line arguments
if __name__ == '__main__':
    desc = 'A UI calculator written in either tkinter or curses'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-t', '--tkinter', metavar='tkinter', default=False,
                        action='store_const', const=True, dest='tkinter',
                        help='Runs the tkinter version of the app')
    parser.add_argument('-c', '--curses', metavar='curses', default=False,
                        action='store_const', const=True, dest='curses',
                        help='Runs the curses version of the app')
    args = parser.parse_args()
    if args.tkinter:
        tkinter_main()
    elif args.curses:
        curses.wrapper(curses_main)
    else:
        parser.print_help()

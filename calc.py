
import curses
import tkinter as tk
from functools import partial
import math

FONT_SIZE = 20


# tkinter
class TkinterCalculator(tk.Frame):

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


if __name__ == '__main__':
    root = tk.Tk()
    app = TkinterCalculator(master=root)
    app.mainloop()
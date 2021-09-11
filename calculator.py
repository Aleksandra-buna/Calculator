import tkinter as tk


class Calculator:
    """ This class is creating calculator: it includes the frontend and calculator logic """

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Calculator')
        self.window.geometry('310x426')
        self.window.resizable(0, 0)

        self.total_expression = ''
        self.arithmetic_expression = ''

        self.display_frame = self.create_display_frame()
        self.arithmetic_lbl, self.total_lbl = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 3)
        }

        self.operations = {'/': '\u00F7', '*': '\u00D7', '+': '+', '-': '-', '%': '%'}

        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_clear_button()
        self.create_del_button()
        self.create_square_root()
        self.create_equals_button()

        self.update_current_label()

    # creating display window
    def create_display_frame(self):
        frame = tk.Frame(master=self.window, height=221, bg='black')
        frame.pack(fill='both', expand=True)
        return frame

    # creating window for buttons
    def create_buttons_frame(self):
        frame = tk.Frame(master=self.window, bg='black')
        frame.pack(fill='both', expand=True)
        return frame

    # creating display arithmetic expressions and current number
    def create_display_labels(self):
        arithmetic_lbl = tk.Label(master=self.display_frame, text=self.arithmetic_expression, anchor=tk.E, bg='black',
                                  fg='orange', padx=24, font=('Roboto', 16))
        arithmetic_lbl.pack(fill='both', expand=True)
        total_lbl = tk.Label(master=self.display_frame, text=self.total_expression, anchor=tk.NE, bg='black',
                             fg='orange', padx=24, font=('Roboto', 40, 'bold'))
        total_lbl.pack(fill='both', expand=True)

        return arithmetic_lbl, total_lbl

    # appending arithmetic operations in current expression
    def add_operator(self, operator):
        self.total_expression += operator
        self.arithmetic_expression += self.total_expression
        self.update_current_label()
        if operator == '%':
            self.arithmetic_expression = str(
                eval(f'{self.arithmetic_expression[:-4]}*({self.total_expression[:-1]}/100)'))
            self.total_expression = self.arithmetic_expression
            self.total_lbl.config(text=self.total_expression[:8])
            self.arithmetic_expression = ''

        else:
            self.total_expression = ''
            self.total_lbl.config(text=self.total_expression)

    # creating buttons arithmetic operations
    def create_operator_buttons(self):
        r = 0
        for operator, value_operator in self.operations.items():
            button = tk.Button(master=self.buttons_frame, text=value_operator, bg='orange', fg='#dc3545',
                               font=('Roboto', 14, 'bold'), command=lambda x=operator: self.add_operator(x))
            button.grid(row=r, column=4, padx=1, pady=1, sticky=tk.NSEW)
            r += 1
            if operator == '%':
                button.grid(row=0, column=3)

    # displaying symbols on the display frame
    def add_to_expression(self, value):
        self.total_expression += str(value)
        self.total_lbl.config(text=self.total_expression)

    # creating digit and auxiliary buttons
    def create_digit_buttons(self):
        for digit, value_digit in self.digits.items():
            button = tk.Button(master=self.buttons_frame, text=str(digit), bg='orange', fg='white',
                               font=('Roboto', 20, 'bold'), command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=value_digit[0], column=value_digit[1], padx=1, pady=1, sticky=tk.NSEW)

    # logic of the button 'C'
    def clear(self):
        self.arithmetic_expression = ''
        self.total_expression = ''
        self.arithmetic_lbl.config(text=self.arithmetic_expression)
        self.total_lbl.config(text=self.total_expression)

    # button "C"
    def create_clear_button(self):
        button = tk.Button(master=self.buttons_frame, text='C', bg='white', fg='#dc3545',
                           font=('Roboto', 18, 'bold'), command=self.clear)
        button.grid(row=0, column=2, padx=1, pady=1, sticky=tk.NSEW)

    # logic of the button 'backspace'
    def backspace(self):
        self.total_expression = self.total_expression[: -1]
        self.total_lbl.config(text=self.total_expression)
        if self.total_expression == '':
            self.arithmetic_expression = self.arithmetic_expression[: -1]
            self.arithmetic_lbl.config(text=self.arithmetic_expression)

    # button 'backspace"
    def create_del_button(self):
        button = tk.Button(master=self.buttons_frame, text='\u232B', bg='#dc3545', fg='white',
                           font=('Roboto', 14, 'bold'), command=self.backspace)
        button.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NSEW)

    # logic of the square root
    def square_root(self):
        self.total_expression = str(eval(f'{self.total_expression} ** 0.5'))

        self.arithmetic_expression = self.total_expression[:8]

        self.total_expression = ''
        self.total_lbl.config(text=self.total_expression)

        self.update_current_label()

    def create_square_root(self):
        button = tk.Button(master=self.buttons_frame, text='\u221ax', bg='orange', fg='#dc3545',
                           font=('Roboto', 18, 'bold'), command=self.square_root)
        button.grid(row=4, column=1, padx=1, pady=1, sticky=tk.NSEW)

    # logic of the button '='
    def equals(self):
        self.arithmetic_expression += self.total_expression
        self.update_current_label()

        try:
            self.total_expression = str(eval(self.arithmetic_expression))
        except ZeroDivisionError:
            self.total_expression = 'ERROR!'
        finally:
            # displaying for max eight symbols
            self.total_lbl.config(text=self.total_expression[:8])
            self.arithmetic_expression = self.total_expression[:8]
            self.total_expression = ''

    # button "="
    def create_equals_button(self):
        button = tk.Button(master=self.buttons_frame, text='=', bg='#dc3545', fg='white',
                           font=('Roboto', 18, 'bold'), command=self.equals)
        button.grid(row=4, column=4, padx=1, pady=1, sticky=tk.NSEW)

    # changing operators to values in dictionary
    def update_current_label(self):
        expression = self.arithmetic_expression
        for operator, value_operator in self.operations.items():
            expression = expression.replace(operator, f' {value_operator} ')
        self.arithmetic_lbl.config(text=expression)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()

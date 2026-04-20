#!/usr/bin/env python3
"""
A modern calculator with a clean UI using tkinter.
Features:
- Basic arithmetic operations (+, -, *, /)
- Advanced operations (square root, power, percentage)
- History tracking
- Clean, modern interface
- Keyboard support
"""

import tkinter as tk
from tkinter import font as tkfont
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Set color scheme
        self.bg_color = "#2c3e50"
        self.display_bg = "#ecf0f1"
        self.btn_number = "#34495e"
        self.btn_operator = "#e67e22"
        self.btn_equals = "#27ae60"
        self.btn_clear = "#c0392b"
        self.btn_advanced = "#8e44ad"
        self.text_color = "#ffffff"
        
        self.root.configure(bg=self.bg_color)
        
        self.current_expression = ""
        self.history = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg=self.bg_color, pady=20)
        display_frame.pack(fill=tk.X)
        
        # History label (small text above main display)
        self.history_label = tk.Label(
            display_frame, 
            text="", 
            bg=self.bg_color, 
            fg="#bdc3c7",
            font=("Arial", 12),
            anchor="e",
            padx=20
        )
        self.history_label.pack(fill=tk.X)
        
        # Main display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 32, "bold"),
            bg=self.display_bg,
            fg="#2c3e50",
            bd=0,
            justify="right",
            padx=20,
            pady=15,
            relief=tk.FLAT
        )
        self.display.pack(fill=tk.X, padx=20, ipady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(expand=True, fill=tk.BOTH, padx=15, pady=10)
        
        # Button configuration
        button_config = [
            # Row 1 - Advanced functions
            ("√", self.btn_advanced, self.on_sqrt),
            ("x²", self.btn_advanced, self.on_square),
            ("%", self.btn_advanced, self.on_percentage),
            ("C", self.btn_clear, self.on_clear),
            
            # Row 2
            ("7", self.btn_number, self.on_number_click),
            ("8", self.btn_number, self.on_number_click),
            ("9", self.btn_number, self.on_number_click),
            ("/", self.btn_operator, self.on_operator_click),
            
            # Row 3
            ("4", self.btn_number, self.on_number_click),
            ("5", self.btn_number, self.on_number_click),
            ("6", self.btn_number, self.on_number_click),
            ("*", self.btn_operator, self.on_operator_click),
            
            # Row 4
            ("1", self.btn_number, self.on_number_click),
            ("2", self.btn_number, self.on_number_click),
            ("3", self.btn_number, self.on_number_click),
            ("-", self.btn_operator, self.on_operator_click),
            
            # Row 5
            ("0", self.btn_number, self.on_number_click),
            (".", self.btn_number, self.on_decimal_click),
            ("=", self.btn_equals, self.on_equals),
            ("+", self.btn_operator, self.on_operator_click),
        ]
        
        # Create buttons in grid
        for i, (text, color, command) in enumerate(button_config):
            row = i // 4
            col = i % 4
            
            if text == "=":
                btn = self.create_button(
                    buttons_frame, text, color, 
                    lambda t=text: command(), 
                    span=1, height=2
                )
            else:
                if callable(command):
                    if text in ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0", "."]:
                        btn = self.create_button(
                            buttons_frame, text, color, 
                            lambda t=text: command(t)
                        )
                    else:
                        btn = self.create_button(
                            buttons_frame, text, color, 
                            command
                        )
                else:
                    btn = self.create_button(
                        buttons_frame, text, color, 
                        lambda t=text: command(t)
                    )
            
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights for responsive layout
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # History panel
        history_frame = tk.Frame(self.root, bg=self.bg_color, height=100)
        history_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(
            history_frame, 
            text="History", 
            bg=self.bg_color, 
            fg="#bdc3c7",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        
        self.history_listbox = tk.Listbox(
            history_frame,
            bg="#34495e",
            fg="#ecf0f1",
            font=("Arial", 10),
            bd=0,
            highlightthickness=0,
            selectbackground=self.btn_operator,
            selectforeground=self.text_color,
            height=4
        )
        self.history_listbox.pack(fill=tk.X, pady=(5, 0))
        
        # Clear history button
        clear_history_btn = tk.Button(
            history_frame,
            text="Clear History",
            bg=self.btn_clear,
            fg=self.text_color,
            font=("Arial", 10, "bold"),
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.clear_history
        )
        clear_history_btn.pack(anchor="e", pady=(5, 0))
        
        # Bind keyboard events
        self.root.bind("<Key>", self.on_key_press)
    
    def create_button(self, parent, text, bg_color, command, span=1, height=1):
        btn = tk.Button(
            parent,
            text=text,
            bg=bg_color,
            fg=self.text_color,
            font=("Arial", 18, "bold"),
            bd=0,
            activebackground=self.adjust_color(bg_color, -20),
            activeforeground=self.text_color,
            cursor="hand2",
            command=command,
            relief=tk.FLAT,
            height=height
        )
        
        # Add hover effect
        btn.bind("<Enter>", lambda e, b=btn, c=bg_color: b.config(bg=self.adjust_color(c, -20)))
        btn.bind("<Leave>", lambda e, b=btn, c=bg_color: b.config(bg=c))
        
        return btn
    
    def adjust_color(self, hex_color, amount):
        """Adjust color brightness"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def update_display(self):
        if self.current_expression == "":
            self.display_var.set("0")
        else:
            self.display_var.set(self.current_expression)
    
    def on_number_click(self, num):
        if self.current_expression == "0" and num != ".":
            self.current_expression = num
        else:
            self.current_expression += num
        self.update_display()
    
    def on_decimal_click(self):
        if "." not in self.current_expression.split()[-1]:
            if self.current_expression == "" or self.current_expression[-1] in "+-*/":
                self.current_expression += "0."
            else:
                self.current_expression += "."
        self.update_display()
    
    def on_operator_click(self, op):
        if self.current_expression and self.current_expression[-1] in "+-*/":
            self.current_expression = self.current_expression[:-1] + op
        elif self.current_expression:
            self.current_expression += op
        self.update_display()
    
    def on_clear(self):
        self.current_expression = ""
        self.display_var.set("0")
        self.history_label.config(text="")
    
    def on_equals(self):
        try:
            # Evaluate the expression
            result = eval(self.current_expression)
            
            # Format result
            if isinstance(result, float):
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
            
            # Add to history
            history_entry = f"{self.current_expression} = {result}"
            self.history.append(history_entry)
            self.history_listbox.insert(0, history_entry)
            
            # Update history label
            if len(self.history) > 0:
                self.history_label.config(text=f"Last: {self.history[0]}")
            
            self.current_expression = str(result)
            self.update_display()
            
        except Exception as e:
            self.display_var.set("Error")
            self.current_expression = ""
    
    def on_sqrt(self):
        try:
            if self.current_expression:
                value = float(eval(self.current_expression))
                if value >= 0:
                    result = math.sqrt(value)
                    if result == int(result):
                        result = int(result)
                    else:
                        result = round(result, 10)
                    
                    history_entry = f"√({self.current_expression}) = {result}"
                    self.history.append(history_entry)
                    self.history_listbox.insert(0, history_entry)
                    
                    self.current_expression = str(result)
                    self.update_display()
                else:
                    self.display_var.set("Error")
                    self.current_expression = ""
        except:
            self.display_var.set("Error")
            self.current_expression = ""
    
    def on_square(self):
        try:
            if self.current_expression:
                value = float(eval(self.current_expression))
                result = value ** 2
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
                
                history_entry = f"({self.current_expression})² = {result}"
                self.history.append(history_entry)
                self.history_listbox.insert(0, history_entry)
                
                self.current_expression = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
            self.current_expression = ""
    
    def on_percentage(self):
        try:
            if self.current_expression:
                value = float(eval(self.current_expression))
                result = value / 100
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
                
                history_entry = f"{self.current_expression}% = {result}"
                self.history.append(history_entry)
                self.history_listbox.insert(0, history_entry)
                
                self.current_expression = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
            self.current_expression = ""
    
    def clear_history(self):
        self.history = []
        self.history_listbox.delete(0, tk.END)
        self.history_label.config(text="")
    
    def on_key_press(self, event):
        key = event.char
        
        if key.isdigit():
            self.on_number_click(key)
        elif key in "+-*/":
            self.on_operator_click(key)
        elif key == ".":
            self.on_decimal_click()
        elif key == "=" or key == "\r":
            self.on_equals()
        elif key == "\x08":  # Backspace
            if self.current_expression:
                self.current_expression = self.current_expression[:-1]
                self.update_display()
        elif key == "c" or key == "C":
            self.on_clear()

def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script with a UI to read CSV files, display top 5 rows, with counter and history.

Usage: python script.py
"""

import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer - Top 5 Rows")
        self.root.geometry("800x600")

        self.history = []
        self.counter = 0

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title label
        title_label = ttk.Label(main_frame, text="CSV Viewer - Top 5 Rows", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=(0, 10))

        # Open file button
        self.open_button = ttk.Button(button_frame, text="Open CSV File", command=self.open_file)
        self.open_button.grid(row=0, column=0, padx=5)

        # Counter label
        self.counter_label = ttk.Label(button_frame, text=f"Files viewed: {self.counter}", font=('Arial', 10))
        self.counter_label.grid(row=0, column=1, padx=20)

        # Clear history button
        self.clear_button = ttk.Button(button_frame, text="Clear History", command=self.clear_history)
        self.clear_button.grid(row=0, column=2, padx=5)

        # Treeview for displaying CSV data
        columns_frame = ttk.Frame(main_frame)
        columns_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        columns_frame.columnconfigure(0, weight=1)
        columns_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(columns_frame, show='headings')
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar
        scrollbar = ttk.Scrollbar(columns_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # History listbox
        history_frame = ttk.LabelFrame(main_frame, text="History", padding="5")
        history_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        history_frame.columnconfigure(0, weight=1)

        self.history_listbox = tk.Listbox(history_frame, height=4)
        self.history_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

    def open_file(self):
        """Open a CSV file and display top 5 rows."""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            self.display_csv(file_path)
            self.counter += 1
            self.counter_label.config(text=f"Files viewed: {self.counter}")
            self.add_to_history(file_path)
            self.status_label.config(text=f"Successfully loaded: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {str(e)}")
            self.status_label.config(text=f"Error loading file: {str(e)}")

    def display_csv(self, file_path):
        """Read CSV and display top 5 rows in the treeview."""
        # Clear existing data
        self.tree.delete(*self.tree.get_children())

        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            # Get header
            try:
                headers = next(reader)
                self.tree["columns"] = [f"col{i}" for i in range(len(headers))]
                
                for i, header in enumerate(headers):
                    self.tree.heading(f"col{i}", text=header)
                    self.tree.column(f"col{i}", width=100, anchor=tk.W)
            except StopIteration:
                self.status_label.config(text="Empty CSV file")
                return

            # Read top 5 rows
            for i, row in enumerate(reader):
                if i >= 5:
                    break
                self.tree.insert('', tk.END, values=row)

    def add_to_history(self, file_path):
        """Add file path to history list."""
        # Only add if not already in history
        if file_path not in self.history:
            self.history.append(file_path)
            self.history_listbox.insert(tk.END, file_path)

    def clear_history(self):
        """Clear the history."""
        self.history = []
        self.history_listbox.delete(0, tk.END)
        self.status_label.config(text="History cleared")


def main():
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

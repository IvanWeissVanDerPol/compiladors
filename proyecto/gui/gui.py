import tkinter as tk
from tkinter import filedialog, messagebox
from gui.gui_helpers import open_text_file, open_json_file, update_tokens, generate_report
from logic.tokenizer import Tokenizer

class LanguageTokenizerGUI:
    def __init__(self, root):
        self.tokenizer = Tokenizer.from_json('proyecto/logic/tokens.json')
        self.root = root
        self.root.title("Tokenizador de Lenguaje Natural")
        self.root.geometry("900x700")
        self.root.minsize(900, 700)
        self._setup_ui()

    def _setup_ui(self):
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.cs_entry, self.cs_text, self.cs_undefined_words_frame, self.cs_evaluation_frame = self._create_file_frame(
            self.scrollable_frame, "Customer Service File", "proyecto/ejemplos/ATC_000.txt")
        self.ce_entry, self.ce_text, self.ce_undefined_words_frame, self.ce_evaluation_frame = self._create_file_frame(
            self.scrollable_frame, "Customer Experience File", "proyecto/ejemplos/EXP_000.txt")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self._create_menu()

        # Add a button to generate the report
        report_button = tk.Button(self.scrollable_frame, text="Generate Report", command=self.generate_report, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        report_button.grid(padx=10, pady=10)
        report_button.bind("<Enter>", lambda e: report_button.config(bg="#45a049"))
        report_button.bind("<Leave>", lambda e: report_button.config(bg="#4CAF50"))

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _create_file_frame(self, parent, label_text, default_path):
        # Frame for the file section
        frame = tk.Frame(parent, padx=10, pady=10, bg="#f0f0f0", bd=2, relief="groove")
        frame.grid(padx=10, pady=10, sticky="nsew")

        # Label for the file section
        label = tk.Label(frame, text=label_text, font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Entry widget for the file path
        entry = tk.Entry(frame, state=tk.NORMAL, width=50, font=("Helvetica", 12))
        entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Text widget for displaying file content
        text_widget = tk.Text(frame, height=10, width=50, font=("Helvetica", 12))
        text_widget.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        # Button to open the file
        open_button = tk.Button(frame, text=f"Open {label_text}", command=lambda: open_text_file(
            entry, text_widget, self.tokenizer, undefined_words_frame, evaluation_frame), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        open_button.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        open_button.bind("<Enter>", lambda e: open_button.config(bg="#45a049"))
        open_button.bind("<Leave>", lambda e: open_button.config(bg="#4CAF50"))

        # Frame for evaluation results
        evaluation_frame = tk.Frame(frame, padx=10, pady=10, bg="#f0f0f0")
        evaluation_frame.grid(row=2, column=0, rowspan=3, sticky="nsew", padx=5, pady=5)

        # Frame for undefined words
        undefined_words_frame = tk.Frame(frame, padx=10, pady=10, bg="#f0f0f0")
        undefined_words_frame.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

        # Open the default file
        open_text_file(entry, text_widget, self.tokenizer, undefined_words_frame, evaluation_frame, default_path=default_path)

        # Configure grid weights
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        return entry, text_widget, undefined_words_frame, evaluation_frame

    def _create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open JSON File", command=lambda: open_json_file(self.tokenizer))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Update Tokens", command=lambda: update_tokens(self.tokenizer, self.root))

    def generate_report(self):
        examples_folder = "proyecto/ejemplos"
        report_file = "proyecto/report.txt"
        generate_report(self.tokenizer, examples_folder, report_file)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageTokenizerGUI(root)
    app.run()

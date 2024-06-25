import tkinter as tk
from tkinter import filedialog, messagebox
from utils import read_file
from logic.tokenizer import Tokenizer
import logging
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def open_text_file(entry, text_widget, tokenizer, undefined_words_frame, evaluation_frame, default_path=None):
    logging.debug(f"open_text_file called with default_path: {default_path}")
    file_path = default_path or filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    logging.debug(f"File path selected: {file_path}")

    if file_path:
        try:
            text = read_file(file_path)
            logging.debug(f"File read successfully: {file_path}")
            logging.debug(f"Text in file:\n{text}")

            update_entry_widget(entry, file_path)
            update_text_widget(text_widget, text, tokenizer)

            non_defined_words = identify_non_defined_words(tokenizer, text)
            logging.debug(f"All non-defined words identified: {non_defined_words}")

            display_undefined_words(non_defined_words, tokenizer, undefined_words_frame, text_widget, text, evaluation_frame)

            tokens = tokenizer.tokenize(text)
            evaluation_results = evaluate_text(tokens, tokenizer, non_defined_words)
            display_evaluation_results(evaluation_frame, evaluation_results)

        except Exception as e:
            logging.error(f"Failed to process the file: {e}")
            messagebox.showerror("Error", f"Failed to process the file: {e}")

def update_entry_widget(entry, file_path):
    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    entry.config(state=tk.DISABLED)

def update_text_widget(text_widget, text, tokenizer):
    text_widget.delete(1.0, tk.END)
    tokens = tokenizer.tokenize(text)
    logging.debug(f"Text tokenized: {tokens}")

    non_defined_words = identify_non_defined_words(tokenizer, text)
    text_widget.tag_configure('undefined', font=('Helvetica', 12, 'bold'), foreground='red')

    for line in text.split('\n'):
        for word in line.split():
            normalized_word = tokenizer.normalize_word(word)
            tag = 'undefined' if normalized_word in non_defined_words.values() else None
            text_widget.insert(tk.END, word + ' ', tag)
        text_widget.insert(tk.END, '\n')

    non_empty_lines = [line for line in text.split('\n') if line.strip()]
    text_widget.config(height=min(len(non_empty_lines), 20))

def identify_non_defined_words(tokenizer, text):
    tokens = tokenizer.tokenize(text)
    logging.debug(f"Tokens: {tokens}")
    non_defined_words = {}
    for token in tokens:
        normalized_word = tokenizer.normalize_word(token)
        if (normalized_word not in tokenizer.positive_words and 
            normalized_word not in tokenizer.negative_words and 
            normalized_word not in tokenizer.neutral_words):
            non_defined_words[token] = normalized_word
            logging.debug(f"Non-defined word found: {token} -> {normalized_word}")
    return non_defined_words

def evaluate_text(tokens, tokenizer, non_defined_words):
    return {
        "Undefined Words": len(non_defined_words),
        "Positive Words": len([word for word in tokens if tokenizer.normalize_word(word) in tokenizer.positive_words]),
        "Negative Words": len([word for word in tokens if tokenizer.normalize_word(word) in tokenizer.negative_words]),
        "Neutral Words": len([word for word in tokens if tokenizer.normalize_word(word) in tokenizer.neutral_words])
    }

def display_undefined_words(non_defined_words, tokenizer, frame, text_widget, text, evaluation_frame):
    logging.debug(f"Displaying undefined words: {non_defined_words}")
    for widget in frame.winfo_children():
        widget.destroy()

    if not non_defined_words:
        logging.debug("No undefined words to display.")
        return

    def add_word_to_json(word, category):
        logging.debug(f"Adding word to JSON: {word}, category: {category}")
        if category == "positive":
            tokenizer.positive_words.append(word)
        elif category == "negative":
            tokenizer.negative_words.append(word)
        elif category == "neutral":
            tokenizer.neutral_words.append(word)

        with open('proyecto/logic/tokens.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data['BUENAS'] = tokenizer.positive_words
            data['MALAS'] = tokenizer.negative_words
            data['NEUTRAS'] = tokenizer.neutral_words
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
        logging.debug(f"Word added to JSON and file updated: {word}")

        listbox.delete(listbox.get(0, tk.END).index(word))

        non_defined_words = identify_non_defined_words(tokenizer, text)
        logging.debug(f"Re-tokenized text and updated non-defined words: {non_defined_words}")

        tokens = tokenizer.tokenize(text)  # Add this line to define tokens
        update_text_widget(text_widget, text, tokenizer)

        evaluation_results = evaluate_text(tokens, tokenizer, non_defined_words)
        logging.debug(f"Updated evaluation results: {evaluation_results}")
        display_evaluation_results(evaluation_frame, evaluation_results)

    listbox_frame = tk.Frame(frame, bg="#f0f0f0")
    listbox_frame.grid(row=0, column=0, padx=10, pady=5, sticky="n")

    category_frame = tk.Frame(frame, bg="#f0f0f0")
    category_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")

    tk.Label(listbox_frame, text="Undefined Words:", font=("Helvetica", 12, "bold"), bg="#f0f0f0").pack(padx=10, pady=5)

    listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, font=("Helvetica", 12))
    logging.debug("Listbox created for undefined words.")
    for original_word, normalized_word in non_defined_words.items():
        listbox.insert(tk.END, f"{normalized_word} ({original_word})")
        logging.debug(f"Inserted word into listbox: {normalized_word} ({original_word})")
    listbox.pack(padx=10, pady=5)
    logging.debug("Listbox packed with padding.")
    tk.Label(category_frame, text="Select Category:", font=("Helvetica", 12, "bold"), bg="#f0f0f0").pack(padx=10, pady=5)

    category_var = tk.StringVar(value="neutral")
    tk.Radiobutton(category_frame, text="Positive", variable=category_var, value="positive", font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=10, pady=5)
    tk.Radiobutton(category_frame, text="Negative", variable=category_var, value="negative", font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=10, pady=5)
    tk.Radiobutton(category_frame, text="Neutral", variable=category_var, value="neutral", font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=10, pady=5)

    tk.Button(category_frame, text="Add Word", command=lambda: add_word_to_json(listbox.get(tk.ACTIVE).split(' ')[0], category_var.get()), font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10, pady=10)

def display_evaluation_results(frame, results):
    logging.debug(f"Displaying evaluation results: {results}")
    for widget in frame.winfo_children():
        widget.destroy()

    for key, value in results.items():
        tk.Label(frame, text=f"{key}: {value}", font=("Helvetica", 12)).pack(padx=10, pady=5)
        logging.debug(f"Displayed result: {key}: {value}")

def open_json_file(tokenizer):
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    logging.debug(f"JSON file path selected: {file_path}")
    if file_path:
        try:
            tokenizer = Tokenizer.from_json(file_path)
            logging.debug(f"JSON file loaded successfully: {file_path}")
            messagebox.showinfo("Success", "JSON file loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load JSON file: {e}")
            messagebox.showerror("Error", f"Failed to load JSON file: {e}")
    return tokenizer

def update_tokens(tokenizer, root):
    def save_tokens():
        try:
            positive_words = positive_text.get("1.0", tk.END).strip().split("\n")
            negative_words = negative_text.get("1.0", tk.END).strip().split("\n")
            neutral_words = neutral_text.get("1.0", tk.END).strip().split("\n")
            tokenizer.positive_words = positive_words
            tokenizer.negative_words = negative_words
            tokenizer.neutral_words = neutral_words
            logging.debug(f"Tokens updated: positive_words={positive_words}, negative_words={negative_words}, neutral_words={neutral_words}")
            update_window.destroy()
            messagebox.showinfo("Success", "Tokens updated successfully")
        except Exception as e:
            logging.error(f"Failed to update tokens: {e}")
            messagebox.showerror("Error", f"Failed to update tokens: {e}")

    update_window = tk.Toplevel(root)
    update_window.title("Update Tokens")

    tk.Label(update_window, text="Positive Words:", font=("Helvetica", 12, "bold")).pack(padx=10, pady=5)
    positive_text = tk.Text(update_window, height=10, width=50, font=("Helvetica", 12))
    positive_text.insert(tk.END, "\n".join(tokenizer.positive_words))
    positive_text.pack(padx=10, pady=5)

    tk.Label(update_window, text="Negative Words:", font=("Helvetica", 12, "bold")).pack(padx=10, pady=5)
    negative_text = tk.Text(update_window, height=10, width=50, font=("Helvetica", 12))
    negative_text.insert(tk.END, "\n".join(tokenizer.negative_words))
    negative_text.pack(padx=10, pady=5)

    tk.Label(update_window, text="Neutral Words:", font=("Helvetica", 12, "bold")).pack(padx=10, pady=5)
    neutral_text = tk.Text(update_window, height=10, width=50, font=("Helvetica", 12))
    neutral_text.insert(tk.END, "\n".join(tokenizer.neutral_words))
    neutral_text.pack(padx=10, pady=5)

    save_button = tk.Button(update_window, text="Save", command=save_tokens, font=("Helvetica", 12))
    save_button.pack(padx=10, pady=10)

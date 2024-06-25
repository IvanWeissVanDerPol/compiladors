import tkinter as tk
from tkinter import filedialog, messagebox
from utils import read_file, log_message, handle_error
from logic.tokenizer import Tokenizer
import json
import os
import matplotlib.pyplot as plt


def process_tokens(tokenizer, text):
    log_message("process_tokens called")
    tokens = tokenizer.tokenize(text)
    non_defined_words = identify_non_defined_words(tokenizer, tokens)
    return tokens, non_defined_words

def create_listbox_frame(parent, non_defined_words):
    log_message("create_listbox_frame called")
    listbox_frame = tk.Frame(parent, bg="#f0f0f0")
    tk.Label(listbox_frame, text="Undefined Words:", font=("Helvetica", 12, "bold"), bg="#f0f0f0").pack(padx=10, pady=5)
    listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, font=("Helvetica", 12))
    for original_word, normalized_word in non_defined_words.items():
        listbox.insert(tk.END, f"{normalized_word} ({original_word})")
    listbox.pack(padx=10, pady=5)
    return listbox_frame, listbox

def create_category_frame(parent, category_var):
    log_message("create_category_frame called")
    category_frame = tk.Frame(parent, bg="#f0f0f0")
    tk.Label(category_frame, text="Select Category:", font=("Helvetica", 12, "bold"), bg="#f0f0f0").pack(padx=10, pady=5)
    categories = [("Positive", "positive"), ("Negative", "negative"), ("Neutral", "neutral")]
    for text, value in categories:
        tk.Radiobutton(category_frame, text=text, variable=category_var, value=value, font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=10, pady=5)
    return category_frame

def open_text_file(entry, text_widget, tokenizer, undefined_words_frame, evaluation_frame, default_path=None):
    log_message("open_text_file called")
    log_message(f"open_text_file called with default_path: {default_path}")
    file_path = default_path or filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    log_message(f"File path selected: {file_path}")

    if file_path:
        try:
            text = read_file(file_path)
            log_message(f"File read successfully: {file_path}")
            log_message(f"Text in file:\n{text}")

            update_entry_widget(entry, file_path)
            tokens, non_defined_words = process_tokens(tokenizer, text)
            update_text_widget_with_tokens(text_widget, text, tokens, non_defined_words, tokenizer)

            display_undefined_words(non_defined_words, tokenizer, undefined_words_frame, text_widget, text, evaluation_frame)
            evaluation_results = evaluate_text(tokens, tokenizer, non_defined_words, text)
            display_evaluation_results(evaluation_frame, evaluation_results)

        except Exception as e:
            handle_error("Failed to process the file", e)

def update_entry_widget(entry, file_path):
    log_message("update_entry_widget called")
    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    entry.config(state=tk.DISABLED)

def update_text_widget_with_tokens(text_widget, text, tokens, non_defined_words, tokenizer):
    log_message("update_text_widget_with_tokens called")
    text_widget.delete(1.0, tk.END)
    text_widget.tag_configure('undefined', font=('Helvetica', 12, 'bold'), foreground='red')
    text_widget.tag_configure('original_undefined', font=('Helvetica', 12, 'bold'), foreground='red')

    longest_line_length = 0

    for line in text.split('\n'):
        if len(line) > longest_line_length:
            longest_line_length = len(line)
        for word in line.split():
            normalized_word = tokenizer.normalize_word(word)
            if normalized_word in non_defined_words.values():
                text_widget.insert(tk.END, word + ' ', 'undefined')
            elif word in non_defined_words:
                text_widget.insert(tk.END, word + ' ', 'original_undefined')
            else:
                text_widget.insert(tk.END, word + ' ')
        text_widget.insert(tk.END, '\n')

    non_empty_lines = [line for line in text.split('\n') if line.strip()]
    text_widget.config(height=min(len(non_empty_lines), 20), width=longest_line_length)

def identify_non_defined_words(tokenizer, tokens):
    log_message("identify_non_defined_words called")
    non_defined_words = {}
    for token, normalized_token in tokens:
        if (normalized_token not in tokenizer.positive_words and 
            normalized_token not in tokenizer.negative_words and 
            normalized_token not in tokenizer.neutral_words):
            non_defined_words[token] = normalized_token
            log_message(f"Normalized word: {normalized_token} token: {token}")
    return non_defined_words

def evaluate_text(tokens, tokenizer, non_defined_words, conversation):
    log_message("evaluate_text called")
    performance_score = tokenizer.evaluate_performance(conversation)
    experience_results = tokenizer.evaluate_experience(conversation)
    
    return {
        "Undefined Words": len(non_defined_words),
        "Positive Words": experience_results["positive"],
        "Negative Words": experience_results["negative"],
        "Neutral Words": experience_results["neutral"],
        "Experience Score": experience_results["score"],
        "Performance Score": performance_score
    }

def display_undefined_words(non_defined_words, tokenizer, frame, text_widget, text, evaluation_frame):
    log_message("display_undefined_words called")
    log_message(f"Displaying undefined words: {non_defined_words}")
    for widget in frame.winfo_children():
        widget.destroy()

    if not non_defined_words:
        log_message("No undefined words to display.")
        return

    def add_word_to_json(word, category):
        log_message("add_word_to_json called")
        log_message(f"Adding word to JSON: {word}, category: {category}")
        getattr(tokenizer, f"{category}_words").append(word)

        with open('proyecto/logic/tokens.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data['BUENAS'] = tokenizer.positive_words
            data['MALAS'] = tokenizer.negative_words
            data['NEUTRAS'] = tokenizer.neutral_words
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
        log_message(f"Word added to JSON and file updated: {word}")

        # Find the item in the listbox and delete it
        for i in range(listbox.size()):
            item = listbox.get(i)
            if item.startswith(word):
                listbox.delete(i)
                break

        tokens, non_defined_words = process_tokens(tokenizer, text)
        update_text_widget_with_tokens(text_widget, text, tokens, non_defined_words, tokenizer)

        evaluation_results = evaluate_text(tokens, tokenizer, non_defined_words, text)
        log_message(f"Updated evaluation results: {evaluation_results}")
        display_evaluation_results(evaluation_frame, evaluation_results)

    listbox_frame, listbox = create_listbox_frame(frame, non_defined_words)
    listbox_frame.grid(row=0, column=0, padx=10, pady=5, sticky="n")

    category_var = tk.StringVar(value="neutral")
    category_frame = create_category_frame(frame, category_var)
    category_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")

    tk.Button(category_frame, text="Add Word", command=lambda: add_word_to_json(listbox.get(tk.ACTIVE).split(' ')[0], category_var.get()), font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10, pady=10)
    
def display_evaluation_results(frame, results):
    log_message("display_evaluation_results called")
    log_message(f"Displaying evaluation results: {results}")
    for widget in frame.winfo_children():
        widget.destroy()

    for key, value in results.items():
        tk.Label(frame, text=f"{key}: {value}", font=("Helvetica", 12)).pack(padx=10, pady=5)
        log_message(f"Displayed result: {key}: {value}")

def open_json_file(tokenizer):
    log_message("open_json_file called")
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    log_message(f"JSON file path selected: {file_path}")
    if file_path:
        try:
            tokenizer = Tokenizer.from_json(file_path)
            log_message(f"JSON file loaded successfully: {file_path}")
            messagebox.showinfo("Success", "JSON file loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {e}")
    return tokenizer

def update_tokens(tokenizer, root):
    log_message("update_tokens called")
    def save_tokens():
        log_message("save_tokens called")
        try:
            tokenizer.positive_words = positive_text.get("1.0", tk.END).strip().split("\n")
            tokenizer.negative_words = negative_text.get("1.0", tk.END).strip().split("\n")
            tokenizer.neutral_words = neutral_text.get("1.0", tk.END).strip().split("\n")
            log_message(f"Tokens updated: positive_words={tokenizer.positive_words}, negative_words={tokenizer.negative_words}, neutral_words={tokenizer.neutral_words}")
            update_window.destroy()
            messagebox.showinfo("Success", "Tokens updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update tokens: {e}")

    update_window = tk.Toplevel(root)
    update_window.title("Update Tokens")

    def create_text_widget(label_text, words):
        log_message("create_text_widget called")
        tk.Label(update_window, text=label_text, font=("Helvetica", 12, "bold")).pack(padx=10, pady=5)
        text_widget = tk.Text(update_window, height=10, width=50, font=("Helvetica", 12))
        text_widget.insert(tk.END, "\n".join(words))
        text_widget.pack(padx=10, pady=5)
        return text_widget

    positive_text = create_text_widget("Positive Words:", tokenizer.positive_words)
    negative_text = create_text_widget("Negative Words:", tokenizer.negative_words)
    neutral_text = create_text_widget("Neutral Words:", tokenizer.neutral_words)

    save_button = tk.Button(update_window, text="Save", command=save_tokens, font=("Helvetica", 12))
    save_button.pack(padx=10, pady=10)
def generate_report(tokenizer, examples_folder, report_file):
    log_message("generate_report called")
    report_lines = []
    file_names = []
    positive_scores = []
    negative_scores = []
    neutral_scores = []
    experience_scores = []
    performance_scores = []

    for root, _, files in os.walk(examples_folder):
        for file_name in files:
            if file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                try:
                    text = read_file(file_path)
                    tokens, non_defined_words = process_tokens(tokenizer, text)
                    evaluation_results = evaluate_text(tokens, tokenizer, non_defined_words, text)  # Pass 'text' as 'conversation'
                    report_lines.append(f"File: {file_name}")
                    for key, value in evaluation_results.items():
                        report_lines.append(f"{key}: {value}")
                    report_lines.append("\n")

                    file_names.append(file_name)
                    positive_scores.append(evaluation_results.get('Positive Words', 0))
                    negative_scores.append(evaluation_results.get('Negative Words', 0))
                    neutral_scores.append(evaluation_results.get('Neutral Words', 0))
                    experience_scores.append(evaluation_results.get('Experience Score', 0))
                    performance_scores.append(evaluation_results.get('Performance Score', 0))
                except Exception as e:
                    handle_error(f"Failed to process file: {file_path}", e)

    with open(report_file, 'w', encoding='utf-8') as report:
        report.write("\n".join(report_lines))
    log_message(f"Report generated: {report_file}")
    messagebox.showinfo("Success", f"Report generated: {report_file}")

    # Generate graph
    x = range(len(file_names))
    plt.figure(figsize=(10, 6))
    plt.plot(x, positive_scores, label='Positive', marker='o')
    plt.plot(x, negative_scores, label='Negative', marker='o')
    plt.plot(x, neutral_scores, label='Neutral', marker='o')
    plt.plot(x, experience_scores, label='Experience', marker='o')
    plt.plot(x, performance_scores, label='Performance', marker='o')
    plt.xticks(x, file_names, rotation='vertical')
    plt.xlabel('Files')
    plt.ylabel('Scores')
    plt.title('Evaluation Scores per File')
    plt.legend()
    plt.tight_layout()
    plt.savefig(report_file.replace('.txt', '.png'))
    plt.show()
    log_message(f"Graph generated: {report_file.replace('.txt', '.png')}")
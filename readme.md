# Language Tokenizer GUI

## Project Overview
The Language Tokenizer GUI is a Python-based application designed to analyze text files and evaluate their content based on predefined positive, negative, and neutral words. The application provides functionalities for tokenizing text, evaluating tokens, and generating reports through a user-friendly graphical interface built with Tkinter.

## Main Components and Their Functions
### 1. Main Entry Point (main.py)
**Purpose:** Initializes the Tkinter root window and starts the Language Tokenizer GUI application.  
**Functionality:**
- Creates the root window using Tkinter.
- Instantiates the LanguageTokenizerGUI class.
- Runs the GUI application.

### 2. Utility Functions (utils.py)
**Purpose:** Provides utility functions such as reading files, logging messages, and handling errors.  
**Functions:**
- `read_file(file_path)`: Reads and returns the content of a file.
- `log_message(message, level=logging.DEBUG)`: Logs messages at specified logging levels.
- `handle_error(message, exception=None)`: Logs error messages and displays them using a message box.

### 3. GUI Implementation (gui.py)
**Purpose:** Implements the graphical user interface for the Language Tokenizer.  
**Components:**
- **Initialization:** Sets up the main window and UI components such as file frames, buttons, and menu options.
- **File Frames:** Creates sections for opening and displaying content from Customer Service and Customer Experience files.
- **Menu Options:** Includes options for opening JSON files and updating tokens.
- **Report Generation:** Adds functionality to generate reports based on the analyzed text files.  
**Key Class:**
- `LanguageTokenizerGUI`: Manages the entire GUI, including setup, file handling, and report generation.

### 4. Tokenizer Logic (tokenizer.py)
**Purpose:** Handles tokenization and evaluation of text based on predefined word categories.  
**Key Functions:**
- `from_json(cls, json_file_path)`: Loads token categories (positive, negative, neutral) from a JSON file.
- `normalize_word(original_word)`: Normalizes words for consistent tokenization.
- `tokenize(text)`: Tokenizes the input text into individual words.
- `evaluate(tokens)`: Evaluates the tokens to count positive, negative, and neutral words.
- `evaluate_performance(conversation)`: Evaluates performance based on predefined conversational criteria.
- `evaluate_experience(conversation)`: Evaluates the overall experience by scoring positive and negative word occurrences.

### 5. Tokens Configuration (tokens.json)
**Purpose:** Stores lists of predefined positive, negative, and neutral words.  
**Structure:**
- `"BUENAS"`: List of positive words.
- `"MALAS"`: List of negative words.
- `"NEUTRAS"`: List of neutral words.

### 6. GUI Helpers (gui_helpers.py)
**Purpose:** Provides helper functions for GUI operations such as file dialogs, token processing, and displaying results.  
**Functions:**
- `process_tokens(tokenizer, text)`: Processes text to tokenize and identify non-defined words.
- `open_text_file(entry, text_widget, tokenizer, undefined_words_frame, evaluation_frame, default_path=None)`: Handles file opening and text processing.
- `update_entry_widget(entry, file_path)`: Updates the file path entry widget.
- `update_text_widget_with_tokens(text_widget, text, tokens, non_defined_words, tokenizer)`: Displays tokens in the text widget with special formatting for undefined words.
- `display_undefined_words(non_defined_words, tokenizer, frame, text_widget, text, evaluation_frame)`: Displays and manages undefined words.
- `evaluate_text(tokens, tokenizer, non_defined_words, conversation)`: Evaluates the text and returns a dictionary of results.
- `generate_report(tokenizer, examples_folder, report_file)`: Generates a report and a graph based on the evaluation of text files.

## How the Project Works
### Initialization:
- The application starts by running main.py, which initializes the Tkinter root window and starts the GUI.

### GUI Setup:
- `LanguageTokenizerGUI` sets up the main window with sections for Customer Service and Customer Experience files.
- Menu options allow users to open JSON files and update tokens.

### File Handling:
- Users can open text files, which are read and displayed in the respective sections.
- The text is tokenized and evaluated using the `Tokenizer` class, highlighting undefined words and displaying evaluation results.

### Tokenization and Evaluation:
- The `Tokenizer` class normalizes and tokenizes the text.
- It evaluates tokens against predefined positive, negative, and neutral words.
- Performance and experience evaluations are conducted based on specific criteria and word counts.

### Report Generation:
- Users can generate reports summarizing the analysis of multiple text files.
- Reports include counts of positive, negative, and neutral words, as well as performance and experience scores.
- A graph visualizing the evaluation scores is generated and saved.

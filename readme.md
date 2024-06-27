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

**Main Logic:**
Main Logic and Important Functions
Tokenizer Class Initialization and JSON Loading


```

class Tokenizer:
    def __init__(self, positive_words, negative_words, neutral_words):
        log_message("Tokenizer.__init__ called")
        self.positive_words = positive_words
        self.negative_words = negative_words
        self.neutral_words = neutral_words

    @classmethod
    def from_json(cls, json_file_path):
        """
        Class method to create a Tokenizer instance from a JSON file.
        The JSON file should contain three keys: 'BUENAS', 'MALAS', and 'NEUTRAS',
        which correspond to positive, negative, and neutral words respectively.
        """
        log_message("Tokenizer.from_json called")
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return cls(
            positive_words=data['BUENAS'],
            negative_words=data['MALAS'],
            neutral_words=data['NEUTRAS']
        )

    def normalize_word(self, original_word):
        """
        Normalize a word to handle number and gender variations.
        Converts the word to lowercase, removes plural 's', and converts feminine 'a' to masculine 'o'.
        Returns 'neutral_number' for digit-only words.
        """
        updated_word = original_word.lower()
        if updated_word.isdigit():
            return 'neutral_number'  # Special token for numbers
        if updated_word.endswith('s'):
            updated_word = updated_word[:-1]  # Remove plural 's'
        if updated_word.endswith('a'):
            updated_word = updated_word[:-1] + 'o'  # Convert feminine to masculine
        return updated_word

    def tokenize(self, text):
        """
        Tokenize the input text into individual words.
        Handles punctuation and special characters, converts text to lowercase,
        and normalizes each token.
        """
        log_message(f"Tokenizer.tokenize called with text={text}")
        tokens = re.findall(r'\b\w+\b', text.lower())
        log_message(f"Tokenized text into tokens: {tokens}")
        normalized_tokens = [(token, self.normalize_word(token)) for token in tokens]
        log_message(f"Normalized tokens: {normalized_tokens}")
        return normalized_tokens

    def def evaluate(self, tokens):
        """
        Evaluate the tokens to count positive, negative, and neutral words.
        Returns a dictionary with counts for each category.
        """
        log_message(f"Tokenizer.evaluate called with tokens={tokens}")
        positive_count = sum(1 for token in tokens if token in self.positive_words)
        negative_count = sum(1 for token in tokens if token in self.negative_words)
        neutral_count = sum(1 for token in tokens if token in self.neutral_words)
        log_message(f"Evaluation results - positive: {positive_count}, negative: {negative_count}, neutral: {neutral_count}")
        
        return {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count
        }

     def evaluate_performance(self, conversation):
        """
        Evaluate the performance of a conversation based on predefined criteria.
        Checks for the presence of specific phrases in the conversation and calculates a performance score.
        """
        log_message("Tokenizer.evaluate_performance called")
        criteria = {
            "greeting": ["Buenas noches","¿Cómo está?","¿Cómo le va?","¡Bienvenido!","¡Bienvenida!","¿En qué puedo ayudarle?","¿Cómo puedo asistirte?","Hola, ¿cómo estás?","Hola, ],
            "ask_number": ["número de teléfono","número de cuenta","número de pedido","número de referencia","número de identificación","número de transacción","número de tarjeta"],
            "provide_info": ["detalle","balance","información","detalles","estado","disponible","transacciones","última operación","historial","datos","documentos","actualización","movimientos"],
            "offer_assistance": ["puedo ayudarle","necesita ayuda","puedo asistirte","puedo hacer algo más","algo más que pueda hacer","requiere asistencia","alguna otra cosa","algo adicional"],
            "end_politely": ["hasta pronto","nos vemos","que tenga buen día","que tenga buena tarde","que tenga buena noche","que pase bien","cuídese","le agradezco","gracias por su tiempo"]
        }
        performance_score = 0
        for key, phrases in criteria.items():
            if any(phrase in conversation.lower() for phrase in phrases):
                performance_score += 1
                log_message(f"Criteria '{key}' met")
        
        log_message(f"Performance score: {performance_score}/{len(criteria)}")
        return performance_score

    def evaluate_experience(self, conversation):
        """
        Evaluate the overall experience of a conversation by scoring positive and negative word occurrences.
        Tokenizes the conversation, counts positive, negative, and neutral words, and calculates an experience score.
        """
        log_message("Tokenizer.evaluate_experience called")
        tokens = self.tokenize(conversation)
        positive_count = sum(1 for _, normalized_word in tokens if normalized_word in self.positive_words)
        negative_count = sum(1 for _, normalized_word in tokens if normalized_word in self.negative_words)
        neutral_count = sum(1 for _, normalized_word in tokens if normalized_word in self.neutral_words)
        
        experience_score = positive_count - negative_count
        log_message(f"Experience score: {experience_score} (positive: {positive_count}, negative: {negative_count}, neutral: {neutral_count})")
        
        return {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
            "score": experience_score
        }

```

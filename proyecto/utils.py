import logging
from tkinter import messagebox

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
    

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def log_message(message, level=logging.DEBUG):
    logging.log(level, message)
    
def handle_error(message, exception=None):
    log_message(f"{message}: {exception}" if exception else message, level=logging.ERROR)
    messagebox.showerror("Error", message)